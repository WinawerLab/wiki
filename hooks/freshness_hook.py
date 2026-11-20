"""MkDocs hook: adds a freshness banner and footer to every page,
and fills in the table on the "Wiki health" page.

The site is rebuilt every week (see .github/workflows/deploy.yml),
so banners appear on their own as pages age.
"""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wikitools import freshness as fr  # noqa: E402

_people = None


def _get_people():
    global _people
    if _people is None:
        _people = fr.load_people()
    return _people


def _fmt(d):
    return d.strftime("%b %-d, %Y") if d else "never"


def _owner_links(owners):
    if not owners:
        return "nobody yet"
    return ", ".join(f"[@{o}](https://github.com/{o})" for o in owners)


def on_page_markdown(markdown, page, config, files):
    rel = page.file.src_uri
    if rel == "about/health.md":
        return markdown.replace("<!-- HEALTH_TABLE -->", health_table())
    st = fr.page_status(rel, page.meta, _get_people())
    edit = fr.edit_url(rel)
    report = fr.problem_url(rel, st.title)

    banners = []
    if st.state == "invalid":
        banners.append(
            '!!! failure "This page is missing its header"\n'
            f"    Problems: {'; '.join(st.problems)}. "
            f"[Fix it here]({edit}). See [How to edit]({fr.SITE}about/how-to-edit/).\n"
        )
    if st.draft:
        banners.append(
            '!!! note "Draft: help write this page"\n'
            "    This page is not finished. If you know something that belongs here, "
            f"[add it]({edit}).\n"
        )
    if st.state == "overdue":
        banners.append(
            '!!! warning "This page may be out of date"\n'
            f"    Nobody has checked it since **{_fmt(st.reviewed)}**. "
            "If you use it, please check it: fix anything that is wrong, then change "
            f"the `reviewed:` date at the top to today. [Edit this page]({edit}) · "
            f"[Report a problem]({report})\n"
        )
    if st.departed_owners and st.owners:
        banners.append(
            '!!! info "This page needs a new owner"\n'
            f"    Its owner ({', '.join('@' + o for o in st.departed_owners)}) is not on the "
            f"current lab list. Want to adopt it? [Put your GitHub name as owner]({edit}).\n"
        )

    footer = (
        "\n\n---\n"
        f'<p class="page-freshness">Owner: {_owner_links(st.owners)} · '
        f"Last checked: {_fmt(st.reviewed)} · "
        f"Next check due: {_fmt(st.due)} · "
        f'<a href="{edit}">Edit</a> · <a href="{report}">Report a problem</a></p>\n'
    )
    # Put banners after the page's first heading, if it has one.
    lines = markdown.split("\n")
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = i + 1
            break
    banner_md = "\n".join(banners)
    if banner_md:
        lines[insert_at:insert_at] = ["", banner_md]
    return "\n".join(lines) + footer


def health_table():
    pages = fr.all_pages()
    order = {"invalid": 0, "overdue": 1, "due_soon": 2, "ok": 3}
    label = {"invalid": "❌ header broken", "overdue": "⚠️ overdue",
             "due_soon": "⏳ due soon", "ok": "✅ fine"}
    pages.sort(key=lambda p: (order[p.state], p.due or dt.date.min))
    n = {k: sum(p.state == k for p in pages) for k in order}
    drafts = sum(p.draft for p in pages)
    no_owner = sum(bool(p.departed_owners) for p in pages)
    rows = ["| Page | Status | Owner | Last checked | Next check due |",
            "|---|---|---|---|---|"]
    for p in pages:
        status = label[p.state] + (" · draft" if p.draft else "")
        if p.departed_owners:
            status += " · needs owner"
        rows.append(
            f"| [{p.title}]({fr.page_url(p.path)}) | {status} | "
            f"{', '.join('@' + o for o in p.owners) or '—'} | {_fmt(p.reviewed)} | {_fmt(p.due)} |"
        )
    summary = (
        f"**{len(pages)} pages.** {n['ok']} fine, {n['due_soon']} due soon, "
        f"{n['overdue']} overdue, {n['invalid']} with a broken header. "
        f"{drafts} drafts. {no_owner} need a new owner.\n\n"
        f"*Built {dt.date.today():%b %-d, %Y}.*\n\n"
    )
    return summary + "\n".join(rows)
