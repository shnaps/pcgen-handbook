---
title: Sources
---

# Sources

A source is one `.pcc` file and the `.lst` files it names. Choosing sources is the first
thing a reader does in PCGen, and the order they load in decides which of two competing
definitions wins.

Shipped data holds **681** `.pcc` files. This page covers how PCGen finds them, how the
list is built, and what order everything ends up being read in.

## Where PCGen looks

Three directories, in this order, each walked to any depth:

| Order | Root | Setting |
|---|---|---|
| 1 | `data/` | `pccFilesPath` |
| 2 | `vendordata/` | `pcgen.files.vendordataPath` |
| 3 | `homebrewdata/` | `pcgen.files.homebrewdataPath` |

*Source: [`CampaignFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/CampaignFileLoader.java)*

Every `*.pcc` under any of them is parsed at startup. Shipped files sit two to six
directories deep, so nesting your own is fine.

The two extra roots exist so bought and homemade data survive a PCGen upgrade that
replaces `data/`. Put your own work in `homebrewdata/`. See
[setup](../../start/setup.md).

## How a data set is laid out

The tree under `data/` is a convention, not a rule the loader enforces. It follows the
same three levels almost everywhere:

```
data/<system>/<publisher>/<product>/
```

Twenty-two directories sit at the top. Most name a system — `35e`, `3e`, `5e`,
`pathfinder`, `modern`, `starfinder`. `35e` alone holds 34 publishers.

Most `.pcc` files land four or five levels deep. A product directory holds its `.pcc` and
the `.lst` files that `.pcc` loads.

### Directories that start with an underscore

Three at the top level are shared rather than owned by a publisher:

| Directory | Holds |
|---|---|
| `_universal` | data any source may load, including the [race every set needs](types.md#group-is-a-second-label-list) |
| `_images` | artwork |
| `publisher_logos` | logos, referenced by `.pcc` files |

The underscore keeps them sorted to the top. Nothing in the loader treats them specially,
so a source reaches them the same way it reaches anything else — by
[path](#depending-on-another-source).

A handful of `.lst` files use the same prefix inside a product directory, `__stats.lst`
and `__align.lst` among them. It means the same thing there: read this first, it is the
foundation the rest builds on. Four files in shipped data do it, so treat it as a hint
and not a system.

### `homebrew` and `customsources`

Both exist at the top level for data that is not a published product. `homebrew` is where
your own work goes if you keep it inside the install.

## Not every PCC is a source

Parsing a `.pcc` makes a campaign object. It does not make an entry in the list.

Of the 681 shipped files, **55 carry no `CAMPAIGN:` tag**. They are fragments — a race,
a chapter, a shared block — pulled in by another file with `PCC:`. They use `KEY:`
instead, so other files can name them without them appearing as something to choose.

That is the pattern to copy for a data set you want to split up.

## How the list is built

Campaigns are bucketed by game mode first. Choose a game mode, and only its sources are
offered.

Inside the advanced panel, the tree is built from **the three levels of `TYPE`**:

```
TYPE:Sample Publisher.Sample Book.Sample Setting
```

Those become producer, format and setting, and they are the folders in the tree.
`BOOKTYPE` and `STATUS` are columns beside it, not grouping. Names sort alphabetically.

*Source: [`AdvancedSourceSelectionPanel.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/gui2/sources/AdvancedSourceSelectionPanel.java)*

### Quick picks

The one-click list above the tree comes from three places:

| Origin | Set by |
|---|---|
| a single source | `SHOWINMENU:YES` plus a `GAMEMODE` in its PCC |
| a game mode's default set | the game mode's own data |
| a saved selection | the reader, stored in their settings |

*Source: [`FacadeFactory.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/system/FacadeFactory.java)*

Twelve shipped files set `SHOWINMENU`, nine `YES` and three `NO`. It marks a source meant to be loaded on its own.

## Load order

Three rules, applied in this order. Everything about `.MOD` depends on them.

### 1. Campaigns, by RANK, highest first

```
RANK:202608
```

Selected campaigns are sorted by `RANK` **descending**, so a higher number loads
earlier. Shipped data writes the publication date as `YYYYMM`, so the newest book loads
first, not the oldest.

### 2. Within a campaign, tag order

Files are read in the order their tags appear in the `.pcc`. Two `SKILL:` lines load in
the order written.

### 3. Across file types, a fixed sequence

The type order is hard-coded and no data can change it:

```
data control → data tables → variables → dynamic → global modifiers →
ability categories → size → stat, save, alignment → proficiencies →
skill → language → feat → ability → race → domain → spell → deity →
class → template → equipment modifier → equipment → companion mod →
kit → bioset
```

*Source: [`SourceFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/SourceFileLoader.java)*

A `.MOD` is applied by the loader that owns the file. A race `.MOD` has to sit in a file
the `.pcc` names with `RACE:`. Putting it in a skill file does nothing. See
[modifying existing data](modifying-data.md).

!!! warning "Order is not enough on its own"
    References are resolved after everything is read, so a reference to a
    not-yet-loaded object is fine. Order matters for `.MOD`, `.COPY=` and `.FORGET`,
    which act on an object that must already exist.

## Depending on another source

Two tags, doing different things.

### PCC: pulls a source in

```
PCC:@/sample_publisher/sample_book/_shared.pcc
```

At startup, every file list from the included campaign is appended to the end of the
including campaign's lists, recursively. Selecting the parent loads both.

The included campaign is still registered in its own right. It can also be selected
alone, unless its own PCC keeps it out of the list.

**A missing include is silent.** The failure is logged and skipped. Nothing tells the
reader that part of the source did not arrive.

*Source: [`CampaignLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/CampaignLoader.java)*

### PRECAMPAIGN requires one

```
PRECAMPAIGN:1,INCLUDES=Testburg
```

An ordinary prerequisite, so the count comes first. It tests what is currently
selected, not what exists on disk. Used 1,516 times across 585 shipped `.pcc` files,
189 of them negated to refuse a combination.

See [publish your own source](../howto/publish-a-source.md) for the four value forms.

## Tags that change how the load behaves

Four PCC tags act on the load itself rather than on presentation.

| Tag | Does |
|---|---|
| `LSTEXCLUDE` | drops named `.lst` files from **the whole load**, not just this campaign |
| `ALLOWDUPES` | permits duplicate keys, and only for `SPELL` or `LANGUAGE` |
| `FORWARDREF` | declares references allowed to stay unresolved |
| `HIDETYPE` | hides objects of a type from selection lists, without unloading them |

`FORWARDREF` is the obscure one and worth understanding. Normally a reference to an
object nobody defined is an error. `FORWARDREF` names types and keys that are allowed to
be missing:

```
FORWARDREF:DOMAIN|Sample Domain,Sample Order Domain
```

That is how a source refers to content in a book the reader may not own, without
producing errors for everyone who does not.

*Source: [`LoadValidator.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/rules/context/LoadValidator.java)*

`ALLOWDUPES` accepts exactly `SPELL` or `LANGUAGE`. Anything else fails to parse.

## When two sources define the same thing

Loading two campaigns that both define `Sample Skill` does not merge them.

Only one survives, and which one is decided by the `SOURCEDATE` your PCC sets. The
reader is not told that it happened. [Keys and names](keys-and-names.md) gives the
rule in full.

*Source: [`LstObjectFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/LstObjectFileLoader.java)*

Setting `SOURCEDATE` in your PCC is therefore not decoration. It decides who wins.

## Campaigns can change settings

```
OPTION:showToolBar=false
```

`OPTION:` writes into the reader's own settings, not into a scratch area for that load.
The change outlives the session.

A reader can refuse it in preferences, and most will never know a source did this. Use it
sparingly.

## What the reader sees when something fails

**A missing `.lst` file does not stop the load.** It is logged and skipped, and the rest
of the source loads. The status bar icon changes to show errors or warnings, and the log
holds the detail.

**A missing `PCC:` include is skipped silently.** Only the log records it.

**An unresolved reference is reported after everything is read.** The message names the
reference, not the file that is missing.

See [when it breaks](../../start/when-it-breaks.md).

## Reloading

**Sources → Reload**, or Shift+R. It empties the loaded data and runs the same load
again in the running program. That is the fastest way to test an edit to a `.lst` file.

## Saved characters and renamed sources

A `.pcg` file records the sources it was built with, by key. If a source was renamed
upstream, a rule in the game mode's `migration.lst` maps the old key to the new one.
Which rules apply depends on the PCGen version that saved the character.

With no matching rule, the source is dropped from the character in silence. The character
opens, missing whatever that source defined. See
[output and saving](../../internals/output-and-saving.md).

## Gotchas

**`RANK` sorts descending.** A higher number loads earlier, which is the opposite of what
most people assume from the word.

**Type order beats everything.** Classes load after races whatever you do, so a `.MOD` on
a class from a race file cannot work.

**A fragment PCC with no `CAMPAIGN:` is invisible, not broken.** That is deliberate. Give
it a `KEY:` and include it.

**`LSTEXCLUDE` is global.** One campaign can exclude a file belonging to another.

**`SOURCEDATE` decides duplicate contests.** Omit it and your definition may lose to one
you meant to replace.

**Data in `data/` is replaced by upgrades.** Your own work belongs in `homebrewdata/`.

## Related

- [PCC](../files/pcc.md) — the file, tag by tag
- [Publish your own source](../howto/publish-a-source.md) — making one others can load
- [Modifying existing data](modifying-data.md) — what load order is for
- [Load pipeline](../../internals/load-pipeline.md) — what happens after the selection
