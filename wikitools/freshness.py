"""Shared freshness logic for the Winawer Lab wiki.

Used in two places:
  * hooks/freshness_hook.py  (MkDocs build: adds banners and the health table)
  * scripts/check_freshness.py (GitHub Actions: weekly report and checks)

Every page in docs/ starts with a small header ("front matter"):

    ---
    title: Money and reimbursement
    owner: JWinawer          # GitHub username, or a list of them
    reviewed: 2026-11-20     # date someone last checked the page was right
    review_every: 12         # months until the next check (default 12)
    status: draft            # optional: "draft" while a page is being written
    ---
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PEOPLE_FILE = ROOT / "people.yml"
REPO = "WinawerLab/wiki"
SITE = "https://winawerlab.github.io/wiki/"
DEFAULT_MONTHS = 12
DUE_SOON_DAYS = 30
# Pages that are built automatically or are only about the wiki itself.
SKIP = {"about/health.md"}

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def add_months(d: dt.date, months: int) -> dt.date:
    y, m = divmod(d.month - 1 + months, 12)
    year, month = d.year + y, m + 1
    for day in (d.day, 30, 29, 28):
        try:
            return dt.date(year, month, day)
        except ValueError:
            continue
    raise ValueError(d)


def load_people() -> dict[str, dict]:
    """Return {github_username_lowercase: person dict}."""
    if not PEOPLE_FILE.exists():
        return {}
    data = yaml.safe_load(PEOPLE_FILE.read_text()) or {}
    out = {}
    for p in data.get("people", []) or []:
        gh = str(p.get("github") or "").strip()
        if gh:
            out[gh.lower()] = p
    return out


@dataclass
class PageStatus:
    path: str                      # relative to docs/
    title: str
    owners: list[str]
    reviewed: dt.date | None
    review_every: int
    draft: bool
    due: dt.date | None = None
    state: str = "ok"              # ok | due_soon | overdue | invalid
    problems: list[str] = field(default_factory=list)
    departed_owners: list[str] = field(default_factory=list)

    @property
    def months_since(self) -> int | None:
        if not self.reviewed:
            return None
        t = dt.date.today()
        return (t.year - self.reviewed.year) * 12 + t.month - self.reviewed.month


def parse_front_matter(text: str) -> dict:
    m = FM_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {"__yaml_error__": True}


def page_status(rel_path: str, meta: dict, people: dict, today: dt.date | None = None) -> PageStatus:
    today = today or dt.date.today()
    problems = []
    if meta.get("__yaml_error__"):
        problems.append("the header block at the top of the page could not be read")

    owners = meta.get("owner") or []
    if isinstance(owners, str):
        owners = [owners]
    owners = [str(o).lstrip("@").strip() for o in owners if str(o).strip()]
    if not owners:
        problems.append("no `owner:` in the header")

    reviewed = meta.get("reviewed")
    if isinstance(reviewed, str):
        try:
            reviewed = dt.date.fromisoformat(reviewed.strip())
        except ValueError:
            problems.append(f"`reviewed: {reviewed}` is not a date like 2026-11-20")
            reviewed = None
    elif isinstance(reviewed, dt.datetime):
        reviewed = reviewed.date()
    elif reviewed is not None and not isinstance(reviewed, dt.date):
        problems.append("`reviewed:` is not a date like 2026-11-20")
        reviewed = None
    if reviewed is None and not any("reviewed" in p for p in problems):
        problems.append("no `reviewed:` date in the header")

    try:
        months = int(meta.get("review_every", DEFAULT_MONTHS))
    except (TypeError, ValueError):
        problems.append("`review_every:` should be a whole number of months")
        months = DEFAULT_MONTHS

    st = PageStatus(
        path=rel_path,
        title=str(meta.get("title") or rel_path),
        owners=owners,
        reviewed=reviewed,
        review_every=months,
        draft=str(meta.get("status", "")).lower() == "draft",
        problems=problems,
    )
    if people:
        st.departed_owners = [
            o for o in owners
            if o.lower() not in people or not people[o.lower()].get("current", False)
        ]
    if reviewed:
        st.due = add_months(reviewed, months)
        if today > st.due:
            st.state = "overdue"
        elif (st.due - today).days <= DUE_SOON_DAYS:
            st.state = "due_soon"
    if problems:
        st.state = "invalid"
    return st


def all_pages(today: dt.date | None = None) -> list[PageStatus]:
    people = load_people()
    out = []
    for f in sorted(DOCS.rglob("*.md")):
        rel = f.relative_to(DOCS).as_posix()
        if rel in SKIP:
            continue
        meta = parse_front_matter(f.read_text(encoding="utf-8"))
        out.append(page_status(rel, meta, people, today))
    return out


def edit_url(rel_path: str) -> str:
    return f"https://github.com/{REPO}/edit/main/docs/{rel_path}"


def problem_url(rel_path: str, title: str) -> str:
    from urllib.parse import quote
    return (f"https://github.com/{REPO}/issues/new?template=page-problem.yml"
            f"&title={quote('Problem on: ' + title)}&page={quote(rel_path)}")


def page_url(rel_path: str) -> str:
    p = rel_path[:-3]
    if p == "index":
        return SITE
    if p.endswith("/index"):
        p = p[: -len("index")]
    else:
        p += "/"
    return SITE + p
