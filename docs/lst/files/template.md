---
title: Template files
---

# Template files

A template is a bundle of changes bolted onto a character that already exists. Loaded by
`TEMPLATE:` in a [PCC](pcc.md).

Use one where a race would be wrong. Something acquired rather than born with,
something several races can gain, or something that stacks with what the character
already is.

Templates have **24** tags of their own, more than any other file type in this handbook.

## Minimum working line

```
Sample Template	VISIBLE:YES
```

The loader requires only the name. Everything else is convention.

## What a template is

`PCTemplate` extends the same base class as `Race` and `Ability`. The difference is how
it is used, not what it is.

| Type | Is |
|---|---|
| race | what the character is |
| ability | something the character took |
| template | something applied on top, possibly more than one |

*Source: [`PCTemplate.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/PCTemplate.java)*

A character may hold several templates. The same template cannot be applied twice.

## Template-specific tags

| Tag | Does |
|---|---|
| `VISIBLE` | where the template is shown |
| `REMOVABLE` | whether the reader may take it off |
| `LEVEL` | effects that switch on at a character level |
| `HD` | effects that switch on within a hit dice range |
| `REPEATLEVEL` | repeat a set of level effects at an interval |
| `ADDLEVEL` | grant levels of a class |
| `LEVELADJUSTMENT` | adjust effective character level |
| `CR` | adjust challenge rating |
| `HITDIE` | set or lock the hit die |
| `SIZE` | set the character's size |
| `RACETYPE` | override the race type |
| `RACESUBTYPE` | add or remove race subtypes |
| `SUBRACE` | set the subrace |
| `REGION`, `SUBREGION` | set region strings |
| `FAVOREDCLASS` | set the favoured class |
| `GENDERLOCK` | force a gender |
| `HANDS`, `LEGS`, `REACH` | set body values |
| `BONUSSKILLPOINTS` | add skill points |
| `LANGBONUS` | grant bonus languages |
| `WEAPONBONUS` | grant weapon proficiencies |
| `NONPP` | set the non-proficiency penalty |

*Source: [`plugin/lsttokens/template/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/template)*

### Tags that look template-specific and are not

Four of the most used tags on template lines are global tags that work anywhere:

| Tag | Uses on templates | Really applies to |
|---|---|---|
| `NATURALATTACKS` | 1,404 | any object |
| `SAB` | 1,219 | any object |
| `TEMPLATE` | 444 | any object, grants another template |
| `ABILITY` | 1,397 | any object |

They cluster on templates because that is where the work is done, not because templates
own them.

## VISIBLE

The most used tag on template lines by a wide margin — 6,397 uses in 8,040 lines. Four
values:

| Value | Means |
|---|---|
| `YES` | shown in the program and on output |
| `DISPLAY` | shown in the program only |
| `EXPORT` | printed on output only |
| `NO` | hidden from both |

Anything else fails to parse.

*Source: [`template/VisibleToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/template/VisibleToken.java)*

`VISIBLE:NO` is normal. Templates are used as invisible carriers for effects at least as
often as they are used as things a reader picks.

## Applying and removing

A template reaches a character three ways:

| Written on another object | Effect |
|---|---|
| `TEMPLATE:Sample Template` | applies it |
| `TEMPLATE:Sample Template.REMOVE` | removes one applied earlier |
| `ADD:TEMPLATE` | grants a choice of templates |

`REMOVABLE:YES` controls something different — whether the *reader* may take the
template off in the program. It only works if the template is visible in the program as
well. A hidden template can never be removed by hand, whatever `REMOVABLE` says.

The `.REMOVE` form is only legal on the plain tag. Combining it with a chooser is
rejected.

## Level-dependent effects

A template can hold effects that appear later:

```
Sample Template	VISIBLE:YES	LEVEL:5:BONUS:STAT|STR|2
```

Three tags do this:

| Tag | Switches on when |
|---|---|
| `LEVEL` | total character level reaches a number |
| `HD` | hit dice fall in a range |
| `REPEATLEVEL` | at every interval of levels |

Each builds a hidden sub-template behind the scenes and applies it when the threshold is
met. That is how one line can carry a progression.

## A complete example

```
# my_templates.lst - example templates
# Invented content. Nothing from a published book.

Sample Blessed	VISIBLE:YES	REMOVABLE:YES	TYPE:Acquired	BONUS:SAVE|ALL|1	SAB:Blessed by the example.	LEVELADJUSTMENT:0
Sample Half-Elemental	VISIBLE:YES	REMOVABLE:NO	TYPE:Inherited	RACETYPE:Outsider	RACESUBTYPE:Sample Elemental	SIZE:M	BONUS:STAT|STR|2	BONUS:STAT|CON|2	LEVELADJUSTMENT:2	CR:1	ABILITY:FEAT|AUTOMATIC|Sample Feat
Sample Veteran	VISIBLE:NO	REMOVABLE:NO	LEVEL:3:BONUS:COMBAT|TOHIT|1	LEVEL:6:BONUS:COMBAT|TOHIT|2
```

Then in the PCC:

```
TEMPLATE:my_templates.lst
```

## Gotchas

**Level and hit dice effects are always hidden.** The sub-template they build is forced
to hidden regardless of the `VISIBLE` on the line. There is no way to show a level tier
in the program as its own entry.

**`HANDS`, `LEGS` and `REACH` can be illegal.** A game mode that turns on the matching
code control makes these tags fail to parse. A template that loads in one game mode can
fail in another.

**`SUBRACE:YES` conflicts with a named subrace.** `YES` means "use this template's own
name". Setting both produces a warning when the data is written back, not a load error.

**`REMOVABLE:YES` on a hidden template does nothing.** Visibility gates removal.

**A template applies once.** Applying the same one twice is refused, so a stacking
effect needs a variable and a bonus rather than two applications.

## Related

- [PCC](pcc.md) — loading template files
- [Race files](race.md) — the alternative when it defines what a character is
- [Bonuses](../concepts/bonuses.md) — what most template lines actually do
- [Tag index](../reference/tag-index.md) — every `PCTemplate` tag
