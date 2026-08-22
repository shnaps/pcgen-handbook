# Backlog

What the handbook could cover next, and what it should not. From a survey of the PCGen
repository and PCGen's own documentation on 2026-08-22, at commit `d262f8b4`.

Ranked by how much a developer learning to modify PCGen would gain. Counts are measured,
not estimated.

## Where the handbook stands

58 pages. The LST data layer is covered for the file types people write most, the
cross-cutting tags are covered, and the internals section now runs from build to output.

The generated [tag index](docs/lst/reference/tag-index.md) lists all 706 tags. What is
missing is hand-written explanation for the long tail, and whole subsystems that have
one page or none.

## Tier 1 — real gaps

### 1. Output tokens — index done, explanation not

**Done.** `tools/scan_output_tokens.py` reads the token classes and
`tools/gen_output_index.py` writes
[the index](docs/outputsheets/token-index.md): **154 tokens**, 49 of them deprecated,
plus the 23 FreeMarker model keys. PCGen's own hand-maintained reference lists 154
anchors, 17 of which are formula functions rather than tokens.

**Left to do.** The index answers *does this exist and where*. It cannot answer *what
arguments does it take*, because no output token declares that anywhere readable — see
the note at the end of this file. Hand-written pages for the twenty or so tokens a sheet
author actually uses would fill that, and a page on writing a sheet would frame them.

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
