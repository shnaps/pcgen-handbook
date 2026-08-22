---
title: Line format
---

# Line format

**One line is one record.** Everything about a feat, a class or a weapon sits on a
single line. There is no nesting, no indentation and no block structure.

Lines get long. That is normal, and it is the first thing that surprises people.

## Fields

A line is split on **tab characters**. The first field is the object's name. Every
field after it is a tag.

```
Sample Feat	TYPE:General	DESC:A feat used in examples.
```

Three fields: the name `Sample Feat`, then `TYPE:General`, then `DESC:...`.

!!! danger "Tabs, not spaces"
    Fields are separated by tabs. Spaces do not separate fields — they are ordinary
    characters inside a name or a value. `Sample Feat` is one name containing a space.

    A file that looks right but loads wrong is usually a file where a tab became
    spaces. Turn on visible whitespace in your editor.

## Tags

A tag is `NAME:value`.

The name is uppercase and comes from a fixed set — PCGen implements 706 of them. See
the [tag index](../reference/tag-index.md). Anything not in that set is an error, not
a custom field.

Values vary by tag. Many use `|` to separate their own arguments:

```
BONUS:SKILL|Climb|2
```

That is one field. The `|` splits the bonus's arguments; it does not split the line.

So there are three levels of separator, and mixing them up is a common mistake:

| Separator | Splits |
|---|---|
| tab | fields on a line |
| `:` | a tag's name from its value |
| `\|` | arguments inside one tag's value |

## Comments

A line starting with `#` is ignored.

```
# Feats for the example campaign.
Sample Feat	TYPE:General
```

The comment character is only recognised at the **start of a line**. A `#` in the
middle of a line is an ordinary character, not the start of a comment.

*Source: [`LstFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/LstFileLoader.java) — `LINE_COMMENT_CHAR`*

Commenting out a line is how you disable data without deleting it. PCC files ship with
most of their file references commented out, and you enable one by removing the `#`.

## Blank lines

Ignored. Use them to group related lines.

## Line endings

Both Windows (`\r\n`) and Unix (`\n`) line endings work. PCGen accepts either.

*Source: [`LstFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/LstFileLoader.java) — `LINE_SEPARATOR_REGEXP`*

## Which tags are legal where

Not every tag works in every file. A tag is implemented by a Java class that declares
the object type it applies to, and PCGen rejects it elsewhere.

`KEYSTAT` applies to `Skill`, so it works in a skill file and nowhere else. `TYPE`
applies to `CDOMObject`, the base type, so it works nearly everywhere.

The **Applies to** column in the [tag index](../reference/tag-index.md) is exactly
this, read from the source.

## A complete small file

```
# my_feats.lst - example feats
# Everything here is invented, not from any published book.

Sample Feat	TYPE:General	DESC:Grants a small climbing bonus.	BONUS:SKILL|Climb|2
Second Sample Feat	TYPE:General	DESC:Does nothing at all.
```

Two feats. Each is one line. Fields separated by tabs.

## Next

- [How loading works](../../start/how-loading-works.md) — what PCGen does with these lines
- [Tag index](../reference/tag-index.md) — every tag, and where each one is legal
