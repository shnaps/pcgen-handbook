---
title: Add a race
---

# Add a race

Goal: a playable race with stat adjustments, languages and a granted ability.

See [race files](../files/race.md) for the full tag list. This page is the working
order.

## Before you start

- A working folder and a campaign that loads — see [Set up](../../start/setup.md).
- `RACE:my_races.lst` uncommented in your `.pcc`.

## 1. The bare race

```
Sample Folk	RACETYPE:Humanoid	SIZE:M	MOVE:Walk,30	TYPE:Base
```

That loads and is selectable. Everything after this adds behaviour.

`RACETYPE` is not optional in practice — anything filtering by type will skip a race
without one.

## 2. Stat adjustments

```
Sample Folk	RACETYPE:Humanoid	SIZE:M	MOVE:Walk,30	TYPE:Base	BONUS:STAT|INT|2	BONUS:STAT|STR|-2
```

One `BONUS:STAT` per stat. Negative values need no special syntax.

`BONUS:STAT` is one of the most-used constructs in shipped data, at 31,969 uses.

## 3. Languages

```
AUTO:LANG|Sample Tongue
AUTO:LANG|Sample Tongue|Sample Trade Speech
```

`AUTO:LANG` grants languages outright. Pipe-separate several in one tag.

Use `LANGBONUS` instead for languages the character *may* choose with bonus language
picks.

## 4. Weapon proficiency

```
AUTO:WEAPONPROF|TYPE=Simple
```

Grant by type rather than listing weapons. Types are how shipped data does it in
nearly every case.

## 5. Granting an ability

A race grants a feat by granting an ability with the feat category:

```
ABILITY:FEAT|AUTOMATIC|Sample Feat
```

| Part | Means |
|---|---|
| `FEAT` | the ability category |
| `AUTOMATIC` | granted, not chosen, and costs nothing |
| `Sample Feat` | what to grant |

`VIRTUAL` instead of `AUTOMATIC` also grants it for free. The difference is display, not
effect: virtual abilities render differently and are counted separately by tokens such as
`VFEAT`. Either way the character possesses it and it satisfies a `PREABILITY` elsewhere.

Neither nature tests the ability's own prerequisites. Only the ones written on the
`ABILITY:` tag are carried and checked.

To let the reader choose instead:

```
ADD:ABILITY|FEAT|NORMAL|TYPE=General
```

!!! warning "Not `FEAT:`"
    Races used to grant feats with a `FEAT:` tag. That is deprecated. See
    [what changed](../../appendix/whats-changed.md).

## 6. Size and reach

```
SIZE:L	REACH:10	HANDS:2	LEGS:2
```

Size affects carrying capacity, weapon sizing and several bonuses. Changing it later
has wide effects.

## The finished file

```
# my_races.lst - example races
# Invented content. Nothing from a published book.

Sample Folk	RACETYPE:Humanoid	RACESUBTYPE:Sample	SIZE:M	MOVE:Walk,30	REACH:5	HANDS:2	LEGS:2	STARTFEATS:1	TYPE:Base	DESC:An example race.	BONUS:STAT|INT|2	BONUS:STAT|STR|-2	AUTO:LANG|Sample Tongue	ABILITY:FEAT|AUTOMATIC|Sample Feat
Sample Large Folk	RACETYPE:Humanoid	SIZE:L	MOVE:Walk,40	REACH:10	HANDS:2	LEGS:2	LEVELADJUSTMENT:1	TYPE:Base	DESC:A larger example race.	BONUS:STAT|STR|4	BONUS:STAT|DEX|-2	AUTO:WEAPONPROF|TYPE=Simple
```

## Monster races

A race that starts with racial hit dice uses `MONSTERCLASS`, which takes a class name
and a level count separated by colons:

```
MONSTERCLASS:Sample Beast:2
```

Note the colon separator. Most other multi-part tags use `|`; this one does not.

Pair it with `MONCSKILL` and `MONCCSKILL` to say which skills those levels treat as
class skills.

## Check it worked

1. Restart PCGen and load your campaign.
2. Start a new character and pick the race.
3. Confirm the stat adjustments appear.
4. Confirm the granted feat is listed and cost nothing.
5. Confirm the language is known.

## When it does not work

| Symptom | Cause |
|---|---|
| Race missing | PCC line commented out |
| Race present, odd filtering behaviour | no `RACETYPE` |
| Stat bonus not applied | stat abbreviation wrong for this game mode |
| Feat not granted | wrong category, or the ability does not exist |
| Feat granted but costs a slot | used `NORMAL` where `AUTOMATIC` was meant |
| Error naming a language | the language is not defined or loaded |

## Related

- [Race files](../files/race.md) — every race tag
- [Add a feat](new-feat.md) — defining what a race grants
- Videos: [Rapid Demonstration of Race Entry](https://www.youtube.com/watch?v=VNSdgSb0Ep8),
  [Homebrew race (Lamia)](https://www.youtube.com/watch?v=fuiReDpK5k0),
  [Shabti Race](https://www.youtube.com/watch?v=Hlr6tVMX7DI) — all 6.05/6.06
