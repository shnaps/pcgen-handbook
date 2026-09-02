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

## 2026-08-22  granting spells, and tab binding

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog items 10 and 11.
- New page `lst/concepts/granting-spells.md`. Section added to `internals/ui-layer.md`.
  65 pages.

### Granting spells

Field-anchored counts: `SPELLS` 10,562 total, `SPELLKNOWN` 5,431, `SPELLLEVEL` 2,628
(1,651 `CLASS`, 977 `DOMAIN`). The backlog's 8,422 and 5,450 were close on the second and
low on the first.

**The same tag name has two grammars.** 2,340 of the `SPELLS` uses are the kit form,
`SPELLS:SPELLBOOK=Prepared Spells|CLASS=...`, parsed by
`plugin/lsttokens/kit/spells/SpellsToken.java`. The other 8,222 are the ordinary form
parsed by `SpellsLst`, where the book is positional and comes first. Copying a line
between the two does not work, and nothing in the tag name says so.

**Options are positional in a way that fails quietly.** `SpellsLst` reads `TIMES=`,
`TIMEUNIT=` and `CASTERLEVEL=` in a loop and breaks at the first argument that is not
one. Everything after the break is a spell name. An option written after a spell is
therefore read as a spell, fails to resolve, and the option is silently absent.

`domain.md` already owns `SPELLLEVEL:DOMAIN`, so the new page names it and links rather
than repeating the example.

### Tab binding

Kept to a section, as the second cross-review settled. `CharacterInfoTab` is four
methods, and the three model methods are a lifecycle rather than accessors — create once
per character, restore to attach and listen, store to detach.

**The restore order is measured, not fixed.** `InfoTabbedPane` restores the visible tab
directly, then queues the rest on a single-thread executor through a `PriorityQueue`
whose comparator reads a timing map of how long each tab took last time. Fast tabs go
first, and a tab never restored sorts ahead of one with a recorded time. So the cost of a
slow tab is paid while the reader is looking at something else.

That is also the constraint on adding a tab: expensive work belongs in `restoreModels`,
where it is timed and feeds the ordering, and no character state may live in the tab's
own fields.

## 2026-08-22  kits, data set layout, and the end of the ranked list

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Backlog items 12 and 13.
- New page `lst/files/kit.md`. Layout section merged into `lst/concepts/sources.md`.
  66 pages. **All thirteen ranked items are done.**

### Kits

Bigger than the reviewers' demotion implied on the data side: **6,922 `STARTPACK` lines
across 309 files**, and the owned lines run to 18,574 `SKILL`, 13,080 `ABILITY` and 8,793
`GEAR`. The demotion still stands on its own reasoning, which was reader need rather than
size, and the reviewers were right that the bulk is generated monster variants.

**The structural fact is that a kit file is not one line per object.** `STARTPACK` opens a
kit and every following line belongs to it until the next `STARTPACK`. A line put in the
wrong place joins the kit above it and stays valid, so nothing warns.

`APPLY` was worth checking rather than guessing. `PERMANENT` records the kit on the
character and refuses a second application. `INSTANT` is not saved with the character and
may be applied repeatedly.

### Data set layout

**The convention is thinner than the backlog claimed.** It called for "the `_` and `__`
prefix convention" as though it were a system. Shipped data has four files using it —
`__stats.lst`, `__align.lst`, `__saves.lst`, `__size.lst` — and three top-level
directories, `_universal`, `_images` and `publisher_logos`. Nothing in the loader treats
any of them specially.

So the section says what is true: `data/<system>/<publisher>/<product>/`, twenty-three
top-level directories, 34 publishers under `35e` alone, and most `.pcc` files four or five
levels deep. The underscore is a sorting hint, not a mechanism, and the page says so
rather than implying a rule.

Merged into `sources.md`, which already owned discovery and load order, as the
cross-review decided.

### The ranked list is finished

Nine items became pages. Four were folded into pages that already owned the ground —
`when-it-breaks.md`, `facets.md`, `ui-layer.md` and `sources.md`. That ratio is worth
noting: a third of a backlog written as "pages to add" was better served by extending
what existed.

Six of the thirteen carried a wrong number or a wrong scope, all caught by measuring
before writing rather than by review afterwards.

## 2026-08-22  three-reviewer verification pass

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages.
- Three reviewers on disjoint scopes: an accuracy audit of the nine new data pages, a
  fresh internals gap pass, and a new lens — an engineer who attempts real changes using
  only the handbook.

**The new lens found what the other two structurally could not.** It did not read pages.
It tried to add an LST tag, an output token and a facet, and recorded where the docs
stopped being enough. All three attempts failed, and two of the failures were in text
written earlier the same day.

Its own summary is the finding worth keeping: an accurate page leaves the reader looking,
a wrong one leaves them confident and wrong. Accuracy review cannot catch it, because
each sentence was defensible about `AbstractStorageFacet` in isolation. Only running the
task exposed it.

### Corrected

- `facets.md` told the reader to implement `copyContents`. All four recommended bases
  already implement it. It also sent wiring to `FacetInitialization`, which holds 42
  listener calls while **109** facets self-wire in `init()` under Spring's
  `default-init-method`. Rewritten as a worked example with the bean declaration and
  `OutputDB.register`.
- `adding-a-tag.md` carried an example that does not compile — `put` with an `ObjectKey`,
  read back with `getString`, which takes a `StringKey`. The key also had to be declared
  and the page never said so. Its test section described three assertions when real tests
  write none and override hooks instead.
- `adding-a-tag.md` routed game mode tags and `BONUS:` subtypes to a contract covering
  neither. Added a three-contracts table: `GameModeLstToken` through `TokenStore`,
  `BonusObj` through `Bonus`.
- **`display-text.md` taught a syntax that does not exist.** `%NAME`, `%CHOICE`, `%LIST`
  and `%FEAT=` are values in the pipe-separated variable list, not placeholders in the
  text. `Description.java` recognises only `%{`, `%%` and digits inside the text. Of the
  135 shipped `DESC` fields using `%CHOICE`, none puts it in the text. Table rewritten.
- **`types.md` listed two unwritable forms.** Only `.CLEAR` takes a leading dot, because
  it is stripped before `checkForIllegalSeparator` runs. `TYPE:.ADD.Weapon` fails. The
  token test parses `ADD.TestWP2` and `REMOVE.TestWP1` without one.
- `granting.md` said eight current `ADD` subtokens. Eight classes register seven distinct
  current names, plus deprecated `FEAT` and `VFEAT`. The prompt title also prepends the
  nature only when it is not `NORMAL`.
- `kit.md` said twelve line kinds. `KitLoader` registers 21 under 20 names.
- Counts restated under one scope: `TYPE` 196,931, `DESC` 99,993, `SPELLS` 8,206 ordinary
  against 2,356 kit. `DESC` is fifth-most-used, not second.

### The method fix

Five of the numeral errors came from two causes: substring counting, and mixing `.lst`
with `.pcc`. `WIKI-SCHEMA.md` now pins the counting scope — `data/**/*.lst`, skip comment
lines, split on tabs, test `startswith`, never substrings. No tool validates a number, so
the written method is the only guard.

### Still open

The largest finding is not yet acted on. `formula-system.md` is 730 words about
PCGen-Formula and contains **zero** mentions of JEP, PJEP, `jepcommands` or `core/term`,
while `overview.md:170` points at it for JEP. Every `DEFINE:X|0` and `BONUS:VAR` — 37,077
and 83,023 uses — evaluates through PJEP. `core/term` is 129 classes declaring 80 PC
terms and 15 EQ terms, the vocabulary `writing-a-sheet.md` already uses and nothing
defines. Verified, ranked first, and queued.

### Cross-review round

All three reviewers verified my fixes and two of them found errors *in the fixes*.

**The counting method I pinned was itself wrong.** It said split on tabs and test
`startswith`. It did not say strip. `LstUtils.processToken` calls `tok.trim()` before
dispatch, so a field with a leading space loads normally, and **196 tag fields in shipped
data have one**. Skipping the strip drops real tags and makes the handbook's counts
disagree with the loader they describe.

That moved three published figures: `DESC` 99,993 to **99,997**, `AUTO:` 7,448 to
**7,449**, `AUTO:SHIELDPROF` 148 to **149**. `DEFINE:` also restated as 37,178 with 37,076
at `|0`, dropping the one `.pcc` use that the old mixed scope had included. The schema now
carries the strip and the reason for it.

**My corrected test snippet did not compile.** Fixing the test section, I pasted a real
test verbatim — an integer-token test on `Race` — into a page whose running example is a
string tag on `Skill`. `AbstractIntegerTokenTestCase` declares four abstract methods the
snippet omitted. Replaced with `AbstractStringTokenTestCase`, which asks for
`getStringKey` and `isClearLegal`, and added what `getConsolidationRule` means:
`OVERWRITE` keeps the second occurrence, `SEPARATE` keeps both.

**My kit correction was wrong in the other direction.** `KitLoader` registers 21 line
kinds under 21 distinct names, sharing 18 classes. I had written 20 names. The reviewer
that supplied the original figure caught its own error.

**The facet example was missing the part that does the work.** Six steps of wiring and no
`dataAdded` or `dataRemoved`. Added both, plus the constraint that `OutputDB.register`
overloads take an `ItemFacet` or a `SetFacet` and a list facet cannot be registered.

**The output token path is now complete.** `AbstractExportToken` is the real base and was
named on no page — it implements `getToken` and hands over a `CharacterDisplay` rather
than a `PlayerCharacter`. `Token` was also called an interface in a table when it is an
abstract class. And output token tests live in `code/src/slowtest/`, which `testing.md`
never said.

**Ownership settled for `OutputDB.register`.** It is a facet method called from a facet's
`init()`, so `facets.md` owns it. `writing-a-sheet.md` now links there instead of saying
keys are "registered" without saying by what.

On priority, the internals reviewer conceded sequence and held severity, which is the
right call: a wrong base class stops the compiler and costs thirty seconds, while a
misunderstood JEP term compiles, loads, and prints a wrong number. Cost of discovery
ranks these, not size of gap. JEP is next.

## 2026-08-23  JEP, the engine the data runs on

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Open item 1.
- `internals/formula-system.md` extended, 730 words to 1,269. No new page.

The page documented `PCGen-Formula` and called itself "the formula system". Almost every
formula in shipped data runs through the other engine, and `overview.md` pointed here for
it.

**Reforked rather than appended.** The old opening was Gradle subprojects, so adding JEP
underneath would have stapled two topics together. It now opens on the fork and hands the
question of which tag reaches which engine to `rules-engine.md`, which owns it. The
existing material became `## PCGen-Formula, the newer engine` with its sections demoted a
level.

**What went in, and what deliberately did not.** The fourteen `plugin/jepcommands/`
functions are listed — a closed set, plugin-registered, and the answer to "what can I
write". A fifteenth, `cl`, is added directly in `PJEP` and never appears in that package.

The 95 terms are not listed. `TermEvaluatorBuilderPCVar` declares 80 and
`TermEvaluatorBuilderEQVar` 15, both enums. The page gives the mechanism instead:
`EvaluatorFactory` concatenates every constant's regex into one alternation and matches
incoming names against it. `COMPLETE_PC_ACCHECK` declares `AC{1,2}HECK` and answers to
both `ACCHECK` and `ACHECK`, which shows why a table of names would be lossy anyway. A
95-row table is transcription, rejected on the same ground as the 150 tag pages.

**The fact that earns the section.** A name that matches no term is not an error. It falls
through and is treated as a variable — the same path a `DEFINE`-declared name takes. So a
misspelt term quietly becomes an undeclared variable and reads as zero. That is why this
gap ranked above defects that stop the compiler: a wrong base class costs thirty seconds,
and this prints a wrong number on a character sheet.

**For a code changer:** a function is a `PCGenCommand` in `plugin/jepcommands/`; a term is
an enum constant plus a `TermEvaluator` class in `pcgen/core/term/`, which is 129 classes.
Neither package has tests, and the page says so.

## 2026-08-23  the last three open items

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Open items 2, 3 and 4.
- No new pages. Three extensions and two corrections to `BACKLOG.md` itself.

**Where facades are implemented.** `ui-layer.md` named the 33 interfaces and counted
`gui2/facade` in its leak table without ever saying it is the package you edit. Two
sentences: 30 classes, `CharacterFacadeImpl` alone 4,097 lines, interface in
`pcgen/facade/core/` and implementation there.

**The converter.** `adding-a-tag.md` said deprecation means moving the class to
`deprecated/` and stopped. That marks the tag and helps nobody whose data already uses it.
`plugin/converter/` holds 28 `TokenProcessorPlugin` classes that rewrite old data, each
naming the object type and the tag it handles, run by `PCGenDataConvert.main`. Neither
package has tests, and the section says so, along with when not to bother: a deprecation
whose fix needs a human decision does not get a plugin.

**The row that hid two dispatchers.** `load-pipeline.md` labelled all 653
`plugin/lsttokens` files "data and game mode tags" in one row. Split to 496 and 157.

I guessed 533 and 120 for that split from an earlier partial count, then measured before
committing: 66 classes at the top of the game mode tree and the rest across eleven
subdirectories, `codecontrol` largest at 43. The guess would have passed every check.
Third time this week that a plausible number came out of memory rather than measurement,
which is the habit `WIKI-SCHEMA.md` now exists to break.

**Corrections to the backlog's own sources table.** `data/zen_test/` is 47 files, and the
row now says what the broken subset actually is rather than promising a corpus.
`docs/listfilepages/lstfileclass/` is marked task-ordering only, because `FEAT:` appears
in 9 of its 25 lessons and `VFEAT` in 6 against `ABILITY:` in 6. Mining it for syntax
would import the exact drift this handbook exists to correct.

**Nothing is open.** Thirteen ranked items and four verification items, all done.

## 2026-08-23  auditing the previous day's edits

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages.
- Two reviewers on disjoint files, then a cross-reviewer sent to attack the contested
  mechanism claims. Eight errors confirmed, one reviewer finding refuted.

The 2026-08-23 edits had never been reviewed. The three-reviewer pass the day before ran
against the pages written on 2026-08-22 and found eleven errors, so the untested batch was
the obvious place to look.

**`formula-system.md`, five errors.** The function table listed `PCLEVEL`, which is not a
JEP function — it is the default first argument of `CHARBONUSTO`, the function the table
omitted. The count of fourteen was right and the membership was not. `PJEP` was credited
with three things it adds; it adds one. The vocabulary is `EvaluatorFactory`'s and the
result cache is `VariableProcessor`'s, and `PJEP` only reports whether a result may be
cached. "There are no tests for either package" was false: five command tests and three
term tests sit in `code/src/slowtest/`, not `code/src/test/`, which is where I looked.
`cl` was presented as a live fifteenth function; it is `@Deprecated` and logs a warning.

**The mechanism was backwards.** The page said an unmatched name falls through and is
treated as a variable, taking the same path a `DEFINE`-declared name takes. The order is
the reverse — `lookupVariable` tries declared variables first, then terms, then export
tokens — and there is no fall-through. All three miss, it returns null, and the JEP pass
abandons the whole value. The zero comes from the old fallback parser, where
`Float.parseFloat` throws into an empty catch.

That correction made the fact sharper, not weaker. The consequence depends on the rest of
the value: in plain arithmetic the bad name alone reads as zero, and in anything with a
function, a comparison or nested parentheses the fallback parser fails too and the whole
value collapses. Both are silent.

**`BONUS:VAR` was 83,023 and is 81,422.** Measured by the method pinned in
`WIKI-SCHEMA.md`. I could not reproduce 83,023 by any variant — counting commented-out
lines gets to 82,929, which is the closest wrong answer available. The figure was in
`BACKLOG.md` twice as well, and `MODIFY` at "a count in the low thousands" is 1,845, so
the page now gives the number.

**One reviewer finding was refuted.** The `DEFINE` figure was reported as wrong, 37,178
against the page's 37,076. Re-measuring showed both are right and they count different
things: 37,178 `DEFINE:` fields in total, 37,076 of them the `|0` form, which is what the
sentence claims. `declaring-variables.md` already carried both numbers correctly. The
backlog carried them each one too high and is now fixed.

**`adding-a-tag.md`, two errors.** "None of them has a `parseNonEmptyToken`" was true of
`plugin/bonustokens/` and false of the game mode tree, where 33 of 157 classes declare
one. "Neither package has tests" was false for `plugin/converter`, which
`PluginBuildTest` covers — as a packaging check that the jar exists, not as behaviour, so
the page now says which. The quoted interface dropped `public` from both methods and is
now exact.

**`ui-layer.md`, one error.** "The interface goes in `pcgen/facade/core/`, the
implementation here" is too strong: `Ability`, `Equipment`, `DataSet` and `Spell` in
`pcgen/core/` implement their facade interfaces directly. It also contradicted the
paragraph three lines above it, which says the separation was not maintained. A page
disagreeing with itself within one screen is the clearest sign the second passage was
written without reading the first.

**`load-pipeline.md`, one label.** The row read `plugin/lsttokens` 496, which is the tree
minus `gamemode`. Top level alone is 57. The label now says "less `gamemode`".

## 2026-08-23  the code expert's survey, and what the other two did to it

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages.
- A third reviewer seat, running against the Java tree rather than against the handbook.
  Its findings then went to the two reviewers who had just audited the pages, for a
  usability verdict. Two of four proposals were conceded.

The backlog was empty, so the question was what to survey next. The previous survey ran
from the source's seat — subsystem size, churn, test counts. This one asked a code expert
a narrower question: which parts of the codebase would a developer need documented. Same
rules as the other reviewers, and the same authority to say a published page should go.

**Four proposals came back. Two survived.**

The one that survived intact is the FreeMarker property vocabulary — what may follow the
dot in `<#list pc.skills as skill>`. `output-and-saving.md` opens the engine and stops
before the property list. The reviewer who audited the formula pages sharpened it: the
fact worth writing is not the list of six keys but the pairing of a fixed set with an open
one that data grows by itself, and the collision behaviour when a `FACTSET` name shadows a
built-in key. It is dropped with an error print rather than merged. I verified that at
`FactSetDefinition.java:70-73` before accepting it.

**Solver View changed homes on a scoping fact.** The survey wanted two sentences in
`formula-system.md`. The reviewer who had just spent an audit inside that page refused:
`SolverViewFrame` imports only `pcgen.base.formula.*` and `pcgen.base.solver.ProcessStep`,
so the debugger inspects the newer engine and can say nothing about a `DEFINE:` or
`BONUS:VAR` value. On a page that now opens by separating two engines, that mention would
teach the opposite of what the page is for. The survey conceded in three sentences.

That is the argument working the way it is supposed to. Neither reviewer could have
reached it alone — one knew the tool existed, the other knew what the page had just become.

**The page proposed for deletion survives.** The survey wanted `architecture.md` cut, on
the claim that four of its five tables are re-owned elsewhere. The second reviewer checked
table by table and found one. The repository-directory table is not the Java package
table. `building.md` has no Gradle-file table at all to duplicate. I checked both myself
before ruling, because a deletion is the only irreversible thing on the list, and it would
have broken eight inbound references and retired a published URL.

The survey conceded and named what should go instead: the Tests table, which restated
`testing.md` row for row, and the two-row `pcgen.*`/`plugin.*` table that `overview.md`
owns. Both removed. The page kept the three passages the cut would have destroyed — that
`docs/` has no build step, the `AGENTS.md` note, and that the test root is `code/src/test`
and not `utest`.

**A 6,292-line package became one line.** `pcgen/gui2/util` holds the hand-rolled tree
table every tab renders through, and `JTreeTable.java` is the fifth most-touched Java file
since 2025. Both reviewers rejected it anyway. Churn there measures the two people
maintaining a widget, not reader demand, and nobody writing data ever opens it. The
survey's staleness framing was also backwards, which it conceded: `gui2` is not dying,
`gui3` is 54 classes against 241.

What went in is the useful residue — `ui-layer.md` now says tab tables render through
`JTreeTable` so a reader stops looking for a framework that was never there.

**Method note.** Every number in the survey was re-measured before it reached the backlog,
including the ones nobody disputed. Two of the reviewers' own claims did not survive that:
one in this round, one in the audit earlier the same day.

## 2026-08-23  writing the two survey items

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages.
- Two sections, one pointer line each, on pages that already owned the ground.

**The property vocabulary.** `output-and-saving.md` now covers what may follow the dot on
an object, which is the gap a sheet author hits immediately after the top-level keys.

The survey and the reviewer both said six fixed keys. Measuring
`CDOMWrapperInfoFacet.initialize` while writing gave **nine**: `key`, `displayname`,
`type`, `source`, `info` and `visibleto` on `CDOMObject`, `desc` and `benefit` on
`PObject`, and `outputname` on seventeen concrete classes. The reviewer had cited a line
range that stopped three lines short. That is the fourth number this week that was right
in shape and wrong in value, and the only reason it did not ship is that the rule says
measure before writing, not after reviewing.

Writing it also turned up two facts nobody had. `getActor` walks up the superclass chain
and stops at `Object`, which explains the asymmetry — `outputname` registered seventeen
times, `key` once. And `CDOMObjectModel.proc` throws a `TemplateModelException` naming the
type and the key when nothing is registered.

**That last one is the fact the section is built around.** A sheet touches three
vocabularies and they fail three different ways. A missing output token substitutes an
empty string. An unknown JEP name reads as zero. An unregistered property stops the export
and says what was wrong. Three subsystems, three answers to the same mistake, and only one
of them tells the truth. The page says so.

**Solver View.** `variables-and-formulas.md` now has the procedure, with the menu path and
Ctrl-F11, because a tool nobody can find is not documented. The section gives the five
columns — Modification Type, Modification, Resulting Value, Priority, Source — since
reading Resulting Value down the table is the technique. It answers which modifier made
the number wrong rather than what the number is.

It closes with what it cannot do. A `DEFINE`-declared variable fed by `BONUS:VAR` never
appears, because the debugger reads the newer engine only. Pairing the tool with its blind
spot is the point: the engine 99.7% of shipped data runs on has no inspector at all.

`formula-system.md` carries one pointer line in its newer-engine half. The procedure is
not there, for the reason the cross-review established — that page is anatomy, and putting
a `MODIFY` debugger beside the JEP section would undo the separation the page opens with.

**Nothing is open.**

## 2026-08-23  auditing the sections written the same day

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages.
- Two auditors on disjoint files. **Thirteen errors**, twelve in work written hours
  earlier and one pre-existing. One auditor number was itself wrong and was re-measured.

Writing a section is not the same as knowing it is right. Both sections written this
morning went out unchecked, and the audit found more in them than the morning pass found
across four files.

**`FACT` does not reach a template on its own.** The worst error. `ContentDefinition.activate`
calls `activateOutput` only when the definition is visible to `VISIBLE_EXPORT`, and the
default with no visibility set is `HIDDEN`. So a fact that loads and works everywhere else
is absent from every template until it is made visible. The page had said loading the
definition was enough. It also named the wrong token — `FACTDEF:` defines a fact in a data
control file, `FACT:` is what an object then carries.

**The collision claim was backwards.** I wrote that a name collision refuses the second
registration and drops the fact. `set` calls `put` unconditionally and returns the old
value only as a report, so the new actor is in and the *earlier* property is the one lost.
The code logs `already exists, ignoring` and then does not ignore it. Worth documenting
precisely because the log says the opposite of what happened.

The scope was also wrong. The map is keyed by class, so a fact on `SKILL` named `key`
never fights the global `key` — `getActor` finds the `Skill` entry before it walks up.
Only a global fact, or one shadowing `outputname` or `type` on a class that has them,
collides at all.

**A reason that sounded good and was not.** I had explained the seventeen `outputname`
registrations by the superclass walk. The walk explains why `key` needs one registration —
it argues *against* repeating `outputname`, which is an `OutputActor<CDOMObject>` and would
work registered once. The seventeen are a whitelist. Reasoning that flatters the mechanism
is the kind that survives review, which is why it needed catching.

**71, not 42.** `pcgen/output/` has seven subpackages. I counted the five I had named and
wrote the total as though it were the package. `model` alone is 20 classes, and
`CDOMObjectModel` — cited three lines above the count — lives in it.

**The contrast that anchored the section was half wrong.** I wrote that a missing output
token substitutes an empty string. The default branch writes the token's own text back
verbatim, and through `pcstring` that echo raises `Invalid export tag`. That error was
pre-existing, in `writing-a-sheet.md`, and had been on the site since the page was
written. Fixed there too, along with the loop bullet that leaned on it.

**Solver View: the shortcut does not exist.** The page said Ctrl-F11. `SolverViewAction`
passes the string `"Ctrl-F11"`, `PCGenAction` tokenises on whitespace and accepts only
`shortcut`, `alt`, `shift-shortcut` or a bare F-key, and one token matching none of them
falls through to `KeyStroke.getKeyStroke`, which returns null. `ACCELERATOR_KEY` is never
set. No key opens that window. The menu label was wrong too — it reads **View Solver
Process**, not Solver View.

That one is now on `formula-system.md` as a fact in its own right. A shortcut declared in
source that silently never registers is worth a reader's attention.

**And the tool has four controls, not two.** Character, scope, object, name. The object is
required for any non-global scope, and leaving it unset empties the table. A name matching
nothing does not clear the table at all — it logs where nobody looks and leaves the
previous variable's rows on screen, which is how you read the wrong answer confidently.
The Priority column is the solver's composite ordering key, not the `PRIORITY` you set.

**An auditor was wrong once.** `architecture.md` was corrected to say six Gradle test
tasks. `testing.md` names five and `build.gradle` registers ten, so the sentence now gives
no count and points at the page that owns the list. `inttest` was missing from that list
and has been added.

**Method.** Every number in both audits was re-measured before use. That caught one
auditor error — a non-recursive count reported as recursive — and confirmed the rest.

## 2026-08-23  checking my own corrections

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Two fixes to the fixes.

The corrections written after the audit were themselves unverified prose, which is the
trap the audit had just demonstrated. Re-measuring them found two.

**`JTreeTable` references.** I wrote "twelve files mention it, six by import". Twelve is
the total across all source roots and it counts `JTreeTable.java` itself, so it flatters
the number. Eleven other files reference it, two of them tests. The `gui2/tabs` split —
61 across subpackages, 21 directly in the folder — was right.

**`outputname`.** Left as "the name after output formatting", which says nothing a reader
can act on. It is the `OUTPUTNAME` tag with `[BASE]` and `[NAME]` expanded, falling back
to the display name when the tag is absent.

Two rounds of correction on one section is the cost of writing before measuring. The
sequence today was: write, audit, fix, audit the fix. Only the last step was cheap.

## 2026-08-23  auditing day one, which nobody had ever checked

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages.
- Four reviewers on disjoint sets, 25 pages written 2026-08-21. **Thirty-four errors.**
  One page came back clean.

The audits so far had all covered recent work. The 25 pages from the first day had never
been checked against the source — `log.md:801-804` records the verification pass as
covering "the nine new data pages", and the earlier whole-wiki read at `:300` was a
structural review whose output was the backlog. So the foundation was the only unexamined
material left, and it is the part a newcomer reads first.

**The worst error was an instruction to fix something that is not broken.**
`first-change.md` told the reader to find the `ABILITY:` line in the shipped template,
which "will be commented out, like most lines", and remove the `#`. That line is live.
So are the twenty other file tags around it. The claim traces to a 2005 readme still
shipped as `how_to_use_this.txt`, which the handbook repeated without opening the file.
The page then blamed the same imaginary comment in its troubleshooting table, and
`how-loading-works.md` built a paragraph on it.

That is the failure this project exists to correct, reproduced inside it: a stale
upstream document copied instead of the code being read.

**And the deprecated form got in anyway.** `how-loading-works.md` used `FEAT:` in its
example PCC and explained it as how you name a feats file. `CampaignFeatToken` is in
`plugin/lsttokens/deprecated/`, no shipped `.pcc` uses `FEAT:` at all, and the previous
page in the same section warns against it. `DECISIONS.md` already records this exact tag
as the project's original cautionary tale.

**Three how-to errors would stop a reader's data working.** `MULT:YES` with no `CHOOSE`
throws on grant, and the finished example on the page had that shape. `SPELLLIST` does
not declare a class's own list — it picks from another class's and its argument must name
a class that exists, so the caster example pointed at nothing. `PROFICIENCY:ARMOR|Medium`
names no object, because armour profs are per item: `Padded`, `Hide`.

**The reference pages contradicted themselves.** `class.md` listed `DOMAIN` as deprecated
and then listed it as a current level tag eleven lines later. `race.md` documented `MOVE`
as replacing when it appends to a list with no clear, and gave `MONNONSKILLHD` as a race
tag when it is a `PCClass` token.

**Every count was wrong in the same direction.** Not one measured number came out lower
than published. `KEY` 71,500 to 74,678. `COST` 44,000 to 45,469. `DOMAINS` 2,100 to 4,587.
`PRESTAT` 4,100 to 3,338 — the exception, and the reason is instructive: that one had been
counted by substring, which double-counted nesting inside `PREMULT`. Rounded estimates
written before the method existed, and every one of them looked exactly like a measurement.

**The log levels were unusable.** `when-it-breaks.md` gave `LST_ERROR`, `LST_WARNING`,
`LST_INFO`. Those are Java constant identifiers. The log writes `LSTERROR`, `LSTWARN`,
`LSTINFO`, so a reader following the page would search their log and find nothing. It also
omitted `Illegal Token`, which is what a misspelt tag actually produces.

**One page was clean.** `line-format.md`. It is the most mechanical page in the handbook,
which is the only pattern visible in the results.

**Rate.** Thirty-four errors across 25 pages, against eleven across nine and thirteen
across two in earlier passes. Unaudited material runs at roughly one and a half errors per
page and does not improve on its own.

## 2026-08-23  closing what the audit left

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages.
- Three backlog items, one new check. Nothing is open.

**Telling people to keep their work where upgrades delete it.** `setup.md` said renaming
a folder under `data/` put it somewhere an upgrade could not touch. The Data Installer
says of that location that a set *"will be replaced when upgrading to a new version of
PCGen"*, and of the Homebrew Data directory that it *"will be available in the new
version if you upgrade"*. The handbook had never mentioned the second one on any page.

`CampaignFileLoader` walks the data, vendor and homebrew directories alike, so nothing
about a campaign depends on living under `data/`. The setup page now sends readers to
the Homebrew Data directory and `first-change.md` follows it there.

This is the worst class of error the handbook can make. A wrong tag fails loudly at load.
This one works perfectly until an upgrade, and then the reader's work is gone with no
message and nothing to debug.

**The SRD rule had no enforcement, so it was not being kept.** `tools/check_srd.py` now
scans fenced blocks and inline code against object names from the shipped RSRD data. It
found `Climb` used as a skill on six pages, `TYPE=Knowledge` on two, and `Sample
Toughness` — which reads as invented and is the SRD feat name with a word in front. Now
`Sample Athletics`, `TYPE=Lore` and `Sample Vigour`.

Three hits are documentation rather than examples: the `Dodge` bonus type, a real key
quoted to show keys may contain spaces, and an armour prof named to explain why a
category fails there. Those sit in an `ALLOWED` set keyed by page and name, each with
its reason, so the same word is still caught anywhere it is used as example content.

Building the check took three passes to tune. Scanning every shipped object name found
132,778 of them and matched generic words — `String`, `Nothing`, `Order`. Narrowing the
source to the RSRD tree and stoplisting size codes and armour categories got the noise to
zero without losing a real hit.

**The precision list, twelve entries.** `BOOKTYPE` is pipe-separated. `SKILLLIST` is
`count|lists`. `DONOTADD` accepts `HITDIE` and `SKILLPOINTS` and nothing else. `CLASSES`
takes class skill lists with `ALL` and `!`. `CATEGORY.` works alongside `CATEGORY=`. The
`*/` prefix is a search across three directories, not a location, and `&` and `$` name
the vendor and homebrew ones. Line endings may be any of the three styles, lines are not
continued, and the loader trims a field before looking for its colon.

**And one error introduced while fixing errors.** Extending the deprecation table, I
wrote that `CHOOSE:NUMBER` is deprecated "without a `MIN` and `MAX`". It is deprecated
outright and delegates to `TEMPVALUE`. Caught by reading `NumberToken.parseToken` before
committing, which is the only reason it is not in this repository. Fourth time today that
checking a claim I had just written found it wrong.

## 2026-08-23  the last 27 pages, and the lens that beat the auditors

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages.
- Five accuracy reviewers on disjoint sets, plus one building a data set from the
  handbook alone. **Ninety-one errors.** Not one page came back clean.

Every page has now had an accuracy pass except `credits.md`.

**The task lens found what five accuracy reviewers could not.** It was told to author a
race, an ability, a class, a skill and a `.pcc` using only the handbook, and forbidden to
read the source except to check afterwards whether what it had been told was true.

Its worst finding is the worst error the handbook has carried. `new-class.md` taught
writing an attack progression down successive level lines as `1`, `2`, `3`.
`ClassLevelChangeFacet.update` adds every `PCClassLevel` from 1 to N, so all those lines
are live at once and untyped bonuses stack. That example gives a third-level character an
attack bonus of six. Five reviewers read that page today. None caught it, because every
sentence in it is defensible alone — the error only appears when you build the thing and
add up the result.

Its verdict on the whole handbook was no: a homebrew set built from these pages does not
work, because no page says a data set is not self-contained. It needs the `_universal`
`DATACONTROL` and `RACE` lines every shipped 35e PCC carries, and a base source for stats,
sizes and saves, since `statsandchecks.lst` in the game mode defines none of them.

**A correction made this morning was itself wrong.** I had changed `new-race.md` to say
`VIRTUAL` grants an ability without checking its own prerequisites. The task lens
contested it, the reviewer who made the original claim was sent the trace, and conceded:
neither nature checks the ability's own prerequisites, because only those written on the
`ABILITY:` tag are carried. The gate it had in mind is on `ADD:ABILITY`, between `NORMAL`
and `VIRTUAL` — a different tag and a different pair. The page lost the distinction
rather than keeping a real-sounding one that does not exist.

**The owner pages were the worst set, at 27.** `bonuses.md` had `.REPLACE` overriding the
plain bonus when replace bonuses stack among themselves and then the higher total wins.
`keys-and-names.md` had `[NAME]` as the first parenthesis when it is first `(` to last
`)`, split on `/` and reversed. `modifying-data.md` had an example using `BONUS:.CLEAR`,
which does not exist at all. `sources.md` had `RANK` inverted — descending sort on a
`YYYYMM` date loads the newest first, not the oldest — and restated one sentence of the
duplicate-key rule that `keys-and-names.md` owns, complete with a dangling reference to a
preference the page never introduces.

**Every count on those five pages was comment-inclusive**, and re-measuring moved all of
them: `BONUS:` 174,114 to 170,741, `KEY:` 71,572 to 74,678, `.MOD` 58,600 to 56,744.
`BONUS:WEAPON` turned out to outrank `SPELLCAST`, so a frequency table was in the wrong
order as well as wrong.

**And the data-location error had spread.** `setup.md` was fixed this morning.
`third-party-data.md` and `publish-a-source.md` were still sending readers to `data/`,
and `third-party-data.md` contradicted itself doing it — its own gotcha says editing
shipped data is temporary because updates overwrite it. Third-party data belongs in the
vendor directory, your own in homebrew, and the page now carries the table.

**Rate.** Ninety-one across 27 pages is 3.4 each, more than double the day-one rate of
1.4. The difference is what the pages are: these are the dense internals and owner pages,
where a paragraph makes six checkable claims rather than one.


## 2026-09-01  the grouping grammar, and the tag nobody documented

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages.
- Two sections. `plugin/grouping` was the only package under `code/src/java` that no page
  cited.

**What was missing.** `variables-and-formulas.md` described the `<grouping>` argument of
`MODIFYOTHER` as "which objects within that scope are affected" and stopped. A reader
could not write the line. The three forms are `ALL`, `KEY=` and `GROUP=`, one class each
in `plugin/grouping/`, and a bare name with no `=` means `KEY`, because `getDynamicGroup`
falls back to it for anything but the literal `ALL`.

`GROUP:` itself existed only as a row in the generated tag index. It is a second label
list on `CDOMObject`, pipe-separated where `TYPE:` is dot-separated, and exactly two
things in the source read it back.

**A sentence on the same page was wrong.** It said shipped data uses `MODIFYOTHER` with
movement modes as the grouping, "which is how movement gets adjusted across a set of
modes at once". Nothing in the data does that. All 192 fields name one mode by key, 189
of them `Walk`.

**Every number I first wrote was measured the wrong way.** A raw grep over `data/` and
`system/` gave 209 uses across three scopes. The pinned method — `.lst` only, skip `#`
lines, split on tabs, strip each field — gives **192**, all in `PC.MOVEMENT`. The
seventeen that vanished were commented out, including both `STAT` lines, which were the
only thing making the scope table look varied. Second time this project has taken a
comment-inclusive count into a draft.

**Two reviewers, five findings, all real.** The first killed a "what breaks" paragraph.
The messages `KEY must have value following =` and `GROUP must have value following =`
exist in the source and cannot be reached from LST text, because `GroupingInfoFactory`
rejects an instruction ending at `=` before the grouping class is ever built
(`GroupingInfoFactory.java:143-147`). It also found the omission that mattered: every
form accepts a bracketed child, `KEY=Walk[ALL]`, and a child yields the matched object's
children rather than the object.

The second found a count wrong by one and a description wrong outright. Thirteen call
sites read `isUnselected()`, not twelve, and they do not all ask about the character's
race. `SourceFileLoader.java:749-765` is the loader **requiring** the flag: a loaded set
of sources must contain a race carrying `GROUP:UNSELECTED`, and with the domain feature
on, exactly one deity. That is the most useful fact in the section and the first draft
walked past it.

It also caught the two race entries being named `<none selected>` with `KEY:None
Selected` rather than `None`, and the phrase "the second field of `MODIFYOTHER`" using
*field* for a pipe-separated argument. The glossary reserves that word for the
tab-separated parts of a line.


## 2026-09-01  three reviewers on one question: can an engineer change the source?

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. Two new pages,
  `running-and-debugging.md` and `changing-behaviour.md`. 68 pages.
- Three seats: the new contributor's onboarding path, a task lens doing three real
  engineering jobs from the pages alone, and a code expert on mechanisms that bite
  silently. **Two published errors**, both on pages that had already passed an accuracy
  audit.

**The task lens found the error, again.** `building.md` said `run` "depends on
`assemble`, then rewrites the JavaFX module path before launching. The build does that by
hand because Gradle's application plugin sets the wrong path." None of that is in
`build.gradle`. The `application` block is three lines setting the main class, the only
`JavaExec` configuration is `maxHeapSize`, and JavaFX arrives as a plain classpath
dependency read from `mods/lib`. The module-path rewriting the page described is on
`Test` tasks.

**A second error in `rules-engine.md`.** The skill trace named
`PCSkillTotalTermEvaluator.resolve` as "the entry point". It is constructed in exactly one
place, `TermEvaluatorBuilderPCVar.java:1370`, and serves the JEP term `SKILLTOTAL.`. The
sheet number comes from `SkillToken`, the GUI number from
`CharacterLevelsFacadeImpl.getSkillBreakdown`. The trace also showed four summands where
`SkillModifier.modifier` has three families: `SKILL` by five keys, then `CSKILL` or
`CCSKILL` by three, then the armour check penalty and the game mode's rank-mod formula.
The page now also says a breakpoint may not be needed, because
`SkillCostDisplay.getModifierExplanation` already prints that breakdown.

**The biggest gap was one nobody had asked about.** Two reviewers reached the same first
answer independently: nothing in `docs/` said how to attach a debugger. `--debug-jvm`
appeared nowhere. Neither did the fact that a token edit has no effect under
`./gradlew run` — `PluginClassLoader` reads class bytes out of `plugins/*plugins.jar`, and
only `jar` declares `dependsOn jarAllPlugins`.

**The code expert's five mechanisms all survived re-measurement**, which has not happened
before. `setDirty` at `PlayerCharacter.java:993` does five things past the save flag,
across 87 call sites and 23 `getSerial()` readers. `CControl` has 54 constants and 293
references, and `getBaseCheck` shows the dual path in one method: a set control reads a
variable, an unset one falls through to the cached hardcoded sum. So the two mechanisms
interlock, and section 2 of the new page can point at section 1.

I re-measured the UI numbers rather than copying them: 47 assertion calls across 26 files,
37 `invokeLater`, 31 `Platform.runLater`, 33 `runOnJavaFXThreadNow`. The reviewer said 27
files and 41 `invokeLater`. Close enough to look right, different enough to matter.

**One claim I could not verify by running it.** The build wants a JDK 25 toolchain and
this machine has none, so `./gradlew run --dry-run` could not resolve a task graph. That
`run` skips `jarAllPlugins` rests on the build files alone: only `jar` declares the
dependency, and the application plugin's `run` puts `build/classes` on the classpath
rather than the jar.

**And one number I invented mid-draft.** I wrote that a saving-throw fix would help "the
seventeen game modes that do not set `BASESAVE`". Nothing measured that. The page now says
every game mode that leaves it unset, which is what the code supports and the data page
already counts.


## 2026-09-01  the correction that was itself wrong

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. JDK 25 is installed now,
  so claims about the build can be run rather than read.
- Both open backlog items closed. One error introduced this morning, found and fixed.

**I broke a correct sentence.** `building.md` said `run` "depends on `assemble`, then
rewrites the JavaFX module path before launching. The build does that by hand because
Gradle's application plugin sets the wrong path." A reviewer reported that none of it was
in `build.gradle`. I checked `build.gradle`, agreed, and replaced the paragraph.

All three of us were reading one file. The configuration is in
`code/gradle/distribution.gradle:80-92`, and it does all three things: `dependsOn
assemble, extractJavaFXLocal`, a `doFirst` that assigns `jvmArgs` outright, and a comment
reading "Required to fixed incorrectly added --module-path". The original sentence was
right in full.

**The gotcha I built on it was wrong too.** I wrote that `./gradlew run` does not rebuild
the plugin jars. `./gradlew run --dry-run` prints the graph: `jarAllPlugins` → `jar` →
`assemble` → `run`. It rebuilds them every time. The true version is narrower and still
worth having — launching `pcgen.system.Main` from an IDE skips Gradle, so the jars on
disk are whatever was built last.

**What running it settled.** `./gradlew run --debug-jvm` prints `Listening for transport
dt_socket at address: 5005` and waits. So `--debug-jvm` survives the `doFirst` that
replaces `jvmArgs`, because Gradle adds the debug agent separately. The page now quotes
the line the reader will see rather than describing it.

**The lesson, and it is not a new one.** A reviewer citing `file:line` was trusted for the
*absence* of something. A citation proves presence. `build.gradle` not containing a `run`
block says nothing about whether the repository configures `run` elsewhere, and one
`grep -rn` across `code/gradle/` would have shown it. Every earlier version of this
mistake on this project has been a number; this one was a negative.

**Both backlog items closed.** `PropertyContext` namespacing went into `startup.md`: one
`options.ini`, every child context prefixing `name + '.'` at each hop up to the root, and
a mis-namespaced read returning the default with nothing logged. My measurements were 47
`initProperty` calls, 222 `PCGenSettings.` and 115 `ConfigurationSettings.`, against the
reviewer's 47, 164 and 100.

`facets.md` now opens its walkthrough by saying when a facet is the wrong answer. Derived
state is a facet. User-set state that has to survive a save is a code control channel.

**Then I ran the rest of the build claims.** `./gradlew build --dry-run` confirms the
quality-gate table exactly: five SpotBugs tasks in the graph, no Checkstyle and no PMD,
`test` but not `itest`, `slowtest`, `datatest` or `inttest`. Two things the graph shows
that the page did not say — `build` compiles the slow and integration tests without
running them, so a compile error there fails it, and it runs the `PCGen-base` and
`PCGen-Formula` unit tests too. Both added.

**One more number was loose.** `testing.md` said `code/src/test/plugin/lsttokens/` holds
"about 398 files, one per tag". 398 is every `.java` under that tree. The tag tests are
**363** `*Test.java` classes; the other 35 are shared bases, 31 of them in `testsupport/`.
`BACKLOG.md` had 363 all along, so the handbook disagreed with itself.


## 2026-09-01  two things about how the Java actually runs

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages. Sections in
  `cdom-model.md` and `ui-layer.md`, and a fifth trap on `changing-behaviour.md`.
- Both were found by asking what the runtime does rather than where the code lives.

**Every CDOM type breaks the `equals`/`hashCode` contract, in one of two ways.**
`PObject.equals` matches key names case-insensitively across any `PObject`, and the
matching `hashCode` is commented out in the source with a bug reference,
`COD#E-1895`.

`PCClass`, `Deity`, `Domain`, `PCTemplate`, `Campaign` and `Kit` override neither, so they
have value equality and identity hashing. `Skill`, `Spell`, `Ability`, `Equipment`,
`Language`, `ArmorProf`, `ShieldProf` and `WeaponProf` override both, and `Race` overrides
only `hashCode` — but every one of those returns `getKeyName().hashCode()`, which is
case-sensitive, against an `equals` that is not. `setKeyName` stores the string it is
handed, so nothing normalises the case away.

The engine avoids the problem rather than fixing it. `AbstractReferenceManufacturer` keys
objects by string in a `KeyMap` and tracks duplicates under a `CaseInsensitiveString`
wrapper. No CDOM object is ever a hash key.

**The interface does not listen to the model.** `facets.md` already documented the
facet-to-facet event graph and its priorities. The hop after that was undocumented, and it
turns out barely to exist: **six** `addDataFacetChangeListener` registrations reach the
interface layer, against **234** facet classes. `CharacterFacadeImpl` mirrors state into
33 `DefaultReferenceFacade` fields and keeps them current with thirteen refresh methods it
calls itself, from the same code path that made the change.

So engine code that mutates a facet directly leaves the widget showing the old value.
`ui-layer.md` already said the facade boundary leaks in the import direction. This is the
cost in the other direction, and it is the fifth entry on `changing-behaviour.md`.

Neither of these is a defect report. Both are things a developer has to know before their
correct fix appears to do nothing.


## 2026-09-01  eight experts on one question: can you change this thing?

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. One new page,
  `internals/design.md`. Seven new sections on existing pages. 69 pages.
- Eight subsystem experts, disjoint scopes, each told what the handbook already covers and
  asked only what it does not. **Forty findings, every one carrying a `file:line`.**

**The new page states the logic rather than the layout.** PCGen runs 20 game modes from
one binary, so a rule cannot be a field. `design.md` names the five patterns that follow
from that, what each buys and costs, and a sixth that explains most of the surprises: when
a hardcoded rule is replaced by a data-driven one, both implementations stay live and the
data picks. Code controls, two formula systems, `FACTDEF`, the deprecated package — all
one migration, unfinished.

It also carries the routing table nothing else had: eleven extension points, what to
implement, which package registers it, and where the test goes.

**Every page now ends with what bites.** The findings went to their owners rather than
into one page, so the loader traps sit on `load-pipeline.md` and the bonus traps on
`rules-engine.md`. `design.md` indexes them.

The seven that changed a page I would have written wrongly:

- `ParseResult.Fail` means "not my syntax", not "stop". `TokenSupport` tries every token
  registered for a name, and commit or rollback happens once per tag afterwards. A token
  that writes and then fails has its writes committed when a later one passes.
- Every bonus is cast to `int` unless its type starts with one of five prefixes or
  contains `DAMAGEMULT`. The cast carries a `// TODO: never used` comment, and the value
  is used twice below it.
- Stacking is decided by the game mode's `BONUSSTACKS` list, not by Java. Untyped,
  `.STACK`, `.REPLACE` and negative bonuses bypass the lookup entirely.
- `PlayerCharacter.clone()` copies state by iterating Spring's storage beans. A facet
  missing from `applicationContext.xml` still runs, via the reflection fallback, and is
  empty on every clone.
- Nothing evicts a character's facet storage. Facets are process singletons, so a listener
  you register and forget holds the `CharID` and leaks the whole character.
- An unknown output token is written to the sheet as literal text. No exception, no log.
- The character's `PCClass` is a clone and its levels are cloned again, and `PCClass.clone`
  re-owns bonuses on the *original* level map before substituting its own.

**Counts I re-measured rather than copied.** 47 assertion calls in 26 files, not 27.
`PCGenSettings.` 222, not 164. 363 token test classes, not "about 398 files". Three of
eight experts were off on a count while right on the mechanism, which is the same ratio
as every earlier round.

**One citation was wrong and lint caught it.** `BatchExporter` is in `pcgen/system/`, not
`pcgen/io/`. That is the check earning its place: I would not have noticed.


## 2026-09-01  the structural review, and the check it produced

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. One page split in two:
  `internals/save-format.md` is new. 70 pages.
- Three reviewers on the structure — the reader's seat, the maintainer's seat, and a code
  expert on whether the pages cut along the codebase's seams.

**They cross-agreed on one call, independently.** Both the maintenance seat and the code
expert said `output-and-saving.md` is two pages. The evidence they each found separately:
the save half has disjoint code (`PCGVer2Creator` and `PCGVer2Parser`, 242 KB between
them, against `ExportHandler` and `plugin/exporttokens`), and the page's own "what bites"
section had a *save* bite filed above the "The save format" heading. Split at that
heading. The export half keeps the path, so no published URL retires.

**I rejected the other cut.** The code expert wanted `plugin-loading.md` merged into
`token-system.md`, on the correct observation that registration and dispatch are one
package and one mechanism. But `plugin-loading.md` has 15 inbound links across 11 pages,
and the actual defect was the *copy* in `load-pipeline.md` §5, which restated five facts
`token-system.md` owns. Cutting the copy fixes it. Merging the owner costs 15 link
rewrites and a retired URL for nothing more. Written down so it is not proposed again.

**Three counts of one thing, all published.** `output-and-saving.md` said 140 export
classes with 49 deprecated in one place and "92 classes" in another; `design.md` said 56
plus 57 from a measurement that had silently included the deprecated package. Measured
once, properly: **140 total, 49 deprecated, 91 live**, and of the 91, **42 extend `Token`
directly and 22 extend `AbstractExportToken`**. So the sentence I wrote yesterday — "most
still extend `Token`" — was wrong twice over.

**The `234` had spread to five pages** and `54` to two. Both now name one owner and link.
Three rows went into the `WIKI-SCHEMA.md` owner table so the linter can grow into them.

**A silent breakage class, now a check.** Every cross-page heading link pointed into
numbered headings — `changing-behaviour.md#1-a-cached-number-…`. Insert a mechanism above
and all four inbound links break, and `mkdocs --strict` does not check fragments at all.
The digits are gone from those headings, and `lint_wiki.py` now validates all **44**
cross-page anchors against the target page's real headings. Tested by breaking one on
purpose before committing.

**The reader's seat found the navigation failure I could not see.** Seventeen loose
concept pages sat directly under "Data files", with `File types`, `How to` and the tag
index nested below them, so a data author scrolled past everything to reach "Add a feat".
The concepts are now a group, which makes the four peers peers. I did not take the
reviewer's reordering — putting `How to` first would have made the nav disagree with
`index.md`, and the grouping alone fixes the burial.

Also from that seat: `archetypes.md` sat fifth in the nav and fifteenth on the index,
`startup.md` was filed under "Getting oriented" rather than at the head of "Reading data",
the index blurb promised `DEFINE` on a page that does not cover it, and
`running-and-debugging.md` still said "four traps" after I made it five. All fixed.

**And a real drift, found by reading two pages against each other.** `pcc.md` said `PCC:`
merges a file list "into this one" and `LSTEXCLUDE:` skips entries. `sources.md` says the
include is recursive, appended to the end, and silent on failure, and that the exclusion
applies to the whole load. Two pages, one fact, one of them vague enough to mislead.
`sources.md` owns both now.


## 2026-09-01  auditing the day's own work

- upstream: PCGen @ `d262f8b44952860ff857132035fb32d8d11361fa`. No new pages. 70 pages.
- Four accuracy reviewers on disjoint sets, plus the task lens. Everything written today
  was in scope: four pages and eleven sections. **About thirty-five errors.**

**The clean sections are the tell.** Two came back with nothing:
`types.md`'s `GROUP:` section and `variables-and-formulas.md`'s grouping section. Those
are the two I wrote after reading every class myself. Everything written from an expert
report needed correcting. The reports were right about mechanisms and wrong about numbers,
which is exactly the split every earlier round found, and I carried the numbers across
without re-scoping them.

**Counts were the dominant failure, and the failure was scope.** "The file carries 87
`setDirty(` call sites" — 87 is the figure for `code/src/java`; the file has 59 lines, 52
of them live calls. The threading table's 37, 31 and 33 counted occurrences including
declarations and two javadoc `{@link}` references; the real call counts are 36, 29 and 32.
`GuiAssertions` has six checks, not four. `PropertyContext`'s "47 times" included the
three declarations, so 44.

I deleted the three crossing-call counts rather than correcting them. They carried no
meaning that the mechanism did not already carry, and each was a separate thing to keep
true.

**Second class: true but incomplete in a way that misleads.** The skill breakdown "the GUI
info panel prints it" — behind a preference defaulting to false. `PatternFilter` picks by
"the output file's extension" — the **template** file's. `BatchExporter` "for the PDF
path" — only when the template is `xslt` or `xsl`.

**An example I invented was wrong.** The `.pcg` sample used `STAT:STR=18` and
`CLASS:...|LEVEL=3`. `PCGVer2Creator` writes `STAT:STR|SCORE:18` and
`CLASS:<key>|LEVEL:3|SKILLPOOL:n`. Sub-fields use `:`, never `=`. The page now says so
under the block, because the shape is not guessable.

**The task lens found the damaging one again.** `design.md` presented a new `BONUS:`
category as complete at one class. The bonus map is write-only until Java asks for the key
— `getTotalBonusTo("FEAT", "POOL")` and about twenty others. Ship `SAMPLEPOOL`, get no
error from any check, and the tag does nothing. It also found that `parseToken` must call
the protected `addBonusInfo` or you get a bonus with no target, and that three steps were
missing from the channel walkthrough: `CControl` holds code controls and channels as
different member kinds, `SourceFileLoader.enableBuiltInControl` creates the variable from
the constant's declared format, and `ChannelUtilities.createVarName` prefixes `CHANNEL*`
so no sheet can read the plain name.

**Wrong file cited once.** `choosers.md` cited `cdom/base/AssociationSupport.java`, which
holds a `HashMap` and no owner key. The `IdentityHashMap`s are in
`core/AssociationSupport.java`. `lint_wiki.py` cannot catch that — both files exist.

**And three that were simply wrong.** `design.md` said 713 tags where the handbook
elsewhere says 693. Its `FACTDEF` row described a Java-fields "old side" that does not
exist — `Deity.java` is 37 lines — so the row duplicated the deprecated-package row and is
gone. `changing-behaviour.md` named `getBaseAttackBonus`, which does not exist; the method
is `baseAttackBonus()`.
