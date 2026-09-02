---
title: Why it is built this way
---

# Why it is built this way

The patterns PCGen repeats, the problem each one solves, and where to put a new class.
Read this before your first change. It is the shortest path to guessing right about code
you have not read yet.

All paths are relative to the PCGen repository root, at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa).

## The problem the design answers

PCGen runs **20 game modes** from data. A game mode is not a plugin and not a fork. It is
files under `system/gameModes/`, and one compiled program serves all of them.

That is the constraint everything else answers to. A rule cannot be a field on a class,
because the next game mode does not have that rule. So the codebase pushes decisions out
of Java and into data. It has been doing that for years, and has never been able to stop
and finish.

Almost every surprise in this codebase is a consequence of that sentence.

## Five patterns

### 1. Objects hold keys, not fields

A `Race` has no `size` field. It has a typed key map, and `TYPE:` and `SIZE:` write into
it. [The object model](cdom-model.md#why-keys-instead-of-fields) covers the mechanics.

**Buys:** a new tag needs no change to `Race`, `Skill` or anything else. Hundreds of tags
exist and the classes they write to stayed the same size. The
[tag index](../lst/reference/tag-index.md) owns the count.

**Costs:** you cannot find what a `Race` holds by reading `Race.java`. You find it by
reading the tokens that write to it.

### 2. One class per tag, found rather than registered

A token declares `getTokenName()` and `getTokenClass()`. It is jarred by package and
discovered at startup. There is no registry file.
[Plugin loading](plugin-loading.md#claimed-by-tokenlibrary) covers how a class is claimed.

**Buys:** adding a tag is one file plus one test. Deleting the file removes the tag
completely, with no stale entry left behind.

**Costs:** a class in the wrong package is not loaded, and the tag is unknown at load
time. Nothing reports it.

### 3. Every token must be able to write itself back

`parseToken` reads a tag. `unparse` regenerates it. Both are required.

**Buys:** two things depend on it. The LST converter rewrites data files between
versions. The token tests assert the round trip, which is what makes them the most
precise statement of what a tag accepts.

**Costs:** you may not store a parsed value in a form you cannot regenerate. That rules
out flattening, normalising, or discarding anything the author wrote.

### 4. Anything needing the whole data set waits

A tag naming another object cannot resolve it during parsing, because file order is not
controlled. So parsing records a `CDOMReference` and resolution happens later, along with
`DeferredToken`, `PostValidationToken` and `PostDeferredToken`.
[The load pipeline](load-pipeline.md#6-post-load-phases) covers the phases.

**Buys:** data authors never have to order their files.

**Costs:** an error can name a file you did not edit, because the dangling reference is
found by whatever pointed at your object.

### 5. Character state lives outside the character

`PlayerCharacter` does not hold the race. A facet does, keyed by `CharID`.
[The character model](facets.md) covers it, and owns the count. The facets are wired to
each other by events with explicit priorities.

**Buys:** new state needs no change to `PlayerCharacter`, and ordering rules are written
as priority numbers rather than as method call order.

**Costs:** one character's state is spread across hundreds of objects. The ordering that
matters sits in a priority table rather than in any call stack.

## The sixth pattern: two live implementations

This is the one that explains the most and is written down the least.

When a hardcoded rule is replaced by a data-driven one, the replacement cannot break the
20 shipped game modes on the day it lands. So both implementations stay live, and the
data chooses between them.

| Where | Old | New | Chosen by |
|---|---|---|---|
| saves, AC, reach, initiative and more | hardcoded in Java | a variable | a **code control** |
| formulas | JEP | `PCGen-Formula` | which tag you wrote |
| superseded tags | 32 classes in `plugin/lsttokens/deprecated/` | their replacements | still parsed, warned about |

Shipped game modes set only a handful of the code controls, so for most data the old path
is the one that runs. That is why the dual path is easy to miss and expensive to forget:
fixing one branch leaves the other wrong. [Data controls](../lst/concepts/data-controls.md#code-controls)
owns the counts. See
[changing behaviour](changing-behaviour.md#half-the-engine-has-two-implementations).

Read the migration as unfinished rather than as mess. Each pair is one rule that was
being moved out of Java when the work stopped.

## Adding a class: what to write and where

Eleven extension points. All of them are discovered by package, so the package is not a
filing decision — it is the registration.

| To add | Write a class that | In package | Test in |
|---|---|---|---|
| an LST tag | implements `CDOMPrimaryToken<T>` | `plugin/lsttokens/…` | `code/src/test/plugin/lsttokens/` |
| a sub-token, such as `ADD:X` | implements `CDOMSecondaryToken<T>` | the parent's subpackage | the same |
| a prerequisite | extends `AbstractPrerequisiteListParser`, plus a tester extending `AbstractPrerequisiteTest` | `plugin/pretokens/parser/` and `…/test/` | `code/src/test/plugin/pretokens/` |
| a `BONUS:` category | extends `BonusObj` | `plugin/bonustokens/` | no per-class test exists |
| an output token | extends `AbstractExportToken` | `plugin/exporttokens/` | `code/src/slowtest/pcgen/io/exporttoken/` |
| a formula function | implements `FormulaFunction` | `plugin/function/` | `code/src/test/…/function/` |
| a `MODIFY` operator | extends `AbstractNumberModifierFactory` or its siblings | `plugin/modifier/<format>/` | `code/src/test/…/modifier/` |
| a grouping | implements `GroupingDefinition<T>` | `plugin/grouping/` | no test package exists |
| a chooser primitive | implements `PrimitiveToken<T>` | `plugin/primitive/<type>/` | `code/src/test/…/primitive/` |
| a chooser qualifier | extends `AbstractPCQualifierToken<T>` | `plugin/qualifier/<type>/` | `code/src/test/…/qualifier/` |
| a JEP command | extends `PCGenCommand` | `plugin/jepcommands/` | `code/src/slowtest/plugin/jepcommands/` |

Three things this table does not tell you.

**A new package needs a build change.** Each package above is jarred by its own task in
`code/gradle/plugins.gradle`. `PluginBuildTest` carries its own hardcoded list of the
plugin packages and fails when the directories on disk do not match it. That list is the
closest thing PCGen has to a registry.

**`Token` and `AbstractExportToken` both work.** Write the second one. The counts are
on [output and saving](output-and-saving.md#what-bites-when-you-change-output), which
owns them.

**`plugin/bonustokens/` has no per-class tests.** Behaviour is covered by `BonusTest`,
`TempBonusTest` and `BonusManagerTest` in `code/src/slowtest/`. A new bonus category is
the one extension point with no template test to copy.

**A new `BONUS:` category does nothing on its own.** Unlike every other row, registering
the class only makes the tag parse. Something in Java has to read the key back. See
[the rules engine](rules-engine.md#what-bites-when-you-change-a-calculation).

*Source: [`plugins.gradle`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/gradle/plugins.gradle)*

## Not an extension point

Facets, output actors and loaders are ordinary classes. They are wired by Spring or by a
hand-written method, not discovered.

| To add | See |
|---|---|
| character state the engine derives | [adding a facet](facets.md#adding-a-facet) |
| character state the user sets | [changing behaviour](changing-behaviour.md#new-character-state-has-to-survive-the-save) |
| something a template can read | [character sheets and output](output-and-saving.md) |

## Where the traps are

Each subsystem page ends with what bites when you change it — the behaviour that produces
a wrong result rather than a failure. Read the one for the area you are touching before
you start.

| Changing | Read |
|---|---|
| the loader, or adding a file type | [load pipeline](load-pipeline.md#what-bites-when-you-change-the-loader) |
| how a number is computed | [rules engine](rules-engine.md#what-bites-when-you-change-a-calculation) |
| the formula engine itself | [formula system](formula-system.md#what-bites-when-you-change-pcgen-formula) |
| character state | [facets](facets.md#what-bites-when-you-add-or-change-a-facet) |
| a choice or selection | [choosers](choosers.md#what-bites-when-you-change-a-choice) |
| a tab or a widget | [interface layer](ui-layer.md#what-bites-when-you-change-the-interface) |
| a sheet | [character sheets and output](output-and-saving.md#what-bites-when-you-change-output) |
| the save format | [the save format](save-format.md#what-bites-when-you-change-the-save-format) |
| `PCClass`, `Equipment` or their neighbours | [object model](cdom-model.md#the-objects-a-character-holds-are-clones) |

Five that cut across all of them are on
[changing behaviour](changing-behaviour.md).

## What the design does not give you

Two seams hold and two leak, and
[the overview measures which](overview.md#the-seams). The two that hold — plugin jars and
the `PCGen-base` and `PCGen-Formula` modules — are the two a tool enforces. The two that
leak are the two policed by convention.

Take that as the rule when you add something. A boundary nobody checks will not survive,
so put new code where a test or the build will notice if it moves.

## Related

- [How PCGen fits together](overview.md) — the measured shape, including where the layers do not hold
- [The object model](cdom-model.md) — keys, references and identity
- [The character model](facets.md) — the facets and their event graph
- [Adding a tag](adding-a-tag.md) — the worked example of pattern 2
- [Changing behaviour](changing-behaviour.md) — the five traps in engine code
- [Running it under a debugger](running-and-debugging.md) — watching any of it happen
