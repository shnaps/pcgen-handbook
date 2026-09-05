---
title: PCC (campaign file)
---

# PCC — the campaign file

A `.pcc` file is **not game data**. It is a manifest. It names a data set, says which
game mode it belongs to, and lists the `.lst` files PCGen should load.

Every campaign you can pick in PCGen's source selection screen is one `.pcc`.

## What it does

Two jobs, and they are worth keeping separate in your head:

1. **Identity** — the name shown in the source list, the game mode, the publisher, how
   it is grouped in the tree.
2. **Routing** — which data files to load, and what kind of data each one holds.

## Minimum working file

```
CAMPAIGN:Testburg
GAMEMODE:35e
TYPE:Homebrew
ABILITY:my_abilities.lst
```

Four lines. A name, a game mode, a place in the tree, and one data file.

Unlike `.lst` files, a PCC has **one tag per line**. There are no tab-separated fields
here.

## Identity tags

| Tag | Does |
|---|---|
| `CAMPAIGN` | the name shown in the source list. Required. |
| `GAMEMODE` | which rules system this belongs to, such as `35e` or `Pathfinder`. Required. |
| `TYPE` | where it sits in the source tree. **Maximum three levels**, separated by `.` |
| `RANK` | sort order among sources. A number. |
| `BOOKTYPE` | classification, pipe-separated for more than one — `Homebrew\|Supplement` |
| `SHOWINMENU` | whether it appears in the source list. Takes `YES` or `NO`. |
| `SETTING`, `GENRE` | descriptive grouping |
| `SOURCELONG`, `SOURCESHORT`, `SOURCEWEB`, `SOURCEDATE` | where the material came from |
| `PUBNAMELONG`, `PUBNAMESHORT`, `PUBNAMEWEB` | publisher |
| `DESC` | description shown to the reader |

`TYPE:Homebrew.Testburg.Rules` produces three nested levels in the source tree. A
fourth is rejected, not ignored.

*Source: [`campaign/TypeToken.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/campaign/TypeToken.java)*

!!! warning "SHOWINMENU matters more than it looks"
    A campaign without `SHOWINMENU:YES` can still be loaded by another PCC, but it will
    not appear in the source list on its own. It is also skipped by PCGen's data test
    harness, so a broken file can pass testing without ever being loaded. See
    [verifying a dataset](../../internals/load-pipeline.md#verifying-a-dataset-loads).

## File-loading tags

Each of these names a data file and says what kind of data it holds. PCGen files the
path under a key, then runs the matching loader.

| Tag | Loads |
|---|---|
| `ABILITY` | abilities, including feats |
| `ABILITYCATEGORY` | custom ability categories |
| `CLASS` | classes |
| `RACE` | races |
| `SKILL` | skills |
| `SPELL` | spells |
| `TEMPLATE` | templates |
| `EQUIPMENT` | equipment |
| `EQUIPMOD` | equipment modifiers |
| `DEITY` | deities |
| `DOMAIN` | domains |
| `KIT` | starting kits |
| `LANGUAGE` | languages |
| `COMPANIONMOD` | companion and familiar modifiers |
| `WEAPONPROF`, `ARMORPROF`, `SHIELDPROF` | proficiencies |
| `BIOSET` | age, height and weight tables |
| `ALIGNMENT`, `SIZE`, `STAT`, `SAVE` | game mode building blocks |
| `DATACONTROL`, `DATATABLE`, `GLOBALMODIFIER`, `VARIABLE`, `DYNAMIC` | formula system data |

The full list is in the [tag index](../reference/tag-index.md) under `Campaign`.

The mapping is mechanical. The whole implementation of the `SKILL:` tag is naming its
key:

```java
public String getTokenName() { return "SKILL"; }
protected ListKey<CampaignSourceEntry> getListKey() { return ListKey.FILE_SKILL; }
```

*Source: [`campaign/SkillToken.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/campaign/SkillToken.java)*

So a data file is loaded as skills because the PCC said `SKILL:`, not because of what
is inside it or what it is called. Name a races file with `SKILL:` and PCGen will try
to read races as skills.

## Paths

Paths are relative to the PCC's own folder by default.

| Form | Means |
|---|---|
| `my_skills.lst` | same folder as the PCC |
| `sub/my_skills.lst` | a subfolder |
| `*/_universal/races.lst` | searched for: homebrew directory, then vendor, then data |
| `@/some/path.lst` | the data directory |
| `&/some/path.lst` | the vendor directory |
| `$/some/path.lst` | your Homebrew Data directory |

The `*/` form is how shared data is reused across campaigns. It is a search rather than
a location, so the same reference resolves differently depending on which of the three
directories holds a matching file. The other three name one directory and do not search.

<!-- src: code/src/java/pcgen/persistence/lst/URIFactory.java -->

## Conditional loading

Append `|PRExxx` to load a file only when a condition holds:

```
CLASS:psionics.lst|PRERULE:1,SYS_PSIONICS
```

## Depending on another campaign

Two tags reach outside this file.

```
PCC:base_set/base_set.pcc
```

`PCC:` pulls in another campaign file. Use it to split a large data set across folders,
or to layer one campaign on another. `LSTEXCLUDE:` names `.lst` files to skip.

Both behave in ways the syntax does not suggest. The include is recursive, a missing one
is silent, and the exclusion is not limited to this campaign. [Sources and load
order](../concepts/sources.md#depending-on-another-source) owns both.

## A complete example

```
# Testburg - example homebrew campaign
CAMPAIGN:Testburg
GAMEMODE:35e
TYPE:Homebrew.Testburg
RANK:9
BOOKTYPE:Homebrew
SHOWINMENU:YES
SETTING:Testburg
GENRE:Fantasy
PUBNAMELONG:Example Publisher
SOURCELONG:Testburg Campaign Guide
SOURCESHORT:TCG
DESC:Example data. Nothing here is from a published book.

ABILITY:my_abilities.lst
SKILL:my_skills.lst
RACE:my_races.lst
CLASS:my_classes.lst
```

## Gotchas

**A file PCGen does not load is a file that does not exist.** Writing data is only
half the job. If the PCC does not name it, nothing happens and nothing complains.

**Commented-out lines are the usual cause.** Shipped templates comment out most file
lines. Removing the `#` is what enables one.

**One tag per line.** No tabs. A PCC is not an LST file.

**`GAMEMODE` must match a real game mode.** It is the name of a folder under
`system/gameModes/`. A typo means the campaign never appears.

**Load order within the PCC does not matter much.** Everything is loaded before
references are resolved, so a class may reference a feat listed later. See
[how loading works](../../start/how-loading-works.md).

## Related

- [Line format](../concepts/line-format.md) — how `.lst` files differ from this
- [Load pipeline](../../internals/load-pipeline.md) — what reads this file
- [Tag index](../reference/tag-index.md) — every `Campaign` tag
