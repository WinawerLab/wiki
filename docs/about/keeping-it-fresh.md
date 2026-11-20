---
title: How it stays up to date
owner: JWinawer
reviewed: 2026-11-20
review_every: 12
---

# How this wiki stays up to date

Wikis usually die the same way: pages go out of date, nobody can tell which ones, so people
stop trusting all of them and stop editing. This wiki tries to prevent that in four ways.

## 1. Every page has an owner and a "last checked" date

The owner is not the only person who may edit the page. Anyone can. The owner is the person
who makes sure *someone* checks it from time to time. Each page also says how often it should
be checked (`review_every`, in months). Pages about money and rules change often, so they get
checked often. Pages about how we work change slowly.

## 2. Readers can see when a page is old

When a page goes past its check date, a yellow banner appears at the top: *"This page may be
out of date."* Readers know to be careful, and anyone can clear the banner by checking the page
and updating the date. The site is rebuilt every week so the banners stay current.

The [Wiki health](health.md) page lists every page and its status.

## 3. A weekly check sends reminders

Every Monday, an automatic check on GitHub:

- updates one GitHub issue, **"Wiki freshness report"**, that lists the pages due for a check,
  grouped by owner (each owner gets a GitHub notification);
- picks a **page of the week**: the page checked longest ago, so every page gets read in turn;
- flags pages whose owner has left the lab (anyone not marked `current: true` in `people.yml`);
- flags pages with a broken header.

A second weekly check looks for **broken links** and opens an issue if it finds any.

## 4. People leaving hand off their pages

The [Leaving the lab](../leaving.md) checklist includes finding new owners for your pages.

## What the automatic checks do not do

They cannot tell whether a page is *right*. Only people can. The checks just make sure that
every page gets looked at regularly, and that readers know how old the information is.

## For maintainers

The checks live in `.github/workflows/` and `scripts/check_freshness.py` in the
[repository](https://github.com/WinawerLab/wiki). If a check itself fails, GitHub opens an issue
titled "Wiki automation failed" so the failure is not silent.
