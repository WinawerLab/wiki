---
title: How to edit
owner: JWinawer
reviewed: 2026-11-20
review_every: 12
---

# How to edit this wiki

You do not need to install anything. Everything happens in your web browser on GitHub.

## Fix or add something on a page (about 1 minute)

1. Click the **pencil icon** at the top right of the page. GitHub opens the page's text.
   (You need a GitHub account and to be on the `winawerlab` team in the
   [WinawerLab organization](https://github.com/WinawerLab). Ask Jon.)
2. Make your change. Pages are written in
   [Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax),
   which is plain text with a few symbols: `#` for headings, `-` for lists, `**bold**`,
   and `[link text](https://...)`.
3. Click **Commit changes…**, write a few words about what you changed, and click
   **Commit changes** again.
4. The site updates by itself in about two minutes.

You cannot break anything for good. Every version of every page is saved, and any change can
be undone.

## The header at the top of each page

Every page starts with a short header between two `---` lines:

```yaml
---
title: Money and reimbursement
owner: your-github-name      # who keeps this page up to date
reviewed: 2026-11-20         # when someone last checked that the page is right
review_every: 12             # months until the next check
status: draft                # only while a page is unfinished; delete the line when done
---
```

**When you check a page and it is right, change `reviewed:` to today's date.** That is all it
takes to clear a yellow "may be out of date" banner. Checking a page counts as much as writing one.

## Start a new page

1. Go to the [docs folder](https://github.com/WinawerLab/wiki/tree/main/docs) on GitHub and open
   the subfolder where the page belongs.
2. Click **Add file → Create new file**. Name it with lowercase words and dashes, ending in `.md`
   (for example `eye-tracking.md`).
3. Copy the [page template](https://github.com/WinawerLab/wiki/blob/main/templates/new-page.md)
   into it, fill in the header with your GitHub name as owner, and write.
4. Add the page to the `nav:` list in [`mkdocs.yml`](https://github.com/WinawerLab/wiki/blob/main/mkdocs.yml)
   so it shows up in the menu. (If you are not sure how, open an issue and someone will do it.)

## What makes a page last

- **Link to official sources; do not copy them.** NYU and CBI rules change. A link stays right
  longer than a copy.
- **Write what is specific to our lab.** That is the part nobody else will write down.
- **Prefer role email addresses** (like psychit@nyu.edu) over people's names.
- **Put a date on facts that change**, for example "as of fall 2026".
- **Short is good.** A short page that is right beats a long page nobody trusts.
- **Delete pages that are no longer useful.** That is a real contribution too.

## Never put these on the wiki

The wiki is public. Never add passwords, keys or tokens, participant names or data, or
anything covered by an IRB protocol. A scanner checks every change for passwords and keys,
but it cannot catch everything.
