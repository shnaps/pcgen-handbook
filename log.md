# Log

Append-only record of ingest and lint runs. Newest last.

Each entry records what was scanned, at which upstream commit, and what changed.
This is what answers "is this current, and when was it last checked?".

Format:

```
## YYYY-MM-DD  <operation>
- upstream: PCGen @ <sha>
- <what changed>
```

---

## 2026-08-22  initial ingest

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`, version `6.09.08.RC1`
- Sparse shallow clone: `code/src/java`, `code/src/test`, `code/src/slowtest`,
  `docs`, `data/zen_test`, `data/35e/homebrew`, `system/gameModes`.
- `scan_tokens.py`: 1,005 token classes parsed, **706 unique tags** written to
  `tags.json`. Family split: 653 `lst`, 129 `pre`, 55 `bonus`, 23 `primitive`,
  13 `qualifier`. 32 flagged deprecated.
- The `lst` count matches the 653 files in `plugin/lsttokens/` exactly, which is the
  check that nothing was silently dropped. An earlier run reported 513 because
  classes were keyed by name, so same-named classes in different packages
  (`race/TypeToken`, `skill/TypeToken`) overwrote each other.
- Cross-check against PCGen's own docs index (`docs/navlistindex.html`): the docs list
  **868** tag entries against 706 implemented. The gap is partly tags documented once
  per file type and counted repeatedly, partly tags that no longer exist. Not yet
  reconciled entry by entry — that work feeds `appendix/whats-changed.md`.

## 2026-08-22  transcript harvest

- Source: YouTube playlist `PLLa5A1qjBOPekqEC_R9BAZW-8q5IT-klM`, 25 videos, 4 h 51 m.
- All 25 have auto-generated English captions (`en-orig`). None have human subtitles,
  so Whisper was not needed.
- 41,273 words captured to `work/transcripts/` (gitignored, not republished).
- **Quality assessed across all 25, not sampled.** Result: **7 ALLCAPS tokens in
  41,273 words.** Tag names are uppercase, so the corpus holds almost no recoverable
  tag syntax. Around 180 mangled domain terms ("PC gen", "TC gen", "list file").
- Conclusion, now measured rather than assumed: transcripts are usable for workflow,
  ordering and failure modes. **Never for syntax.** Every tag on a page derived from a
  video is verified against `tags.json` before it ships.

## 2026-08-22  correction found in published content

- `first-change.md` told readers to use PCC `FEAT:`, following
  `data/35e/homebrew/my_homebrew/`, whose template dates from 2005.
- `FEAT:` is implemented by `plugin/lsttokens/deprecated/CampaignFeatToken.java` and
  logs a deprecation notice directing authors to `ABILITY:` with `CATEGORY:` entries.
  PCGen's own test data uses `ABILITY:`, including the file it names
  `pcgen_test_advanced_feats.lst`.
- Fixed, and a section added explaining the old form, since the shipped templates and
  every video tutorial predate the change.
- Method note worth keeping: **the shipped homebrew templates are not a reliable
  teacher.** Verify against the token class, not against the templates.

## 2026-08-22  widened the checkout, corrected two claims

- Sparse checkout widened from `data/35e` + `data/zen_test` (2.3 MB) to all of `data`
  and `system` (151 MB, **6,311 `.lst` files** across 19 game modes). The narrow
  sample was too small to support claims about how tags are used in practice.
- **Correction: `KEY:` usage.** An earlier grep reported zero uses and I described the
  tag as an occasional tool for when a display name might change. The grep was faulty.
  Counted properly: **71,566 uses across 1,296 files.** Setting a key is normal
  practice in real data, not an edge case. `new-feat.md` corrected.
- `OUTPUTNAME` confirmed at roughly 14,000 uses, supporting the earlier finding that it
  is current rather than superseded, despite older tutorials calling it the old way.
- Standing caveat: `check_examples.py` validates tag *names* against `tags.json` but
  not their *arguments*. Value syntax has to be checked by hand against shipped data or
  the token class. Both errors caught so far were in argument syntax, not tag names.

## 2026-08-22  internals expanded to the wider code base

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`, version `6.09.08.RC1`.
  No re-scan; `tags.json` unchanged.
- Sparse checkout widened again to add `code/gradle` and `code/standards`, so build and
  style citations resolve for `lint_wiki.py` like source citations already did.
- Seven pages added to `internals/`, taking it from 7 to 14. Scope moves past the LST
  loader for the first time: `building.md`, `startup.md`, `cdom-model.md`, `facets.md`,
  `ui-layer.md`, `output-and-saving.md`, `contributing.md`.
- Facts were gathered by seven scoped source reads, one per page, and each numeric claim
  was re-counted directly before it shipped.

### Measurements taken, all at the pinned commit

- `PlayerCharacter.java` is 9,910 lines and holds a `CharID` plus about 107 facet
  references. Character state lives in one static map in `AbstractStorageFacet`, keyed
  by character and facet class. 248 facet classes.
- `pcgen/gui2` 241 files, `pcgen/gui3` 54, `pcgen/facade/core` 33.
- Export tokens: 17 classes in `pcgen/io/exporttoken/`, 140 in `plugin/exporttokens/`,
  49 of those deprecated. Unrelated to LST tokens, and easy to confuse with them.

### Finding: the facade boundary is documented but not maintained

`CharacterFacade` states that the interface layer may operate only through the facade
interfaces. Measured: **93 of 241 `gui2` files import `pcgen.core` directly**, 26 of
them inside `gui2/facade/` and 67 outside it. `PCGenFrame` is one of the 67, and 14 of
the 33 `facade/core` interfaces import core classes themselves.

Recorded on `ui-layer.md` as a measurement rather than repeating the stated rule. Same
failure mode this handbook exists for: a documented claim the code stopped honouring.

### Finding: the style checks gate nothing

Checkstyle and PMD are unhooked from the build with `sourceSets = []`. PMD and SpotBugs
both set `ignoreFailures`. CI runs `build`, `testCoverage`, `itest`, `datatest` and
`slowtest`, and never `allReports`. So a change breaking every configured style rule
still goes green. On `contributing.md`.

## 2026-08-22  data layer widened, and a survey of what is left

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No re-scan; `tags.json`
  unchanged.
- Eight pages added: `bonuses`, `choosers`, `keys-and-names`, `data-controls`,
  `files/template`, `files/spell`, `files/domain`, `internals/overview`. 52 pages total.

### Corrections to my own measurements

- **`BONUS:` counts were inflated.** The pattern `BONUS:([A-Z]+)` also matches inside
  `TEMPBONUS:`, so `BONUS:PC` and `BONUS:ANYPC` appeared as real subtypes. Neither
  exists — no class in `plugin/bonustokens/` handles either name. Recounted with a
  boundary: **174,114 `BONUS:` uses in 2,937 files**, and 3,243 `TEMPBONUS:` uses.
- Caught by a source read disagreeing with the corpus number, which is the check that
  is supposed to catch this.

### Measurements taken

- `CHOOSE:` about 11,200 uses, and 5,421 of them are `CHOOSE:NOCHOICE` — a chooser that
  presents nothing, written to satisfy the rule that `MULT:YES` requires a chooser.
- Naming tags: `KEY:` 71,572 uses in 1,296 files, `OUTPUTNAME` 14,097, `SORTKEY` 12,268
  (7,716 of them on abilities), `NAMEISPI` 6,496. `.MOD` on 56,733 lines.
- Templates: 8,040 lines in 359 files, `VISIBLE` on 6,397 of them. Spells: 36,510 lines,
  `CLASSES:` on 25,399. Domains: 904 lines, `SPELLLEVEL:DOMAIN` on 864.
- Only **5 of PCGen's 54 code controls** are set by any shipped game mode.

### Finding: the package layering is not a hierarchy

Import counts at the pinned commit: `cdom` and `core` import each other 288 and 185
files deep; `rules` and `persistence` both ways; `gui2` and `gui3` both ways. Nine files
in `pcgen.core` import the Swing interface package.

Three edges are genuinely one-directional: `output` and `pluginmgr` depend downward
only, and the interface depends on `facade` rather than the reverse.

Recorded on `internals/overview.md` as measured fact. The two seams that hold are the
two a tool enforces — plugin jars and the Java module boundary. The two that leak are
policed by convention.

### Survey

`BACKLOG.md` added at the repository root: a ranked list of what to cover next, what to
leave alone, and which upstream sources supply topics. Built from four scoped reads of
`docs/`, `data/`, `system/` and `plugin/lsttokens/`.

Headline numbers from it: PCGen documents **164 output tokens** the handbook has no
reference for; `plugin/lsttokens/kit/` has 47 test classes and no page;
`installers/release-notes/` covers **5.10 through 6.09.05** and has never been read.

## 2026-08-22  output tokens indexed from source

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. `tags.json` unchanged.
- Two tools added: `scan_output_tokens.py` and `gen_output_index.py`, and a new
  `outputsheets/` section holding the generated index.

**154 output tokens**, 49 of them deprecated. 17 classes in `pcgen/io/exporttoken/`,
140 in `plugin/exporttokens/`, 3 abstract helpers skipped. No duplicate names.

The scan was possible for the same reason the LST scan is: **80 of the 154 return a
string literal from `getTokenName()` and 74 return a constant declared in the same
file. None are computed.** Also collected the 23 FreeMarker model keys, registered
under literal names from about 15 files across the tree.

Two things the source will not give up, and the page says so rather than guessing:

- **Argument syntax.** There is no sub-token registry. `Token.java` declares a
  separator constant that nothing else uses, and each class parses its own remainder
  with a tokenizer and an if/else chain. `STAT.0.MOD` is one name and two arguments
  that exist only inside that chain.
- **What replaces a deprecated token.** The only signal is the package name — no
  annotation, no javadoc tag, no logged message. The LST side logs a migration message
  from the token itself; this side gives a directory.

For comparison, PCGen's own `navtokenindex.html` is hand-maintained and lists 154
anchors, 17 of which are formula functions rather than tokens. The generated index and
the hand-written one agree on the count by coincidence, not by construction.

## 2026-08-22  source loading documented, and a correction

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. `tags.json` unchanged.
- Three pages added: `lst/concepts/sources.md`, `lst/howto/publish-a-source.md`,
  `internals/source-selection.md`. 56 pages total.

### Correction to a published claim

`keys-and-names.md` said the first object loaded wins a key clash. **That is wrong.**
`LstObjectFileLoader.storeObject` allows an override by default and settles it by
`SOURCEDATE`: the newer object survives and the other is forgotten. A new object with no
date, or an older one, is the one discarded. Turning the preference off makes the clash
an error naming both files instead.

Found by a source read contradicting an earlier page, then confirmed by reading the
method. Page corrected, and the rule is now stated in full on `sources.md`.

### Measurements

- **680 `.pcc` files** in shipped data, nested two to six directories deep.
- **55 carry no `CAMPAIGN:` tag.** They are fragments included by `PCC:` and carry a
  `KEY:` instead, so they never appear in the source list.
- `PRECAMPAIGN` in 552 files, 843 uses, 124 of them negated. Four value forms:
  `INCLUDES=` 327, `BOOKTYPE=` 262, a plain name 203, `INCLUDESBOOKTYPE=` 175.
- `SHOWINMENU` in **11 files only**. Since `datatest` skips a `.pcc` without it, almost
  no shipped source is covered by that harness.
- `RANK` is written as a publication date, `YYYYMM`. `BOOKTYPE` is `Supplement` in 417
  of 615 cases. `STATUS` is `BETA` 268 times against `RELEASE` 116.
- `TYPE` depth: two levels 111 times, three 66, one 17.

### The load order rule, written down

Three rules in sequence, from `SourceFileLoader.loadCampaigns`: selected campaigns
sorted by `RANK` **descending**, then file order as the tags appear in each PCC, then a
**hard-coded sequence of file types** — data control, tables, variables, dynamic, global
modifiers, ability categories, size, stat/save/alignment, proficiencies, skill,
language, feat, ability, race, domain, spell, deity, class, template, equipment
modifier, equipment, companion mod, kit, bioset.

Data cannot reorder that last one. It is the reason a `.MOD` on a class cannot be
written from a race file.

### Other findings worth keeping

- `HELP:` on a PCC parses and **nothing reads it**. The only reference to its storage key
  is the token class itself.
- `OPTION:` writes into the reader's own persistent settings, not a per-load scratch
  area. A source changes a preference and it outlives the session.
- A missing `PCC:` include is skipped silently, logged only.
- `FORWARDREF` exists to declare references allowed to stay unresolved, which is how a
  source refers to a book the reader may not own.

## 2026-08-22  the rules engine and rule toggles

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. `tags.json` unchanged.
- Two pages added: `internals/rules-engine.md` and `lst/concepts/rule-toggles.md`.
  58 pages total. These close the gap between the tag pages and the formula system page:
  the tags were documented, the calculation that reads them was not.

### The convergence loop

`PlayerCharacter.calcActiveBonuses` does not compute once. It rebuilds the whole bonus
map repeatedly until two consecutive results match, logs an error at 29 passes and gives
up at 31. The reason is stated in a source comment and nowhere else: a variable can carry
a prerequisite that depends on a second variable whose value is not correct until the map
is complete.

There is no dirty flag. Every mutation rebuilds everything.

### Two of everything

- **Two evaluators.** JEP handles `DEFINE:` and `BONUS:` values; PCGen-Formula handles
  `MODIFY:`. Which one runs is fixed when the tag is parsed, not chosen at runtime.
- **Two variable stores.** A `DEFINE:` value lives under a `VariableKey` reached through
  `PlayerCharacter.getVariable`. A `MODIFY:` value lives in `SolverManager`'s own store,
  reached through `VariableContext`. Neither sees the other.

Both pairs run on the same character at the same time.

### Rule toggles

339 entries across the 19 shipped game modes, but only **35 distinct names** — game modes
mostly offer the same toggles. `PARM:` is used 221 times against `VAR:` 119, and 60
entries carry `EXCLUDE:`.

Measured in data: `PRERULE` is used **12,775 times across 139 files, but only 148 of
those as a field of its own.** It is almost always appended inside a `BONUS:` value, which
is the shape a data author should copy.

A toggle's `VAR:` is a lookup key, not a character variable. `PREVAR` and `BONUS:` cannot
read it. Data has exactly one lever, `PRERULE`; everything else is a hardcoded check in
Java, which is why a data set cannot add a toggle the engine honours.

### Another stale header found upstream

Shipped `rules.lst` files claim in their header that the reader-visible label is looked up
in `Language.properties`, with `DESC:` as a fallback. The preferences panel reads `DESC:`
directly and no such lookup exists anywhere. Recorded on the page.

### Measurement note, no correction needed

Re-counted prerequisites two ways. Field-level positive uses total 100,575; counting every
occurrence, including those appended inside other tags, gives 239,482. `prerequisites.md`
uses the field-level figures and they check out exactly, including "about 13,000 negated
across 33 tags" against a measured 13,365 across 33.

## 2026-08-22  two-reviewer structural audit

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. `tags.json` unchanged.
- Two independent reviewers read the whole wiki against the source: one judging
  structure and coverage, one judging whether the wiki shortens the path to safely
  changing the code. They then cross-reviewed each other's verdicts and had to defend or
  concede each with evidence.

### The finding that matters

**The handbook had no rule for which page owns a fact.** Duplicate-key resolution was
explained on five pages. `datatest` on seven. `SHOWINMENU` on six. Every copy read
correctly, which is the problem: nothing looked wrong, so nothing prompted a fix.

Then one copy drifted. `lst/files/domain.md` said two sources with the same key resolve
by first-loaded-wins, the opposite of what `keys-and-names.md` and `sources.md` said and
the opposite of `LstObjectFileLoader.storeObject`. `lint_wiki.py` passed clean over it.

This is the failure `DECISIONS.md` was written to prevent, reproduced inside the
handbook that diagnosed it.

**Fixed structurally, not just locally.** `WIKI-SCHEMA.md` gains a "one fact, one owner"
rule with a table of owned facts, and `lint_wiki.py` now reports any page re-explaining
a fact it does not own. The check caught three pages on its first run — two of them
sentences written minutes earlier while removing the duplication it was built to find.

### Acted on

- **Cut** `appendix/video-index.md`. Its only unique content was a caption measurement
  already in `credits.md`, and every how-to links its own video directly.
- **Merged into their owners**: the `rules.lst` table from `game-modes.md`, the token
  registration mechanism from `load-pipeline.md`, the `datatest` section from
  `load-pipeline.md`, the domains section from `deity.md`, the contribution workflow
  from `report-a-bug.md`, and duplicated example blocks from `new-skill.md` and
  `new-equipment.md`.
- **`index.md` made a real navigation contract.** It listed 35 of 57 pages while
  `DECISIONS.md` calls it the contract. The 22 missing were mostly the file-type and
  how-to pages — the half a data author needs most. Three pages went orphan when
  `video-index.md` was cut, which is how the gap surfaced.

### Kept against a reviewer's advice, with reasons

- `internals/plugin-loading.md`. One reviewer wanted it merged. It is the only page
  carrying the `TokenLibrary` routing table and the "a scan of the classes is
  exhaustive" argument, which is the stated justification for `scan_tokens.py` and
  therefore for the project's whole method. The duplicated summary in `load-pipeline.md`
  was cut instead.
- `lst/files/domain.md` and `lst/howto/new-skill.md`. Merging either would break a
  one-page-per-file-type rule and a complete how-to series. The duplication was removed;
  the pages stayed.

### Twelve claims audited against the source

Six confirmed, three wrong, three misleading — all corrected in the preceding entry. The
telling part is which: **every error was a numeral**, and `check_examples.py` and
`lint_wiki.py` were green throughout. Neither tool validates a number.


## 2026-08-22  internals coverage measured against the Java tree

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No page content changed.
- The two-reviewer audit scored coverage from a data author's seat. Nothing had scored
  `docs/internals/` against the code it documents, so the question "is internals thin"
  had no measured answer.

Counted every package under `code/src/java/pcgen/` and `code/src/java/plugin/` by lines,
classes and commits since 2023-01-01, then extracted the packages the seventeen internals
pages cite and subtracted.

**Internals is the largest section, not the smallest.** 17 pages, 14,568 words — more
than `start/`, `lst/`, `outputsheets/` and `appendix/` together. The audit had also moved
content *out* of it: token registration and `datatest` were merged away, and one reviewer
argued to cut `plugin-loading.md` entirely.

**The real gap is prerequisites.** `plugin/pretokens/` is 215 classes, 18,973 lines and
138 commits since 2023 — more changed than `lsttokens` at 95, and third in the whole
repository. It carries 79 test files. Seven data pages cite it as an implementing class.
No internals page cites it at all. A `PRExxx` is a parser, a tester and a writer against
`AbstractPrerequisiteTest`, and the handbook never says so.

Five smaller gaps behind it, and three packages measured and rejected. Ranked in
`BACKLOG.md` under "Internals gaps, measured against the Java tree".

Churn was used as the ranking signal rather than size. `cdom/facet/` is the biggest
subsystem-to-page ratio in the handbook — 248 classes against 885 words — but a package
nobody changes is a page nobody needs.
