---
title: The formula system
---

# The formula system

The formula system is two Gradle subprojects of its own, separate from the main source
tree. It is what `MODIFY` and `MODIFYOTHER` drive.

For the data-side view, see
[variables and formulas](../lst/concepts/variables-and-formulas.md).

## Two modules

`settings.gradle` is three lines, and two of them are this:

```groovy
include 'PCGen-base', 'PCGen-Formula'
```

| Module | Holds | Java files |
|---|---|---|
| `PCGen-base` | generic utilities with no formula knowledge — collections, format managers, maths, graphs | ~210 |
| `PCGen-Formula` | the formula language itself — parser, visitors, scopes, solver | ~215 |

The split is deliberate. `PCGen-base` knows nothing about formulas, and `PCGen-Formula`
knows nothing about PCGen's game objects. PCGen glues both to its own model in
`pcgen/cdom/formula/` and `pcgen/rules/context/VariableContext.java`.

!!! note "Not in a default sparse checkout"
    Both directories are real, but they are easy to miss. A sparse checkout scoped to
    `code/src` excludes them entirely, which makes it look as though the formula system
    has no source. Add them explicitly.

## The language is generated

`PCGen-Formula/code/src/` has three source roots, not one:

| Root | Is |
|---|---|
| `javacc` | the grammar |
| `jjtree` | the syntax tree definition |
| `java` | hand-written code, plus the generated parser |

So the formula language has a real grammar rather than being parsed by hand. That is
why formula syntax is stricter and more consistent than tag argument syntax.

## Packages worth knowing

Under `PCGen-Formula/code/src/java/pcgen/base/formula/`:

| Package | Holds |
|---|---|
| `base` | the contracts — `VariableID`, `VariableLibrary`, `FormulaFunction`, `EvaluationManager` |
| `parse` | the generated tree nodes |
| `visitor` | the passes over that tree |
| `inst` | concrete implementations |
| `function`, `library`, `factory`, `analysis` | supporting pieces |

## From string to value

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

## Scopes

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

## Functions

`code/src/java/plugin/function/` holds eight functions available inside formulas:

| Function | Does |
|---|---|
| `getFact` | read a `FACT` |
| `Get`, `getOther` | read a variable, from this object or another scope |
| `Lookup` | look a value up in a table |
| `Group` | the objects matching a group or type |

Plus `ListAll`, `key` and `INPUT`.

These are registered by the same plugin mechanism as tags — see
[plugin loading](plugin-loading.md).

## How the solver orders modifiers

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

## Related

- [Variables and formulas](../lst/concepts/variables-and-formulas.md) — the data side
- [The token system](token-system.md) — how `MODIFY` reaches this
- [Repository layout](architecture.md) — where the modules sit
