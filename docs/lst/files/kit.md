---
title: Kit files
---

# Kit files

A kit is a bundle applied to a character in one step. Starting equipment, a monster's
default statistics, an NPC package.

Shipped data holds **6,922** kits across 309 files. Most are generated monster defaults
rather than hand-written packages, so read them for syntax and not as style.

## The shape

A kit file is not one line per object. It is a header line and then the lines it owns.

```
STARTPACK:Sample Explorer	TYPE:Kit	VISIBLE:YES	EQUIPBUY:0
NAME:Sample Explorer
SKILL:Sample Skill	RANK:2
GEAR:Test Blade	QTY:1
ABILITY:CATEGORY=FEAT|Sample Feat
```

`STARTPACK` opens a kit and names it. Every line after it belongs to that kit, until the
next `STARTPACK`. That is the part to get right, because indentation and blank lines mean
nothing here.

*Source: [`plugin/lsttokens/kit/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/kit)*

## The header line

| Tag | Uses | Does |
|---|---|---|
| `VISIBLE` | 6,191 | whether it appears in the kit list |
| `EQUIPBUY` | 5,890 | how bought equipment is priced |
| `TYPE` | 5,728 | [types](../concepts/types.md), used to group kits |
| `PREMULT` | 4,650 | who may take it |
| `APPLY` | 793 | permanent, or once |
| `TOTALCOST` | 143 | a budget for the whole kit |

`VISIBLE:QUALIFY` is the common value in shipped data. It shows the kit only to a
character who qualifies for it, which is how monster defaults stay out of the way.

## The lines a kit owns

Twelve kinds, in twelve packages under `plugin/lsttokens/kit/`. By use in shipped data:

| Line | Uses | Grants |
|---|---|---|
| `SKILL` | 18,574 | ranks in a skill |
| `ABILITY` | 13,080 | an ability, with its category |
| `GEAR` | 8,793 | equipment |
| `STAT` | 4,846 | a statistic value |
| `RACE` | 4,765 | the character's race |
| `NAME` | 4,462 | the character's name |
| `ALIGN` | 4,098 | alignment |
| `SPELLS` | 2,356 | spells, in the kit's own grammar |
| `KIT` | 2,120 | another kit, applied as part of this one |
| `TEMPLATE` | 523 | a template |
| `SELECT` | 420 | how many of the following to take |
| `CLASS`, `FUNDS`, `GENDER`, `TABLE`, `LANGBONUS` | under 500 each | as named |

A `KIT` line inside a kit is how the generated monster packs are built. One base kit
covers the creature type, then a small kit per variant.

## Prerequisites go on the line they gate

```
RACE:Sample Folk	!PRERACE:1,%
```

Each owned line carries its own `PRExxx`. The header's `PREMULT` decides whether the kit
may be taken at all. A line's own prerequisite decides whether that one line applies.

`%` in a prerequisite is the wildcard for any value, which is how a monster default
recognises a character who has no race yet.

## Gotchas

**Losing track of which `STARTPACK` you are under.** A line added in the wrong place joins
the kit above it. Nothing warns you, because the line is valid either way.

**`SPELLS` in a kit is not the `SPELLS` tag.** It is a separate token class with a
different grammar. See [granting spells](../concepts/granting-spells.md).

**`APPLY:PERMANENT` against `APPLY:INSTANT`.** A permanent kit is recorded on the
character and cannot be applied a second time. An instant one is not saved with the
character and may be applied as often as you like.

**Reading shipped kits as examples of style.** The bulk of them are generated variants of
one monster, repeated per colour or size. The syntax is correct and the structure is not
what a hand-written kit should look like.

## Where to look

| Task | Class |
|---|---|
| the header tags | `plugin/lsttokens/kit/startpack/` |
| the base line tags | `plugin/lsttokens/kit/` — 10 classes |
| each owned line kind | `plugin/lsttokens/kit/{skill,gear,ability,spells,...}/` |
| accepted and rejected syntax | `code/src/test/plugin/lsttokens/kit/` — 47 tests |

## Related

- [Prerequisites](../concepts/prerequisites.md) — the `PRExxx` on each line
- [Granting spells](../concepts/granting-spells.md) — why a kit's `SPELLS` differs
- [Equipment files](equipment.md) — what a `GEAR` line points at
- [Types](../concepts/types.md) — how kits are grouped
