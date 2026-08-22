# Backlog

What the handbook could cover next, and what it should not. From a survey of the PCGen
repository and PCGen's own documentation on 2026-08-22, at commit `d262f8b4`.

Ranked by how much a developer learning to modify PCGen would gain. Counts are measured,
not estimated.

## Where the handbook stands

57 pages, after a two-reviewer structural audit on 2026-08-22 cut one and merged five
sections into the page that owns them.

The generated [tag index](docs/lst/reference/tag-index.md) covers all 706 tags. What is
missing is explanation for the long tail, and whole subsystems with one page or none.

## Ranked, after cross-review

Two reviewers judged this independently — one on structure and coverage, one on whether
the wiki shortens the path to safely changing the code — then attacked each other's
verdicts. This order is what survived.

### 1. `DEFINE:` and declaring a variable

Both reviewers put it first, and one changed position to agree. `DEFINE:` is used
**37,644 times across 1,290 files**; `MODIFY:` 3,005. `variables-and-formulas.md`
covers only `MODIFY:` and says so in a section titled "What this page does not cover".

The front page promises "`DEFINE`, `MODIFY` and the newer formula system". Two of the
three are missing. A reader who needs a variable has a dead end, not a thin patch.

### 2. Granting: `ADD:`, `AUTO:` and `REMOVE:`

`AUTO:` 7,723 uses, `ADD:` 3,826, 13 token classes with 13 tests. The tags appear as
examples on twelve pages — race, template, domain, archetypes, new-class — and are
explained on none.

### 3. `TYPE`

Appears in 23 of 57 pages and is defined in none of them. `equipment.md` says type
decides everything about an item without saying what a type is. Dot syntax, `TYPE=`
matching in choosers and prerequisites, and the three PCC levels belong on one page.

### 4. Kit files

`plugin/lsttokens/kit/` — 49 token classes and **47 tests**, the richest untouched
specification in the repository. `KIT:` appears in 368 PCC files, more than `SKILL:`
(277), `DEITY:` (129) or `DOMAIN:` (98), each of which has a full page.

### 5. Equipment modifiers

`EQMOD:` 9,652 uses; 26 token classes, 14 tests. `equipment.md` gives it a paragraph.

### 6. Writing a character sheet

`outputsheets/` has 210 commits since 2023. The generated token index lists 154 tokens
and states plainly that it cannot give their arguments. Nothing covers the FreeMarker
side from the author's end.

### 7. Verifying your data loads

Absorbs `datatest`, `config.ini`, the `SHOWINMENU` trap, and the deliberately broken
sets in `data/zen_test/pcgen_broken_tests/`. One reviewer argued this should replace the
invented symptoms in `when-it-breaks.md` with real ones, rather than becoming a separate
debugging page. Agreed.

### 8. Spell delivery outside a class list

`SPELLS:` 8,422 uses, `SPELLKNOWN:` 5,450. Only `SPELLLEVEL:DOMAIN` is explained.

### 9. Ability display tags

The most-edited data files in three years are class ability files. Their lines are
carried by `ASPECT` (11,861 uses), `SAB` (11,508), `BENEFIT` and `NATURALATTACKS`
(6,483), each of which gets at most a table row.

### 10. How a data set is laid out

The `_` and `__` prefix convention and the publisher directory shape. Cheapest item
here.

## Internals gaps, measured against the Java tree

The ranked list above scores what a data author needs. It says nothing about what a
developer changing PCGen's Java needs, because neither reviewer measured that. This
section does, on 2026-08-22 at commit `d262f8b4`.

Method: every package under `code/src/java/pcgen/` and `code/src/java/plugin/` by line
count, class count and commits since 2023-01-01, set against the packages the seventeen
`docs/internals/` pages actually cite. Churn is the ranking signal — a package nobody
changes is a package nobody needs explained.

The section is not thin overall. At 17 pages and 14,568 words it is larger than the rest
of the handbook combined. The gaps are specific.

### 1. Prerequisites as code

`plugin/pretokens/` is **215 classes and 18,973 lines, changed in 138 commits since
2023** — the third-most-changed tree in the repository, ahead of `lsttokens` at 95. It
has **79 test files**. No internals page cites it once. Seven data pages cite it as the
implementing class and stop there.

Every prerequisite is a triple: `parser/PreAlignParser`, `test/PreAlignTester`,
`writer/PreAlignWriter`, against `PrerequisiteTest` and `AbstractPrerequisiteTest` in
`pcgen/core/prereq/`. Adding a `PRExxx` means writing three classes and knowing which
does what. Nothing in the handbook says so.

Highest-value internals page not yet written.

### 2. Facets, past the concept

`cdom/facet/` is **248 classes and 34,187 lines**; `cdom/` overall is the most-changed
package at 223 commits. `internals/facets.md` is 885 words and seven citations. It
explains what a facet is and how one registers. It does not cover the facet families,
the event ordering between them, or which to extend for a new stored fact.

The largest ratio of subsystem to page in the handbook.

### 3. Export tokens and the output model

`plugin/exporttokens/` is 140 classes and 13,683 lines. `pcgen/output/` adds 71 classes.
`internals/output-and-saving.md` cites `pcgen/io/exporttoken` — the smaller, older half —
and one FreeMarker class. This is the internals half of ranked item 6 and should be
written with it.

### 4. Bonus resolution

`core/BonusManager` plus `plugin/bonustokens/`, 55 classes. Cited once across internals,
from five data pages. How a `BONUS:` is parsed, stacked and applied is the mechanism
behind a large share of the data language and has no page.

### 5. Choosers and qualifiers

`cdom/choiceset/`, `core/chooser/`, `plugin/primitive/` and `plugin/qualifier/` — about
4,300 lines with **40 test files** between the last two. Zero internals citations. The
tests make this cheap to write correctly.

### 6. The Swing tab layer

`gui2/tabs/` is 61 classes and 22,334 lines; `gui2/facade/` is 30 classes and 17,108.
`internals/ui-layer.md` is 846 words and stops at the Swing-versus-JavaFX split, which it
does cover correctly. Ranked last here because `gui2` is being migrated to `gui3` — 24
commits against 13 since 2024 — so a deep page documents code that is moving.

### Measured and not worth a page

| Package | Why not |
|---|---|
| `core/term`, 129 classes | the JEP-era variable path. `rules-engine.md` already frames both formula systems and names `VariableProcessor`; a page would document the half being replaced |
| `gui2/converter`, 33 classes | a standalone `PCGenDataConvert.main` migration tool, not a subsystem anyone extends |
| `core/namegen`, `io/migration` | small, self-contained, no churn |

## Rejected, with reasons

**~150 hand-written tag pages.** The generated index already gives name, accepting class
and implementing class. A hand-written page adds what the token test states, and 150 of
them nearly triple the maintenance surface for the smallest marginal gain on this list.
Both reviewers rejected it independently.

**A companion-mod page.** `plugin/lsttokens/companionmod/` has 9 classes and **zero
tests**, so syntax would have to be inferred from token classes alone. `DECISIONS.md`
records that exact situation producing the `FEAT:`/`ABILITY:` error. Not worth the risk
for a narrow feature.

**A full game-mode file reference.** `game-modes.md` plus the generated index cover the
ground. Reproducing a 120 KB `miscinfo.lst` page is not documentation, it is
transcription.

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

Every one of these supplies **topics and facts**, never text. The handbook writes
original prose, cites the implementing class, and uses invented example content.

| Source | Supplies |
|---|---|
| `code/src/test/plugin/lsttokens/` — 363 test classes | accepted and rejected syntax, per tag |
| `installers/release-notes/` — 5.10 to 6.09.05 | what changed, and when |
| `plugin/lsttokens/deprecated/` — 32 classes | the deprecation map |
| `data/zen_test/` — 45 files | small complete data sets, and broken ones |
| `docs/listfilepages/lstfileclass/` — 25 lessons | which tasks a beginner needs, in what order |
| `docs/listfilepages/rulesguide/` — 3 worked examples | how rules are modelled in data |
| `system/gameModes/` — 20 modes | what a game mode is made of |

## Answered: output tokens can be indexed, up to a point

`tools/scan_tokens.py` works because every LST token declares `getTokenName()` as a
literal. Output tokens turned out to be the same: of 154 classes, **80 return a literal
and 74 return a constant declared in the same file. None are computed.** Three abstract
helpers declare no name and are skipped. Zero duplicate names.

So the scanner was written, and the name, class, package, origin and deprecation flag are
generated. The FreeMarker model keys came along with it — all 23 are registered under
literal names, though from 15 or so files scattered across the tree rather than one
package.

Two things stay hand-written, and this is why the reference is only half solved:

- **Argument grammar.** There is no sub-token registry. `Token.java` declares a
  separator constant that nothing else uses, and each class parses its own remainder
  with a tokenizer and an if/else chain. `STAT.0.MOD` is one name and two arguments that
  exist only as literals inside that chain. Extracting them means reading each class.
- **Deprecation replacements.** The only signal is the package name. No annotation, no
  javadoc tag, no logged message, and nothing naming a successor. Where the LST side gets
  a migration message from the token itself, this side gets a directory.

Both facts are worth keeping: they are the difference between a system designed to be
read and one that merely can be.
