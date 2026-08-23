---
title: Add a class
---

# Add a class

Goal: a working class with skills, attack progression and features gained by level.

See [class files](../files/class.md) for the structure and full tag list. This page is
the working order.

## Before you start

- A working folder and a campaign that loads — see [Set up](../../start/setup.md).
- `CLASS:my_classes.lst` uncommented in your `.pcc`.
- The skills and feats the class uses must exist, or their names will not resolve.

## 1. The class line

```
CLASS:Sample Class	HD:8	TYPE:Base	STARTSKILLPTS:4	MODTOSKILLS:YES	MAXLEVEL:20
```

Hit die, type, skill points, and whether intelligence adds to them.

`MODTOSKILLS:YES` is the usual case. `NO` makes skill points a flat number.

## 2. Split it across lines

A class may have as many `CLASS:` lines as you want. Each adds tags to the same class:

```
CLASS:Sample Class	HD:8	TYPE:Base	STARTSKILLPTS:4	MODTOSKILLS:YES	MAXLEVEL:20
CLASS:Sample Class	CSKILL:Sample Skill|Sample Athletics
CLASS:Sample Class	DESC:An example class.
```

Do this. One line carrying everything runs to hundreds of fields and is unreadable.

## 3. Class skills

```
CSKILL:Sample Skill|Sample Athletics
```

Pipe-separated. `CCSKILL` does the same for cross-class skills.

On a class line these apply from level one. On a level line they apply from that level
onward.

## 4. Level lines

Field 0 is the level number:

```
1	BONUS:COMBAT|BASEAB|1
2	BONUS:COMBAT|BASEAB|2
3	BONUS:COMBAT|BASEAB|3
```

Progression is written out level by level. There is no formula that fills it in.

Skip levels where nothing happens — they need not be consecutive.

!!! danger "Attack bonus is `BASEAB`, not `BAB`"
    `BONUS:COMBAT|BAB` was removed. Older tutorials still teach it and PCGen now
    reports an error. Use `BONUS:COMBAT|BASEAB`.

## 5. Features by level

```
1	BONUS:COMBAT|BASEAB|1	ABILITY:FEAT|AUTOMATIC|Sample Feat
4	BONUS:COMBAT|BASEAB|4	ABILITY:FEAT|AUTOMATIC|Sample Focus
```

Same grant syntax as a race. `AUTOMATIC` costs the character nothing.

To let the reader choose at that level:

```
4	ADD:ABILITY|FEAT|NORMAL|TYPE=General
```

## 6. Saves

```
CLASS:Sample Class	BONUS:SAVE|Fortitude|2
```

Put a flat bonus on the class line, or step it up across level lines if it improves
with level.

## Spellcasting

A caster needs the stat, a spell type, and per-level counts:

```
CLASS:Sample Caster	HD:6	TYPE:Base	SPELLSTAT:INT	MEMORIZE:YES	FACT:SpellType|Arcane
1	CAST:1,0
2	CAST:2,1
```

`CAST` is comma-separated, one number per spell level, starting at level 0. `KNOWN`
takes the same shape for spells known.

`MEMORIZE:YES` for prepared casters, `NO` for spontaneous.

Do not reach for `SPELLLIST` here. It does not declare a class's own list — it picks
from another class's, and its argument must name a class that already exists. A class
casts from its own list without it.

## The finished file

```
# my_classes.lst - example class
# Invented content. Nothing from a published book.

CLASS:Sample Class	HD:8	TYPE:Base	STARTSKILLPTS:4	MODTOSKILLS:YES	MAXLEVEL:20	DESC:An example class.
CLASS:Sample Class	CSKILL:Sample Skill|Sample Athletics
CLASS:Sample Class	BONUS:SAVE|Fortitude|2

1	BONUS:COMBAT|BASEAB|1	ABILITY:FEAT|AUTOMATIC|Sample Feat
2	BONUS:COMBAT|BASEAB|2
3	BONUS:COMBAT|BASEAB|3
4	BONUS:COMBAT|BASEAB|4	ADD:ABILITY|FEAT|NORMAL|TYPE=General
5	BONUS:COMBAT|BASEAB|5
```

## Classes that can be lost

If a class has prerequisites a character can stop meeting, say what it becomes:

```
CLASS:Sample Class	EXCLASS:Sample Ex-Class
```

Without it the character is left in an invalid state. It is rare in shipped data — 30
uses — but the classes that need it need it badly.

## Check it worked

1. Restart PCGen and load your campaign.
2. Make a character and take a level in the class.
3. Confirm skill points, class skills and attack bonus.
4. Take a second level and confirm the progression advances.
5. Confirm the granted feat appeared at the right level.

## When it does not work

| Symptom | Cause |
|---|---|
| Class missing | PCC line commented out |
| Levels attached to the wrong class | a level line above its `CLASS:` line |
| Error on attack bonus | used `BAB` instead of `BASEAB` |
| No skill points | `STARTSKILLPTS` missing |
| Skills not class skills | `CSKILL` missing, or names do not resolve |
| Feature never appears | granted on a level the character has not reached |
| Spells not castable | `SPELLSTAT` or `FACT:SpellType` missing |

## Related

- [Class files](../files/class.md) — every class tag and the line structure
- [Add a skill](new-skill.md) — what `CSKILL` points at
- [Add a feat](new-feat.md) — what the class grants
- Videos: [Homebrew Class making](https://www.youtube.com/watch?v=qKY7GtBx4rI),
  [Making a Class from Scratch](https://www.youtube.com/watch?v=4qxvG07zC9o) — 6.05/6.06
