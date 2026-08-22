---
title: Add a feat
---

# Add a feat

Goal: a working feat, including the version that asks the reader to choose something.

Feats are [abilities](../files/ability.md) with `CATEGORY:FEAT`. If you have done
[your first change](../../start/first-change.md), you have already written the simple
kind. This page covers the patterns you hit after that.

## Before you start

- A working folder and a campaign that loads — see [Set up](../../start/setup.md).
- `ABILITY:my_abilities.lst` uncommented in your `.pcc`.

## A plain feat

```
Sample Feat	CATEGORY:FEAT	TYPE:General	DESC:Grants a small bonus to Climb.	BONUS:SKILL|Climb|2
```

Field order does not matter to PCGen. It matters to you — keep the same order in every
line and the file stays readable, and find-and-replace across it stays safe.

!!! danger "No trailing space after the name"
    Fields are separated by tabs. A space before that tab becomes part of the feat's
    name. `Sample Feat ` and `Sample Feat` are two different feats, and the one with
    the trailing space will not match anything that references it.

    This is hard to see and easy to do. Turn on visible whitespace.

## A feat the reader chooses for

Most interesting feats ask a question: which skill, which weapon, which school. That
needs three tags working together.

```
Sample Focus	CATEGORY:FEAT	TYPE:General	MULT:YES	STACK:NO	CHOOSE:SKILL|ALL	DESC:Grants a bonus to one chosen skill.	BONUS:SKILL|%LIST|2
```

| Tag | Job |
|---|---|
| `CHOOSE:SKILL\|ALL` | ask which skill |
| `MULT:YES` | allow taking it again for a different skill |
| `STACK:NO` | but not twice for the *same* skill |
| `%LIST` | in the bonus, means "what was chosen" |

`%LIST` only means something when there is a `CHOOSE` on the same line. Without one it
resolves to nothing and the bonus quietly does nothing.

### MULT and STACK

| `MULT` | `STACK` | Behaviour |
|---|---|---|
| `NO` | — | once only |
| `YES` | `NO` | repeatable, each taking must pick something different |
| `YES` | `YES` | repeatable, and the effects add up |

`MULT:YES` with no `CHOOSE` is usually a mistake — repeated takings would be identical.

*Source: [`MultToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/ability/MultToken.java), [`StackToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/ability/StackToken.java)*

## Narrowing the choice

`CHOOSE:SKILL|ALL` offers every skill. Usually you want fewer.

```
CHOOSE:SKILL|TYPE=Craft
```

Choices can be built from types, explicit lists, or a mix. See the
[tag index](../reference/tag-index.md) for the primitives each chooser accepts.

## Referring to a feat from somewhere else

With no `KEY`, an object is looked up by its name, so a prerequisite names the feat:

```
Sample Focus, Greater	CATEGORY:FEAT	TYPE:General	PREABILITY:1,CATEGORY=FEAT,Sample Focus	DESC:Requires the basic version.
```

Setting `KEY:` changes what the object is looked up *by*. The tag calls
`reassociateKey`, so the key replaces the display name as the identifier:

```
Sample Focus	CATEGORY:FEAT	KEY:SampleFocus_Basic	TYPE:General
Sample Focus, Greater	CATEGORY:FEAT	TYPE:General	PREABILITY:1,CATEGORY=FEAT,SampleFocus_Basic
```

The key is written bare in the reference. There is no prefix.

*Source: [`KeyLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/KeyLst.java)*

!!! tip "Setting a key is normal practice, not an edge case"
    `KEY` appears about **71,500 times across 1,296 files** in PCGen's shipped data.
    Real data sets set keys routinely rather than relying on display names.

    A common convention is to encode the distinguishing part into the key, so related
    entries stay unambiguous. Names carrying a qualifier are usually written with a
    separator, and the key spells out what makes each one different.

Set a key whenever the display name might change, contains punctuation, or is close
enough to another name to be confused.

`OUTPUTNAME` separately controls the name *shown* to the reader. Older tutorials call
it the old way of doing things. It is not — shipped data uses it about 14,000 times.

## Prerequisites

There are 129 `PRExxx` tags, and they behave the same way wherever they appear. See
[the tag index](../reference/tag-index.md).

## The finished file

```
# my_abilities.lst - example feats
# Invented content. Nothing from a published book.

Sample Feat	CATEGORY:FEAT	TYPE:General	DESC:Grants a small bonus to Climb.	BONUS:SKILL|Climb|2
Sample Focus	CATEGORY:FEAT	KEY:SampleFocus_Basic	TYPE:General	MULT:YES	STACK:NO	CHOOSE:SKILL|ALL	DESC:Grants a bonus to one chosen skill.	BONUS:SKILL|%LIST|2
Sample Toughness	CATEGORY:FEAT	TYPE:General	MULT:YES	STACK:YES	DESC:Grants extra hit points.	BONUS:HP|CURRENTMAX|3
```

## Check it worked

1. Restart PCGen. Data is read at load time, not live.
2. Load your campaign.
3. Make a character and open the feat tab.
4. For `Sample Focus`, confirm it prompts for a skill, and that taking it twice offers
   only skills you have not already picked.

## When it does not work

| Symptom | Cause |
|---|---|
| Feat missing entirely | `CATEGORY:FEAT` missing, or the PCC line still commented out |
| Feat exists but not in the normal list | `TYPE:General` missing |
| No prompt to choose | `CHOOSE:` missing or malformed |
| Chooses, but the bonus does nothing | `%LIST` used with no `CHOOSE` on the same line |
| Cannot take it a second time | `MULT:YES` missing |
| Second taking does nothing | `STACK:NO` — that is what it means |
| Nothing matches a reference to it | trailing space in the name |

PCGen writes load errors to `logs/` in the install folder, with the file and line.
Read that before guessing.

## Related

- [Ability files](../files/ability.md) — every ability tag
- [Your first change](../../start/first-change.md) — the simplest version
- Video: [Homebrew Basics 2 — Simple Feats & Skills](https://www.youtube.com/watch?v=9tha4tQ1zNk)
  shows this being done, though against PCGen 6.05
