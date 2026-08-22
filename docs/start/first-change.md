---
title: Your first change
---

# Your first change

Goal: a feat you wrote, loaded into PCGen, selectable on a character. About twenty
minutes.

Everything here is invented. Nothing comes from a published book.

## Before you start

You need a working folder from [Set up](setup.md). This page assumes
`data/35e/homebrew/testburg/`.

## 1. Write the feat

Open `my_feats.lst` in your folder. Ignore the commented notes for now.

Add one line at the bottom:

```
Sample Feat	TYPE:General	DESC:Grants a small bonus to Climb.	BONUS:SKILL|Climb|2
```

!!! danger "Those gaps are tabs"
    Between `Sample Feat` and `TYPE:General` is a **tab**, not spaces. Same between
    every other field. Turn on visible whitespace and check before saving.

    `|` characters inside `BONUS:SKILL|Climb|2` are typed normally. Only the field
    separators are tabs.

Reading it left to right:

| Part | Meaning |
|---|---|
| `Sample Feat` | the name. First field, no tag. |
| `TYPE:General` | a general feat, so it appears in the normal feat list |
| `DESC:...` | the description shown in PCGen |
| `BONUS:SKILL\|Climb\|2` | +2 to Climb while the character has this feat |

Save the file.

## 2. Tell the campaign to load it

Writing the file is not enough. PCGen only reads files a `.pcc` names.

Open `my__campaign.pcc`. Find the line naming the feats file. It will be commented
out, like most lines in the template:

```
#FEAT:my_feats.lst
```

Remove the `#`:

```
FEAT:my_feats.lst
```

<!-- src: code/src/java/plugin/lsttokens/campaign/FeatToken.java -->

That single character is the difference between a file PCGen loads and a file PCGen
ignores. Most first attempts fail here.

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

Select it, then look at the character's Climb skill. It should be 2 higher.

If it is there and the bonus applies, you have written data PCGen loaded and used.
Everything else in this handbook is the same two steps: write a line, name the file in
a `.pcc`.

## When it does not work

Almost always one of these:

| Symptom | Cause |
|---|---|
| Campaign not in the source list | PCGen did not find the `.pcc`, or rejected it |
| Campaign loads, feat missing | The `FEAT:` line is still commented out |
| Error on load | A tag name is wrong, or fields are separated by spaces |
| Feat appears, no bonus | `BONUS:` typo — check the `\|` characters |

PCGen writes load errors to a log file in `logs/` inside the install folder. It names
the file and line number. Read it before guessing.

The quickest check: undo your change, confirm it loads clean, then redo it one field
at a time.

## Next

[How loading works](how-loading-works.md) — why this worked, so the next change is not
guesswork.
