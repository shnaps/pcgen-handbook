---
title: Keys and names
---

# Keys and names

One object can carry four different names. They do different jobs, and picking the
wrong one is the usual cause of a reference that will not resolve.

| Written | Called | Used for |
|---|---|---|
| field 0 | the display name | what the reader sees |
| `KEY:` | the key | what other data refers to |
| `OUTPUTNAME:` | the output name | what a character sheet prints |
| `SORTKEY:` | the sort key | where it appears in a list |

## The key defaults to the name

An object always has a key. Without a `KEY:` tag, the key **is** the display name.

```
Sample Feat	CATEGORY:FEAT	TYPE:General
Sample Feat	CATEGORY:FEAT	TYPE:General	KEY:SampleFeat
```

The first has the key `Sample Feat`. The second has the key `SampleFeat` and still
displays as `Sample Feat`.

Setting a key is normal practice, not an edge case. Shipped data uses `KEY:` **74,678
times across 1,299 files**.

## Why set one

Because the display name is allowed to change and the key is not.

Everything that points at an object points at its key: prerequisites, `ADD:` tags,
spell lists, deity domains. Rename an object with no `KEY:` and every one of those
references breaks. Rename one that has a key and nothing notices.

Set the key when you create the object. Adding one later moves the target and breaks the
references you already wrote.

## Lookup is case-insensitive

`SampleFeat` and `samplefeat` find the same object. The reference store compares keys
without regard to case.

## Two objects, one key

One of them is discarded. Which one depends on `SOURCEDATE`.

By default PCGen allows the later definition to override the earlier, and settles it by date. The object
whose `SOURCEDATE` is newer survives, and the other is forgotten. A new
object with no date, or with an older one, loses. Nothing is reported either way.

*Source: [`LstObjectFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/LstObjectFileLoader.java)*

Turning that preference off makes the clash an error naming both files instead.

Whatever survives that, a later check reports same-key objects that are not equal:

```text
More than one Skill with key/name Sample Skill was built
```

Identical duplicates are forgiven silently, which is why reloading the same file twice
is harmless.

This matters most when two [sources](sources.md) are loaded together.

Keys are unique per object type, so a skill and a feat may share one. Abilities are
unique per category plus key, so a feat and a class ability may also share one.

## Modifying data matches on the key

`.MOD`, `.COPY=` and `.FORGET` all find their target by **key**, never by display name.

```
SampleFeat.MOD	BONUS:SKILL|Sample Skill|1
```

If the object has a `KEY:`, that is what goes before `.MOD`. Writing the display name
there finds nothing, and a `.MOD` that finds nothing reports an error rather than
applying.

*Source: [`LstObjectFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/LstObjectFileLoader.java)*

Abilities need their category as well:

```
CATEGORY=FEAT|SampleFeat.MOD	BONUS:SKILL|Sample Skill|1
```

Without the `CATEGORY=` part the loader cannot tell which ability you mean, and it says
so in the log.

`.COPY=` sets the copy's display name **and** its key to the new name. The copy does not
inherit the original's key, so nothing pointing at the original follows the copy.

See [modifying existing data](modifying-data.md) for the three suffixes in full.

## OUTPUTNAME

What the character sheet prints, when that differs from the display name. About 14,097
uses.

```
Sample Blade (Silver)	OUTPUTNAME:Silver Sample Blade
```

Two substitutions are understood:

| Written | Produces |
|---|---|
| `OUTPUTNAME:[BASE]` | the display name with any `(...)` part removed |
| `[NAME]` inside a value | the text between the first `(` and the last `)`, split on `/` and rejoined in reverse |

`[BASE]` is the common one. It turns a family of parenthesised variants into a clean
printed name.

*Source: [`OutputNameFormatting.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/analysis/OutputNameFormatting.java)*

Equipment modifiers are the exception. `OUTPUTNAME` on one is accepted with a warning
and rewritten to `NAMEOPT:TEXT=`,
because naming there is handled by `NAMEOPT`.

## SORTKEY

Where an object sits in a list. It changes display order and nothing else — never
identity, never lookup.

```
Sample Blade	SORTKEY:Blade, Sample
```

About 12,268 uses, and 7,716 of those are on abilities. Ability lists are long, so this
is where an author most wants "Weapon Focus (Longsword)" filed under W rather than under
its parenthetical.

Sorting falls back to the display name when there is no sort key.

## NAMEISPI

A yes-or-no flag, 6,434 uses. "PI" is **product identity** — a name the publisher
owns.

```
Sample Deity	NAMEISPI:YES	ALIGN:LG
```

It changes one thing: names marked this way are shown differently in the program. Output sheets ignore it. It is
a legal marker for third-party material, not a display preference.

Since this handbook uses [invented example content](../../appendix/credits.md), the flag
rarely applies here. It appears constantly in shipped data.

## DISPLAYNAME is something else

`DISPLAYNAME:` looks like it belongs on this page and does not. It names ability
categories, fact definitions and size adjustments — declarations, not game objects.

```
ABILITYCATEGORY:Sample Feat	VISIBLE:YES	CATEGORY:FEAT	DISPLAYNAME:Sample Feat
```

4,266 uses, in 132 files. On an ordinary race, skill or feat line, field 0 is the
display name and `DISPLAYNAME:` has no meaning.

## Gotchas

**`KEY:` late on the same line is too late for tags before it.** Fields are read left to
right, so a tag that reads the current key sees the display name if `KEY:` comes after
it. Put `KEY:` early.

**Renaming a key does not rewrite references.** Objects already resolved keep working.
Any text reference to the old key fails afterwards with an unconstructed reference.

**A key containing `.MOD` confuses the loader.** The suffix is found by substring search,
so a key containing a literal `.MOD` is a real hazard. `Sword .MODified` is read as a
modification of `Sword `. The match is case-sensitive and needs the dot, so `Automodule`
is safe. Keep keys plain anyway.

**A key containing `|` breaks ability modification.** The category form splits on the
first pipe.

**Sort keys do not affect lookup.** If a reference is not resolving, the sort key is
never the reason.

## Related

- [Line format](line-format.md) — where field 0 comes from
- [Modifying existing data](modifying-data.md) — `.MOD`, `.COPY=` and `.FORGET`
- [The object model](../../internals/cdom-model.md) — keys and names in Java
- [When it breaks](../../start/when-it-breaks.md) — reading an unconstructed reference
