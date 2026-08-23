---
title: Declaring a variable
---

# Declaring a variable

`DEFINE` creates a variable on an object. Other tags can then read it, and `BONUS:VAR`
can change it.

This is the older of PCGen's two variable systems, and the one shipped data uses.
Shipped data writes `DEFINE:` **37,178** times.

## The one form to write

```
Sample Feat	CATEGORY:FEAT	TYPE:General	DEFINE:TestPower|0
```

Declare the variable at zero. Supply the value with a separate bonus.

**37,076 of those 37,178 uses — 99.7% — are exactly this shape.** Treat any other form
as something to read, not something to write.

*Source: [`DefineLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/DefineLst.java)*

## Declare, then bonus

The two tags are a pair. Neither does the job alone:

```
Sample Feat	CATEGORY:FEAT	TYPE:General	DEFINE:TestPower|0	BONUS:VAR|TestPower|2
```

`DEFINE` says the variable exists. `BONUS:VAR` moves it. A formula elsewhere reads
`TestPower` and gets 2.

`BONUS:VAR` is the most-used bonus subtype in shipped data. [Bonuses](bonuses.md) owns
the subtype table.

## The trap: a bonus to an undeclared variable does nothing

**`BONUS:VAR` is applied only when the variable was declared.** This is the failure
worth knowing before you write either tag.

Reading a variable runs in two steps. PCGen looks the name up as a declared key. When it
finds one, it resolves the declared value and **then** adds the `VAR` bonuses. When it
finds nothing, it falls back to evaluating the name as a formula, and bonuses are
skipped entirely.

So a `BONUS:VAR|TestPower|2` with no matching `DEFINE:TestPower|0` anywhere in the loaded
data contributes nothing. Nothing is logged. The number is lower than intended, and nothing says why.

*Source: [`PlayerCharacter.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/PlayerCharacter.java)*

## Declarations do not stack

Two objects may declare the same variable. The declared values do not add up.

When a formula reads the variable, PCGen resolves every declaration and keeps the
**highest** one. Three objects each declaring `DEFINE:TestPower|0` still give zero.
Output sheets can ask for the lowest instead, with `VAR.MIN`.

Bonuses behave the other way. That is the point of declaring at zero. The declaration
sets a floor, and bonuses accumulate on top of it under the normal stacking rule.

*Source: [`VariableFacet.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/analysis/VariableFacet.java)*

## What breaks

**A missing second argument.** `DEFINE:TestPower` fails with `varName|varFormula or
LOCK.<stat>|value syntax requires an argument`.

**An empty name.** `DEFINE:|0` fails with `Empty Variable Name found in DEFINE`.

**More than one argument.** `DEFINE:TestPower|0|2` fails with `syntax requires only one
argument`.

**An invalid formula.** The value is parsed before it is stored. A formula that will not
parse fails the line with `Formula in DEFINE was not valid`.

**A non-zero value.** It still loads, but logs a deprecation notice telling you to use a
`DEFINE` of 0 and a bonus. `MAXLEVELSTAT=` is the one exemption.

**An object that cannot hold variables.** `DEFINE` on an `Ungranted` object type fails
outright.

## Forms that no longer work

`DEFINE:LOCK.` and `DEFINE:UNLOCK.` are both rejected at parse time. Each names its
replacement in the error, and both point at `DEFINESTAT`.

[What changed](../../appendix/whats-changed.md) carries the detail. Do not write either
form in new data.

## Where to look

| Task | Class |
|---|---|
| the `DEFINE:` tag | `plugin/lsttokens/DefineLst.java` |
| the `BONUS:VAR` subtype | `plugin/bonustokens/Var.java` |
| reading a variable, and when bonuses apply | `pcgen/core/PlayerCharacter.java`, `getVariable` |
| combining several declarations | `pcgen/cdom/facet/analysis/VariableFacet.java` |

## Related

- [Bonuses](bonuses.md) — `BONUS:VAR`, and the stacking rule that decides what adds up
- [Variables and formulas](variables-and-formulas.md) — the newer system, `MODIFY` and `MODIFYOTHER`
- [The rules engine](../../internals/rules-engine.md) — two formula systems, and where each keeps its values
- [The formula system](../../internals/formula-system.md) — JEP, its fourteen functions and its closed term vocabulary
- [What changed](../../appendix/whats-changed.md) — the deprecated `DEFINE` forms
