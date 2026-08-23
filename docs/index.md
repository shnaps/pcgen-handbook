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

New to all of this? Read these in order. About an hour, and you will have made a
working change.

| Page | What you get |
|---|---|
| [Set up](start/setup.md) | PCGen installed, and a folder of your own to work in |
| [Your first change](start/first-change.md) | A feat you wrote, loaded and visible in PCGen |
| [How loading works](start/how-loading-works.md) | Why that worked, so the next change is not guesswork |
| [When it breaks](start/when-it-breaks.md) | Reading `pcgen.log`, and the failures you meet first |

## Data files

How the file format actually works.

**Concepts**

| Page | What it covers |
|---|---|
| [Line format](lst/concepts/line-format.md) | One line is one record. Tabs, fields and comments |
| [Keys and names](lst/concepts/keys-and-names.md) | Four names per object, and which one references use |
| [Types](lst/concepts/types.md) | The label almost every other tag matches on |
| [Modifying existing data](lst/concepts/modifying-data.md) | `.MOD`, `.COPY=` and `.FORGET` |
| [Sources](lst/concepts/sources.md) | How PCGen finds, lists and orders what it loads |
| [Game modes](lst/concepts/game-modes.md) | What a rules system is made of, in `system/gameModes/` |
| [Data controls](lst/concepts/data-controls.md) | What must be declared before a file may use it |
| [Prerequisites](lst/concepts/prerequisites.md) | The 129 `PRExxx` conditions and the one shape they share |
| [Rule toggles](lst/concepts/rule-toggles.md) | Optional rules the reader switches on, and `PRERULE` |
| [Bonuses](lst/concepts/bonuses.md) | `BONUS:`, and the stacking rule that catches everyone |
| [Granting things](lst/concepts/granting.md) | `AUTO` gives it, `ADD` asks the player to pick |
| [Text the player reads](lst/concepts/display-text.md) | `DESC`, `ASPECT`, `BENEFIT`, `SAB` and one shared grammar |
| [Choosers](lst/concepts/choosers.md) | `CHOOSE:`, and why it does nothing on its own |
| [Archetypes](lst/concepts/archetypes.md) | Swapping out part of a class, the way real data does it |
| [Declaring a variable](lst/concepts/declaring-variables.md) | `DEFINE`, and the bonus that does nothing without it |
| [Variables and formulas](lst/concepts/variables-and-formulas.md) | `DEFINE`, `MODIFY` and the newer formula system |

**File types** — one page per kind of `.lst` file

| Page | Defines |
|---|---|
| [PCC](lst/files/pcc.md) | the campaign file that loads everything else |
| [Ability](lst/files/ability.md) | feats and other abilities |
| [Skill](lst/files/skill.md) | skills |
| [Race](lst/files/race.md) | races |
| [Class](lst/files/class.md) | classes, and their per-level lines |
| [Template](lst/files/template.md) | changes applied on top of a character |
| [Equipment](lst/files/equipment.md) | weapons, armour and gear |
| [Deity](lst/files/deity.md) | deities |
| [Domain](lst/files/domain.md) | domains |
| [Spell](lst/files/spell.md) | spells |

**How to** — one page per task

| Page | Task |
|---|---|
| [Add a feat](lst/howto/new-feat.md) | the usual first change |
| [Add a skill](lst/howto/new-skill.md) | a skill, with the two decisions it needs |
| [Add a race](lst/howto/new-race.md) | a race |
| [Add a class](lst/howto/new-class.md) | a class, including spellcasting |
| [Add equipment](lst/howto/new-equipment.md) | a weapon, armour, a container |
| [Use data someone else wrote](lst/howto/third-party-data.md) | installing and extending a source |
| [Publish your own source](lst/howto/publish-a-source.md) | packaging yours for other people |
| [Report a bug](lst/howto/report-a-bug.md) | where to file, and in which project |

**Reference**

| Page | What it covers |
|---|---|
| [Tag index](lst/reference/tag-index.md) | All 706 tags PCGen implements — 693 current, 23 deprecated |

## Character sheets

A separate system from the data files, with its own tags.

| Page | What it covers |
|---|---|
| [Writing a character sheet](outputsheets/writing-a-sheet.md) | FreeMarker, and the four things a real sheet uses |
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
| [Source selection](internals/source-selection.md) | From the dialog to the loader, and what sets load order |
| [Load pipeline](internals/load-pipeline.md) | From a `.pcc` on disk to a loaded object, class by class |
| [The token system](internals/token-system.md) | How every tag is a class, and why that matters |
| [Plugin loading](internals/plugin-loading.md) | Why adding a tag needs no registration |
| [The formula system](internals/formula-system.md) | The two modules behind `MODIFY` |

**The model**

| Page | What it covers |
|---|---|
| [The object model](internals/cdom-model.md) | What a race is in memory, and why it has no fields |
| [The character model](internals/facets.md) | 234 facet classes, and why the character object holds nothing |
| [The rules engine](internals/rules-engine.md) | How a number is computed, and the loop that repeats until it settles |

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
