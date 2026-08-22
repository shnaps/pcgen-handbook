---
title: Game modes
---

# Game modes

A game mode is a rules system. `35e`, `Pathfinder`, `Modern`, `Starfinder` and others
ship with PCGen — 20 folders in total.

Every campaign names one with `GAMEMODE:` in its [PCC](../files/pcc.md), and that
decides which rules the data is read under.

## Where they live

`system/gameModes/<Name>/`. The folder name is what `GAMEMODE:` must match.

This is separate from `data/`. Game modes define the rules; `data/` defines the content
those rules operate on.

## What makes a folder a game mode

PCGen only treats a folder as a game mode if it contains **both**:

- `miscinfo.lst`
- `statsandchecks.lst`

Both must be present. Neither needs to have much in it.

*Source: [`GameModeFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/GameModeFileLoader.java)*

!!! note "`statsandchecks.lst` is mostly a marker"
    The name suggests it defines stats and saving throws. It does not. Across every
    shipped game mode it holds only bonus spell level lines, and six modes have it
    empty.

    Stats are ordinary data objects, loaded from `data/` by `STAT:` in a PCC. Look
    there, not here, when you want to change a stat.

## The files

Loaded in this order:

| File | Holds |
|---|---|
| `miscinfo.lst` | most of the mode. See below. |
| `statsandchecks.lst` | bonus spell levels |
| `level.lst` | experience thresholds and skill rank caps per level |
| `rules.lst` | optional rules the user can switch on and off |
| `equipmentslots.lst` | where equipment can be worn |
| `paperInfo.lst` | paper sizes for output |
| `bio/traits.lst`, `bio/locations.lst` | character background lists |
| `load.lst` | carrying capacity and encumbrance |
| `sizeAdjustment.lst` | size categories |
| `equipIcons.lst` | icons |
| `codeControl.lst` | switches for engine features |
| `migration.lst` | renames, so old data keeps working |
| `pointbuymethods.lst` | point buy configurations |
| `unitset.lst` | units of measurement |

Only `miscinfo.lst` and `statsandchecks.lst` are required. A mode includes the rest as
it needs them.

## miscinfo.lst

The biggest file, and the one with the most tags. 229 tags in the
[tag index](../reference/tag-index.md) apply to game mode files, most of them here.

It is not one object per line. Each line starts with a **line type** saying what it
defines:

| Line type | Defines |
|---|---|
| `WIELDCATEGORY` | how weapon size relates to wielding |
| `ACTYPE` | armour class types and how they combine |
| `TAB` | interface tabs and their names |
| `BASEDICE` | weapon damage progression by size |
| `WEAPONTYPE`, `WEAPONCATEGORY` | weapon classification |
| `ROLLMETHOD` | stat generation methods |
| `CLASSTYPE` | class categories |
| `ABILITYCATEGORY` | ability categories such as feats |
| `SPELLRANGE` | named spell ranges |
| `OUTPUTSHEET` | default character sheets |
| `UNITSET` | measurement units |

So one file defines a great deal of what the interface shows and how the rules behave.

## Optional rules

`rules.lst` defines switches the user sees in preferences. Field 0 is `NAME:` with the
key the rule is referred to by:

```
NAME:SampleOptionalRule	VAR:SYS_SAMPLERULE	DEFAULT:Yes	DESC:What the rule does.
```

| Tag | Is |
|---|---|
| `NAME` | the rule key, in field 0 |
| `VAR` | the variable data checks against |
| `DEFAULT` | `Yes` or `No` |
| `DESC` | the text shown in preferences |

Data then checks it with `PRERULE`, which is how one data set supports a rule being on
or off.

## Migration

`migration.lst` maps old names to new ones so data written for an earlier version keeps
loading. In `35e` it is the largest file in the folder by a wide margin.

This is worth knowing when something loads despite using an old name — migration may be
quietly translating it.

## Making your own

Copy an existing mode's folder, rename it, and set `GAMEMODE:` in your PCC to the new
folder name.

PCGen ships `system/my_gamemode/` as a starting point.

A new game mode is a large undertaking. Most homebrew does not need one — adding data
to an existing mode covers nearly everything. Reach for a new mode when the rules
themselves differ, not the content.

## Gotchas

**`GAMEMODE:` must match the folder name.** A mismatch means the campaign never
appears, with no obvious error.

**Game mode files are not `.lst` data files in the usual sense.** They use line types
rather than one object per line, and their tags are not valid in `data/` files.

**Changing a shipped game mode is risky.** An update replaces it. Copy it first, exactly
as with homebrew data.

## Related

- [PCC](../files/pcc.md) — where `GAMEMODE:` is set
- [Tag index](../reference/tag-index.md) — game mode file tags are marked `gamemode-file`
- Videos: [Gamemode](https://www.youtube.com/watch?v=9vbBuuCmVjU),
  [Create additional Ability Scores](https://www.youtube.com/watch?v=2P9KYV3cD8s) —
  both 6.05/6.06
