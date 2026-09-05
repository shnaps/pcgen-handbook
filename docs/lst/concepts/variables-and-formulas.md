---
title: Variables and formulas
---

# Variables and formulas

PCGen 6.07 added a formula system built around named variables and modifiers that act
on them. Its two main tags are `MODIFY` and `MODIFYOTHER`.

!!! warning "Not in the official documentation"
    `MODIFY` and `MODIFYOTHER` are implemented on `master` and appear nowhere in
    PCGen's published tag documentation. Everything on this page was read from the
    source and checked against shipped data.

    That also means there is no upstream reference to fall back on. Where this page
    says something is unverified, it means exactly that.

## What it is for

The older way to adjust a number is `BONUS`. It works, and most shipped data still
uses it. The formula system is a separate mechanism: you declare a variable, then
modify it with an explicit operator and an explicit ordering.

The practical difference is control. `MODIFY` states which operation applies and, when
it matters, in what order relative to other modifiers.

## MODIFY

```
MODIFY:<variable>|<operator>|<instructions>[|PRIORITY=<n>]
```

Three required arguments, separated by `|`. A real line from shipped data:

```
MODIFY:ItemLevel|SET|2
```

| Argument | Is |
|---|---|
| `<variable>` | the variable name. Must be legal in the current scope. |
| `<operator>` | what to do. See the table below. |
| `<instructions>` | the value or formula to apply |
| `PRIORITY=<n>` | optional, controls ordering |

Square brackets and parentheses group, so a formula containing `|` inside them is not
split by the argument separator.

*Source: [`ModifyLst.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/ModifyLst.java)*

## Operators

| Operator | Works on |
|---|---|
| `SET` | any value type |
| `ADD` | numbers, and sets |
| `MULTIPLY` | numbers |
| `DIVIDE` | numbers |
| `MIN` | numbers |
| `MAX` | numbers |

`SET` is by far the most used — 1,703 uses in shipped data against 142 for `ADD`.
The rest are rare enough that shipped data barely demonstrates them.

Each operator is a separate class under `plugin/modifier/`. They are grouped by the
type of value they act on: `number`, `set`, `bool`, `string`, `dice`, `cdom`,
`orderedpair` and `dynamic`. Only `number` has the full arithmetic set.

*Source: [`plugin/modifier/`](https://github.com/PCGen/pcgen/tree/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/modifier)*

## PRIORITY

```
MODIFY:SomeVariable|ADD|2|PRIORITY=100
```

Controls the order modifiers are applied in. It is **the only association the system
recognises.** Anything else is rejected with an error naming the association, and the
same association twice on one tag is also rejected.

Priority defaults to 0 when not set.

*Source: [`AssociationUtilities.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/cdom/formula/AssociationUtilities.java)*

## MODIFYOTHER

Same idea, but it reaches into a different scope and applies to a group of objects
there.

```
MODIFYOTHER:<scope>|<grouping>|<variable>|<operator>|<instructions>[|PRIORITY=<n>]
```

Two extra arguments in front:

| Argument | Is |
|---|---|
| `<scope>` | the scope to reach into. **Must not be the global scope.** |
| `<grouping>` | which objects within that scope are affected. Three forms, below. |

The remaining three behave exactly as in `MODIFY`. PCGen rejects the line if the scope
name is not legal, or if it names the global scope.

*Source: [`ModifyOtherLst.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/ModifyOtherLst.java)*

## The grouping argument

`<grouping>` picks the objects inside the scope. It takes one of three forms, and each
form is a separate class under `plugin/grouping/`. Written plain, with no bracket after
it, each form yields the objects it matches:

| Form | Affects | Matched against |
|---|---|---|
| `ALL` | every object in the scope | nothing |
| `KEY=<key>` | the one object with that key | the object key, exactly |
| `GROUP=<label>` | objects whose `GROUP:` tag carries that label | the label, exactly |

A bare name with no `=` means `KEY`. `getDynamicGroup` falls back to `KEY` for anything
that is not the literal `ALL`, so these two lines do the same thing:

```
MODIFYOTHER:PC.MOVEMENT|Walk|Speed|SET|30
MODIFYOTHER:PC.MOVEMENT|KEY=Walk|Speed|SET|30
```

All **192** `MODIFYOTHER` fields in shipped data use the bare form. `ALL` and `GROUP=`
appear in the token test and nowhere in the data.

`GROUP=` is the only reason a data author writes the [`GROUP:` tag](types.md#group-is-a-second-label-list).

Every form also accepts a bracketed child: `ALL[ALL]`, `KEY=Walk[ALL]`. A child changes
what the grouping yields. The matched object is not passed on — its children are, and the
child grouping is applied to those. `ModifyOtherLst` protects `[` and `]` from the `|`
split, so a child may contain either.

No shipped line uses a child, and this handbook has not verified how the child's object
type resolves past one level. It is part of the grammar, not part of what is documented
here.

**What breaks.** Ending the grouping at the `=`, as in `KEY=`, fails in the parser. The
log carries `Error in parsing Group: Expected target after '=', but string ended`, then
`MODIFYOTHER unable to build group from: KEY=`. Writing a value after `ALL` fails
somewhere else — the grouping class throws `Instructions using = prohibited for ALL
Grouping`, which `getGrouping` does not catch, so the second message never appears.

*Source: [`plugin/grouping/`](https://github.com/PCGen/pcgen/tree/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/grouping), [`GroupingInfoFactory.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/cdom/grouping/GroupingInfoFactory.java), [`ChoiceSetLoadUtilities.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/rules/persistence/ChoiceSetLoadUtilities.java), [`ModifyOtherLstTest.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/test/plugin/lsttokens/ModifyOtherLstTest.java)*

## Scopes

A variable exists inside a scope rather than globally. `MODIFY` therefore validates the
variable name against the current scope. `MODIFYOTHER` has to name a scope before it
can name a variable.

Shipped data reaches into one scope only. All **192** `MODIFYOTHER` fields name
`PC.MOVEMENT` and pick a single movement mode by key, 189 of them `Walk`. Nothing in the
data modifies a set of modes at once.

## Seeing what a variable resolved to

PCGen ships a debugger for this system and does not advertise it. It is **Tools > View
Solver Process**, and it has no keyboard shortcut.

Four controls, and the third catches people out:

| Control | Set it to |
|---|---|
| character | which loaded character to inspect |
| scope | the scope the variable lives in |
| object | the object holding it, needed for any scope but global |
| variable name | the name itself |

Leave the object unset in a non-global scope and the table empties. A name that matches
nothing does not clear the table at all. It logs an error you will not see and leaves the
previous variable's rows on screen. Check the name before you trust what you are reading.

What it lists is every modifier applied to that variable, in the order they were applied:

| Column | Shows |
|---|---|
| Modification Type | the kind of modifier |
| Modification | its instructions |
| Resulting Value | the value after that step |
| Priority | the solver's ordering key |
| Source | where the modifier came from |

The first row is always the default value rather than a modifier from your data.

Reading Resulting Value down the table is the technique. It answers which modifier made
the number wrong, which is the question a `MODIFY` bug actually raises.

Treat the Priority column as an ordering key and not as your `PRIORITY` value. It is a
composite of the priority you set and the modifier's own inherent priority, so
`PRIORITY=100` does not show as 100.

It covers this system only. Solver View reads the newer engine, so a variable declared
with `DEFINE` and fed by `BONUS:VAR` does not appear here at all. Those have no inspector
— see [declaring a variable](declaring-variables.md).

## Where the tags are legal

Both apply to objects that hold variables. In the [tag index](../reference/tag-index.md)
that is shown as `VarHolder`.

## What this page does not cover

Being honest about the edges, since there is no upstream documentation to check
against:

- **How variables get declared for this system.** Game modes define them, and
  `DATACONTROL` and the `VARIABLE` file tags are involved. The exact declaration syntax
  is not covered here because it was not verified. The older system declares with
  `DEFINE` — see [declaring a variable](declaring-variables.md).
- **Formula syntax itself.** What may appear in `<instructions>` is a language of its
  own, implemented in the separate `PCGen-Formula` module.
- **When to prefer this over `BONUS`.** Most shipped data still uses `BONUS`. There is
  no upstream guidance on migration, and this handbook will not invent any.

## Related

- [The formula system](../../internals/formula-system.md) — how it works underneath
- [Tag index](../reference/tag-index.md) — every current tag
- [What changed](../../appendix/whats-changed.md) — including this as an undocumented addition
- Video: [Formula System ORDEREDPAIR](https://www.youtube.com/watch?v=Oicxs-dI7gU) covers
  an early piece of this system, recorded around 6.06
