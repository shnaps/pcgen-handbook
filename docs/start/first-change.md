---
title: Your first change
---

# Your first change

Goal: a feat you wrote, loaded into PCGen, selectable on a character. About twenty
minutes.

Everything here is invented. Nothing comes from a published book.

## Before you start

You need a working folder from [Set up](setup.md). This page calls it `testburg/`, and
it sits in your Homebrew Data directory rather than under `data/`.

## 1. Write the feat

Open `my_abilities.lst` in your folder. Ignore the commented notes for now.

!!! note "Not `my_feats.lst`"
    Feats are a *category of ability* in current PCGen, so they go in the abilities
    file. The separate feats file still works but is deprecated. See
    [the note below](#about-the-old-feat-file).

Add one line at the bottom:

```
Sample Feat	CATEGORY:FEAT	TYPE:General	DESC:Grants a small bonus to Sample Athletics.	BONUS:SKILL|Sample Athletics|2
```

!!! danger "Those gaps are tabs"
    Between `Sample Feat` and `TYPE:General` is a **tab**, not spaces. Same between
    every other field. Turn on visible whitespace and check before saving.

    `|` characters inside `BONUS:SKILL|Sample Athletics|2` are typed normally. Only the field
    separators are tabs.

Reading it left to right:

| Part | Meaning |
|---|---|
| `Sample Feat` | the name. First field, no tag. |
| `CATEGORY:FEAT` | this ability is a feat. Required — see below. |
| `TYPE:General` | a general feat, so it appears in the normal feat list |
| `DESC:...` | the description shown in PCGen |
| `BONUS:SKILL\|Sample Athletics\|2` | +2 to that skill while the character has this feat |

`CATEGORY:` is what makes this a feat rather than some other kind of ability. Leave it
out and the line is rejected outright, with `A Category is required for an Ability` in
the log.

Save the file.

## 2. Tell the campaign to load it

Writing the file is not enough. PCGen only reads files a `.pcc` names.

Open `my__campaign.pcc` and find the line naming the abilities file:

```
ABILITY:my_abilities.lst
```

<!-- src: code/src/java/plugin/lsttokens/campaign/AbilityToken.java -->

The shipped template already has this line live, along with the twenty other file tags
around it, so there is nothing to uncomment. Check it is there and matches your file
name. A `#` at the start of a line makes it a comment, and PCGen skips it. That is worth
knowing before you start commenting lines out to narrow a problem down.

While you are in the file, check `CAMPAIGN:` near the top. That name is what you will
look for in PCGen's source list. Change it to something you will recognise:

```
CAMPAIGN:Testburg
```

Save.

## 3. Load it

Start PCGen. If it was already running, restart it — data is read at load time, not
live.

On the source selection screen, find your campaign and load it.

## 4. Check it worked

Make a character. Go to the feat selection tab and look for `Sample Feat`.

Select it, then look at the character's Sample Athletics skill. It should be 2 higher.

If it is there and the bonus applies, you have written data PCGen loaded and used.
Everything else in this handbook is the same two steps: write a line, name the file in
a `.pcc`.

## When it does not work

Almost always one of these:

| Symptom | Cause |
|---|---|
| Campaign not in the source list | PCGen did not find the `.pcc`, or rejected it |
| Campaign loads, feat missing | The `ABILITY:` line does not name your file |
| Campaign loads, feat still missing | `CATEGORY:FEAT` is missing, so the line was rejected |
| Error on load | A tag name is wrong, or fields are separated by spaces |
| Feat appears, no bonus | `BONUS:` typo — check the `\|` characters |

PCGen writes load errors to `pcgen.log`, in the folder it was started from. It names
the file and line number. Read it before guessing.

The quickest check: undo your change, confirm it loads clean, then redo it one field
at a time.

## About the old feat file

Older tutorials put feats in `my_feats.lst` and load them with `FEAT:` in the PCC. That
still works, and PCGen will still load it. The shipped template does not do this — it
names `my_feats.lst` with `ABILITY:`, and no `.pcc` in `data/` uses `FEAT:` at all.

It is deprecated. PCGen's own message when it sees the tag says to use `ABILITY:` and
put `CATEGORY:` entries in the data file instead. Its own test data does exactly that
— even the file named `..._feats.lst` is loaded with `ABILITY:`.

| Old | Current |
|---|---|
| `FEAT:my_feats.lst` in the PCC | `ABILITY:my_abilities.lst` |
| no category tag on the line | `CATEGORY:FEAT` on the line |

Feats became one category of ability. Abilities cover feats, class features, racial
traits and anything else a character can have, and the category says which kind.

Worth knowing because the shipped template dates from 2005 and every video tutorial
predates the change. If you follow one of those and it works, nothing is broken — but
new data should use `ABILITY:`.

*Source: [`CampaignFeatToken.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/deprecated/CampaignFeatToken.java) — in the `deprecated` package*

## Next

[How loading works](how-loading-works.md) — why this worked, so the next change is not
guesswork.
