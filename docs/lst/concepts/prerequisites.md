---
title: Prerequisites
---

# Prerequisites

A prerequisite is a condition on something. `PRExxx` tags gate whether a feat can be
taken, a class entered, a bonus applied, or a file loaded.

There are **129** of them. They all share one shape, so learning that shape is most of
the work.

## The shape

```
PREXXX:<count>,<item>,<item>,...
```

The leading number is **how many of the listed items must match**, not a level or a
value.

```
PRERACE:1,Sample Folk,Sample Large Folk
```

That passes if the character is either one. `PRERACE:2,...` would require both, which
for races is impossible — but for skills or feats, requiring two of a list is common.

*Source: [`AbstractPrerequisiteListParser.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/prereq/AbstractPrerequisiteListParser.java)*

## Negation

Put `!` in front to invert it:

```
!PRERACE:1,Sample Folk
```

Passes when the character is *not* that race. Shipped data uses the negated form about
13,000 times across 33 different prerequisite tags, so it is a normal thing to write,
not a trick.

## Comparison families

Several prerequisites come as a family with a comparison suffix:

| Suffix | Means |
|---|---|
| `EQ` | equal to |
| `NEQ` | not equal to |
| `GT` | greater than |
| `GTEQ` | greater than or equal |
| `LT` | less than |
| `LTEQ` | less than or equal |

`PREVAR`, `PRESTAT`, `PRESIZE`, `PREHANDS`, `PRELEGS`, `PREREACH`, `PRESR`,
`PREBASESIZE` and `PREAGESET` all have this family.

```
PREVARGTEQ:SampleVariable,4
```

`PREVARGTEQ` is the third most used prerequisite in shipped data, at about 9,800 uses.

!!! tip "The suffix is not always the idiomatic form"
    Some of these families are barely used, because the plain tag already expresses the
    comparison in its value. Stats are the clearest case:

    ```
    PRESTAT:1,INT=13
    ```

    That means one stat from the list at 13 **or higher**. Shipped data writes it this
    way 3,338 times and never writes `PRESTATGTEQ` at all.

    Check how real data writes a prerequisite before reaching for a suffixed variant.

## Combining conditions

Plain prerequisites on one line are combined with AND — every one must pass.

For OR, or for anything nested, use `PREMULT`:

```
PREMULT:1,[PRERACE:1,Sample Folk],[PREABILITY:1,CATEGORY=FEAT,Sample Feat]
```

Each bracketed group is a complete prerequisite. The leading count says how many groups
must pass, so `1` is OR and a count equal to the number of groups is AND.

`PREMULT` is the second most used prerequisite overall, at 15,808 uses. Nesting
is where real data spends most of its complexity.

## The ones you will actually meet

Ranked by use in shipped data:

| Tag | Uses | Checks |
|---|---|---|
| `PREABILITY` | 16,302 | has an ability, by category |
| `PREMULT` | 15,808 | combines other prerequisites |
| `PREVARGTEQ` | 9,800 | a variable is at least some value |
| `PRECLASS` | 7,127 | has levels in a class |
| `PRETYPE` | 4,600 | the object has a type |
| `PRETEXT` | 3,600 | free text shown to the reader, always passes |

### PREABILITY

The most used prerequisite, and it needs a category:

```
PREABILITY:1,CATEGORY=FEAT,Sample Feat
```

Without `CATEGORY=` it cannot tell which kind of ability you mean.

`PREFEAT` still exists and is handled by the same parser, but new data should use
`PREABILITY` — see [what changed](../../appendix/whats-changed.md).

### PRETEXT

Worth knowing because it surprises people: it does not test anything. It displays a
requirement to the reader that PCGen cannot check itself. It always passes.

## Where they go

A prerequisite applies to whatever it shares a line with. On a feat it gates taking the
feat. On a `BONUS` it gates that bonus. On a PCC file line it gates loading the file.

```
Sample Feat	CATEGORY:FEAT	TYPE:General	PRESTAT:1,INT=13
Sample Feat	CATEGORY:FEAT	TYPE:General	BONUS:SKILL|Sample Athletics|2|PRERACE:1,Sample Folk
```

The first gates the whole feat. The second grants the feat freely but applies its bonus
only to that race.

## How they are implemented

Each prerequisite is three classes, not one:

| Package | Does |
|---|---|
| `plugin/pretokens/parser` | reads the tag text |
| `plugin/pretokens/test` | evaluates it against a character |
| `plugin/pretokens/writer` | writes it back out |

Useful when checking behaviour: the parser tells you what syntax is accepted, the
tester tells you what it actually means.

*Source: [`plugin/pretokens/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/pretokens)*

## Gotchas

**The first number is a count, not a threshold.** `PRESKILL:1,Sample Skill=5` means one
skill from the list at rank 5, not skill rank 1.

**Case does not matter for the tag name.** Lookup lowercases it. Data and this handbook
use uppercase throughout.

**A misspelt name inside a prerequisite is not caught at the line.** Names resolve after
loading, so the error names the reference, not your file.

**`PRETEXT` never fails.** If you used it expecting a check, nothing is being checked.

## Related

- [Tag index](../reference/tag-index.md) — all 129 prerequisites
- [Ability files](../files/ability.md) — the most common place to use one
- [What changed](../../appendix/whats-changed.md) — `PREFEAT` and the ability migration
