# Backlog

What the handbook could cover next, and what it should not. From a survey of the PCGen
repository and PCGen's own documentation on 2026-08-22, at commit `d262f8b4`.

Ranked by how much a developer learning to modify PCGen would gain. Counts are measured,
not estimated.

## Where the handbook stands

52 pages. The LST data layer is covered for the file types people write most, the
cross-cutting tags are covered, and the internals section now runs from build to output.

The generated [tag index](docs/lst/reference/tag-index.md) lists all 706 tags. What is
missing is hand-written explanation for the long tail, and whole subsystems that have
one page or none.

## Tier 1 — real gaps

### 1. Output token reference

PCGen's own docs describe **164 output tokens** across ten category pages, roughly
430 KB. The source holds 17 classes in `pcgen/io/exporttoken/` and 140 in
`plugin/exporttokens/`, 49 of them deprecated.

The handbook has one page on the whole system. A developer writing a character sheet has
nothing to look things up in.

This is a separate system from LST tags, and readers confuse the two constantly. Whether
an index can be generated the way `tags.json` is depends on how the token classes declare
their names — see the note at the end of this file.

### 2. Kit files

`plugin/lsttokens/kit/` — 10 tokens plus 10 sub-object packages, and **47 test classes**,
the richest test coverage of any uncovered file type. Kits are the starting-package
mechanism: gear, abilities and class levels granted at creation.

Best effort-to-value ratio in this list. The tests do most of the work of establishing
the syntax.

### 3. ADD: and AUTO:

`plugin/lsttokens/add/` (8 classes) and `auto/` (5). These grant things to a character
from any object type, so they appear on races, classes, templates and abilities alike.
The handbook mentions them and explains neither.

One page covering both. 13 tests exist.

### 4. Equipment modifier files

`plugin/lsttokens/equipmentmodifier/` — 15 classes, 14 tests. EQMOD entries are how
masterwork, magic bonuses and special materials attach to equipment. The equipment page
points at them and stops.

### 5. FreeMarker sheet authoring

The current way to write a character sheet. PCGen documents it in four pages under
`docs/freemarkeroutputpages/`, including a tutorial. The code is live in
`pcgen/io/freemarker/` and `pcgen/output/`.

Nothing in the handbook covers writing a sheet, only how sheets are executed.

### 6. Data control and game mode depth

Now partly covered by [data controls](docs/lst/concepts/data-controls.md).
`plugin/lsttokens/gamemode/` still holds **66 classes across 11 sub-packages** —
stat rolling, age sets, class types, unit sets, wield categories, tabs. The game modes
page is thin against that.

`system/gameModes/<mode>/miscinfo.lst` alone is documented upstream in a 120 KB page.

## Tier 2 — worth doing

### 7. What changed, from two real sources

`plugin/lsttokens/deprecated/` holds **32 classes**, each naming its replacement. That
is a complete, checkable deprecation map, and the tooling could generate it.

Separately, `installers/release-notes/` covers **5.10 through 6.09.05**, with older
releases in `previous_releases/`. The handbook's `whats-changed.md` was written from tag
scanning alone and has never read these.

### 8. Debugging, taught from the broken data set

`data/zen_test/pcgen_test_advanced/pcgen_broken_tests/` is deliberately broken. It
contains a malformed prerequisite, a bogus time unit on a `SPELLS:` entry, and an empty
file. `zen_test/zen_test_broken_link/` demonstrates a dangling `PCC:` reference.

Real errors with known causes, shipped in the repository. That is the material for a
debugging page that shows actual messages rather than invented ones.

### 9. How a data set is laid out

The convention across `data/` is consistent and nowhere written down:

- `_name.pcc` — the campaign file others load
- `prefix__datacontrols.lst` — declarations, double underscore
- `prefix_feats.lst` — content, single underscore
- `data/<gamemode>/<publisher>/<product>/` directory shape

Worth a short page. Anyone reading a second data set benefits immediately.

### 10. Companion mod files

`plugin/lsttokens/companionmod/` — 9 classes, **no tests**. Familiars and animal
companions scale through these. Writing the page means establishing the syntax from the
token classes alone, so it costs more than the others.

### 11. Small file types

`subclass/` (3), `weaponprof/` (1), `sizeadjustment/` (4), `eqslot/` (4), `load/` (6),
`paper/` (7), `rules/` (5), `level/` (4). Thin individually. One combined reference page
covering the game mode support files would carry all of them.

### 12. Hand-written tag pages

The original plan's last item: `lst/reference/tags/`, about 150 pages for the tags that
actually come up. Zero written. The generated index covers all 706 meanwhile, so this
deepens rather than fills a gap.

Lower here than in the original plan, because the subsystem gaps above leave a reader
with nothing at all, while the tag index at least answers "does this exist and where".

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

## Open question: can output tokens be indexed automatically?

`tools/scan_tokens.py` works because every LST token declares `getTokenName()` as a
string literal. Output tokens declare `getTokenName()` too, but they parse the rest of
the marker themselves — `STAT.0.MOD` is one token name and two arguments, with no
sub-token registry to read.

If the names are literals, a scanner is cheap and the reference at the top of this list
becomes mostly generated. If a meaningful share are computed, or if the argument grammar
lives only in comments, the page has to be written by hand and stays expensive.

Settling this decides how item 1 gets built.
