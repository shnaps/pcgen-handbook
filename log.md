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

## 2026-08-22  second cross-review, and a retraction

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No page content changed.
- Two reviewers re-ranked the whole backlog as one list — one from the data author's
  seat, one from a Java developer's — then cross-reviewed.

**The preceding entry's internals ranking was wrong, and is retracted.** Two errors, both
mine, both caught by a reviewer.

**The churn figures were file-touches, not commits.** `git log --name-only` prints one
line per file per commit; counting those lines counts files. `plugin/pretokens` is **4
commits since 2023, not 138**, and **130 of the 138 touches are one PMD sweep**,
`7f818006e3`, dropping a redundant `implements`. The remaining three are a Java 17 move, a
file relocation and a fork merge. The inflation is not uniform — pretokens runs 34 files
per commit against `cdom`'s 7 — so it does not cancel out in a ranking. It promoted a
subsystem with essentially no real work to first place.

**The citation extraction produced a false negative.** It matched only paths prefixed
`code/src/java/` and missed every bare `plugin/...` citation. `adding-a-tag.md:25`,
`load-pipeline.md:147` and `plugin-loading.md:20` all cite `plugin/pretokens`, and
`prerequisites.md:144-151` already carries the parser/test/writer table the entry called
missing.

Three of six internals gaps did not survive. Prerequisites-as-code and bonus resolution
were dropped outright, export tokens merged into the output item.

**What the reviewers converged on.** `TYPE` takes first place from `DEFINE:` on a
principle worth keeping: **a silent gap outranks an admitted one.** An admitted gap sends
the reader elsewhere; a silent gap sends them into a wrong edit. `variables-and-formulas.md`
says plainly that it does not cover declaring a variable. `equipment.md` says type decides
everything about an item and never says what a type is. The second is the worse failure,
and `TYPE` is used 282,966 times against `DEFINE:`'s 37,179.

`DEFINE:` also shrank. 99.7% of its uses are one form, `DEFINE:X|0`; `LOCK.` and `UNLOCK.`
hard-fail to `DEFINESTAT` and non-zero values call `deprecationPrint`. The page teaches
one shape and sends the rest to `appendix/whats-changed.md`.

**Method note for the next audit.** Rank on commits, never on `--name-only` lines. Extract
citations by package name, not by path prefix. Both errors passed every existing check —
`check_style.py`, `lint_wiki.py` and `mkdocs build --strict` were green throughout, as
they were for the twelve numeral errors in the first audit. No tool here validates a
number.

## 2026-08-22  types page

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog item 1.
- New page `lst/concepts/types.md`. 58 pages.

The gap was real: `TYPE` is set 197,550 times and matched 63,926 times in shipped data,
appears on 23 of 57 pages, and was explained on none.

**Two facts had no possible other owner.**

Dots change meaning depending on side. `TYPE:Weapon.Melee` sets two separate types.
`TYPE=Weapon.Melee` matches objects carrying both — `AbstractReferenceManufacturer` tests
each type and breaks at the first miss. Setting is a list, matching is an AND.

Negation works in one place and not the other. `TokenUtilities.getTypeOrPrimitive` rejects
`!TYPE=` and `!TYPE.` outright, logs `!TYPE not supported in token` and returns null, so
the tag is dropped. `ChoiceSetLoadUtilities` handles `!TYPE.` and wraps it in a
`NegatingPrimitive`. `choosers.md` already documented the working form. Without the page
those two read as a contradiction.

**A trap found while reading the source.** `TYPE:` in a `.pcc` is a different token class
entirely. `campaign/TypeToken.java` stores three dot-separated positions — data producer,
data format, campaign setting — and omitting a position resets it rather than leaving it
alone. Two classes register the name `TYPE` and the file being loaded picks which runs.

**Ownership.** `equipment.md` kept the consequence and links out; its explanation of the
dot syntax was removed. Added a row to the `WIKI-SCHEMA.md` table and to `OWNED` in
`lint_wiki.py`.

Note on that check: the first version of the pattern was written with `\b` word
boundaries that reached the file as literal backspace bytes, so the rule matched nothing.
It passed `lint_wiki.py` cleanly, because a dead rule and a satisfied rule look identical.
Test an ownership pattern against a string it should catch before trusting it.

## 2026-08-22  declaring a variable

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog item 2.
- New page `lst/concepts/declaring-variables.md`. 59 pages.

The reviewers' split held up. `DEFINE` has one shape worth teaching — 37,077 of its
37,179 uses are `DEFINE:X|0` — so the page teaches that and sends the rest to
`appendix/whats-changed.md`.

**The fact that justifies the page.** `PlayerCharacter.getVariable` looks a name up as a
declared variable key. On a hit it resolves the declared value and then adds
`getTotalBonusTo("VAR", name)`. On a miss it falls back to evaluating the name as a
formula and sets `includeBonus = false`.

So a `BONUS:VAR` naming a variable that no `DEFINE` declared contributes nothing, and
nothing is logged. That is why data declares at zero and bonuses carry the value. Neither
tag's own page could state this — it lives in the join between them.

**Declarations do not stack.** `VariableFacet.getVariableValue` resolves every
declaration of a name and keeps one, min or max by a flag. `VariableProcessor:537` passes
`true`, so a formula reading a variable gets the highest declaration. Bonuses stack;
declarations do not. Declaring at zero sets a floor and leaves the arithmetic to bonuses.

**A typo worth documenting.** The parse failure for `DEFINE:LOCK.` names
`DEFINESTAT:LOCL|` as the replacement. `DefineStatLst` accepts `LOCK`, `UNLOCK`,
`NONSTAT`, `STAT`, `MINVALUE` and `MAXVALUE`. There is no `LOCL`, so a reader searching
the error text finds nothing. Recorded in `whats-changed.md`.

**Ownership.** Added `BONUS:VAR` applying only to a declared variable to the schema table
and to `OWNED`. Tested the pattern against three strings before committing this time —
two it must catch, one it must not.

## 2026-08-22  granting things

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog item 3.
- New page `lst/concepts/granting.md`. 60 pages.

**The item shrank from three tags to two.** `REMOVE:` registers one subtoken,
`REMOVE:FEAT`, and both it and its parent `RemoveLst` sit in
`plugin/lsttokens/deprecated/`. The subtoken reports that feat-based tokens are
deprecated in favour of ability-based ones.

The feat-to-ability move gave `ADD:FEAT` a successor in `ADD:ABILITY` and left `REMOVE`
without one. There is no `REMOVE:ABILITY`. So the page teaches `AUTO` and `ADD`, and
`whats-changed.md` gains a section saying `REMOVE` has no current form. The backlog item
named three tags because the first-pass count did not check the package.

**Two measurement corrections.** A naive `ADD:[A-Za-z]+` scan reported `ADD:SKILLPOINTS`
194 times and `ADD:HITDIE` 18 times. Both are false — the matches come from inside
`DONOTADD:SKILLPOINTS`, a different tag. A `REMOVE:` scan reported 342 uses; the real
figure is 35, the rest being `.REMOVE.` inside `TYPE:` and `ALTTYPE:`.

Field-anchored counts, splitting lines on tabs and skipping comments: `AUTO:` 7,448
fields, `ADD:` 3,678, `REMOVE:` 35. Substring counting inflated two of the three.

**The facts worth the page.** A `PRExxx` in an `AUTO` must be the last argument, and
`.CLEAR` must be the first — each has its own hard failure. `%LIST` lets an `AUTO` grant
whatever a chooser on the same object selected. `ADD:ABILITY` takes an optional leading
count and the parser tells the forms apart by counting pipes. Nature must be `NORMAL` or
`VIRTUAL`; `AUTOMATIC` and `ANY` are rejected by name, which is the code stating the
division between the two tags.

## 2026-08-22  text the player reads

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog item 4.
- New page `lst/concepts/display-text.md`. 61 pages.

**The item was scoped wrong twice, in opposite directions.**

Too narrow: the backlog named `ASPECT`, `SAB`, `BENEFIT` and `NATURALATTACKS` and missed
`DESC`, which is written **100,395** times — more than the other four together, and second
only to `TYPE` in the whole data language. `DESC` appeared as an example on eighteen pages
and was explained on none of them, the same silent gap that put `TYPE` first.

Too wide: `NATURALATTACKS` is not display text. It grants natural weapons. It belongs with
race and template content and was dropped from this page.

**The fact that made it one page rather than four.** `BENEFIT`, `SAB` and `TEMPDESC` all
construct the same `Description` object as `DESC`. One placeholder grammar covers all
four: `%1` and `%{1}` for positional variables, `%%` for a literal percent, and the named
`%NAME`, `%CHOICE`, `%LIST` and `%FEAT=`. Documenting them separately would have produced
four copies of one grammar, which is what `WIKI-SCHEMA.md` exists to stop.

**Two failures that are not errors.** A `%` with no digits after it is read as an
unescaped literal, so the text renders wrong and nothing is logged. And `AspectName` is a
case-insensitive map built on demand, so a misspelt aspect name is not rejected — it
creates a second aspect nothing reads, and the sheet shows a blank. Shipped data carries
**226 distinct aspect names** and the code registers none of them.

Field-anchored counts: `DESC` 100,395, `ASPECT` 11,774, `SAB` 11,297, `BENEFIT` 5,438,
`TEMPDESC` 1,035. The backlog's 11,861 and 11,508 were close but counted substrings.

**Ownership.** Added aspect names not being validated to the schema table and to `OWNED`,
tested against two strings it must catch and one it must not.

## 2026-08-22  real failure messages

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog item 5.
- No new page. `start/when-it-breaks.md` rewritten in place, as the reviewer argued.

**The named source did not hold what the item claimed.** The backlog pointed at
"deliberately broken sets in `data/zen_test/pcgen_broken_tests/`". That path does not
exist; the directory is one level down, under `pcgen_test_advanced/`. What it holds is
five files, most of them commented out, covering two narrow cases — a `SPELLS:` with an
invented `TIMEUNIT`, and a `SPELLKNOWN:` naming a fake qualifier. It is not a corpus of
beginner mistakes.

The `error.txt` files shipped under `data/35e/` are not PCGen output either. They are
`prettylst.pl` reports from 2008, a third-party Perl tool. Quoting them would have taught
messages PCGen never prints.

**Where the real messages are.** `LstUtils` and `LanguageBundle.properties`. The symptom
table now carries the text the loader actually writes, so a reader can search for it:
`Invalid Token - does not contain a colon`, `Invalid Token - starts with a colon`,
`Error parsing file <file> line <n>`, and the deprecation template.

**The addition that matters most.** Three failures skip the line and let the load finish,
so the run looks clean: `.COPY skipped`, `.MOD skipped`, and the duplicate-object warning.
The first two are load-order problems, not spelling ones — the object has to exist before
the line that changes it runs. Linked out to `sources.md` and `keys-and-names.md` rather
than restating either, since `keys-and-names.md` owns duplicate resolution.

**Two repairs made on the way.** The page pointed at
`load-pipeline.md#verifying-a-dataset-loads`, but `testing.md` owns the harness; the link
now goes to the owner. And the citation to `LanguageBundle.properties` failed
`lint_wiki.py` because the sparse clone stopped at `code/src/java`. Widened it with
`git sparse-checkout add code/src/resources` rather than dropping the citation.

## 2026-08-22  facets, past the concept

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog item 6.
- No new page. `internals/facets.md` extended, 885 words to 1,356.

A second facets page would have been the duplication `WIKI-SCHEMA.md` forbids, so the
three named gaps were filled in place.

**The fourteen bases are a tree, and one edge decides everything.**
`AbstractStorageFacet` stores; `AbstractDataFacet` extends it and adds the event
broadcast. A facet that does not extend `AbstractDataFacet` cannot be listened to. The
page now names all fourteen with what each holds, and calls out the pair most easily
confused: `AbstractSourcedListFacet` keeps a set of sources, `AbstractSingleSourceListFacet`
assumes one owner and replaces it. The first is what makes the shared-language behaviour
already on the page work.

**Event order is deterministic and documented in code, not in docs.** Listeners live in a
`TreeMap` keyed by an integer priority, so priorities fire ascending. Within one priority
they fire in registration order — the array is built by prepending and read back to
front, which cancels out.

Four registrations use a non-zero priority, and together they are the character model's
ordering rules: `NaturalEquipSetFacet` at 1, `BonusActiviationFacet` at 1000,
`MovementResultFacet` at 2000, `CalcBonusFacet` at 5000. Everything else defaults to zero
and therefore runs before all four. That is the fact a developer adding a listener needs
and could not get from the old page.

**Adding a facet is four steps.** Pick the base by how the value is held, implement
`copyContents` — the one abstract method, contract is a deep copy — register with Spring
so `FacetLibrary` does not fall back to reflection, then wire listeners by hand in
`FacetInitialization`.

## 2026-08-22  writing a character sheet

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog item 7.
- New page `outputsheets/writing-a-sheet.md`. 62 pages.

Only the author's half was missing. `internals/output-and-saving.md` already carried the
engine choice, the token contract and the registration paths, so the code side needed
nothing and the two halves did not need merging after all.

**The measurement that shaped the page.** Across all 27 shipped FreeMarker sheets:
6,988 `pcstring` calls, 1,531 `pcvar`/`pchasvar`, 878 `@loop`, 44 `pcboolean`, and
**zero direct reads of the data model**.

The first count of model use returned 39, all of them `checks`. Every one turned out to
be a `<@loop>` index variable named `checks` interpolated into a legacy token string, not
the model key of the same name. The real figure is zero.

So the honest advice is that FreeMarker is only the templating layer. The vocabulary is
still the 154 output tokens, and the 23 model keys are registered but have no working
example behind them and no sheet that would break if one changed.

**A claim I wrote and had to retract before committing.** The page said `pcvar` cannot
read a variable no `DEFINE` declared. Wrong: `PCVarFunction` calls
`getVariableValue(formula, "")`, the formula path, which is why `COUNT[CLASSES]-1` works
at all.

The real trap is the reverse and sharper. `pchasvar` calls `hasVariable`, which is
`variableFacet.contains(VariableKey.valueOf(name))` — true only for a declared variable,
and false for a built-in. So guarding a block with `pchasvar` can hide a value `pcvar`
would have printed. Checking the class before committing turned a wrong sentence into the
page's best gotcha.

## 2026-08-22  equipment modifier files

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog item 8.
- New page `lst/files/equipment-modifier.md`. 63 pages.

One page covers both halves — the `EQMOD` tag that attaches a modifier and the file that
defines one — because neither is usable without the other.

**Count corrected again.** The backlog said 12,086 uses. That was raw substring matching.
Field-anchored, splitting on tabs and skipping comments, it is **9,628**. Three of the
eight items written so far had an inflated count in the backlog, all from the same cause.

**Two separators, two meanings.** In `EQMOD`, dots separate modifiers and pipes separate
one modifier's arguments. `EQMOD:MWORKW.PLUS1W` is two modifiers;
`EQMOD:SPL_CHRG|SPELLNAME[...]...` is one with bracketed values.

**The `=` to `|` conversion.** `EqmodToken` stores each choice as
`addChoice(token.replace('=', '|'))`. The field separator is already `|`, so data cannot
write one, and `=` is how the value gets through. Worth stating plainly because nothing
in the tag's own syntax hints at it.

**Two keys that are not modifiers.** `_WEIGHTADD` and `_DAMAGE` are read by the tag and
never resolved as references. `EQMOD:NONE` is deprecated and ignored.

**A naming detail worth having.** `NAMEOPT` decides what a modified item is called —
`NORMAL`, `NOLIST`, `NONAME`, `SPELL` or literal `TEXT=`. It is the answer to a modified
item reading badly on a sheet, and it had no mention anywhere in the handbook.

Some shipped data uses modifier keys containing spaces, such as `Material ~ Adamantine`.
Legal. A key containing a dot would not be, since dots separate modifiers.

## 2026-08-22  how a chooser resolves

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog item 9.
- New page `internals/choosers.md`. 64 pages. `lst/concepts/choosers.md` keeps the tag.

**The grammar has two operators, and they are not obvious.** `getChoiceSet` splits on `|`
first, then splits each part on `,`. Pipes are alternatives, commas are intersections. So
`SKILL|TYPE=Knowledge,TYPE=Int` is one alternative requiring both types, not two
alternatives. Both splits respect `[]` and `()` grouping, so a bracketed argument may
contain either separator.

**Resolution order is fixed.** Each term is offered to the qualifier factory first, and to
the primitive factory only if that returns null. A term matching neither logs `Choice
argument was not valid` and the entire set returns nothing rather than degrading.

**The two contracts differ in one telling way.** `PrimitiveToken.initialize` takes a class
and a value. `QualifierToken.initialize` also takes a `SelectionCreator` and a `negated`
flag. A primitive narrows by a property of the object. A qualifier narrows by the
character's relationship to it, and has to know whether it was inverted.

Counted: 21 primitives across 10 target types, 19 qualifiers across 13. Spells carry nine
primitives, more than any other target. Skills carry five qualifiers.

This also closes the loop on the `!TYPE` asymmetry recorded when the types page was
written. The chooser path wraps a negated group in a `NegatingPrimitive`; the ordinary
reference path rejects the same text. The types page owns that fact and this page links
to it rather than restating it.
