---
title: How a chooser resolves
---

# How a chooser resolves

A `CHOOSE:` tag is a string. Turning it into a list the player picks from takes two
stages. A parse at load time builds the set. A manager at selection time presents it.

[Choosers](../lst/concepts/choosers.md) owns the tag syntax. This page is the code path
behind it.

## The grammar is two operators

`ChoiceSetLoadUtilities.getChoiceSet` splits the argument twice:

| Separator | Means |
|---|---|
| `\|` | or |
| `,` | and |

Pipes are split first, then each part is split on commas. Terms joined by commas become a
`CompoundAndPrimitive`. The results are then joined as alternatives.

So `SKILL|TYPE=Lore,TYPE=Int` reads as one alternative that must satisfy both types,
not as two alternatives.

Both splits respect grouping pairs, `[]` and `()`, so a bracketed argument may contain
either separator without being cut.

*Source: [`ChoiceSetLoadUtilities.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/rules/persistence/ChoiceSetLoadUtilities.java)*

## Four kinds of term

Each comma-separated term is resolved in a fixed order. A qualifier is tried first, and a
primitive only if that fails.

| Written | Becomes |
|---|---|
| `Sample Skill` | a single reference |
| `TYPE=Lore` | a group reference. See [types](../lst/concepts/types.md) |
| `!TYPE.Lore` | a `NegatingPrimitive` wrapping the group |
| `PC[...]`, `CLASS[...]` | a qualifier |

A term that resolves to neither logs `Choice argument was not valid` and the whole set
returns nothing.

## Primitives and qualifiers

Both are plugins, registered the same way as [LST tokens](plugin-loading.md), and both
implement `PrimitiveCollection`. The difference is what they are given.

```java
public interface PrimitiveToken<T> extends LstToken, PrimitiveCollection<T>
{
    boolean initialize(LoadContext context, Class<T> cl, String value, String args);
}

public interface QualifierToken<T extends CDOMObject> extends LstToken, PrimitiveCollection<T>
{
    boolean initialize(LoadContext context, SelectionCreator<T> cl, String condition,
                       String value, boolean negated);
}
```

A primitive narrows by a property of the object. A qualifier narrows by the character's
relationship to it, and knows whether it was negated.

**21 primitives across 10 target types:**

| Target | Primitives |
|---|---|
| spell | 9 — school, subschool, descriptor, class list, domain list, spell book, type, prohibited, all |
| race | 3 — race type, race subtype, base size |
| pcclass | 2 — class, spellcaster |
| pobject | 2 — ability, feat |
| weaponprof | 2 — deity weapon, type |
| deity, domain, equipment, language, skill | 1 each |

**19 qualifiers across 13 target types.** `PC[...]` appears for nine of them and means
what the character already has. Skills carry the most: class, cross-class, exclusive, no
rank, and ranks.

*Source: [`PrimitiveToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/rules/persistence/token/PrimitiveToken.java)*

## Combining sets

`pcgen/cdom/choiceset/` holds thirteen implementations. Three shapes matter:

| Class | Is |
|---|---|
| `ReferenceChoiceSet` | the plain case, a set of references |
| `CompoundAndChoiceSet`, `CompoundOrChoiceSet` | the two operators above, as objects |
| `QualifiedDecorator` | wraps a set so prerequisites are tested per option |

`ModifyChoiceDecorator` and `CollectionToAbilitySelection` handle the ability cases, where
a choice produces a category and nature as well as an object.

## At selection time

`ChooserUtilities` picks a manager for the choice, and `CDOMChoiceManager` runs it: build
the list, remove what the character cannot take, ask, then apply.

`NoChoiceManager` covers `CHOOSE:NOCHOICE`, where nothing is asked and the object is
granted outright. `UserInputManager` covers the free-text case.

Two controllers adjust the rules for particular kinds of choice.
`AbilityChooseController` and `SkillChooseController` decide how many picks are allowed
and whether a repeat is permitted.

## What this means when you change something

**A new primitive is a plugin class, not a change to the parser.** Implement
`PrimitiveToken`, register it, and it becomes available in every `CHOOSE:` that targets
that type.

**Negation is not uniform.** The chooser path builds a `NegatingPrimitive` for `!TYPE.`,
while an ordinary object reference rejects the same text. That asymmetry is
[on the types page](../lst/concepts/types.md), which owns it.

**The tests are the specification.** `code/src/test/plugin/primitive/` has 21 files and
`plugin/qualifier/` has 19, one per class.

## What bites when you change a choice

### A selection is keyed by object identity

`AssociationSupport` holds both of its maps as `IdentityHashMap`s keyed on the owner
instance. `CNAbilityFactory` exists to intern `CNAbility` objects so this works at all,
and `Globals.emptyLists()` resets that interning.

Hand `restoreChoice` an owner that is equal but not identical and the selection lands
under a key nothing reads. No exception. The choice is gone.

### A saved selection re-attaches only on an identical unparse string

Restoring an `ADD:` selection compares the string in the `.pcg` file against
`choices.getLSTformat()` with `equals`. Change how a choice set unparses and every
existing character file fails to match, with a warning rather than an error.

This is the constraint that blocks changing unparse output. It is not only the token
tests.

### The dialog is skipped using the unfiltered count

`ConcreteTransitionChoice.driveChoice` returns early when the number of picks equals
`set.size()`. That size is the raw set, not the qualifier-filtered list it returns. Add a
filter and PCGen can auto-grant the shortened list without asking.

The interface has a matching case: with the single-choice preference set, a one-item list
commits and returns before the dialog is shown. A change that narrows an offer to one
turns into a silent grant.

### An item missing from the set is dropped without a message

`CDOMChoiceManager` applies a choice only when `info.getSet(pc).contains(item)`, an
`equals` test. A primitive that returns freshly built value objects without `equals` and
`hashCode`, or a `getSet` that recomputes differently between calls, makes every
selection vanish.

*Source: [`AssociationSupport.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/AssociationSupport.java), [`PCGVer2Parser.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/PCGVer2Parser.java), [`ConcreteTransitionChoice.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/base/ConcreteTransitionChoice.java), [`CDOMChoiceManager.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/chooser/CDOMChoiceManager.java)*

## Where to look

| Task | Class |
|---|---|
| parsing a `CHOOSE:` argument | `pcgen/rules/persistence/ChoiceSetLoadUtilities.java` |
| the primitive contract | `pcgen/rules/persistence/token/PrimitiveToken.java` |
| the qualifier contract | `pcgen/rules/persistence/token/QualifierToken.java` |
| set implementations | `pcgen/cdom/choiceset/` — 13 classes |
| running a choice | `pcgen/core/chooser/CDOMChoiceManager.java` |
| accepted and rejected syntax | `code/src/test/plugin/{primitive,qualifier}/` — 40 tests |

## Related

- [Choosers](../lst/concepts/choosers.md) — the `CHOOSE:` tag itself
- [Types](../lst/concepts/types.md) — `TYPE=` groups, and where negation works
- [Plugin loading](plugin-loading.md) — how primitives and qualifiers are registered
- [The token system](token-system.md) — the same dispatch, for LST tags
- [Granting things](../lst/concepts/granting.md) — `%LIST`, which reads a chooser's result
