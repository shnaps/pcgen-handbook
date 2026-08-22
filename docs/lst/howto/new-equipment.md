---
title: Add equipment
---

# Add equipment

Goal: a weapon, a set of armour and a container that all work in the interface.

See [equipment files](../files/equipment.md) for the full tag list. This page is the
working order.

## Before you start

- A working folder and a campaign that loads — see [Set up](../../start/setup.md).
- `EQUIPMENT:my_equipment.lst` uncommented in your `.pcc`.

## 1. Decide the type first

```
TYPE:Weapon.Melee.Martial
TYPE:Armor.Medium
TYPE:Gear.Container
```

Do this before anything else. `TYPE` decides which other tags mean anything, how
proficiency matches, and where the item shows up.

An item that loads but behaves wrongly nearly always has the wrong type.

## 2. Cost and weight

```
Sample Gear	TYPE:Gear	COST:5	WT:1
```

Every item needs both. `WT` accepts decimals for light items.

At this point the item exists and can be bought.

## 3. A weapon

```
Sample Blade	TYPE:Weapon.Melee.Martial	DAMAGE:1d8	CRITMULT:x2	CRITRANGE:2	WIELD:OneHanded	COST:20	WT:4
```

| Tag | Note |
|---|---|
| `DAMAGE:1d8` | dice notation |
| `CRITMULT:x2` | the `x` is required |
| `CRITRANGE:2` | how many numbers threaten, not the threshold |
| `WIELD:OneHanded` | also `Light` and `TwoHanded` |

A ranged weapon adds `RANGE`:

```
Sample Bow	TYPE:Weapon.Ranged.Martial	DAMAGE:1d6	CRITMULT:x3	CRITRANGE:1	WIELD:TwoHanded	RANGE:60	COST:75	WT:2
```

## 4. Proficiency

```
PROFICIENCY:WEAPON|Sample Blade
```

The named proficiency must exist as its own object, in a weapon proficiency file
loaded by the PCC. Without it, nobody is ever proficient with the item.

Point several items at one proficiency to group them.

## 5. Armour

```
Sample Mail	TYPE:Armor.Medium	ACCHECK:-4	MAXDEX:3	SPELLFAILURE:25	COST:150	WT:30	PROFICIENCY:ARMOR|Medium
```

`ACCHECK` is written **negative**. A positive number gives a bonus.

The AC bonus comes from a `BONUS`, not from a dedicated tag.

## 6. A container

```
Sample Pack	TYPE:Gear.Container	CONTAINS:50|Gear	COST:2	WT:2
```

`CONTAINS` sets the capacity and what may go in.

## 7. Variants without repetition

Rather than writing every version of an item, define the base and attach a modifier:

```
EQMOD:MWORKW
```

Modifiers live in their own file, loaded with `EQUIPMOD:` in the PCC. This is how one
base weapon becomes its masterwork and enchanted versions without duplicating lines.

Use `BASEITEM` on an item that is a variant of another.

## The finished file

The weapon this page built, on its own line:

```
# my_equipment.lst - example items
# Invented content. Nothing from a published book.

Sample Blade	TYPE:Weapon.Melee.Martial	DAMAGE:1d8	CRITMULT:x2	CRITRANGE:2	WIELD:OneHanded	PROFICIENCY:WEAPON|Sample Blade	COST:15	WT:4
```

[Equipment files](../files/equipment.md) carries the full example, with the bow, the
armour and the container beside it.

## Check it worked

1. Restart PCGen and load your campaign.
2. Make a character and open the inventory tab.
3. Buy each item and confirm cost and weight.
4. Equip the weapon and confirm damage and critical.
5. Equip the armour and confirm the check penalty and max dexterity apply.
6. Put something in the container.

## When it does not work

| Symptom | Cause |
|---|---|
| Item missing | PCC line commented out |
| Item present, not usable as a weapon | wrong `TYPE` |
| Never proficient with it | `PROFICIENCY` names something that does not exist |
| Armour gives a bonus to checks | `ACCHECK` written positive |
| Critical multiplier ignored | `CRITMULT` missing the `x` |
| Container holds nothing | `CONTAINS` missing or its type filter excludes everything |

## Related

- [Equipment files](../files/equipment.md) — every equipment tag
- [PCC](../files/pcc.md) — loading equipment and modifier files
- Videos: [Equipment Creation](https://www.youtube.com/watch?v=O8KhHtd5ih0),
  [Creating Custom Items](https://www.youtube.com/watch?v=J3omE2FIGs8) — 6.05/6.06
