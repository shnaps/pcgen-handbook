# PCGen Handbook

**How PCGen works underneath — data files, code, and how to change them.**

📖 **[Read it](https://shnaps.github.io/pcgen-handbook/)**

An unofficial guide to modifying [PCGen](https://pcgen.org): the `.lst` and `.pcc`
data format, the workflow for changing it, and the code that loads it.

## Why

PCGen's official docs are thorough but have drifted from the code. Their tag pages
mostly stopped carrying version markers around 6.03. Checked against `master`:

- `ACVALUE`, `BABABBREV`, `DISPLAYVARIABLE` and `ACABBREV` are still documented but
  **no longer exist**.
- `MODIFY` and `MODIFYOTHER`, from the formula system added in 6.07, **exist but are
  not documented**.

So this handbook works the other way round. Facts come from PCGen's Java source;
explanations are written by hand.

## How it stays correct

Every LST tag is a Java class declaring its own name and the object type it applies
to. Those declarations are the specification, so the handbook reads them directly.

```
tools/scan_tokens.py   →  tags.json      every tag PCGen implements
tools/gen_index.py     →  tag index page
tools/scan_output_tokens.py → output-tokens.json   every output token
tools/gen_output_index.py   → output token index page
tools/check_examples.py   every tag used in an example must exist upstream
tools/check_style.py      sentence length, banned filler
tools/lint_wiki.py        orphans, nav gaps, broken source citations
tools/ingest.py           re-scan upstream, diff, report drift
```

`check_examples.py`, `check_style.py` and `lint_wiki.py` run on every push. `ingest.py` runs weekly
and opens an issue when a tag the handbook cites is added, removed or changed.

Currently tracking PCGen `6.09.08.RC1` at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa)
— 693 current tags indexed, with 23 deprecated ones listed separately.

## Building locally

```sh
pip install -r requirements.txt
python -m mkdocs serve
```

To refresh the tag data from upstream:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/PCGen/pcgen.git work/pcgen-src
git -C work/pcgen-src sparse-checkout set code/src/java code/src/test code/src/slowtest code/gradle code/standards docs data system PCGen-base PCGen-Formula
git -C work/pcgen-src rev-parse HEAD > PCGEN-SHA
python tools/scan_tokens.py && python tools/gen_index.py
```

`work/` is gitignored. It holds research sources that are not republished.

## Layout

```
docs/start/      getting from nothing to a working change
docs/lst/        the data file format
docs/internals/  building, startup, the object model, the loader and the token system
docs/appendix/   credits, glossary
WIKI-SCHEMA.md   what each page type must contain
log.md           record of upstream scans
```

## Contributing

Corrections welcome. Every page has an edit link.

Read [`WIKI-SCHEMA.md`](WIKI-SCHEMA.md) before adding a page — it defines the required
sections per page type and the citation format.

## Licence

LGPL-2.1, matching PCGen, so text could be contributed upstream without a licence
conversation.

Not affiliated with the PCGen project. See
[credits](https://shnaps.github.io/pcgen-handbook/appendix/credits/) for sources.
