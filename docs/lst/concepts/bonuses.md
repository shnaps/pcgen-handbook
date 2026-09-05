---
title: Bonuses
---

# Bonuses

A bonus is a `BONUS:` tag: a number added to something on the character. It is the most
used tag in PCGen's data by a wide margin — **170,741 uses across 2,753 files**.

There are 55 bonus subtypes. Learning the shape and the stacking rule covers nearly
all of them.

## The shape

```
BONUS:<subtype>|<target>|<value>|<extras>
```

```
BONUS:STAT|STR|2
BONUS:SKILL|Sample Skill|2
BONUS:COMBAT|AC|1|TYPE=Armor
```

| Part | Is |
|---|---|
| subtype | what kind of thing is being changed, such as `STAT` or `SKILL` |
| target | which one, comma separated for several |
| value | a number or a formula |
| extras | `TYPE=` and any `PRExxx`, in any order |

A comma-separated target list applies the bonus to each entry separately:

```
BONUS:SKILL|Sample Skill,Sample Craft|2
```

*Source: [`Bonus.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/core/bonus/Bonus.java)*

## The value is a formula

The value field is not restricted to a number. It becomes a `Formula`, so a variable or
an expression works:

```
BONUS:SKILL|Sample Skill|SampleVariable
BONUS:HP|CURRENTMAX|TL*2
```

See [variables and formulas](variables-and-formulas.md).

The value may not start with `PRE`. That is checked at parse time and rejected, because
otherwise a misplaced prerequisite would silently become a value.

## Stacking

This is the part worth reading twice.

**By default, bonuses of the same type do not stack. Only the largest applies.**

```
BONUS:COMBAT|AC|1|TYPE=Armor
BONUS:COMBAT|AC|3|TYPE=Armor
```

The character gets 3, not 4.

Three things change that:

| Written | Effect |
|---|---|
| no `TYPE=` at all | stacks with everything |
| `TYPE=<name>` | only the largest of that name applies |
| `TYPE=<name>.STACK` | always adds, even against the same name |
| `TYPE=<name>.REPLACE` | stacks with other `.REPLACE` bonuses of that name, then the higher of that total and the plain total wins |

The game mode also carries a list of type names that stack anyway. `Dodge` is the
familiar example in the d20 modes. So a type stacks if the game mode says it does, or
if the data says `.STACK`.

**Negative values always sum.** A penalty is never discarded because a larger penalty of
the same type exists. That asymmetry surprises people who assume the max rule is
symmetric.

*Source: [`BonusManager.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/core/BonusManager.java)*

## Prerequisites on a bonus

Append any `PRExxx` and the bonus applies only when it passes:

```
BONUS:SKILL|Sample Skill|2|PRERACE:1,Sample Folk
```

The prerequisite is evaluated **every time the character is recalculated**, not once at
load. That is what makes conditional bonuses track a changing character.

See [prerequisites](prerequisites.md).

## Where a bonus is legal

The `BONUS` token declares `CDOMObject`, so it works on nearly every object type: races,
classes, abilities, templates, equipment, domains, deities.

Two refusals:

- Objects marked `Ungranted` reject it. Spells are the case you will meet.
- `PREAPPLY:` inside a `BONUS:` is rejected. That belongs to `TEMPBONUS:`.

*Source: [`BonusLst.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/BonusLst.java)*

## The ones you will actually meet

Ranked by use in shipped data:

| Subtype | Uses | Changes |
|---|---|---|
| `VAR` | 82,287 | a variable |
| `STAT` | 34,052 | an ability score |
| `SKILL` | 10,971 | a skill total |
| `COMBAT` | 10,550 | attack, AC, initiative |
| `ABILITYPOOL` | 9,064 | how many abilities of a category may be taken |
| `WEAPONPROF=` | 6,569 | a weapon proficiency |
| `SAVE` | 5,442 | a saving throw |
| `WEAPON` | 2,280 | a weapon's attack or damage |
| `SPELLCAST` | 1,591 | spells per day |
| `SITUATION` | 1,218 | a situational modifier |

`BONUS:VAR` dominates because it feeds the variable system rather than a fixed
character field. Data defines a variable, bonuses adjust it, and other tags read it.

### Subtypes that take a tag on the subtype itself

A few subtypes are written with `=` and a tag before the first pipe:

```
BONUS:WEAPONPROF=TYPE.Sample|TOHIT|1
```

`WEAPONPROF` is the common one. The token registers itself under the name
`WEAPONPROF=`, so writing it without the `=` part fails to find a handler.

## TEMPBONUS

`TEMPBONUS:` is a different tag, not a variant spelling. It defines a bonus the reader
switches on and off in the interface — a spell effect, a potion, a condition.

```
TEMPBONUS:PC|STAT|STR|4
```

| Sub-token | Applies to |
|---|---|
| `PC` | the character carrying the ability |
| `ANYPC` | the same character. The difference is where the effect may be offered from |
| `EQ` | a piece of equipment |

Note the third is `EQ`, not `EQUIP`.

Shipped data has 3,225 `TEMPBONUS:` uses against 170,741 `BONUS:` uses, so it is a
specialist tool rather than a default.

## Where it is applied

Bonuses are collected into a map when the character recalculates. Two useful places to
put a breakpoint:

| Method | Does |
|---|---|
| `PlayerCharacter.calcActiveBonuses` | triggers a recalculation |
| `BonusManager.buildActiveBonusMap` | builds the totals |

Read back through `PlayerCharacter.getTotalBonusTo(type, name)`. See
[the character model](../../internals/facets.md).

## Gotchas

**A malformed bonus is skipped, not fatal.** An unknown subtype, a bad formula or an
empty target logs an error and loading continues. The line loads; the bonus does not
exist. Check the log.

**`BONUS:ABILITYPOOL` validates late.** A wrong category name passes the line and is
reported after loading, so the error names the tag rather than the file.

**Untyped bonuses always stack.** Leaving `TYPE=` off is not a neutral choice. It is the
choice that stacks with everything.

**`.STACK` is part of the type string.** `TYPE=Armor` and `TYPE=Armor.STACK` are not the
same type, and mixing both on one character behaves accordingly.

**A comma in the target is a list, not part of a name.** An object whose name contains a
comma cannot be targeted directly.

## Related

- [Variables and formulas](variables-and-formulas.md) — what `BONUS:VAR` feeds, and `MODIFY`
- [Prerequisites](prerequisites.md) — conditions on a bonus
- [Choosers](choosers.md) — the other big cross-cutting tag
- [Tag index](../reference/tag-index.md) — all 55 bonus subtypes
