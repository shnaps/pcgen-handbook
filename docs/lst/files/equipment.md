---
title: Equipment files
---

# Equipment files

An equipment file defines items: weapons, armour, gear, containers. Loaded by
`EQUIPMENT:` in a [PCC](pcc.md).

Equipment has 34 tags of its own, more than any other common file type. Which ones
matter depends entirely on what kind of item you are writing.

## Minimum working line

```
Sample Gear	TYPE:Gear	COST:5	WT:1
```

A name, what kind of thing it is, what it costs, what it weighs.

`COST` and `WT` appear on nearly every item — about 44,000 and 29,500 uses in shipped
data.

## TYPE decides everything

```
TYPE:Weapon.Melee.Simple
TYPE:Armor.Medium
TYPE:Gear
```

Dot-separated, and it is not just labelling. `TYPE` determines which other tags mean
anything, how proficiency is matched, and where the item appears in the interface.

Get this right first. A weapon without a weapon type will not behave as a weapon.

## Weapons

| Tag | Takes | Does |
|---|---|---|
| `DAMAGE` | dice notation | damage dealt |
| `CRITMULT` | `x2`, `x3`, or `-` | critical multiplier |
| `CRITRANGE` | a number | how many numbers threaten a critical |
| `WIELD` | `Light`, `OneHanded`, `TwoHanded` | how it is held |
| `RANGE` | a number | range increment |
| `ALTDAMAGE`, `ALTCRITMULT`, `ALTCRITRANGE` | as above | the second head of a double weapon |
| `PROFICIENCY` | `WEAPON\|<name>` | which proficiency covers it |
| `REACH`, `REACHMULT` | numbers | reach in feet, and a multiplier |
| `FUMBLERANGE` | a number | fumble threshold |

```
Sample Blade	TYPE:Weapon.Melee.Martial	DAMAGE:1d8	CRITMULT:x2	CRITRANGE:2	WIELD:OneHanded	COST:20	WT:4	PROFICIENCY:WEAPON|Sample Blade
```

`CRITMULT` takes the `x` prefix. `CRITMULT:-` means no critical.

## Armour and shields

| Tag | Does |
|---|---|
| `ACCHECK` | armour check penalty, written negative |
| `MAXDEX` | maximum dexterity bonus allowed |
| `SPELLFAILURE` | arcane spell failure percentage |
| `PROFICIENCY` | `ARMOR\|<name>` or `SHIELD\|<name>` |

```
Sample Mail	TYPE:Armor.Medium	ACCHECK:-4	MAXDEX:3	SPELLFAILURE:25	COST:150	WT:30	PROFICIENCY:ARMOR|Medium
```

The AC bonus itself comes from a `BONUS`, not a dedicated tag.

## Containers

```
CONTAINS:50|Gear
```

`CONTAINS` sets capacity and what may go inside. `BASEQTY` sets how many come as one
purchase.

## Equipment modifiers

`EQMOD` attaches a modifier defined in an equipment modifier file:

```
EQMOD:MWORKW
```

Modifiers are how one base item becomes many variants without writing each out.
`ALTEQMOD` applies to the second head of a double weapon.

Equipment modifier files are loaded with `EQUIPMOD:` in the PCC and have their own 26
tags, including several `CHOOSE:` variants specific to building items.

## Other tags worth knowing

| Tag | Does |
|---|---|
| `BASEITEM` | marks this as a variant of another item |
| `SLOTS` | how many equipment slots it occupies |
| `QUALITY` | free-form quality descriptors |
| `SPROP` | special property text shown to the reader |
| `MODS` | whether the item accepts modifiers |
| `VISIBLE` | where it appears |
| `ICON` | image for the interface |
| `EDR` | equipment damage reduction |

## A complete example

```
# my_equipment.lst - example items
# Invented content. Nothing from a published book.

Sample Blade	TYPE:Weapon.Melee.Martial	DAMAGE:1d8	CRITMULT:x2	CRITRANGE:2	WIELD:OneHanded	COST:20	WT:4	SPROP:An example weapon.
Sample Bow	TYPE:Weapon.Ranged.Martial	DAMAGE:1d6	CRITMULT:x3	CRITRANGE:1	WIELD:TwoHanded	RANGE:60	COST:75	WT:2
Sample Mail	TYPE:Armor.Medium	ACCHECK:-4	MAXDEX:3	SPELLFAILURE:25	COST:150	WT:30
Sample Pack	TYPE:Gear.Container	CONTAINS:50|Gear	COST:2	WT:2
```

Then in the PCC:

```
EQUIPMENT:my_equipment.lst
```

## Gotchas

**`TYPE` is load-bearing.** Most equipment behaviour keys off it. An item that loads
but behaves wrongly almost always has the wrong type.

**`ACCHECK` is negative.** Writing `4` gives a bonus, not a penalty.

**`CRITMULT` needs the `x`.** `CRITMULT:2` is not the same as `CRITMULT:x2`.

**Proficiency is a separate object.** `PROFICIENCY:WEAPON|Sample Blade` points at a
weapon proficiency that has to exist, defined in its own file and loaded by the PCC.

**`RATEOFFIRE` is deprecated.** See [what changed](../../appendix/whats-changed.md).

## Related

- [PCC](pcc.md) — how this file gets loaded
- [Add equipment](../howto/new-equipment.md) — working order
- [Tag index](../reference/tag-index.md) — every `Equipment` tag
