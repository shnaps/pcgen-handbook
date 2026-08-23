---
title: Skill files
---

# Skill files

A skill file defines skills a character can put ranks into. Loaded by `SKILL:` in a
[PCC](pcc.md).

Skills are one of the smaller file types — seven tags of their own, plus the global
tags every object gets.

## Minimum working line

```
Sample Skill	KEYSTAT:INT	USEUNTRAINED:YES
```

A name, the stat it keys off, and whether you can try it without training.

## Skill-specific tags

| Tag | Takes | Does |
|---|---|---|
| `KEYSTAT` | a stat abbreviation | which ability score modifier applies |
| `USEUNTRAINED` | `YES` / `NO` | whether a character with no ranks can attempt it |
| `EXCLUSIVE` | `YES` / `NO` | whether only certain classes may take it |
| `ACHECK` | `NONE`, `YES`, `NONPROF` | how armour check penalty applies |
| `CLASSES` | class list | which classes treat it as a class skill |
| `SITUATION` | text | named situational variants of the skill |
| `VISIBLE` | see [below](#visible) | where the skill shows up |

*Source: [`plugin/lsttokens/skill/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/skill)*

### KEYSTAT

Names a stat defined by the game mode, so the valid values depend on the game mode
rather than being fixed. In `35e` they are the usual six abbreviations.

```
Sample Skill	KEYSTAT:DEX
```

The value is resolved as a reference, so a stat that does not exist is reported after
loading rather than at the line itself.

*Source: [`KeystatToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/skill/KeystatToken.java)*

### ACHECK

| Value | Means |
|---|---|
| `NONE` | armour never affects this skill |
| `YES` | the normal armour check penalty applies |
| `NONPROF` | penalty applies only when not proficient with the armour worn |
| `DOUBLE` | double the normal penalty |
| `WEIGHT` | penalty scales with total weight carried, not with armour |

Five values, and `YES` is far and away the common one — it is 242 of the 251 uses in
shipped data.

*Source: [`SkillArmorCheck.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/enumeration/SkillArmorCheck.java)*

### VISIBLE

Controls where the skill appears. Several values are aliases for the same thing:

| Value | Means |
|---|---|
| `YES`, `ALWAYS` | visible everywhere. The normal case. |
| `DISPLAY`, `GUI` | shown in the program, kept off exported sheets |
| `EXPORT`, `CSHEET` | on exported sheets only, hidden in the program |
| `NO` | hidden. For skills that exist only to be referenced. |

A `|READONLY` suffix marks the skill as not directly assignable. It is rejected with
`EXPORT` and `CSHEET`.

*Source: [`skill/VisibleToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/skill/VisibleToken.java)*

### SITUATION

Names situational uses of one skill, so they can be listed separately without being
separate skills.

```
Sample Skill	KEYSTAT:INT	SITUATION:In darkness	SITUATION:While climbing
```

## Global tags worth knowing

These are not skill-specific but come up constantly:

| Tag | Does |
|---|---|
| `TYPE` | classification, dot-separated. Used for grouping and prerequisites. |
| `KEY` | unique identifier if the name is not unique enough |
| `DESC` | description text |
| `BONUS` | grant a bonus while the character has ranks |
| `PRExxx` | conditions on taking it |
| `SOURCEPAGE` | page reference |

## A complete example

```
# my_skills.lst - example skills
# Invented content, nothing from a published book.

Sample Skill	KEYSTAT:INT	USEUNTRAINED:YES	ACHECK:NONE	TYPE:General	DESC:An example skill.
Sample Craft	KEYSTAT:INT	USEUNTRAINED:NO	ACHECK:NONE	EXCLUSIVE:YES	TYPE:General.Craft	DESC:An example exclusive skill.
Sample Athletics	KEYSTAT:STR	USEUNTRAINED:YES	ACHECK:YES	TYPE:General	DESC:An example skill affected by armour.
```

Then in the PCC:

```
SKILL:my_skills.lst
```

## Gotchas

**`USEUNTRAINED:NO` is not the same as `EXCLUSIVE:YES`.** The first stops a character
using the skill with zero ranks. The second restricts which classes can put ranks in
at class-skill cost. They are independent.

**`KEYSTAT` is game mode dependent.** A skill file written for `35e` may reference a
stat a different game mode does not define.

**Class skill lists usually live on the class, not the skill.** `CLASSES` on a skill
works, but most data sets declare class skills from the class side instead. Pick one
approach and stay with it, or the same skill ends up defined in two places.

**Skills are referenced by name from many places.** Renaming one breaks every class,
feat and template that mentions it. Set a `KEY` and reference that instead if you
expect the display name to change.

## Related

- [PCC](pcc.md) — how this file gets loaded
- [Line format](../concepts/line-format.md) — tabs, fields and comments
- [Tag index](../reference/tag-index.md) — every `Skill` tag
