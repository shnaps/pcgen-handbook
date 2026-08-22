---
title: Ability files
---

# Ability files

An ability file defines things a character *has*: feats, class features, racial traits,
special qualities. Loaded by `ABILITY:` in a [PCC](pcc.md).

Abilities are the single most useful file type to understand, because so much of what
a class or race grants is an ability underneath.

## Feats are abilities

This trips up anyone following an older tutorial. PCGen used to have a separate feat
file loaded with `FEAT:`. Feats are now one **category** of ability.

| Old | Current |
|---|---|
| `FEAT:my_feats.lst` in the PCC | `ABILITY:my_abilities.lst` |
| no category tag | `CATEGORY:FEAT` on each line |

The old form still loads, and PCGen logs a deprecation warning telling you to switch.
Its own test data uses `ABILITY:`.

*Source: [`CampaignFeatToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/deprecated/CampaignFeatToken.java) — in the `deprecated` package*

## Minimum working line

```
Sample Feat	CATEGORY:FEAT	TYPE:General
```

Without `CATEGORY`, PCGen loads the line but the ability will not appear where you
expect it.

## Ability-specific tags

| Tag | Takes | Does |
|---|---|---|
| `CATEGORY` | a category name | which kind of ability this is. Effectively required. |
| `MULT` | `YES` / `NO` | may be taken more than once |
| `STACK` | `YES` / `NO` | repeated takings stack their effects |
| `COST` | a number | how much of the selection budget it uses |
| `VISIBLE` | `YES`, `NO`, `DISPLAY`, `EXPORT` | where it shows up |
| `BENEFIT` | text | short summary of what it grants |
| `ASPECT` | name and value | named display values, useful on sheets |
| `ADDSPELLLEVEL` | a number | raises effective spell level |

*Source: [`plugin/lsttokens/ability/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/ability)*

Two more exist and are deprecated: `APPLIEDNAME` and `MODIFYFEATCHOICE`.

### CATEGORY

`FEAT` is built in. Other categories come from the game mode, or from your own
`ABILITYCATEGORY:` file.

```
Sample Feat	CATEGORY:FEAT	TYPE:General
Sample Class Feature	CATEGORY:Special Ability	TYPE:ClassFeature
```

### MULT and STACK together

These are separate questions and the combination matters:

| `MULT` | `STACK` | Result |
|---|---|---|
| `NO` | — | take it once |
| `YES` | `NO` | take it several times, each for a different choice |
| `YES` | `YES` | take it several times and the effects add up |

`MULT:YES` almost always goes with a `CHOOSE:` tag, because taking it repeatedly only
makes sense if each taking picks something different.

### COST

Defaults to 1. `COST:0` grants an ability without spending the character's budget,
which is how classes and races hand out bonus feats.

## Global tags worth knowing

| Tag | Does |
|---|---|
| `TYPE` | classification. `TYPE:General` puts a feat in the normal list. |
| `DESC` | description shown to the reader |
| `BONUS` | the actual mechanical effect |
| `CHOOSE` | prompt the reader to pick something |
| `PRExxx` | conditions on taking it |
| `KEY` | stable identifier when the display name may change |

## A complete example

```
# my_abilities.lst - example abilities
# Invented content, nothing from a published book.

Sample Feat	CATEGORY:FEAT	TYPE:General	DESC:Grants a small bonus to Climb.	BONUS:SKILL|Climb|2
Sample Focus	CATEGORY:FEAT	TYPE:General	MULT:YES	STACK:NO	CHOOSE:SKILL|ALL	DESC:Grants a bonus to one chosen skill.	BONUS:SKILL|%LIST|2
Sample Toughness	CATEGORY:FEAT	TYPE:General	MULT:YES	STACK:YES	DESC:Grants extra hit points.	BONUS:HP|CURRENTMAX|3
```

Then in the PCC:

```
ABILITY:my_abilities.lst
```

The second line is the common pattern worth studying. `CHOOSE:SKILL|ALL` asks which
skill, and `%LIST` in the bonus means "whatever was chosen".

## Gotchas

**Missing `CATEGORY` fails quietly.** The line loads. The ability just never turns up
in the feat list. This is the most common first mistake.

**`TYPE:General` is what puts a feat in the normal selection list.** A feat with no
type still loads but may not be selectable in the usual place.

**`MULT:YES` without `CHOOSE` is usually a mistake.** Taking the same ability twice
with nothing to differentiate the takings rarely does what you meant.

**`%LIST` only works with a `CHOOSE`.** It refers to what the chooser picked. In a
line with no chooser it resolves to nothing.

**Granting is separate from defining.** This file defines what the ability *is*.
Something else — a class, race or template — has to grant it before a character has
it.

## Related

- [PCC](pcc.md) — how this file gets loaded
- [Your first change](../../start/first-change.md) — writing one end to end
- [Tag index](../reference/tag-index.md) — every `Ability` tag
