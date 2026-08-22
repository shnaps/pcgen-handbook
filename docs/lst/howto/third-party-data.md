---
title: Use data someone else wrote
---

# Use data someone else wrote

Goal: install a data set you did not write, and understand where it goes.

Two routes: an installable archive, or copying folders in by hand.

## Where data lives

Under `data/`, organised by game mode and then by publisher:

```
data/35e/<publisher>/<book>/
data/pathfinder/<publisher>/<book>/
```

PCGen ships data from many publishers this way. Anything you add follows the same
shape, and PCGen finds it by scanning for `.pcc` files rather than by being told.

## Installable archives

Some data is distributed as a `.pcz` file, which is a zip archive with an install
descriptor inside. PCGen has a data installer that reads it.

The descriptor carries a few tags of its own:

| Tag | Does |
|---|---|
| `DEST` | where the contents should be installed |
| `MINVER` | the minimum PCGen version required |
| `MINDEVVER` | the minimum development version required |

*Source: [`campaign/installable/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/campaign/installable)*

If the version you are running is older than `MINVER`, the install is refused and
PCGen says so. That is the usual reason a data set will not install: it was built for
a newer PCGen.

The installer accepts `.pcz` and `.zip`.

## Installing by hand

Most third-party data is just folders. Copy them under the right game mode:

```
data/35e/some_publisher/some_book/
```

Restart PCGen. If the folder contains a `.pcc` with a valid `GAMEMODE:`, the campaign
appears in the source list.

Nothing registers a data set. PCGen scans for `.pcc` files at startup, so putting the
files in the right place is the whole installation.

## Out-of-cycle data

Some data is released outside PCGen's normal release cycle, usually for older or less
common game systems. It is distributed separately rather than shipping with PCGen.

It installs the same way: put it under the matching game mode and restart. The only
difference is where you obtained it.

Check that the game mode it needs exists in your install. Out-of-cycle sets sometimes
target a game mode that does not ship with PCGen, in which case you need that too.

## Loading several sources together

Select more than one campaign in the source list and PCGen loads them together. This
is normal, and it is how a core book plus supplements is meant to work.

Two things to expect when mixing sources:

- **Name collisions.** Two sets defining the same name will conflict. The error
  appears after loading, not at the line.
- **Game mode mismatch.** Sets built for different game modes cannot load together.
  The list only offers what matches.

A set can depend on another by naming it with `PCC:` in its own campaign file, which
pulls the other one's file list in.

## Adding to someone else's data

Do not edit it in place. An update replaces the folder and your changes go with it.

Instead make your own campaign that modifies theirs:

- `.MOD` on an object changes what an existing set defined.
- `.COPY` makes a variant under a new name, leaving the original alone.
- `.FORGET` removes an entry.
- `PCC:` pulls their campaign in so yours loads on top.

Each is written as a suffix on the object name in field 0, so a line modifying an
existing feat starts `Sample Feat.MOD` rather than `Sample Feat`.

## Gotchas

**A data set that does not appear was not found.** Check it is under a game mode
folder inside `data/`, and that its `.pcc` names a game mode that exists.

**Install refused with a version message.** The set needs a newer PCGen than you are
running. Nightly builds are usually newer than the last release.

**Editing shipped data is temporary.** Updates overwrite it. Copy first.

**Third-party data can be as old as the videos.** A set written for 6.05 may use tags
that have since been removed. See [what changed](../../appendix/whats-changed.md).

## Related

- [PCC](../files/pcc.md) — what makes a folder a loadable campaign
- [Set up](../../start/setup.md) — where the install folder is
- [When it breaks](../../start/when-it-breaks.md) — reading load errors
- Videos: [Install or use 3rd Party Sources](https://www.youtube.com/watch?v=yYzOJzUVNP0),
  [Install OOC data](https://www.youtube.com/watch?v=HY3jsMl3jo4) — both 6.05/6.06
