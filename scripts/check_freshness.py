#!/usr/bin/env python3
"""Check every wiki page's header and review date.

Usage:
    python scripts/check_freshness.py            # print a summary; exit 1 if a header is broken
    python scripts/check_freshness.py --report report.md --status status.json

--report writes the weekly report used as the body of the "Wiki freshness report" issue.
--status writes a small status file (job, last_attempt, last_success, ok, message).
The script also prints "ACTION_NEEDED=true/false" for the workflow to read.
"""
import argparse
import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wikitools import freshness as fr  # noqa: E402


def fmt(d):
    return d.isoformat() if d else "never"


def build_report(pages):
    today = dt.date.today()
    invalid = [p for p in pages if p.state == "invalid"]
    overdue = [p for p in pages if p.state == "overdue"]
    soon = [p for p in pages if p.state == "due_soon"]
    orphaned = [p for p in pages if p.departed_owners]

    lines = [f"_Weekly check, {today:%A %B %-d, %Y}. "
             f"{len(pages)} pages: {len(overdue)} overdue, {len(soon)} due within "
             f"{fr.DUE_SOON_DAYS} days, {len(orphaned)} need a new owner, "
             f"{len(invalid)} with a broken header._", ""]
    lines += ["**How to clear an item:** open the page, check it is still right, fix what is not, "
              "and set `reviewed:` at the top to today's date. If a page is no longer useful, "
              "delete it. Both are fine.", ""]

    by_owner = defaultdict(list)
    for p in overdue + soon:
        for o in (p.owners or ["(no owner)"]):
            by_owner[o].append(p)
    if by_owner:
        lines.append("## Pages to check, by owner")
        for owner in sorted(by_owner, key=str.lower):
            who = owner if owner.startswith("(") else "@" + owner
            lines.append(f"\n### {who}")
            for p in sorted(by_owner[owner], key=lambda x: x.due or today):
                tag = "overdue since" if p.state == "overdue" else "due"
                lines.append(f"- [ ] [{p.title}]({fr.page_url(p.path)}): {tag} {fmt(p.due)} "
                             f"([edit]({fr.edit_url(p.path)}))")
    if orphaned:
        lines += ["", "## Pages whose owner has left (or is not in `people.yml`)"]
        for p in orphaned:
            lines.append(f"- [ ] [{p.title}]({fr.page_url(p.path)}): owner "
                         f"{', '.join('@' + o for o in p.departed_owners)}. "
                         "Who will adopt it?")
    if invalid:
        lines += ["", "## Pages with a broken header"]
        for p in invalid:
            lines.append(f"- [ ] [{p.path}]({fr.edit_url(p.path)}): {'; '.join(p.problems)}")

    # Page of the week: the page checked longest ago, so every page gets looked at in turn.
    dated = [p for p in pages if p.reviewed]
    if dated:
        pick = min(dated, key=lambda p: p.reviewed)
        owners = ", ".join("@" + o for o in pick.owners) or "anyone"
        lines += ["", "## Page of the week",
                  f"[{pick.title}]({fr.page_url(pick.path)}) was checked longest ago "
                  f"({fmt(pick.reviewed)}). {owners}: a 5-minute read this week?"]
    lines += ["", "---", "_This issue is updated by the `freshness` workflow every Monday. "
              "It closes itself when nothing needs attention. "
              f"Full table: [Wiki health]({fr.SITE}about/health/)._"]
    action = bool(overdue or soon or orphaned or invalid)
    return "\n".join(lines) + "\n", action


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report")
    ap.add_argument("--status")
    args = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    status = {"job": "wiki-freshness", "last_attempt": now, "last_success": None,
              "ok": False, "message": ""}
    prev = Path(args.status) if args.status else None
    if prev and prev.exists():
        try:
            status["last_success"] = json.loads(prev.read_text()).get("last_success")
        except Exception:
            pass
    try:
        pages = fr.all_pages()
        if not pages:
            raise RuntimeError("found no pages in docs/; something is wrong with the checkout")
        report, action = build_report(pages)
        if args.report:
            Path(args.report).write_text(report)
        invalid = [p for p in pages if p.state == "invalid"]
        for p in pages:
            flag = {"ok": " ", "due_soon": "~", "overdue": "!", "invalid": "X"}[p.state]
            print(f"[{flag}] {p.path:45s} owner={','.join(p.owners) or '-':15s} "
                  f"reviewed={fmt(p.reviewed)} due={fmt(p.due)}"
                  + (f"  PROBLEMS: {'; '.join(p.problems)}" if p.problems else ""))
        print(f"ACTION_NEEDED={'true' if action else 'false'}")
        status.update(ok=True, last_success=now,
                      message=f"{len(pages)} pages checked; "
                              f"{sum(p.state == 'overdue' for p in pages)} overdue; "
                              f"{len(invalid)} broken headers")
        code = 1 if invalid else 0
    except Exception as e:  # report loudly, never fail silently
        status["message"] = f"check crashed: {type(e).__name__}: {e}"
        print(status["message"], file=sys.stderr)
        code = 2
    if args.status:
        Path(args.status).write_text(json.dumps(status, indent=2) + "\n")
    sys.exit(code)


if __name__ == "__main__":
    main()
