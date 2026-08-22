---
title: PCGen Handbook
---

# PCGen Handbook

**How PCGen works underneath — data files, code, and how to change them.**

This is for people who want to *modify* PCGen. If you only want to build a character,
use PCGen's own help instead.

PCGen keeps every class, race, feat, spell and item in plain text files. Nothing is
hard-coded. Once you can read those files, you can add anything the rules engine
supports, and you never need to touch Java to do it.

!!! warning "Unofficial"
    Not run by the PCGen project. Written against PCGen `6.09.08.RC1` on the `master`
    branch. The last tagged release is from February 2023, and most people working on
    PCGen now run a nightly build.

## Start here

New to all of this? Read these three in order. About an hour, and you will have made
a working change.

| Page | What you get |
|---|---|
| [Set up](start/setup.md) | PCGen installed, and a folder of your own to work in |
| [Your first change](start/first-change.md) | A feat you wrote, loaded and visible in PCGen |
| [How loading works](start/how-loading-works.md) | Why that worked, so the next change is not guesswork |

## Data files

How the file format actually works.

**Concepts**

| Page | What it covers |
|---|---|
| [Line format](lst/concepts/line-format.md) | One line is one record. Tabs, fields and comments |
| [Keys and names](lst/concepts/keys-and-names.md) | Four names per object, and which one references use |
| [Modifying existing data](lst/concepts/modifying-data.md) | `.MOD`, `.COPY=` and `.FORGET` |
| [Data controls](lst/concepts/data-controls.md) | What must be declared before a file may use it |
| [Prerequisites](lst/concepts/prerequisites.md) | The 129 `PRExxx` conditions and the one shape they share |
| [Bonuses](lst/concepts/bonuses.md) | `BONUS:`, and the stacking rule that catches everyone |
| [Choosers](lst/concepts/choosers.md) | `CHOOSE:`, and why it does nothing on its own |
| [Variables and formulas](lst/concepts/variables-and-formulas.md) | `DEFINE`, `MODIFY` and the newer formula system |

**Reference**

| Page | What it covers |
|---|---|
| [Tag index](lst/reference/tag-index.md) | All 706 tags PCGen implements, read from the source |

## Character sheets

A separate system from the data files, with its own tags.

| Page | What it covers |
|---|---|
| [Output token index](outputsheets/token-index.md) | All 154 output tokens, read from the source |
| [Output and saving](internals/output-and-saving.md) | How a sheet is run, and the `.pcg` save format |

## Internals

For changing PCGen itself, not just its data. New to the code base? Read the first
three in order.

**Getting oriented**

| Page | What it covers |
|---|---|
| [How PCGen fits together](internals/overview.md) | The whole program on one page, with the real dependency directions |
| [Repository layout](internals/architecture.md) | Where everything is, and how it builds |
| [Building from source](internals/building.md) | Compile it, run it, and what each Gradle task does |
| [Startup sequence](internals/startup.md) | Launch to main window, task by task |

**Reading data**

| Page | What it covers |
|---|---|
| [Load pipeline](internals/load-pipeline.md) | From a `.pcc` on disk to a loaded object, class by class |
| [The token system](internals/token-system.md) | How every tag is a class, and why that matters |
| [Plugin loading](internals/plugin-loading.md) | Why adding a tag needs no registration |
| [The formula system](internals/formula-system.md) | The two modules behind `MODIFY` |

**The model**

| Page | What it covers |
|---|---|
| [The object model](internals/cdom-model.md) | What a race is in memory, and why it has no fields |
| [The character model](internals/facets.md) | 248 facets, and why the character object holds nothing |

**Program and output**

| Page | What it covers |
|---|---|
| [The interface layer](internals/ui-layer.md) | Swing, JavaFX, and a boundary that leaks |
| [Output and saving](internals/output-and-saving.md) | Character sheets, output tokens and the `.pcg` format |

**Changing PCGen**

| Page | What it covers |
|---|---|
| [Adding a tag](internals/adding-a-tag.md) | Writing one, with its test |
| [Testing](internals/testing.md) | Token tests, and checking a dataset loads clean |
| [Contributing](internals/contributing.md) | The standards a change meets, and the ones nobody checks |

## Why this exists

PCGen's official documentation is thorough but has drifted from the code. Its tag
pages mostly stopped carrying version markers around 6.03. Since then PCGen added a
new formula system, and removed tags the docs still list.

Checked against the source, four tags the official docs still document —
`ACVALUE`, `BABABBREV`, `DISPLAYVARIABLE` and `ACABBREV` — no longer exist. The
formula system tags `MODIFY` and `MODIFYOTHER` do exist, and are not documented.

So this handbook is built the other way round. The [tag index](lst/reference/tag-index.md)
is generated from PCGen's own Java classes, and a scheduled job re-reads them and
reports when something changes. Explanations are written by hand; facts come from the
code.

See the [glossary](appendix/glossary.md) for how terms are used here, and
[credits](appendix/credits.md) for sources.
