---
title: Types
---

# Types

A type is a label attached to an object. Almost every other tag uses types to decide
what a rule applies to.

Types are the most-used construct in the data language. Shipped data sets a type
**197,550** times and matches on one **63,926** times. A weapon is a weapon because
something wrote `TYPE:Weapon` on it, not because PCGen knows what a weapon is.

## Setting a type

```
Test Blade	TYPE:Weapon.Melee.Simple	COST:5	WT:1
```

Dots separate types. That line sets **three** types, not one compound type. The object
is now a `Weapon`, a `Melee` and a `Simple`, and matches any of them.

Types are stored as a list on the object under `ListKey.TYPE`.

*Source: [`TypeLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/TypeLst.java)*

## Matching a type

Two forms mean the same thing:

```
TYPE=Weapon
TYPE.Weapon
```

Both are accepted wherever a token takes an object reference. The parser strips five
characters and treats the rest identically.

Dots in a match mean **and**, not or:

```
TYPE=Weapon.Melee
```

That matches objects carrying `Weapon` **and** `Melee`. Every listed type must be
present. The check runs one type at a time and stops at the first miss.

*Source: [`TokenUtilities.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/rules/persistence/TokenUtilities.java)*

Matching is case-insensitive. The value is upper-cased before lookup and types are held
in a case-insensitive map, so `TYPE=weapon` finds `TYPE:Weapon`.

*Source: [`PObject.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/PObject.java)*

## Changing a type that already exists

Four operators, for use with [`.MOD`](modifying-data.md):

| Form | Does |
|---|---|
| `TYPE:.CLEAR` | empties the list |
| `TYPE:.CLEAR.Weapon` | empties the list, then adds `Weapon` |
| `TYPE:.ADD.Weapon` | adds without clearing |
| `TYPE:.REMOVE.Weapon` | drops one type |

Three combinations are rejected at parse time, each with its own message:

- `.REMOVE.ADD.` — "Non-sensical use of .REMOVE.ADD."
- `.ADD.REMOVE.` — "Non-sensical use of .ADD.REMOVE."
- `.CLEAR` anywhere but the start — "Non-sensical use of .CLEAR"

A bare `.CLEAR` followed by anything other than a dot also fails, with "expected next
character to be .".

Duplicates are dropped. Adding a type the object already has changes nothing.

## Negation depends on where you write it

`!TYPE=` and `!TYPE.` are **not** accepted in an ordinary object reference. The parser
logs `!TYPE not supported in token` and returns nothing, so the tag is discarded.

[Choosers](choosers.md) take a different path and do support `!TYPE.`, which wraps the
type in a negating primitive. That page owns the chooser syntax.

If a negated type silently does nothing, check which of the two you are writing.

*Source: [`ChoiceSetLoadUtilities.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/rules/persistence/ChoiceSetLoadUtilities.java)*

## `TYPE:` in a `.pcc` is a different tag

The same three letters mean something unrelated in a campaign file. It sets no type
list. It records three dot-separated facts about the data set:

```
TYPE:Sample Publisher.Sample System.Sample Setting
```

| Position | Stored as |
|---|---|
| first | data producer |
| second | data format |
| third | campaign setting |

Leaving out the second or third position resets it rather than leaving it alone.

Two different token classes register the name `TYPE`, one for campaigns and one for
everything else. Which one runs depends on the file being loaded.

*Source: [`campaign/TypeToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/campaign/TypeToken.java)*

## What breaks

**A type that never matches.** Nothing warns you that `TYPE=Weapn` matched no objects.
The reference resolves to an empty group and the rule quietly applies to nothing.

**A dot in the wrong place.** A type may not start or end with a dot, and may not be
empty between two dots. Each logs `Type may not start or end with .` or `Attempt to
acquire empty Type`.

**A type containing `=`, `,` or `|`.** Rejected when the reference is built. These
characters separate arguments in the tags that consume types.

**Assuming a type does something on its own.** It does not. A type is a label. The
behaviour lives in whatever tag matches on it — a [prerequisite](prerequisites.md), a
[chooser](choosers.md), or a [bonus](bonuses.md).

## Where to look

| Task | Class |
|---|---|
| the `TYPE:` tag | `plugin/lsttokens/TypeLst.java` |
| the `TYPE:` tag in a `.pcc` | `plugin/lsttokens/campaign/TypeToken.java` |
| `TYPE=` in a reference | `pcgen/rules/persistence/TokenUtilities.java` |
| what a type match means | `pcgen/core/PObject.java`, `isType` |
| building the matched group | `pcgen/cdom/reference/AbstractReferenceManufacturer.java` |
| accepted and rejected syntax | `code/src/test/plugin/lsttokens/TypeLstTest.java` |

## Related

- [Equipment files](../files/equipment.md) — where types decide the most
- [Prerequisites](prerequisites.md) — `PRETYPE`, and testing a type on a character
- [Choosers](choosers.md) — `TYPE=` as a selection, and negation that works
- [Modifying existing data](modifying-data.md) — `.MOD`, which the four operators are for
- [The CDOM model](../../internals/cdom-model.md) — `ListKey` and how a list tag is stored
