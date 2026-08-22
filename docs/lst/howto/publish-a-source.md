---
title: Publish your own source
---

# Publish your own source

Turn a folder of `.lst` files into a source that appears in PCGen's source list. It
carries its own credits and licence, and loads cleanly for someone else.

This is the other half of [using data someone else wrote](third-party-data.md).

## Before you start

You need a working `.pcc` and at least one `.lst` file it loads. If you do not have
that yet, start with [your first change](../../start/first-change.md) and the
[PCC page](../files/pcc.md).

## What the loader actually requires

Nothing.

A `.pcc` file with no tags at all parses, registers and loads. There is no required tag,
no validation of the name, and no complaint about a missing game mode.

*Source: [`CampaignLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/CampaignLoader.java)*

That is worth knowing because it means every rule below is about being **usable**, not
about loading. A source with no `CAMPAIGN:` loads fine and is nameless in the list.

## 1. Identity

```
CAMPAIGN:Testburg Expanded
GAMEMODE:35e
TYPE:Sample Publisher.Sample Book
RANK:202608
BOOKTYPE:Supplement
STATUS:RELEASE
```

| Tag | Does |
|---|---|
| `CAMPAIGN` | the name in the source list |
| `GAMEMODE` | which rules system. Without it the source cannot be a quick pick |
| `TYPE` | where it sits in the source tree |
| `RANK` | sort order, highest first |
| `BOOKTYPE` | a grouping label |
| `STATUS` | `RELEASE`, `BETA`, `ALPHA` or `TESTONLY` |

`TYPE` takes at most **three** levels separated by `.`, and a fourth fails to parse. The
levels become producer, format and setting.

*Source: [`campaign/TypeToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/campaign/TypeToken.java)*

Shipped data uses two levels most often, three in 66 cases and one in 17.

!!! tip "RANK is a date in practice"
    The tag takes any number. Shipped data almost always writes the publication date as
    `YYYYMM` — `200301`, `201408`. Copying that convention puts your source in a
    sensible place among others rather than at one extreme.

`STATUS` is honest signalling. 268 shipped sources say `BETA` against 116 saying
`RELEASE`, so marking your own as beta is normal rather than apologetic.

## 2. Credits

```
PUBNAMELONG:Sample Publisher
PUBNAMESHORT:Sample
PUBNAMEWEB:https://example.invalid/
SOURCELONG:Testburg Expanded
SOURCESHORT:TBX
SOURCEWEB:https://example.invalid/testburg
SOURCEDATE:2026-08
DESC:An example supplement.
```

These fill the panel beside the source list. Every shipped source sets all of them.

## 3. Licensing

Four tags, and they do something visible:

| Tag | Effect |
|---|---|
| `ISOGL:YES` | PCGen shows the Open Game Licence, with your `COPYRIGHT` lines appended |
| `COPYRIGHT` | one Section 15 line. Repeat the tag for several |
| `ISLICENSED:YES` | PCGen shows your own licence text |
| `LICENSE` | the text, or `FILE=some_file.txt` to read it from a file |
| `ISMATURE:YES` | PCGen shows a content warning |

The dialogs appear after the selected data finishes loading, before the reader gets
control. A reader may switch them off in preferences.

*Source: [`PCGenFrame.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/gui2/PCGenFrame.java)*

```
ISOGL:YES
COPYRIGHT:Testburg Expanded, Copyright 2026, Sample Publisher.
```

!!! warning "This is a declaration, not advice"
    Setting `ISOGL:YES` tells PCGen to show the Open Game Licence. It does not make your
    material Open Game Content, and getting the Section 15 chain right is your
    responsibility. If your content is entirely your own and uses no licensed material,
    you do not need these tags at all.

## 4. Presentation

```
COVER:cover.png
LOGO:logo.png
URL:WEBSITE|https://example.invalid/testburg|Testburg online
INFOTEXT:Requires the base Testburg set.
```

`URL` takes three parts: a kind, the address, and a description. The kind is `WEBSITE`,
`SURVEY`, or anything else, which is treated as a purchase link.

*Source: [`campaign/UrlToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/campaign/UrlToken.java)*

`HELP:` parses and nothing reads it. Skip it.

## 5. Appearing as a quick pick

```
SHOWINMENU:YES
```

The rule is exact: a source gets its own one-click entry when `SHOWINMENU:YES` **and**
it declares at least one `GAMEMODE`. `TYPE` plays no part.

*Source: [`FacadeFactory.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/system/FacadeFactory.java)*

Only 11 of the 680 shipped `.pcc` files set it. It is for a source meant to be loaded on
its own, not for one supplement among many.

It also matters for testing. `datatest` skips a `.pcc` without it, so a source that never
sets `SHOWINMENU` is never checked by that harness. See [testing](../../internals/testing.md).

## 6. Depending on another source

```
PRECAMPAIGN:1,INCLUDES=Testburg
```

`PRECAMPAIGN` is an ordinary prerequisite, so it takes a count first. Four value forms
are used in shipped data:

| Form | Matches | Uses |
|---|---|---|
| `INCLUDES=Name` | that source, or a source that includes it | 829 |
| `BOOKTYPE=Supplement` | any source of that book type | 262 |
| a plain name | that source | 245 |
| `INCLUDESBOOKTYPE=Core Rules` | book type, following inclusions | 180 |

189 of the 1,516 uses are negated with `!`, which is how a source says "do not load
me alongside that one". 967 of them stand as a line of their own; the rest are
appended inside another tag.

*Source: [`PreCampaignTester.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/pretokens/test/PreCampaignTester.java)*

To pull another source in rather than merely require it, use `PCC:`. See
[sources](../concepts/sources.md).

## The finished file

```
# _testburg_expanded.pcc - example campaign file
# Invented content. Nothing from a published book.

CAMPAIGN:Testburg Expanded
GAMEMODE:35e
TYPE:Sample Publisher.Sample Book
RANK:202608
BOOKTYPE:Supplement
STATUS:RELEASE
SHOWINMENU:YES

PUBNAMELONG:Sample Publisher
PUBNAMESHORT:Sample
PUBNAMEWEB:https://example.invalid/
SOURCELONG:Testburg Expanded
SOURCESHORT:TBX
SOURCEWEB:https://example.invalid/testburg
SOURCEDATE:2026-08
DESC:An example supplement for the Testburg setting.
INFOTEXT:Adds one feat and one skill.

PRECAMPAIGN:1,INCLUDES=Testburg

ABILITY:my_feats.lst
SKILL:my_skills.lst
```

Blank lines and `#` comments are ignored, so group the tags for whoever reads it next.

## Verify it

1. Put the folder under your data directory. See [setup](../../start/setup.md).
2. Start PCGen and open the source list. Your `CAMPAIGN` name should appear under the
   `TYPE` path you gave it.
3. Select it and load. Any licence dialogs you configured appear at the end.
4. Check the log for errors. See [when it breaks](../../start/when-it-breaks.md).

For an automated check, point `datatest` at your folder — described in
[testing](../../internals/testing.md).

## Common failures

**The source does not appear at all.** Check `GAMEMODE` matches an installed game mode
exactly, and that the file has a `.pcc` extension and sits under a data root.

**It appears with no name.** Missing `CAMPAIGN:`.

**It appears but not as a quick pick.** `SHOWINMENU:YES` needs `GAMEMODE` beside it.

**It loads but the reader sees nothing new.** The file-loading tags name paths relative
to the `.pcc`. A typo there is silent, and the file is never read.

**Everything loads, then errors name objects you did not write.** Your data references
something a required source provides. Add the `PRECAMPAIGN` line so PCGen refuses the
combination rather than half-loading it.

## Related

- [PCC](../files/pcc.md) — the file, tag by tag
- [Sources](../concepts/sources.md) — how PCGen finds and orders them
- [Use data someone else wrote](third-party-data.md) — the reading side
- [Report a bug](report-a-bug.md) — when the fault is upstream
