---
title: Data controls
---

# Data controls

Some things have to be declared before any file may use them. A `FACT:` needs a fact
definition. A custom ability category needs a category definition. Skip the declaration
and the tag that uses it fails, in a file that looks correct.

This page covers the declarations, and the separate set of switches that turn engine
features on and off for a whole game mode.

## Declare before use

Two kinds of declaration, both loaded before ordinary data:

| Declares | Written as | Lives in |
|---|---|---|
| a fact field | `FACTDEF:` / `FACTSETDEF:` | a `__datacontrols.lst` file |
| an ability category | `ABILITYCATEGORY:` | an `abilitycategories.lst` file |

Both are pulled in from the [PCC](../files/pcc.md), and both must load before the data
that uses them.

## FACTDEF

A fact is a named field a data author adds without touching Java. Deity titles and
symbols work this way, which is why [deity files](../files/deity.md) have so few tags of
their own.

```
FACTDEF:DEITY|Title	DATAFORMAT:STRING	REQUIRED:NO	VISIBLE:YES	EXPLANATION:The deity's title.
```

| Part | Says |
|---|---|
| `FACTDEF:DEITY|Title` | the object type, then the fact name |
| `DATAFORMAT` | the value type: `STRING`, `NUMBER`, `SIZEADJUSTMENT` and others |
| `REQUIRED` | whether every object of that type must set it |
| `VISIBLE` | `YES`, `DISPLAY`, `EXPORT` or `NO`. **Unset means hidden**, so a fact with no `VISIBLE` reaches no output sheet |
| `EXPLANATION` | text for whoever reads the declaration later |

After that declaration, any deity line may write:

```
Sample Deity	ALIGN:LG	FACT:Title|The Example
```

`FACTSETDEF:` is the same, for a fact that holds several values rather than one. A deity
belongs to one pantheon or to five, so pantheon is a fact set.

*Source: [`plugin/lsttokens/datacontrol/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/datacontrol)*

Shipped data declares facts in 83 files, and fact sets in 13. PCGen ships declarations
for the compatibility facts, which is why the old deity tags still map across.

## ABILITYCATEGORY

Feats are the ability category everyone meets first. A data set can define its own:

```
ABILITYCATEGORY:Sample Talent	VISIBLE:YES	EDITABLE:YES	EDITPOOL:YES	FRACTIONALPOOL:NO	CATEGORY:FEAT	TYPE:SampleTalent	PLURAL:Sample Talents	DISPLAYNAME:Sample Talent
```

| Part | Says |
|---|---|
| `CATEGORY` | which underlying pool it draws from |
| `TYPE` | which abilities belong to it |
| `EDITPOOL` | whether the reader may change the pool total by hand |
| `FRACTIONALPOOL` | whether half points are allowed |
| `DISPLAYLOCATION` | where it appears in the program |

`CATEGORY:` on the declaration names the pool the new category draws from, which is why
the example above says `CATEGORY:FEAT`. An ability joins the new category through `TYPE:`
and keeps `CATEGORY:FEAT`, exactly as the example line shows. Tags such as
`ABILITY:Sample Talent|AUTOMATIC|...` then refer to the category by name.

403 shipped `.lst` files carry category declarations, so custom categories are ordinary
practice rather than an advanced trick.

See [ability files](../files/ability.md).

## Where declarations live

The naming convention is a strong signal, and worth copying:

| Pattern | Holds |
|---|---|
| `_something.pcc` | the campaign file others load |
| `prefix__datacontrols.lst` | fact and fact set declarations |
| `prefix__stats.lst`, `__saves.lst`, `__align.lst`, `__size.lst` | the basics a game mode needs |
| `prefix_feats.lst`, `prefix_classes.lst` | ordinary content |

A double underscore marks a declaration file. A single underscore marks content. The
convention is not enforced, and following it makes a data set legible to anyone who has
read another one.

## DEFAULTVARIABLEVALUE

Declaration files also set what an unset variable of each format means:

```
DEFAULTVARIABLEVALUE:NUMBER|0
DEFAULTVARIABLEVALUE:STRING|
```

Without a default, a formula reading an unset variable has nothing to read. See
[variables and formulas](variables-and-formulas.md).

## Code controls

A different mechanism, and easy to confuse with the above. Code controls switch **engine
features** on and off for a whole game mode. They are not declared by a data set and
cannot be set per campaign.

They live in one file per game mode:

```
system/gameModes/35e/codeControl.lst
```

PCGen defines 54 possible controls. Shipped game modes use five:

| Control | Used by | Does |
|---|---|---|
| `ALIGNMENTFEATURE` | 18 modes | turns the alignment system on or off |
| `DOMAINFEATURE` | 17 modes | turns divine domains on or off |
| `FACE` | 3 modes | routes reach and face through a variable |
| `STATINPUT` | 1 mode | changes how stats are entered |
| `STATMODSAVE` | 1 mode | changes how saves read stat modifiers |

```
ALIGNMENTFEATURE:NO
```

That one line is why alignment does not appear in some game modes.

Code controls also disable tags. `HANDS`, `LEGS` and `REACH` stop parsing when the
matching control is active. That is how a [template](../files/template.md) loading in
one game mode fails in another.

The other 49 controls exist in the code and no shipped data uses them.

## Gotchas

**An undeclared fact fails where it is used, not where it is missing.** The error names
the deity or race line, and the actual fault is a missing declaration file.

**Declaration files must load first.** The PCC decides the order. A data control line
after the content that needs it is too late.

**An ability category is not a type.** `TYPE:` selects which abilities belong to a
category. The category itself is a separate declaration.

**Code controls are per game mode, not per campaign.** A data set cannot switch one on
for itself.

**A code control can make previously valid data fail.** That is a feature, not a bug:
the tag is disabled because the game mode models the thing differently.

## Related

- [Deity files](../files/deity.md) — the file type most dependent on facts
- [Ability files](../files/ability.md) — categories in use
- [Game modes](game-modes.md) — where code controls live
- [PCC](../files/pcc.md) — how declaration files are loaded
