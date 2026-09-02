---
title: The formula system
---

# The formula system

PCGen has **two formula engines**, and both are live. This page covers what each is made
of. [The rules engine](rules-engine.md) owns which tag reaches which one.

The split matters before you read either half. Almost every formula in shipped data runs
through the older engine, JEP. The newer one, `PCGen-Formula`, is a separate pair of
Gradle subprojects and is what `MODIFY` drives.

For the data-side view, see
[declaring a variable](../lst/concepts/declaring-variables.md) for the older engine and
[variables and formulas](../lst/concepts/variables-and-formulas.md) for the newer.

## JEP, the engine the data runs on

Every `DEFINE:X|0` and every `BONUS:VAR` value is a JEP expression. That is 37,076 and
81,422 uses in shipped data respectively, against 1,845 for `MODIFY`.

JEP is an external expression parser. PCGen subclasses it as `PJEP`, and what `PJEP` adds
is the functions. It sets two variables of its own, `TRUE` and `FALSE`, and
`ClassLevelCommand` injects `CL` for the length of one expression. The term vocabulary
belongs to `EvaluatorFactory` and the result cache to `VariableProcessor`; `PJEP` only
reports whether a result may be cached.

*Source: [`PJEP.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/util/PJEP.java)*

### The fourteen functions

`plugin/jepcommands/` holds a closed set, registered through the same
[plugin mechanism](plugin-loading.md) as LST tags. Each class returns its own name:

| Function | Does |
|---|---|
| `MIN`, `MAX` | the smaller or larger of its arguments |
| `CEIL`, `FLOOR` | round up, round down |
| `IF` | a condition |
| `OR` | a boolean |
| `COUNT`, `COUNTDISTINCT` | how many of something the character has |
| `VAR` | read a variable by name |
| `MASTERVAR` | read one from a master, for companions |
| `CLASSLEVEL` | levels in a named class |
| `CHARBONUSTO` | a bonus total the character has, by category and name |
| `SKILLINFO` | a fact about a skill |
| `ROLL` | dice |

A fifteenth, `cl`, is added directly in `PJEP` rather than through the plugin loader, so
it does not appear in that package. It is deprecated and logs a warning when it runs.
Write `CLASSLEVEL` instead.

### The variable vocabulary is a closed set matched by regex

Names such as `BAB`, `ACCHECK`, `CASTERLEVEL` and `COUNT[CLASSES]` are not variables. They
are **terms**, and `EvaluatorFactory` holds two vocabularies of them:

| Factory | Built from | Terms |
|---|---|---|
| `EvaluatorFactory.PC` | `TermEvaluatorBuilderPCVar` | 80, plus one for statistics |
| `EvaluatorFactory.EQ` | `TermEvaluatorBuilderEQVar` | 15 |

Each is an enum. A constant carries a regex and the keys it answers to, so
`COMPLETE_PC_ACCHECK` declares the pattern `AC{1,2}HECK` and matches both `ACCHECK` and
`ACHECK`. The factory concatenates every pattern into one alternation at construction and
matches an incoming name against it.

**A name that matches no term is not an error, and nothing is logged.** `lookupVariable`
tries the declared variables first, then the terms, then the export tokens. When all three
miss it returns null and the JEP pass abandons the whole value. The raw text then goes to
the old fallback parser, which understands only `+ - * /` and `.IF.`.

What the reader sees depends on the rest of the value. In plain arithmetic the unmatched
name [reads as zero](../lst/concepts/declaring-variables.md) and the rest still computes.
In a value using a JEP function, a comparison or nested parentheses, the fallback parser
fails too and the whole value collapses to zero.

That is the single most useful fact on this page for a data author. The vocabulary is
closed, a misspelt term never announces itself, and the `BONUS:VAR` applies a wrong number
rather than failing.

*Source: [`VariableProcessor.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/VariableProcessor.java)*

*Source: [`EvaluatorFactory.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/term/EvaluatorFactory.java)*

The full lists are in the two enums. They are not reproduced here — 95 rows of name and
description is transcription, and the enums stay correct on their own.

### Adding to JEP

| To add | Write |
|---|---|
| a function | a `PCGenCommand` subclass in `plugin/jepcommands/`, returning its name from `getFunctionName` |
| a term | an enum constant in `TermEvaluatorBuilderPCVar` or `...EQVar`, plus a `TermEvaluator` class in `pcgen/core/term/` |

`pcgen/core/term/` is 129 classes, one per term family. `VariableProcessorPC` is where a
name reaches `EvaluatorFactory.PC` and becomes a value.

Both packages have tests, in `code/src/slowtest/` rather than `code/src/test/`: five
command tests under `plugin/jepcommands/`, and three under `pcgen/core/term/`.
`EvaluatorFactoryTest` is 294 KB and exercises the term vocabulary name by name.

## PCGen-Formula, the newer engine

This half has a debugger. **Tools > View Solver Process** lists every modifier applied to
one variable and the value after each step, launched from `PCGenActionMap.java:303`. It
reads this engine only — [variables and formulas](../lst/concepts/variables-and-formulas.md)
covers using it.

Its accelerator does not work, which is worth knowing before you go looking for the key.
`SolverViewAction` passes `"Ctrl-F11"`, and `PCGenAction` tokenises on whitespace and
accepts only `shortcut`, `alt`, `shift-shortcut` or a bare `F`-key. One token matching
none of those falls through to `KeyStroke.getKeyStroke`, which returns null, so
`ACCELERATOR_KEY` is never set.

### Two modules

`settings.gradle` is three lines, and two of them are this:

```groovy
include 'PCGen-base', 'PCGen-Formula'
```

| Module | Holds | Java files |
|---|---|---|
| `PCGen-base` | generic utilities with no formula knowledge — collections, format managers, maths, graphs | ~210 |
| `PCGen-Formula` | the formula language itself — parser, visitors, scopes, solver | 144 |

The split is deliberate. `PCGen-base` knows nothing about formulas, and `PCGen-Formula`
knows nothing about PCGen's game objects. PCGen glues both to its own model in
`pcgen/cdom/formula/` and `pcgen/rules/context/VariableContext.java`.

!!! note "Not in a default sparse checkout"
    Both directories are real, but they are easy to miss. A sparse checkout scoped to
    `code/src` excludes them entirely, which makes it look as though the formula system
    has no source. Add them explicitly.

### The language is generated

`PCGen-Formula/code/src/` has three source roots, not one:

| Root | Is |
|---|---|
| `javacc` | the grammar |
| `jjtree` | the syntax tree definition |
| `java` | hand-written code, plus the generated parser |

So the formula language has a real grammar rather than being parsed by hand. That is
why formula syntax is stricter and more consistent than tag argument syntax.

### Packages worth knowing

Under `PCGen-Formula/code/src/java/pcgen/base/formula/`:

| Package | Holds |
|---|---|
| `base` | the contracts — `VariableID`, `VariableLibrary`, `FormulaFunction`, `EvaluationManager` |
| `parse` | the generated tree nodes |
| `visitor` | the passes over that tree |
| `inst` | concrete implementations |
| `function`, `library`, `factory`, `analysis` | supporting pieces |

### From string to value

Three visitors do the work, and they are separate passes over the same tree:

| Visitor | Answers |
|---|---|
| `SemanticsVisitor` | is this formula valid, and what type does it produce |
| `DependencyVisitor` | what does it depend on |
| `EvaluateVisitor` | what is its value now |

The entry points on PCGen's side:

- **Build and validate** — `VariableContext.getValidFormula()`, which delegates to
  `FormulaFactory` and drives the semantics pass.
  *(`pcgen/rules/context/VariableContext.java`)*
- **Evaluate** — `NEPFormula.resolve(EvaluationManager)`, called from
  `pcgen/cdom/calculation/FormulaCalculation.java`.

Validation happening separately from evaluation is why a bad formula is reported when
data loads rather than when a character is built.

### Scopes

A scope is an `ImplementedScope`. PCGen's subinterface is `PCGenScope`, in
`pcgen/cdom/formula/scope/`, with implementations for the global scope, equipment,
skills, stats and dynamic scopes.

Two steps bind a variable:

1. **Declared** into a scope at load time by `assertLegalVariableID(name, scope,
   formatManager)` on `VariableContext`. The `VARIABLE` file tokens call this.
2. **Instanced** at runtime — each object gets a `ScopeInstance`, and
   `getVariableID(instance, name)` produces the key the solver uses.

So the same variable name on two different objects is two different variables. That is
what `MODIFYOTHER` needs a scope argument for.

### Functions

`code/src/java/plugin/function/` holds eight functions available inside formulas:

| Function | Does |
|---|---|
| `getFact` | read a `FACT` |
| `Get`, `getOther` | read a variable, from this object or another scope |
| `Lookup` | look a value up in a table |
| `Group` | the objects matching a group or type |

Plus `ListAll`, `key` and `INPUT`.

`Group` takes the same three grouping forms as the second field of `MODIFYOTHER` — `ALL`, `KEY=` and `GROUP=`. They are written up in
[variables and formulas](../lst/concepts/variables-and-formulas.md#the-grouping-argument).

These are registered by the same plugin mechanism as tags — see
[plugin loading](plugin-loading.md).

### How the solver orders modifiers

When several modifiers apply to one variable, each variable gets a `Solver` holding its
default plus every modifier applied to it.

The solver keeps them in a `TreeMap` keyed by priority, so iteration is in priority
order. Priority is a single `long`, composed of two parts:

```java
return ((long) getUserPriority() << 32) + toDo.getInherentPriority();
```

*Source: [`CalculationModifier.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/calculation/CalculationModifier.java)*

The consequence is worth stating plainly:

- **`PRIORITY=n` from the data wins**, because it occupies the high 32 bits.
- **The operator's own inherent priority breaks ties** at equal user priority. That is
  what makes `SET` apply before `ADD` before `MULTIPLY` with no order written anywhere.
- **User priority defaults to 0**, so data that sets no priority is ordered entirely by
  operator.

That is why `PRIORITY` is rarely needed — the default ordering already matches what
arithmetic expects.

## What bites when you change PCGen-Formula

The formula engine is a separate Gradle project with its own module boundary. Five things
differ from working inside `pcgen`.

### The parser is generated, and two files are not

`jjtree` and `javacc` run as build tasks and write into `build/generated/`. Nothing under
them is checked in. Two exceptions are hand-maintained in the source tree:
`SimpleNode.java` and `Operator.java`. The build deletes JJTree's own stub so the two do
not collide.

`SimpleNode.java` still carries a "Do not edit this line" banner from the generator. Edit
the generated copy, or regenerate without that delete, and nothing compiles.

### A function is four visitors, not one method

`FormulaFunction` declares five methods, and each is driven by a different visitor:

| Method | Visitor |
|---|---|
| `isStatic` | `StaticVisitor` |
| `allowArgs` | `SemanticsVisitor` |
| `evaluate` | `EvaluateVisitor` |
| `getDependencies` | `DependencyVisitor` |

`allowArgs` and `getDependencies` have to agree. A function that validates but declares
no dependency runs against a variable the solver never queued. It reads a stale value,
with no error.

### A new `FormatManager` must override `equals` and `hashCode`

`VariableID.equals` compares the format manager, and `SimpleSolverManager` keys its
solvers by `VariableID` in a `HashMap`. `SupplierValueStore` keys a second `HashMap` on
the format manager itself, which is where its `hashCode` matters. The `FormatManager`
interface declares neither requirement.

Two instances of a format manager with identity equality make the lookup miss, and the
variable reads its default. Most shipped implementations override both, but not all —
`ColumnFormatManager` and `HandedManager` override neither.

### A wrong default value for a format is never reported

`createSolver` calls `initializeFrom`, whose default implementation looks the value up by
identifier string and casts it unchecked. The one guard, `SupplierValueStore
.validateDefaults`, returns a result that `VariableContext.validateDefaults` discards.

### Operator registration order breaks ties

`SimpleOperatorLibrary.addAction` appends, and the lookup returns the **first** action
that accepts the argument classes. Register one ahead of an existing action that also
matches and it shadows the old one, changing the result format without an error.

*Source: [`FormulaFunction.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/PCGen-Formula/code/src/java/pcgen/base/formula/base/FormulaFunction.java), [`VariableID.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/PCGen-Formula/code/src/java/pcgen/base/formula/base/VariableID.java), [`SimpleSolverManager.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/PCGen-Formula/code/src/java/pcgen/base/solver/SimpleSolverManager.java), [`SimpleOperatorLibrary.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/PCGen-Formula/code/src/java/pcgen/base/formula/inst/SimpleOperatorLibrary.java), [`FormatManager.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/PCGen-base/code/src/java/pcgen/base/util/FormatManager.java)*

## Related

- [Variables and formulas](../lst/concepts/variables-and-formulas.md) — the data side
- [The token system](token-system.md) — how `MODIFY` reaches this
- [Repository layout](architecture.md) — where the modules sit
