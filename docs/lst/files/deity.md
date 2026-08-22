---
title: Deity files
---

# Deity files

A deity file defines gods a character may follow. Loaded by `DEITY:` in a
[PCC](pcc.md).

Deities have **three** tags of their own. Six more were deprecated and replaced by the
fact system, which is the highest deprecation ratio of any file type. Follow an older
tutorial here and most of what it shows is out of date.

## Minimum working line

```
Sample Deity	ALIGN:LG	DOMAINS:Sample Domain
```

## The three current tags

| Tag | Takes | Does |
|---|---|---|
| `ALIGN` | an alignment | the deity's alignment |
| `DOMAINS` | domain list | which domains followers may take |
| `DEITYWEAP` | weapon list | the favoured weapon |

*Source: [`plugin/lsttokens/deity/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/deity)*

`DOMAINS` and `DEITYWEAP` are the two you will use most, at about 2,100 and 1,100 uses
in shipped data.

## Descriptive fields use FACT

Everything descriptive moved to `FACT` and `FACTSET`.

| Deprecated tag | Current form |
|---|---|
| `SYMBOL` | `FACT:Symbol\|<text>` |
| `TITLE` | `FACT:Title\|<text>` |
| `WORSHIPPERS` | `FACT:Worshippers\|<text>` |
| `APPEARANCE` | `FACT:Appearance\|<text>` |
| `PANTHEON` | `FACTSET:Pantheon\|<name>` |
| `RACE` | `FACTSET:Race\|<name>` |

`FACT` holds one value. `FACTSET` holds several, which is why pantheon and race use it
— a deity can belong to more than one.

Shipped data uses `FACTSET:Pantheon` about 1,160 times and `FACT:Symbol` about 725
times. This is the normal way to write a deity now, not an edge case.

These facts are declared in a data control file before use. PCGen ships declarations
for the compatibility ones, which is why the old tags still map across.

## Global tags worth knowing

| Tag | Does |
|---|---|
| `DESC` | description text |
| `BONUS` | bonuses granted to followers |
| `TYPE` | classification |
| `PRExxx` | conditions on following the deity |
| `SOURCEPAGE` | page reference |
| `NAMEISPI` | whether the name is product identity |

## A complete example

```
# my_deities.lst - example deities
# Invented content. Nothing from a published book.

Sample Deity	ALIGN:LG	DOMAINS:Sample Domain|Sample Order Domain	DEITYWEAP:Sample Blade	FACT:Title|The Example	FACT:Symbol|A plain circle	FACT:Worshippers|Scribes and clerks	FACTSET:Pantheon|Sample Pantheon	DESC:An example deity.
Sample Trickster	ALIGN:CN	DOMAINS:Sample Domain	DEITYWEAP:Sample Blade	FACT:Title|The Unseen	FACTSET:Pantheon|Sample Pantheon
```

Then in the PCC:

```
DEITY:my_deities.lst
```

## Domains

A deity's `DOMAINS` list names domains that must exist, so load the domain file too.
Domains are a separate file type with its own page: [domain files](domain.md).

## Gotchas

**Most deity tutorials are out of date.** Six of nine tags changed. Check anything a
video shows against the [tag index](../reference/tag-index.md).

**`DOMAINS` names objects that must exist.** A domain that is not defined and loaded
resolves to nothing, and the error appears after loading rather than at the line.

**`FACT` needs the fact to be declared.** The compatibility ones ship with PCGen. A
fact name of your own has to be defined before you can set it.

**`FACTSET` is not a repeated `FACT`.** Use `FACTSET` where several values are
legitimate, and `FACT` where only one is.

## Related

- [PCC](pcc.md) — loading deity and domain files
- [What changed](../../appendix/whats-changed.md) — the six deprecated deity tags
- [Tag index](../reference/tag-index.md) — every `Deity` tag
- Video: [Deities — adding and using](https://www.youtube.com/watch?v=DWZqd6iF-64),
  recorded against 6.05/6.06 and predating the fact system
