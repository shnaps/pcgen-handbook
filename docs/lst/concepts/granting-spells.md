---
title: Granting spells
---

# Granting spells

A class spell list is not the only way a character gets a spell. Three tags hand spells
out from elsewhere, and they do different jobs.

| Tag | Uses | Does |
|---|---|---|
| `SPELLS` | 8,206 | grants casting outright, with its own caster level and DC |
| `SPELLKNOWN` | 5,431 | adds a spell to what a class knows |
| `SPELLLEVEL` | 2,628 | declares what level a spell is for a class or domain |

## SPELLS

This is the innate and at-will case. A race, template or ability grants the spell
directly, and nothing about the character's classes is involved.

```
SPELLS:Class|TIMES=ATWILL|CASTERLEVEL=(max(TL,1))|Sample Light,11+CHA
```

The first argument is the **spell book** the spell goes into. It is required and may not
be empty. Everything after it is either an option or a spell.

| Option | Takes |
|---|---|
| `TIMES=` | a formula, or `ATWILL` |
| `TIMEUNIT=` | the period the count applies to |
| `CASTERLEVEL=` | a formula |

Each may appear once. A second one fails the line with `Found two TIMES entries` or the
equivalent.

**Options must come before the spells.** The parser reads options in a loop and stops at
the first argument that is not one. Anything after that is a spell name, so an option
written late is read as a spell and never resolves.

### The DC goes after a comma

```
Sample Light,11+CHA
```

The part after the comma is a DC formula, stored separately from the spell reference.
Without it the spell uses the default.

`SPELLS:.CLEARALL` removes every granted spell.

*Source: [`SpellsLst.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/SpellsLst.java)*

## SPELLKNOWN

Adds a spell to a class's known list, at a level you name. Every use in shipped data
takes the `CLASS` form.

```
SPELLKNOWN:CLASS|Sample Caster=1|Sample Light|Sample Ward
```

The class and level are joined with `=`. The spells follow.

This differs from `SPELLS` in that the character still casts it as that class, using the
class's caster level and slots. It is a change to the list, not a separate grant.

## SPELLLEVEL

Declares what level a spell counts as. Two forms:

`SPELLLEVEL:CLASS` is the common one at 1,651 uses. `SPELLLEVEL:DOMAIN` has 977 and is
owned by [domain files](../files/domain.md), which shows it in context.

```
SPELLLEVEL:CLASS|Sample Caster=2|Sample Ward
```

The shape matches `SPELLKNOWN`. The difference is that this sets the level a spell sits
at rather than granting knowledge of it.

## Kit files use a different grammar

A kit's `SPELLS` is a separate token class with its own syntax, and names the book with a
tag rather than by position:

```
SPELLS:SPELLBOOK=Prepared Spells|CLASS=Sample Caster|Sample Light
```

Shipped data has 2,356 of these against 8,206 of the ordinary form. The tag name is the
same and the grammar is not. Check which file you are in before copying a line.

## Gotchas

**An option after a spell name.** Not an error. It is read as a spell name, fails to
resolve, and the option you meant is silently absent.

**An empty first argument.** `SPELLS:|Sample Light` fails with `SpellBook in SPELLS
cannot be empty`. The book is positional and has no default.

**Expecting `SPELLKNOWN` to grant casting.** It does not. It adds to a list the class
already draws from. A character with no levels in that class gains nothing.

**Copying a kit line into an ability.** The `SPELLBOOK=` form parses only in a kit.

**`SPELLKNOWN` also exists as a bonus.** `BONUS:SPELLKNOWN` is a different thing again,
changing how many spells are known rather than which.

## Where to look

| Task | Class |
|---|---|
| the `SPELLS` tag | `plugin/lsttokens/SpellsLst.java` |
| the kit form | `plugin/lsttokens/kit/spells/SpellsToken.java` |
| the `SPELLKNOWN` tag | `plugin/lsttokens/SpellknownLst.java` |
| the `SPELLLEVEL` tag | `plugin/lsttokens/SpelllevelLst.java` |
| the bonus of the same name | `plugin/bonustokens/SpellKnown.java` |

## Related

- [Spell files](../files/spell.md) — defining a spell in the first place
- [Domain files](../files/domain.md) — `SPELLLEVEL:DOMAIN` in context
- [Class files](../files/class.md) — the spell list a class casts from
- [Granting things](granting.md) — `AUTO` and `ADD`, for everything that is not a spell
- [Prerequisites](prerequisites.md) — the `PRExxx` that may end any of these
