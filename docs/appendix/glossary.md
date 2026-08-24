---
title: Glossary
---

# Glossary

Terms as this handbook uses them. PCGen's own documentation and the videos sometimes
use these words loosely — here they mean one thing each.

## The file format

**tag**
: `NAME:value` as written in a data file, such as `KEYSTAT:INT`. Always uppercase.
  There are 693 current ones. Never called a token, field or attribute here.

**token**
: the Java class implementing a tag. `KeystatToken` implements `KEYSTAT`. See
  [the token system](../internals/token-system.md).

**field**
: one tab-separated part of a line. Field 0 is the object's name; the rest are tags.

**line**
: one record. One line is one object, except in class files and game mode files.

**LST file**
: a `.lst` data file. Holds objects.

**PCC file**
: a `.pcc` campaign file. Holds no game data — it names a data set and lists the files
  to load. See [PCC](../lst/files/pcc.md).

**campaign**
: what a PCC defines. A book, a supplement or your own data set. Not a game session.

**game mode**
: a rules system, such as `35e` or `Pathfinder`. Lives in `system/gameModes/`. See
  [game modes](../lst/concepts/game-modes.md).

## Objects and references

**key**
: the identifier an object is looked up by. Defaults to the name; `KEY:` overrides it.
  Used 74,678 times in shipped data.

**reference**
: one object naming another. Resolved after all files load, which is why a bad name is
  reported late. See [how loading works](../start/how-loading-works.md).

**type**
: dot-separated classification, as in `TYPE:Weapon.Melee.Martial`. Drives filtering,
  prerequisites and, for equipment, which other tags apply.

**category**
: which kind of ability something is. `CATEGORY:FEAT` makes an ability a feat.

## Mechanics

**prerequisite**
: a `PRExxx` condition. 129 of them. Never shortened to "prereq" here. See
  [prerequisites](../lst/concepts/prerequisites.md).

**bonus**
: a `BONUS:` modifier. 55 subtypes.

**chooser**
: a `CHOOSE:` tag and the selection it drives. `%LIST` refers back to what was chosen.

**variable**
: a named value in the formula system, existing inside a scope rather than globally.
  See [variables and formulas](../lst/concepts/variables-and-formulas.md).

**scope**
: where a variable lives. The same name in two scopes is two variables.

## Working with data

**homebrew**
: data you wrote. Not "custom content" or "mods".

**load order**
: the sequence files are read in. Matters less than people expect, because references
  resolve after everything loads.

**deprecated**
: still works, logs a warning, should not be used in new data. 23 tags are deprecated.
  See [what changed](whats-changed.md).

**removed**
: no longer exists. PCGen reports an error. `BONUS:COMBAT|BAB` is the one most likely
  to catch you.

**`.MOD`**
: a suffix on field 0 that changes an object another file defined. See
  [modifying existing data](../lst/concepts/modifying-data.md).

## Verbs

Used consistently, because the difference matters when reading a log:

| Verb | Means |
|---|---|
| load | read a file into PCGen |
| parse | turn a line or tag into data |
| resolve | connect a reference to its target |
| grant | give an ability to a character |
| apply | put a template or modifier into effect |
| override | replace an earlier value |

"Process" is avoided — it hides which of these is happening.

## Spelling

**PCGen**
: one word, capital P and G. Not "PcGen" or "PC Gen".

**LST**, **PCC**
: uppercase in prose, lowercase only as file extensions (`.lst`, `.pcc`).

Tag names are written exactly as they appear in a file: `KEYSTAT`, `PRERACE`,
`BONUS:COMBAT|BASEAB`.

## Related

- [Tag index](../lst/reference/tag-index.md) — every current tag
- [What changed](whats-changed.md) — deprecated and removed terms
- [Line format](../lst/concepts/line-format.md) — where fields and tags come from
