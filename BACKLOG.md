# Backlog

What the handbook could cover next, and what it will not. Decisions here are binding
until new evidence overturns them — the point of writing a rejection down is that it does
not get proposed again.

The narrative of how each item was decided is in `log.md`. This file holds the state.

## Where the handbook stands

**70 pages.** The generated [tag index](docs/lst/reference/tag-index.md) covers all 706
tags. `docs/internals/` is 22 pages, larger than every other section combined. Every
subsystem page ends with a "what bites" section, indexed from
`internals/design.md`.

A structural review on 2026-09-01 split `output-and-saving.md` and left the rest of the
shape intact.

**Every page has been through an accuracy audit** except `appendix/credits.md`, which is
licences and attribution. The 2026-09-01 material — four pages and eleven sections — was
audited the same day by four reviewers and a task lens, which found about thirty-five
errors, all fixed.

**Every Java package is cited.** All 26 second-level packages under `code/src/java` are
named by at least one page. `plugin/grouping` was the last that was not, closed on
2026-09-01.

**Nothing else is open.** The two items the developer audit left were closed on
2026-09-01: `PropertyContext` namespacing is in `internals/startup.md`, and
`internals/facets.md` now says when a facet is the wrong mechanism. The three the day-one
audit left were closed on 2026-08-23 — the upgrade-safety advice in `setup.md`, the SRD
content in examples, and the precision list. The second of those produced
`tools/check_srd.py`, so that rule has enforcement behind it rather than good intentions.

**The build runs on this machine as of 2026-09-01**, so a claim about a Gradle task can be
checked by running it rather than read off the build files. The first thing that proved
was that a correction made from `build.gradle` alone was wrong, because `run` is
configured in `code/gradle/distribution.gradle`.

## Decided against, with the evidence

These were proposed and refused. Each entry says why, so the argument does not have to be
had twice.

**~150 hand-written tag pages.** The generated index already gives name, accepting class
and implementing class. A hand-written page adds only what the token test states, and 150
of them nearly triple the maintenance surface for the smallest marginal gain available.
Two reviewers rejected it independently.

**Merging `plugin-loading.md` into `token-system.md`.** Proposed by the code expert on
2026-09-01, on the correct observation that `TokenLibrary` registration and `TokenSupport`
dispatch are one package and one mechanism. Rejected: the page has **15 inbound links
across 11 pages**, and the actual defect was the duplicate copy in `load-pipeline.md` §5,
which restated five facts `token-system.md` owns. The copy was cut. Merging the owner buys
nothing further and retires a published URL.

**A companion-mod page.** `plugin/lsttokens/companionmod/` has 9 classes and **zero
tests**, so syntax would have to be inferred from token classes alone. `DECISIONS.md`
records that exact situation producing the `FEAT:`/`ABILITY:` error. Not worth the risk
for a narrow feature.

**A full game-mode file reference.** `game-modes.md` plus the generated index cover the
ground. Reproducing a 120 KB `miscinfo.lst` page is transcription, not documentation.

**Prerequisites as code.** Ranked first among internals gaps in the first pass, on two
errors. Its 138 "commits" were file-touches; the real figure is **4 commits since 2023**,
and **130 of the 138 touches are one PMD sweep**, `7f818006e3`, dropping a redundant
`implements`. The claim that no internals page cites `plugin/pretokens` was also false —
`adding-a-tag.md:25`, `load-pipeline.md:147` and `plugin-loading.md:20` all do, and
`prerequisites.md:144-151` already carries the table said to be missing.

**Bonus resolution.** `rules-engine.md:71-107` already owns it: the two-stage
`buildActiveBonusMap`, static-then-recursive order, the bonus-type key format,
`getTotalBonusTo`, and per-pass prerequisite re-testing. A second page is the exact
duplication `WIKI-SCHEMA.md` forbids.

**Deleting `architecture.md`.** Proposed on the claim that four of its five tables were
re-owned elsewhere. Verified table by table, only one was: `:16-25` lists repository
directories against `overview.md`'s Java package trees, and `building.md` has no
Gradle-file table at all. The duplicated Tests table was removed and the page kept. A cut
would also have broken eight inbound references and retired a published URL.

**`pcgen/gui2/util` as a topic.** 51 classes, 6,292 lines, and `JTreeTable.java` is the
fifth most-touched Java file since 2025 — the strongest churn signal measured anywhere.
Rejected anyway by both reviewers: nobody adding a tag, writing a sheet or authoring LST
opens it, so that churn measures the people maintaining a widget. One line went into
`ui-layer.md` so readers stop hunting for a framework.

| Package | Size | Why not |
|---|---|---|
| `pcgen/cdom/content` | 43 classes, 5,522 lines | 9 commits since 2023, **all nine mechanical**. Reader-facing half is `cdom-model.md:47-48,92` |
| `pcgen/cdom/helper` | 34 classes, 4,189 lines | 5 commits, all mechanical |
| `pcgen/output/channel`, `cdom/formula` | 33 classes, 3,257 lines | 6 commits, every one PMD, SpotBugs, a dependency removal or a build change |
| `pcgen/pluginmgr` | 15 classes | **0 commits since 2023.** `overview.md`'s one line is the whole story |
| `pcgen/core/character` | 9 classes, 2,591 lines | 4 commits: Java 17, a subproject split, a fork merge, a test fix |
| `pcgen/core/namegen` | 12 classes | random names, no engine role |
| `ListContext` | — | 21 callers against `getObjectContext`'s 266. A paragraph in `adding-a-tag.md`, never a page |
| `Logging.deprecationPrint` | `Logging.java:60,66` | uncited, but one paragraph in `adding-a-tag.md` |

## Not worth covering

| Upstream material | Why not |
|---|---|
| `docs/menupages/` (142 files), `tabpages/`, `walkthroughpages/` | end-user interface reference, not modification |
| `docs/installationpages/` | installing is one section of `start/setup.md` |
| `docs/sourcehelp/` | per-publisher legal and Open Game Content notes |
| `docs/acknowledgments/` | licences and credits |
| `gmgen` | four dice classes, no callers, documented upstream in 11 pages |
| `docs/sourcehelp/4e_docs/` | a stub heading with no page and no matching data |
| `vendordata/`, `homebrewdata/` | empty placeholders filled at install time, one line elsewhere |

## Sources worth mining, with the constraint that applies

Every one supplies **topics and facts**, never text. The handbook writes original prose,
cites the implementing class, and uses invented example content.

| Source | Supplies |
|---|---|
| `code/src/test/plugin/lsttokens/` — 363 test classes | accepted and rejected syntax, per tag |
| `installers/release-notes/` — 5.10 to 6.09.05 | what changed, and when |
| `plugin/lsttokens/deprecated/` — 32 classes | the deprecation map |
| `data/zen_test/` — 47 files | small complete data sets. The broken subset is five files under `pcgen_test_advanced/pcgen_broken_tests/`, mostly commented out, covering two narrow cases |
| `docs/listfilepages/lstfileclass/` — 25 lessons | task ordering only. `FEAT:` appears in 9 lessons and `VFEAT` in 6, against `ABILITY:` in 6. Never take syntax from it |
| `docs/listfilepages/rulesguide/` — 3 worked examples | how rules are modelled in data |
| `system/gameModes/` — 20 modes | what a game mode is made of |

## A standing limit: output tokens index only halfway

`tools/scan_tokens.py` works because every LST token declares `getTokenName()` as a
literal. Output tokens are the same — of 154 classes, 80 return a literal and 74 a
constant declared in the same file, none computed — so name, class, package, origin and
deprecation flag are generated. The 23 FreeMarker model keys came with it.

Two things stay hand-written, and this is why the reference is only half solved:

- **Argument grammar.** There is no sub-token registry. Each class parses its own
  remainder with a tokenizer and an if/else chain. `STAT.0.MOD` is one name and two
  arguments that exist only as literals inside that chain.
- **Deprecation replacements.** The only signal is the package name. No annotation, no
  javadoc tag, no logged message, nothing naming a successor. Where the LST side gets a
  migration message from the token itself, this side gets a directory.

## Written

Reasoning for each is in `log.md` under its date.

| Item | Landed in | Date |
|---|---|---|
| `TYPE`, the most-used construct in the data | `lst/concepts/types.md` | 08-22 |
| Declaring a variable, and `BONUS:VAR` with it | `lst/concepts/declaring-variables.md` | 08-22 |
| Granting: `ADD:`, `AUTO:`, `REMOVE:` | `lst/concepts/granting.md` | 08-22 |
| Ability display tags | `lst/concepts/display-text.md` | 08-22 |
| Verifying your data loads | folded into `start/when-it-breaks.md` | 08-22 |
| Facets, past the concept | `internals/facets.md` | 08-22 |
| The output side, both halves | `outputsheets/writing-a-sheet.md` | 08-22 |
| Equipment modifiers | `lst/files/equipment-modifier.md` | 08-22 |
| Choosers and qualifiers | `internals/choosers.md` | 08-22 |
| Spell delivery outside a class list | `lst/concepts/granting-spells.md` | 08-22 |
| Tab binding | section in `internals/ui-layer.md` | 08-22 |
| Kit files | `lst/files/kit.md` | 08-22 |
| How a data set is laid out | merged into `lst/concepts/sources.md` | 08-22 |
| JEP, the engine the data runs on | `internals/formula-system.md` | 08-23 |
| Where facades are implemented | `internals/ui-layer.md` | 08-23 |
| The LST converter | `internals/adding-a-tag.md` | 08-23 |
| Two dispatchers, split apart | `internals/load-pipeline.md` | 08-23 |
| The FreeMarker property vocabulary | `internals/output-and-saving.md` | 08-23 |
| Solver View, the variable debugger | `lst/concepts/variables-and-formulas.md` | 08-23 |
| The `MODIFYOTHER` grouping forms | `lst/concepts/variables-and-formulas.md` | 09-01 |
| The `GROUP:` tag, and the race every set needs | `lst/concepts/types.md` | 09-01 |
| Attaching a debugger, and running a test from an IDE | `internals/running-and-debugging.md` | 09-01 |
| The four engine mechanisms that fail quietly | `internals/changing-behaviour.md` | 09-01 |
| The design logic, and where a new class goes | `internals/design.md` | 09-01 |
| What bites, per subsystem, from eight experts | seven existing pages | 09-01 |
