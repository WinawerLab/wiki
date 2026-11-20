---
title: Where data and files live
owner: JWinawer
reviewed: 2024-06-10
review_every: 12
---

# Where data and files live

## The lab server

Our main storage is a Synology server. **Data and analysis code for lab projects belong here**,
not only on a laptop.

| From | Address |
|---|---|
| Mac (Finder → Go → Connect to Server) | `smb://winawerlab.psych.nyu.edu/server` |
| Windows | `\\winawerlab.psych.nyu.edu\server` |
| Web browser | `https://winawerlab.psych.nyu.edu` (your browser may show a security warning) |

Log in with your NYU NetID as `ad\yournetid` and your NetID password.
Ask Jon if you do not have access. You must be on the NYU network or VPN.

!!! question "To fill in"
    How project folders on the server should be organized (a plan is being drafted),
    and how the server is backed up.

## Lab Google Drive

There is a shared lab Google Drive. Ask Jon for access. Use it for documents, not large data.

## GitHub

Code goes in Git and on GitHub, in the [WinawerLab organization](https://github.com/WinawerLab).
Data and figures do not go in Git: they are large and change as whole files.

## NYU high performance computing (HPC)

NYU has a computing cluster for large analyses. See
[NYU Research Technology Services](https://www.nyu.edu/life/information-technology/research-computing-services/high-performance-computing.html)
for accounts and documentation. Papers that use it must include an acknowledgment; see
[Authorship and publishing](../how-we-work/authorship.md#nyu-high-performance-computing-hpc).

## Learning good data habits

NYU Libraries runs a [data management guide](https://guides.nyu.edu/data_management) and classes.
