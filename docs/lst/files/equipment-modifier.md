---
title: Equipment modifier files
---

# Equipment modifier files

An equipment modifier changes an item without a new item being written. Masterwork,
material, magical enhancement and spell charges are all modifiers.

One `.lst` file defines them. The [`EQMOD`](equipment.md) tag on a piece of equipment
attaches them. Shipped data attaches modifiers **9,628** times.

## Attaching one

```
Test Blade	TYPE:Weapon.Melee	EQMOD:MWORKW
```

Dots separate modifiers. Pipes separate one modifier's arguments.

```
EQMOD:MWORKW.PLUS1W
EQMOD:SPL_CHRG|SPELLNAME[Sample Spell]SPELLLEVEL[3]CASTERLEVEL[5]CHARGES[50]
```

The first line attaches two modifiers. The second attaches one and gives it four
bracketed values.

`ALTEQMOD` does the same for the second head of a double weapon.

### Two keys that are not modifiers

| Key | Does |
|---|---|
| `_WEIGHTADD` | sets a weight adjustment directly |
| `_DAMAGE` | overrides the damage string |

Both are read by the tag itself and never resolved as a modifier. `EQMOD:NONE` is
deprecated and ignored, with a notice.

### `=` becomes `|`

An argument written with `=` is stored with a `|` in its place. The separator inside a
field is already `|`, so data cannot write one, and this is how the value survives.

*Source: [`EqmodToken.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/equipment/EqmodToken.java)*

## Defining one

The line starts with the modifier's key, then its tags.

```
Sample Keen	TYPE:Weapon	PLUS:1	COST:0	ITYPE:Magic	NAMEOPT:NORMAL	SPROP:Doubles threat range
```

Fifteen tags are current, plus eleven `CHOOSE` variants.

| Tag | Does |
|---|---|
| `PLUS` | the enhancement bonus, as a number |
| `COST` | what it adds to the price. May be a formula |
| `COSTDOUBLE` | whether the cost doubles |
| `COSTPRE` | cost applied before other adjustments |
| `ITYPE` | [types](../concepts/types.md) the modified item gains |
| `ARMORTYPE` | changes the armour type |
| `REPLACES` | other modifier keys this one displaces |
| `ASSIGNTOALL` | applies to every head, not just one |
| `NAMEOPT` | how the modified item is named |
| `FORMATCAT` | where the name fragment goes |
| `VISIBLE` | whether it shows |
| `CHARGES` | a charge range |
| `FUMBLERANGE` | changes the fumble range |
| `SPROP` | a special property line |
| `BONUS` | any [bonus](../concepts/bonuses.md), as elsewhere |

### Naming the modified item

`NAMEOPT` decides what the player sees:

| Value | Result |
|---|---|
| `NORMAL` | the name, with the choices in brackets |
| `NOLIST` | the name only |
| `NONAME` | the choices only |
| `SPELL` | the first choice treated as a spell |
| `TEXT=` | literal text you supply |

This is the tag to reach for when a modified item reads badly on the sheet.

*Source: [`NameoptToken.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/equipmentmodifier/NameoptToken.java)*

### Choices

A modifier can ask for a value when it is applied. Eleven forms:

`ABILITY`, `EQUIPMENT`, `FEAT`, `SKILL`, `SKILLBONUS`, `STATBONUS`, `NUMBER`, `STRING`,
`NOCHOICE`, `EQBUILDER.EQTYPE`, `EQBUILDER.SPELL`.

The chosen value is available to the modifier's other tags as `%CHOICE`:

```
Sample Material	COST:3*%CHOICE	CHOOSE:NUMBER|MIN=1|MAX=10
```

[Choosers](../concepts/choosers.md) owns the general `CHOOSE:` syntax. These eleven are
the subset an equipment modifier accepts.

## Gotchas

**A modifier key that does not exist.** The reference fails to resolve, and the error
names the item rather than the modifier file.

**A dot inside a modifier key.** Dots separate modifiers, so a key containing one is read
as two. Some shipped data uses keys with spaces, such as `Material ~ Adamantine`, which
is legal. Dots are not.

**Writing `|` in an argument.** It splits the argument. Use `=` and let the loader convert
it.

**Expecting `EQMOD:NONE` to clear modifiers.** It is ignored and logs a deprecation
notice.

## Where to look

| Task | Class |
|---|---|
| the `EQMOD` tag | `plugin/lsttokens/equipment/EqmodToken.java` |
| the modifier file's tags | `plugin/lsttokens/equipmentmodifier/` — 15 classes |
| the choice forms | `plugin/lsttokens/equipmentmodifier/choose/` — 11 classes |
| naming options | `pcgen/cdom/enumeration/EqModNameOpt.java` |
| accepted and rejected syntax | `code/src/test/plugin/lsttokens/equipmentmodifier/` — 14 tests |

## Related

- [Equipment files](equipment.md) — the items modifiers attach to
- [Types](../concepts/types.md) — what `ITYPE` adds
- [Bonuses](../concepts/bonuses.md) — `BONUS` on a modifier
- [Choosers](../concepts/choosers.md) — `CHOOSE:` and `%CHOICE`
