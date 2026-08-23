---
title: Writing a character sheet
---

# Writing a character sheet

A character sheet is a template PCGen fills in and writes out. The file extension picks
the engine, which [output and saving](../internals/output-and-saving.md) covers. Write
new sheets as FreeMarker, ending `.ftl`.

## What shipped sheets actually do

PCGen ships **27** FreeMarker sheets. Counted across all of them:

| Idiom | Uses |
|---|---|
| `pcstring(...)` | 6,988 |
| `pcvar(...)`, `pchasvar(...)` | 1,531 |
| `<@loop ...>` | 878 |
| `pcboolean(...)` | 44 |
| reading the data model directly | 0 |

**No shipped sheet reads the data model.** Every one of the 27 goes through `pcstring`
and friends into the older token engine.

This matters before you start. FreeMarker is the templating layer. The vocabulary is
still [output tokens](token-index.md), and that is the part with 27 working examples
behind it.

## The four things you will write

### `pcstring` — get a value as text

```
${pcstring('NAME')}
${pcstring('CLASS.0.LEVEL')}
```

The argument is an output token, exactly as the older engine spells it. The
[token index](token-index.md) lists all 154.

### `pcvar` — get a number

```
${pcvar('COUNT[CLASSES]')}
```

The argument is a formula, not just a name, which is why `COUNT[CLASSES]-1` works. It
returns a number, so it can be compared and used in arithmetic.

`pchasvar` tests whether a variable exists:

```
<#if (pchasvar('CMB'))>
```

**The two do not agree.** `pcvar` evaluates a formula, so it resolves built-in terms and
undeclared names alike. `pchasvar` asks a narrower question: was this name declared by a
[`DEFINE`](../lst/concepts/declaring-variables.md)? A built-in variable returns false.

So guarding a block with `pchasvar` can hide a value `pcvar` would have printed.

*Source: [`PCHasVarFunction.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/freemarker/PCHasVarFunction.java)*

### `pcboolean` — test a condition

```
<#if (pcboolean('VAR.HASFEAT:Sample Feat'))>
```

### `@loop` — repeat over a count

This is the idiom to learn, because output tokens are indexed rather than iterable:

```
<@loop from=0 to=pcvar('COUNT[CLASSES]-1') ; class , class_has_next>
	${pcstring('CLASS.${class}.NAME')}<#if class_has_next>, </#if>
</@loop>
```

Two variables are declared after the `;` — the index, and a flag saying whether another
pass follows. The `-1` is required: `COUNT` returns how many there are, and the index
starts at zero.

The index is then interpolated back into the token string. That nesting —
`'CLASS.${class}.NAME'` — is what most of a real sheet consists of.

`@equipsetloop` is the same idea for equipment sets, and takes no arguments:

```
<@equipsetloop>
	${pcstring('EQSET.NAME')}
</@equipsetloop>
```

## A sheet that works

```
<#ftl encoding="UTF-8" strip_whitespace=true>
<html>
<body>
<h1>${pcstring('NAME')}</h1>
<p>${pcstring('RACE')}</p>
<p>Classes:
<@loop from=0 to=pcvar('COUNT[CLASSES]-1') ; c , c_has_next>
	${pcstring('CLASS.${c}.NAME')} ${pcstring('CLASS.${c}.LEVEL')}<#if c_has_next>, </#if>
</@loop>
</p>
</body>
</html>
```

Save it under the game mode's sheet folder and it appears in the export list.

## The data model

A model is built from the character and handed to FreeMarker, keyed by the same
`CharID` the [facets](../internals/facets.md) use. Its 23 top-level keys are listed in
the [token index](token-index.md).

Treat it as untested ground. The keys are real and registered. Nothing PCGen ships reads
them, so there are no working examples to copy, and no sheet would break if one changed.

## What breaks

**A token name that does not exist.** The older engine substitutes an empty string. The
sheet renders with a gap and nothing is logged.

**Forgetting `-1` in a loop.** The last pass asks for an index past the end. That is the
empty-string case again, so it shows up as a stray blank row.

**Quoting.** `pcstring` takes a FreeMarker string, and the token inside it often contains
its own dots and equals signs. Single quotes outside, `${}` inside, is the shipped
convention.

**Guarding with `pchasvar` when you meant `pcvar`.** `pchasvar` is true only for a name
a `DEFINE` declared. Built-in variables return false, and the block never renders.

## Where to look

| Task | Place |
|---|---|
| every output token | [token index](token-index.md) |
| worked examples | `outputsheets/base.xml.ftl`, 3,438 lines |
| the smallest shipped sheet | `outputsheets/d20/fantasy/htmlxml/common/misc.ftl` |
| how the directives are implemented | `pcgen/io/freemarker/` |
| how the engine is chosen | [output and saving](../internals/output-and-saving.md) |

## Related

- [Token index](token-index.md) — all 154 output tokens and the 23 model keys
- [Output and saving](../internals/output-and-saving.md) — the two engines, and the save format
- [Declaring a variable](../lst/concepts/declaring-variables.md) — what `pcvar` can read
- [Facets](../internals/facets.md) — where the model's data comes from
