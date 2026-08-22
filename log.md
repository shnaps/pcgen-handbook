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

