---
title: The save format
---

# The save format

What a `.pcg` file holds, what it points at, and where it lives. This is the counterpart
of [the load pipeline](load-pipeline.md): a separate parser, a separate tag set, and no
LST token classes at all.

## The file

A saved character is a `.pcg` file: plain text, one `TAG:value` per line, `|` inside a
line for sub-fields, `#` comments marking sections.

```text
PCGVERSION:2.0
VERSION:6.09.08
CHARACTERNAME:Test Hero
STAT:STR=18
CLASS:Test Warrior|LEVEL=3
```

*Source: [`PCGVer2Creator.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/PCGVer2Creator.java)*

Two versions appear and they are not the same thing. `PCGVERSION` is the format
version, fixed at `2.0`. `VERSION` is the PCGen build that wrote the file, and the
parser splits it to decide how to read what follows.

Reading is the mirror class:

*Source: [`PCGVer2Parser.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/PCGVer2Parser.java)*

It resembles the LST format on the surface. It is a separate parser with its own tag
set, and none of the LST token classes are involved.

## What a save file refers to

Sources are stored by campaign key, not by path. On load, each key is looked up in the
loaded campaigns, after passing through `SourceMigration`, which remaps keys that were
renamed upstream.

A key that resolves to nothing is skipped in silence. If nothing resolves at all, the
log gets one line:

```text
Character's campaign entry was empty.
```

The character still loads. It loads without the data that defined half of it, which is
the usual cause of a character opening with items and abilities missing.

## Where characters are saved

The default is the platform documents folder, under a PCGen directory, in
`characters/`. On Windows that is `%USERPROFILE%\Documents`. The path is a setting, so
the preferences dialog can move it.

*Source: [`PCGenSettings.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/system/PCGenSettings.java)*

The `characters/` directory in the repository is unrelated. It holds sample characters
shipped with the program, and the integration tests use them.
## What bites when you change the save format

### A reference to a missing object is lost on the next save

`PCGVer2Parser` adds a warning and returns from the line, then `PCGIOHandler.read` clears
the dirty flag. The character is now in memory without that data, and saving writes it
back that way.

### Renames are fixed by data, not by Java

`migration.lst` rules are matched against the file's `VERSION` by `MigrationUtils`. Adding
a Java special case for a renamed object is the wrong layer.

### New state needs four edits, not one

A channel, an `IOConstants` tag, a writer and a reader. See
[changing behaviour](changing-behaviour.md#new-character-state-has-to-survive-the-save).

*Source: [`PCGVer2Parser.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/PCGVer2Parser.java), [`MigrationUtils.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/migration/MigrationUtils.java)*

## Related

- [Character sheets and output](output-and-saving.md) — the export half of `pcgen/io`
- [The load pipeline](load-pipeline.md) — the same job for data files
- [Changing behaviour](changing-behaviour.md) — what new character state has to do
- [Sources and load order](../lst/concepts/sources.md) — what a campaign key resolves against
