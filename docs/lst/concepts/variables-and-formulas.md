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

*Source: [`ModifyLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/ModifyLst.java)*

## Operators

| Operator | Works on |
|---|---|
| `SET` | any value type |
| `ADD` | numbers, and sets |
| `MULTIPLY` | numbers |
| `DIVIDE` | numbers |
| `MIN` | numbers |
| `MAX` | numbers |

`SET` is by far the most used — about 1,726 uses in shipped data against 181 for `ADD`.
The rest are rare enough that shipped data barely demonstrates them.

Each operator is a separate class under `plugin/modifier/`. They are grouped by the
type of value they act on: `number`, `set`, `bool`, `string`, `dice`, `cdom`,
`orderedpair` and `dynamic`. Only `number` has the full arithmetic set.

*Source: [`plugin/modifier/`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/modifier)*

## PRIORITY

```
MODIFY:SomeVariable|ADD|2|PRIORITY=100
```

Controls the order modifiers are applied in. It is **the only association the system
recognises.** Anything else is rejected with an error naming the association, and the
same association twice on one tag is also rejected.

Priority defaults to 0 when not set.

*Source: [`AssociationUtilities.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/formula/AssociationUtilities.java)*

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
| `<grouping>` | which objects within that scope are affected |

The remaining three behave exactly as in `MODIFY`. PCGen rejects the line if the scope
name is not legal, or if it names the global scope.

*Source: [`ModifyOtherLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/ModifyOtherLst.java)*

## Scopes

A variable exists inside a scope rather than globally. `MODIFY` therefore validates the
variable name against the current scope. `MODIFYOTHER` has to name a scope before it
can name a variable.

Shipped data uses `MODIFYOTHER` with movement modes as the grouping, which is how
movement gets adjusted across a set of modes at once.

## Where the tags are legal

Both apply to objects that hold variables. In the [tag index](../reference/tag-index.md)
that is shown as `VarHolder`.

## What this page does not cover

Being honest about the edges, since there is no upstream documentation to check
against:

- **How variables get declared.** Game modes define them, and `DATACONTROL` and the
  `VARIABLE` file tags are involved. The exact declaration syntax is not covered here
  because it was not verified.
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
