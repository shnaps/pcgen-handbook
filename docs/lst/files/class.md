---
title: Class files
---

# Class files

A class file defines what a character *does* as it levels. Loaded by `CLASS:` in a
[PCC](pcc.md).

Class files are the one file type with a structure of their own. Everything else is one
line per object. A class is a group of lines.

## Two kinds of line

```
CLASS:Sample Class	HD:8	TYPE:Base	STARTSKILLPTS:4
CLASS:Sample Class	CSKILL:Sample Skill
1	BONUS:COMBAT|BASEAB|1
2	ABILITY:FEAT|AUTOMATIC|Sample Feat
```

| Line starts with | Is |
|---|---|
| `CLASS:<name>` | a **class line** — properties of the class as a whole |
| a bare number | a **level line** — what happens at that level |

Both kinds are still ordinary [LST lines](../concepts/line-format.md): field 0, then
tab-separated tags.

### Class lines repeat

A class can have as many `CLASS:` lines as you want. Each adds more tags to the same
class. Splitting a long class across several lines is normal and keeps the file
readable, since one line would otherwise run to hundreds of fields.

### Level lines

Field 0 is the level number. Everything after applies when the character reaches that
level.

```
1	BONUS:COMBAT|BASEAB|1	CSKILL:Sample Skill
5	ABILITY:FEAT|AUTOMATIC|Sample Feat
```

Levels need not be consecutive. Only write the ones where something happens.

## Class tags

| Tag | Does |
|---|---|
| `HD` | hit die size |
| `STARTSKILLPTS` | skill points per level before intelligence |
| `CSKILL`, `CCSKILL` | class and cross-class skills |
| `SKILLLIST` | a named skill list to draw from |
| `MAXLEVEL` | level cap |
| `LEVELSPERFEAT` | how often the class grants a bonus feat |
| `XTRAFEATS` | extra feats at first level |
| `MODTOSKILLS` | whether the intelligence modifier applies to skill points |
| `EXCLASS` | what this class becomes if its requirements stop being met |
| `EXCHANGELEVEL` | trade levels with another class |
| `ALLOWBASECLASS` | whether it may be taken as a base class |
| `ATTACKCYCLE` | how extra attacks accrue |
| `VISIBLE` | where the class appears |
| `ROLE` | intended role, for display |
| `ISMONSTER` | whether it is a monster class |
| `PRERACETYPE` | restrict by race type |

Spellcasting adds another group: `SPELLSTAT`, `BONUSSPELLSTAT`, `SPELLLIST`,
`SPELLBOOK`, `MEMORIZE`, `KNOWNSPELLS`, `KNOWNSPELLSFROMSPECIALTY`, `PROHIBITED`,
`PROHIBITSPELL`, `ITEMCREATE`, `ADDDOMAINS`.

*Source: [`plugin/lsttokens/pcclass/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/pcclass)*

Four are deprecated: `ABB`, `CLASSTYPE`, `DOMAIN` and `SPELLTYPE`.

## Level line tags

Some tags belong on level lines rather than class lines:

| Tag | Does |
|---|---|
| `CAST` | spells castable per day at this level |
| `KNOWN` | spells known at this level |
| `SPECIALTYKNOWN` | extra specialty spells known |
| `HITDIE` | override the hit die at this level |
| `CSKILL`, `CCSKILL` | add class skills from this level |
| `ADDDOMAINS`, `DOMAIN` | domains granted |
| `DONOTADD` | suppress something otherwise granted |

Global tags such as `BONUS`, `ABILITY` and `ADD` work on level lines too, and that is
where most of a class's progression is written.

## A complete example

```
# my_classes.lst - example class
# Invented content. Nothing from a published book.

CLASS:Sample Class	HD:8	TYPE:Base	STARTSKILLPTS:4	MODTOSKILLS:YES	MAXLEVEL:20	DESC:An example class.
CLASS:Sample Class	CSKILL:Sample Skill|Sample Athletics
CLASS:Sample Class	BONUS:SAVE|Fortitude|2

1	BONUS:COMBAT|BASEAB|1	ABILITY:FEAT|AUTOMATIC|Sample Feat
2	BONUS:COMBAT|BASEAB|2
3	BONUS:COMBAT|BASEAB|3
4	BONUS:COMBAT|BASEAB|4	ABILITY:FEAT|AUTOMATIC|Sample Focus
```

Then in the PCC:

```
CLASS:my_classes.lst
```

## Gotchas

**A level line with no class line above it has no owner.** Level lines attach to the
most recent class. Reordering a file can silently attach levels to the wrong class.

**Blank lines do not end a class.** They are ignored, like anywhere else. The next
`CLASS:` line is what starts a new class.

**`CSKILL` on a class line applies from level one.** On a level line it applies from
that level. The difference matters for classes that gain skills partway through.

**Bonus progression is written out, not calculated.** There is no formula for a
progression across levels — each level line states its own value.

**`EXCLASS` is easy to forget.** A class with prerequisites that a character can stop
meeting needs somewhere to go, or the character is left in an invalid state.

!!! warning "`BONUS:COMBAT|BAB` was removed"
    Older tutorials and older data write base attack bonus as `BONUS:COMBAT|BAB`. That
    was removed because of how it behaved around epic class levels, and PCGen now
    reports an error if it sees it.

    Use **`BONUS:COMBAT|BASEAB`** instead. It appears about 2,100 times in shipped
    data, while `BAB` appears nowhere.

    *Source: [`bonustokens/Combat.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/bonustokens/Combat.java)*

## Related

- [PCC](pcc.md) — how this file gets loaded
- [Skill files](skill.md) — what `CSKILL` refers to
- [Ability files](ability.md) — what classes grant
- [Tag index](../reference/tag-index.md) — every `PCClass` tag
- Videos: [Homebrew Class making](https://www.youtube.com/watch?v=qKY7GtBx4rI) and
  [Making a Class from Scratch](https://www.youtube.com/watch?v=4qxvG07zC9o), recorded
  against PCGen 6.05/6.06
