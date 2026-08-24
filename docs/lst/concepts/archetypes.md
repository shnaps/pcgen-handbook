---
title: Archetypes
---

# Archetypes

An archetype swaps some of a class's features for different ones. PCGen has **no
archetype file type**. It is a pattern built from abilities in a category of their own.

The pattern is well established — `CATEGORY:Archetype` appears 1,763 times across 151
shipped files.

## The shape

Three pieces:

1. An **ability category** called `Archetype`, declared once.
2. One **ability per archetype**, in that category, gated to its class.
3. Each of those abilities **grants replacement features** as further abilities.

## 1. Declare the category

Ability categories are defined in a file loaded by `ABILITYCATEGORY:` in the
[PCC](../files/pcc.md):

```
ABILITYCATEGORY:Archetype	CATEGORY:Archetype	VISIBLE:NO	EDITABLE:YES	EDITPOOL:YES	FRACTIONALPOOL:NO
```

| Tag | Does |
|---|---|
| `CATEGORY` | the underlying category the pool draws from |
| `VISIBLE` | `YES`, `QUALIFY` or `NO` — whether it is listed among the ability categories |
| `EDITABLE` | whether the reader may add or remove entries in the program |
| `EDITPOOL` | whether the number of picks can be changed |
| `FRACTIONALPOOL` | whether part-picks are allowed |

The full set is `ABILITYLIST`, `CATEGORY`, `DISPLAYLOCATION`, `DISPLAYNAME`,
`EDITABLE`, `EDITPOOL`, `FRACTIONALPOOL`, `PLURAL`, `POOL`, `TYPE` and `VISIBLE`.

`VISIBLE:NO` is what shipped data uses. Archetypes are chosen through the class rather
than from a tab of their own.

## 2. Define the archetype

An ordinary ability line with the archetype category:

```
Sample Archetype	CATEGORY:Archetype	KEY:SampleArchetype	TYPE:SampleClass	COST:0	PRECLASS:1,Sample Class=1	DESC:An example archetype.
```

`PRECLASS` is what ties it to one class. `COST:0` keeps it from spending the
character's normal budget.

Nearly every archetype line in shipped data carries `KEY`, `COST`, `PRECLASS` and
`DESC`. Most also use `PREMULT` for more involved conditions.

## 3. Grant the replacement features

The archetype ability grants the features that replace the standard ones:

```
Sample Archetype	CATEGORY:Archetype	KEY:SampleArchetype	COST:0	PRECLASS:1,Sample Class=1	ABILITY:Class Feature|AUTOMATIC|Sample Replacement Feature
```

`ABILITY:<category>|AUTOMATIC|<name>` is the grant form. Shipped data grants into
categories such as `Special Ability`, `Class Feature` and `Internal`, the first being
by far the most common.

## Removing what it replaces

This is the part with no single answer. An archetype has to suppress the standard
features it swaps out. Shipped data does that by making the standard feature
conditional rather than by deleting it.

The usual approach is a marker the standard feature checks:

- The archetype sets a fact or variable.
- The class feature carries a prerequisite that fails when that marker is present.

Starfinder data uses per-class facts named for the class, such as a fact holding which
archetype a mystic or operative has taken. Other data sets use variables with `DEFINE`
and `PREVAR` instead.

Both work. Pick one and use it consistently, because mixing them makes the conditions
hard to follow.

## What the videos show

The two archetype videos predate this arrangement. The 6.06 release changed how
archetypes are marked, and shipped data now uses facts where older data used other
means.

Treat the videos as showing the *problem* — swapping class features cleanly — rather
than the current solution.

## Gotchas

**There is no archetype file.** Archetypes go in an abilities file, loaded with
`ABILITY:`. Looking for `ARCHETYPE:` in the [tag index](../reference/tag-index.md) will
find nothing.

**The category must exist before the abilities that use it.** Load the ability
category file from the PCC.

**`PRECLASS` gates availability, not application.** Without it, an archetype for one
class is offered to every class.

**Suppressing the replaced feature is the real work.** Granting new features is easy.
The standard feature has to be made conditional, or the character ends up with both.

## Related

- [Ability files](../files/ability.md) — the file archetypes live in
- [Prerequisites](prerequisites.md) — `PRECLASS`, `PREMULT` and the marker conditions
- [Variables and formulas](variables-and-formulas.md) — the variable approach
- Videos: [Adding Archetypes](https://www.youtube.com/watch?v=7f4E4m1jH9Y),
  [Making New Class Archetypes](https://www.youtube.com/watch?v=lAoIBKSomVQ),
  [6.06 Archetype FACT Improvement](https://www.youtube.com/watch?v=hTovFiKOdqE)
