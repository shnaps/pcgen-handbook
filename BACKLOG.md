# Backlog

What the handbook could cover next, and what it should not. From a survey of the PCGen
repository and PCGen's own documentation on 2026-08-22, at commit `d262f8b4`.

Ranked by how much a developer learning to modify PCGen would gain. Counts are measured,
not estimated.

## Where the handbook stands

**66 pages.** The generated [tag index](docs/lst/reference/tag-index.md) covers all 706
tags. What is missing is explanation for the long tail.

`docs/internals/` is 18 pages — larger than every other section combined.

**All thirteen ranked items are done, 2026-08-22.** Nine became pages, four were folded
into pages that already owned the ground. That section below is the record of what was
decided and why, not a queue.

A three-reviewer verification pass on 2026-08-22 found eleven errors in the new pages and
reopened the queue. All four items it raised are now done, 2026-08-23. Nothing is open.

## Closed: the verification pass

From the three-reviewer verification pass, 2026-08-22. All four done 2026-08-23.

### 1. The JEP formula engine — done 2026-08-23, `internals/formula-system.md` extended

**The handbook documents the formula engine the data barely uses and not the one it runs
on.** `formula-system.md` is 730 words entirely about `PCGen-Formula` and `MODIFY`, with
zero mentions of JEP, PJEP, `jepcommands` or `core/term`. `overview.md` points at it for
JEP. Every `DEFINE:X|0` and `BONUS:VAR` — 37,076 and 83,023 uses — evaluates through PJEP.

Churn 7 commits since 2023. Tests 0.

Scope, as the cross-review settled it:

- Extend, but replace the opening. As it stands the page opens on Gradle subprojects, so
  appending JEP staples two topics together. Open on the fork instead: two engines, and
  which one runs is decided when the tag is parsed.
- **Include** the 14 functions in `plugin/jepcommands/`. A closed set, plugin-registered
  at `PJEP.java:84-91`, and it answers "what can I write".
- **Do not** table the 95 terms. `TermEvaluatorBuilderPCVar` declares 80 and
  `TermEvaluatorBuilderEQVar` 15. Give the mechanism — `EvaluatorFactory` builds two
  vocabularies, PC and EQ, from regex enums — plus six or eight representative terms and
  a pointer. A 95-row table is transcription, rejected on the same ground as the 150 tag
  pages below.
- The fact a data author needs: the vocabulary inside a `BONUS:` value is closed and
  matched by regex, so a name that is not in it is not an error, it is a variable.
- The fact a code changer needs: a new function is a `PCGenCommand` in
  `plugin/jepcommands/`, a new term is an enum constant plus a `TermEvaluator` class in
  `pcgen/core/term/`, and `PJEP.java:99` adds `cl` outside both.

### 2. Where facades are implemented — done 2026-08-23, `internals/ui-layer.md`

`pcgen/gui2/facade/` is 30 classes, 9 commits, 1 test, and zero handbook citations.
`CharacterFacadeImpl` is 4,097 lines. `ui-layer.md` names the 33 interfaces and counts the
package in its leak table, but never says this is where you edit to add a facade method.
Two sentences.

### 3. The LST converter — done 2026-08-23, `internals/adding-a-tag.md`

`pcgen/gui2/converter/` 9 classes plus `plugin/converter/` 28, 10 commits, 0 tests, zero
citations. `adding-a-tag.md` says deprecation means moving the class to `deprecated/`. It
omits that a `ConvertPlugin` can rewrite the data instead. One paragraph.

### 4. `load-pipeline.md` hides two dispatchers — done 2026-08-23

Its table labels all 653 `plugin/lsttokens` files "data and game mode tags" in one row.
The count is right. Game mode tokens use a different registry, which
[adding a tag](docs/internals/adding-a-tag.md) now explains. One row, split in two.

## Ranked, after two cross-reviews

Two reviewers judged this independently — one from the data author's seat, one from the
seat of a developer changing the Java — then attacked each other's verdicts and had to
defend or concede each with evidence. Second pass on 2026-08-22, after the first pass's
internals ranking was found to rest on a broken measurement. This order is what survived.

Counts are measured at commit `d262f8b4`, by the method now pinned in `WIKI-SCHEMA.md`.
Churn is commits, not file-touches — the distinction that invalidated the first pass.

Some figures quoted in this section predate that method and were restated on the pages
themselves. The pages are correct; treat this section as the reasoning, not the numbers.

### 1. `TYPE` — written 2026-08-22, `lst/concepts/types.md`

**282,966 uses**: 197,550 as its own field, 21,490 embedded in other fields, 63,926 as
`TYPE=`. The most-used construct in the data language. It appears in 23 of 57 pages and
is defined in none of them, internals included.

`equipment.md` tells the reader type decides everything about an item without saying what
a type is. Both reviewers converged on the principle behind this: **a silent gap outranks
an admitted one.** An admitted gap sends the reader elsewhere. A silent gap sends them
into a wrong edit.

Dot syntax is a real grammar, so the page is short and fully citable: `TypeLst.java:47`
`.CLEAR`, `:76` the dot split, `:83` `.ADD.`, `:92` `.REMOVE.`, `:100` rejecting `.CLEAR`
mid-string. The owning page must carry the Java half — `ListKey.TYPE` and `TYPE=`
resolution through `cdom/reference`, 9 commits since 2023 — because no other page can.

### 2. `DEFINE:X|0`, and `BONUS:VAR` with it — written 2026-08-22, `lst/concepts/declaring-variables.md`

**37,179 `DEFINE:` fields, and 37,077 of them — 99.7% — are the `|0` form.** The value
arrives separately through `BONUS:VAR`, at 83,023 uses.

The gap is admitted: `variables-and-formulas.md:125-127` says declaring a variable is not
covered, `bonuses.md:129` points at the missing page, and `docs/index.md:52` promises
`DEFINE`.

**Teach one form.** `DefineLst.java:65-68` hard-fails `UNLOCK.` and `:96-101` hard-fails
`LOCK.`, both redirecting to `DEFINESTAT`; `:85-90` calls `deprecationPrint` on any
non-zero, non-`MAXLEVELSTAT=` formula. Those forms go to `appendix/whats-changed.md`. At
99.7% one shape, this is roughly a third of the page originally planned, which is why it
sits below `TYPE` without loss.

### 3. Granting: `ADD:`, `AUTO:` and `REMOVE:` — written 2026-08-22, `lst/concepts/granting.md`

`plugin/lsttokens/add/` 8 classes, `auto/` 5, with 8 and 5 tests. The tags appear as
unexplained examples on twelve pages — race, template, domain, archetypes, new-class.

Ranked above display tags because an ability must work before it reads well.

### 4. Ability display tags — written 2026-08-22, `lst/concepts/display-text.md`

**139 of the 189 commits to `data/` since 2023 touch ability files — 74%.** The single
strongest churn signal measured anywhere in this backlog. `ASPECT` has 11,861 uses, `SAB`
11,508; each gets at most a table row today.

One reviewer ranked this second on that churn and the other sixth, arguing display text is
not what blocks a newcomer. Both hold: the churn is real, and the dependency on item 3 is
real. It sits directly behind the tags that make an ability do anything.

### 5. Verifying your data loads — done 2026-08-22, folded into `start/when-it-breaks.md`

Nothing above is safe to write without a pass/fail loop, which is the argument that moved
this up. Absorbs `datatest`, `config.ini`, the `SHOWINMENU` trap, and the deliberately
broken sets in `data/zen_test/pcgen_broken_tests/`. Replaces the invented symptoms in
`when-it-breaks.md` with real ones rather than becoming a separate page.
`internals/testing.md` is 553 words, the shortest internals page.

### 6. Facets, past the concept — done 2026-08-22, `internals/facets.md` extended

`cdom/facet/` is 248 classes and 34,187 lines across **18 commits since 2023**, twelve of
them since 2025. `internals/facets.md` is 885 words: it gives 4 of 14 base classes and the
extension pattern in three lines. The largest subsystem-to-page ratio in the handbook.

Highest-ranked internals item. It sits below the data items because those cover facts no
page owns at all, while this one deepens a page that exists and is correct.

### 7. The output side, both halves — written 2026-08-22, `outputsheets/writing-a-sheet.md`

`docs/outputsheets/` holds only the generated index, which states it cannot give token
arguments. Nothing covers the FreeMarker side from the author's end, and nothing covers
adding an output token from the code side. One subsystem, one work item — not two.

### 8. Equipment modifiers — written 2026-08-22, `lst/files/equipment-modifier.md`

`EQMOD:` 12,086 uses; 26 classes, 14 tests. `equipment.md` gives it a paragraph. Ranked on
usage: no measurable commit churn on eqmod data files since 2023.

### 9. Choosers and qualifiers — written 2026-08-22, `internals/choosers.md`

`cdom/choiceset/`, `core/chooser/`, `plugin/primitive/` and `plugin/qualifier/` — about
4,300 lines with **40 test files** between the last two, and zero internals citations for
`cdom/choiceset` or `core/chooser`. `choosers.md` covers the data face only. The tests make
this cheap to write correctly.

### 10. Spell delivery outside a class list — written 2026-08-22, `lst/concepts/granting-spells.md`

`SPELLS:` 8,422 uses, `SPELLKNOWN:` 5,450. Only `SPELLLEVEL:DOMAIN` is explained.

### 11. Tab binding — done 2026-08-22, section in `internals/ui-layer.md`

How a tab binds to `CharacterFacade`, added to `internals/ui-layer.md`, which already owns
the boundary fact.

`gui2` out-churns its own replacement: 30 commits since 2023 against `gui3`'s 16, and 21
against 12 since 2025. One reviewer moved to drop this on staleness and conceded — the old
layer is still where work lands, and `ui-layer.md:42` already records that nothing suggests
it is changing soon. The other conceded that a page documenting 39,442 moving lines is
still wrong. A section is what survived both.

### 12. Kit files — written 2026-08-22, `lst/files/kit.md`

`plugin/lsttokens/kit/` has 49 classes and 47 tests, but **7 data commits since 2023
across 314 `STARTPACK:` files**, and the files are dominated by machine-generated monster
packs. Kits consume `TYPE`, `PRE` and `ABILITY` — downstream of items 1 to 4, not a
substitute for them.

Both reviewers demoted this from fourth independently. Class and test counts measure
specification size, not reader need.

### 13. How a data set is laid out — done 2026-08-22, merged into `lst/concepts/sources.md`

The `_` and `__` prefix convention and the publisher directory shape. Two paragraphs
merged into `lst/concepts/sources.md`, which already owns discovery and load order. Not a
page — a page would break "one fact, one owner".

## Dropped in the second cross-review, with reasons

**Prerequisites as code.** Ranked first among internals gaps in the first pass, on two
errors. Its 138 "commits" were file-touches; the real figure is **4 commits since 2023**,
and **130 of the 138 touches are one PMD sweep**, `7f818006e3`, dropping a redundant
`implements`. The remaining three are a Java 17 move, a file relocation and a fork merge.
The claim that no internals page cites `plugin/pretokens` was also false —
`adding-a-tag.md:25`, `load-pipeline.md:147` and `plugin-loading.md:20` all do, and
`prerequisites.md:144-151` already carries the parser/test/writer table said to be missing.
Both reviewers dropped it. Nothing is owed here.

**Bonus resolution.** `rules-engine.md:71-107` already owns it: the two-stage
`buildActiveBonusMap`, static-then-recursive order, the bonus-type key format,
`getTotalBonusTo`, and per-pass prerequisite re-testing. A second page is the exact
duplication `WIKI-SCHEMA.md` forbids. The only remainder is `plugin/bonustokens/` — 55
classes, 3 commits, and **zero tests**, which is the condition used to reject the
companion-mod page.

**Export tokens as a separate internals item.** `output-and-saving.md:72` already cites
`plugin/exporttokens/` and its 140 classes and `:89` cites `pcgen/output/model/`. Merged
into item 7.

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
| `data/zen_test/` — 47 files | small complete data sets. The broken subset is five files under `pcgen_test_advanced/pcgen_broken_tests/`, mostly commented out, covering two narrow cases |
| `docs/listfilepages/lstfileclass/` — 25 lessons | task ordering only. `FEAT:` appears in 9 lessons and `VFEAT` in 6, against `ABILITY:` in 6. Never take syntax from it |
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
