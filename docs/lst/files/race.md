---
title: Race files
---

# Race files

A race file defines what a character *is* — size, movement, type, and whatever the race
grants. Loaded by `RACE:` in a [PCC](pcc.md).

Races have 22 tags of their own plus the global set. Most of a race's interesting
behaviour comes from global tags such as `BONUS`, `AUTO` and `ADD`, not from
race-specific ones.

## Minimum working line

```
Sample Folk	RACETYPE:Humanoid	SIZE:M	MOVE:Walk,30
```

What it is, how big, how fast.

## Race-specific tags

| Tag | Takes | Does |
|---|---|---|
| `RACETYPE` | a type name | the broad category. Required in practice. |
| `RACESUBTYPE` | a subtype name | finer classification. Repeatable. |
| `SIZE` | a size code | size category |
| `MOVE` | `mode,speed` pairs | movement |
| `REACH` | a number | reach in feet |
| `HANDS` | a number | how many hands the race has |
| `LEGS` | a number | how many legs |
| `HITDIE` | a number | hit die when the race grants hit dice |
| `HITDICEADVANCEMENT` | a list | monster advancement steps |
| `LEVELADJUSTMENT` | a number | effective level added to real levels |
| `CR`, `CRMOD` | a number | challenge rating and modifier |
| `FAVCLASS` | a class | favoured class |
| `STARTFEATS` | a number | feats granted at first level |
| `LANGBONUS` | a language list | bonus languages available |
| `WEAPONBONUS` | a weapon list | weapons the race is treated as proficient with |
| `MONSTERCLASS` | class and levels | monster class levels the race starts with |
| `MONCSKILL`, `MONCCSKILL` | skill lists | class and cross-class skills for monster levels |
| `MONNONSKILLHD` | a formula | hit dice granting no skill points |
| `SKILLMULT` | a number | multiplier on skill points |
| `XTRASKILLPTSPERLVL` | a number | extra skill points per level |
| `ROLE` | text | intended role, for display |

*Source: [`plugin/lsttokens/race/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/race)*

Two are deprecated: `CHOOSE` and `FEAT`.

### MOVE

Pairs of movement mode and speed, comma separated:

```
MOVE:Walk,30
MOVE:Walk,20,Swim,20
```

The mode name comes from the game mode, so which modes exist depends on it.

### SIZE

A size code such as `M` or `L`. It also accepts a formula, which is how races that
size themselves from something else are written.

### LEVELADJUSTMENT

Added to a character's real levels to give effective level. A race with
`LEVELADJUSTMENT:2` plays as though two levels higher for anything keyed to effective
level.

## Granting things

Most of what a race actually *does* comes from global tags:

| Tag | Use |
|---|---|
| `BONUS` | stat, skill and save adjustments |
| `AUTO:LANG` | languages known automatically |
| `AUTO:WEAPONPROF` | automatic weapon proficiency |
| `ABILITY` | grant an ability, usually with `CATEGORY` |
| `ADD:ABILITY` | let the reader choose an ability |
| `PRExxx` | conditions on taking the race |
| `TYPE` | classification for prerequisites and choosers |
| `DESC` | description text |

Granting a feat means granting an ability with `CATEGORY:FEAT`. The old `FEAT` tag on
races is deprecated.

## A complete example

```
# my_races.lst - example races
# Invented content. Nothing from a published book.

Sample Folk	RACETYPE:Humanoid	RACESUBTYPE:Sample	SIZE:M	MOVE:Walk,30	REACH:5	HANDS:2	LEGS:2	STARTFEATS:1	TYPE:Base	DESC:An example race.	BONUS:STAT|INT|2	BONUS:STAT|STR|-2
Sample Large Folk	RACETYPE:Humanoid	SIZE:L	MOVE:Walk,40	REACH:10	HANDS:2	LEGS:2	LEVELADJUSTMENT:1	TYPE:Base	DESC:A larger example race.	BONUS:STAT|STR|4
```

Then in the PCC:

```
RACE:my_races.lst
```

## Gotchas

**`RACETYPE` is not optional in practice.** A race with no type will load, then behave
oddly wherever something filters by type — which is a lot of places.

**`SIZE` affects more than it looks.** Reach, carrying capacity, weapon sizing and
several bonuses key off it. Changing size on an existing race has wide effects.

**`MOVE` replaces rather than adds.** Writing it twice does not give two movement
modes. Put every mode in one tag, comma separated.

**`LEVELADJUSTMENT` is easy to overspend.** It applies to everything keyed to effective
level, so a small number is a large change.

**Races reference things by name.** A `FAVCLASS` naming a class that does not exist is
reported after loading, not at the line.

## Related

- [PCC](pcc.md) — how this file gets loaded
- [Ability files](ability.md) — what a race usually grants
- [Tag index](../reference/tag-index.md) — every `Race` tag
- Videos: [Rapid Demonstration of Race Entry](https://www.youtube.com/watch?v=VNSdgSb0Ep8)
  and [Homebrew race (Lamia)](https://www.youtube.com/watch?v=fuiReDpK5k0), both
  recorded against PCGen 6.05/6.06
