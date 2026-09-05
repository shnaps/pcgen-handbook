---
title: Modifying existing data
---

# Modifying existing data

You often want to change something another data set defined, without editing that set.
Three suffixes do this, written on the object name in field 0.

`.MOD` is one of the most used mechanisms in the whole format — 56,744 uses in
shipped data.

## The three suffixes

| Suffix | Does | Uses in shipped data |
|---|---|---|
| `.MOD` | change an existing object | 56,744 |
| `.COPY=` | make a new object from an existing one | ~3,900 |
| `.FORGET` | remove an object | 74 |

*Source: [`LstObjectFileLoader.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/persistence/lst/LstObjectFileLoader.java)*

## .MOD

Add tags to something that already exists:

```
Sample Feat.MOD	BONUS:SKILL|Sample Athletics|2
```

Everything after field 0 is applied to the existing object. Tags you do not mention are
left alone.

This is how a supplement adjusts a core book without touching it. It is also how your
own campaign adjusts a third-party set that an update would otherwise overwrite.

The object must exist. A `.MOD` naming something nothing defined is reported after
loading.

### Replacing rather than adding

Some tags accumulate. Writing another `BONUS` adds a second bonus rather than replacing
the first. To clear what is there before setting your own, use `.CLEAR`:

```
Sample Feat.MOD	BONUS:SKILL|Sample Athletics|4
```

Whether a tag accumulates or overwrites depends on the tag. List-valued tags
accumulate; single-valued ones overwrite.

## .COPY=

Make a variant under a new name, leaving the original alone:

```
Sample Feat.COPY=Sample Feat, Greater
```

The new object starts as a duplicate. Follow it with a `.MOD` on the new name to change
what makes it different:

```
Sample Feat.COPY=Sample Feat, Greater
Sample Feat, Greater.MOD	BONUS:SKILL|Sample Athletics|4
```

Note the `=`. `.MOD` and `.FORGET` take no value, `.COPY` requires one.

## .FORGET

Remove an object entirely:

```
Sample Feat.FORGET
```

Rare — 74 uses across all shipped data. Reach for it when a set you are including
defines something you do not want at all.

Prefer excluding at the file level with `LSTEXCLUDE` in the [PCC](../files/pcc.md) when
you want to drop many things at once.

## Order of processing

This is the part that catches people. The three are **not applied in the order they
appear in the file.** They are collected during loading and applied afterwards, in a
fixed order:

```mermaid
flowchart LR
    A["all files load"] --> B[".COPY"] --> C[".MOD"] --> D[".FORGET"]
```

Consequences worth knowing:

- **A `.MOD` can target something a `.COPY` created**, even if the `.MOD` line appears
  first in the file. Copies are all made before any modification runs.
- **A `.FORGET` beats a `.MOD`.** Modifying something and then forgetting it leaves
  nothing, whichever order the lines appear in.
- **File order still matters for definitions**, just not for these three. An object has
  to be defined by some file before another can modify it.

## Where to put them

In your own data set, not in the one you are changing.

```
<homebrew data dir>/testburg/testburg.pcc
<homebrew data dir>/testburg/my_overrides.lst
```

Then load both campaigns together, or pull theirs in with `PCC:` so yours always loads
on top.

Editing the other set directly works until it is updated, and then it does not.

## Gotchas

**The name has to match exactly.** Including any trailing space. A `.MOD` that matches
nothing fails after loading, naming the reference rather than your line.

**Load both sets.** A `.MOD` only works if the thing it modifies was loaded in the same
session.

**`.COPY` needs `=`, the others do not.** `Sample Feat.COPY` with no name is not
meaningful.

**Accumulating tags need `.CLEAR`.** Otherwise you add to what is there instead of
replacing it.

## Related

- [Line format](line-format.md) — field 0 and the tab-separated rest
- [PCC](../files/pcc.md) — `LSTEXCLUDE` and pulling in another campaign
- [Use data someone else wrote](../howto/third-party-data.md) — the usual reason to do this
