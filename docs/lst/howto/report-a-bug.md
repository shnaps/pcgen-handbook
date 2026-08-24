---
title: Report a bug
---

# Report a bug

Goal: get a problem in front of the people who can fix it, in a form they can act on.

PCGen tracks work in **Jira**, not GitHub issues. That surprises people arriving from
the repository.

## Where to file

| Tracker | For |
|---|---|
| [Jira](https://pcgenorg.atlassian.net) | the primary tracker. Make an account here. |
| [CODE project](https://pcgenorg.atlassian.net/projects/CODE/issues) | bugs in the program itself |
| [DATA project](https://pcgenorg.atlassian.net/projects/DATA/issues) | bugs in the shipped game data |

PCGen's own README directs contributors to Jira and says work is tracked there so
release notes can be generated from it.

GitHub issue templates exist too, but Jira is where the project actually works.

## Which project

The split matters, because the two are fixed by different people.

- **A rule is implemented wrongly, a class grants the wrong thing, a book's content is
  missing or mistyped** — that is `DATA`. It is fixed by editing `.lst` files, and you
  could fix it yourself.
- **A tag does not behave as documented, the program crashes, the interface is wrong** —
  that is `CODE`. It is fixed in Java.

If you are not sure, read the failing line. If the fix would be a change to a `.lst`
file, it is data.

## What to include

Anything that lets someone reproduce it without asking you questions:

1. **PCGen version.** Release or nightly, and which. This is the single most common
   omission, and the answer often is that a nightly already fixed it.
2. **Game mode and sources loaded.** A bug in one book's data is invisible without them.
3. **What you did, what happened, what you expected.** In that order.
4. **The log.** `pcgen.log` names the file and line. Paste the relevant part rather
   than describing it. See [when it breaks](../../start/when-it-breaks.md).
5. **A minimal example** if you can make one. Two lines that reproduce it beats a whole
   data set.

## Check it is not already known

Search Jira before filing. Also check whether a nightly build fixes it. The last tagged
release is `7.00.001` from February 2026, so a bug found in a release may have been fixed long
ago.

## Fixing it yourself

Data bugs are approachable, which is the reason this handbook exists. The workflow —
ticket, branch, build, pull request — is the same one code changes follow, and
[contributing](../../internals/contributing.md) covers it.

## Asking first

[Discord](https://discord.gg/M7GH5BS) is the active channel. Ask there if you are
unsure whether something is a bug, or which project it belongs in. It is faster than
filing and waiting.

## A caveat on documentation bugs

There is a `DOCS` project in Jira. It has open tickets going back years and none have
been resolved since 2018.

Filing there records the problem, but do not expect a response. Documentation is the
part of the project with the least attention — which is why this handbook reads the
source instead.

## Related

- [When it breaks](../../start/when-it-breaks.md) — diagnosing before reporting
- [What changed](../../appendix/whats-changed.md) — check the tag was not removed
- Video: [How to Submit a Bug or Feature Request](https://www.youtube.com/watch?v=kKWRIkU1LZ8),
  recorded against 6.05/6.06
