# Winawer Lab Wiki

The lab's working handbook: **https://winawerlab.github.io/wiki/**

Written by the lab, for the lab. Anyone can read it; lab members (the
[WinawerLab](https://github.com/WinawerLab) GitHub organization) can edit it.

## Editing

Click the pencil icon on any page of the site. GitHub's editor opens; change the text and click
**Commit changes**. The site rebuilds in about two minutes. Full guide:
[How to edit](https://winawerlab.github.io/wiki/about/how-to-edit/).

## How it stays up to date

Every page starts with a header naming an `owner`, the date it was last `reviewed`, and how often
it should be checked (`review_every`, months). Old pages show a yellow banner, and a weekly check
reminds owners. Details: [How it stays up to date](https://winawerlab.github.io/wiki/about/keeping-it-fresh/).

## What is where

| Path | What |
|---|---|
| `docs/` | The pages (Markdown) |
| `mkdocs.yml` | Site settings and the menu (`nav:`) |
| `people.yml` | Lab members; used to check page owners |
| `templates/new-page.md` | Starting point for a new page |
| `meta/` | Working notes for the lab, not part of the site (for example the old-wiki triage list) |
| `wikitools/`, `hooks/`, `scripts/` | Freshness logic: banners, health table, weekly report |
| `.github/workflows/` | Automation: publish site, weekly freshness check, weekly link check, secret scan |

## Automated jobs

| Workflow | When | What it does | If it fails |
|---|---|---|---|
| `deploy.yml` | every push to `main`; Mondays | builds and publishes the site | opens a "Wiki automation failed" issue |
| `freshness.yml` | Mondays | updates the "Wiki freshness report" issue; monthly @mention of owners; commits `.github/freshness-status.json` | same |
| `links.yml` | Mondays | opens/updates a "Broken links" issue | same |
| `secrets.yml` | every push and pull request | scans for passwords, keys and tokens | same |

## Preview locally (optional)

```bash
pip install -r requirements.txt
mkdocs serve        # then open http://127.0.0.1:8000
python scripts/check_freshness.py
```
