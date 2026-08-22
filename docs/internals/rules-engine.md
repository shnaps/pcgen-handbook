---
title: The rules engine
---

# The rules engine

How a number on the character sheet is produced. The data is loaded, the choices are
made, and something has to turn that into "your skill total is 11".

That something is not one class. It is a bonus map rebuilt from scratch on every
change, and two formula systems running side by side. Around them sits a loop that
repeats until the answer stops moving.

All paths are relative to the PCGen repository root, at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa).

## Two formula systems, both live

| System | Evaluates | Reached from |
|---|---|---|
| JEP | the older formula strings | `DEFINE:`, and the value field of `BONUS:` |
| PCGen-Formula | the newer variable system | `MODIFY:` and `MODIFYOTHER:` |

Which one runs is decided **when the tag is parsed**, not at runtime. `DEFINE:` builds a
`JEPFormula`; `MODIFY:` builds a modifier registered with a `SolverManager`. There is no
dispatcher choosing between them later.

*Source: [`FormulaFactory.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/base/FormulaFactory.java)*

Every character carries both. See [the formula system](formula-system.md) for the newer
one and [variables and formulas](../lst/concepts/variables-and-formulas.md) for the data
author's view.

## Nothing is incremental

There is no dirty flag that lets PCGen skip work. Adding a level, equipping an item,
setting a stat, or loading a character all call the same method, and it rebuilds the
whole bonus map:

```java
public void calcActiveBonuses()
```

*Source: [`PlayerCharacter.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/PlayerCharacter.java)*

Most callers invoke it explicitly. Only race changes trigger it through a listener, and
`CalcBonusFacet` carries a comment saying the other paths were left explicit on purpose.

## The convergence loop

This is the part that surprises people. `calcActiveBonuses` does not compute once. It
computes repeatedly until the result stops changing.

The reason is written in the source, and nowhere else. One variable can carry a
prerequisite that depends on a second variable. That second value is not correct until
the map is finished, so the first pass can be wrong.

Each pass checkpoints the map, rebuilds, and compares. If it has not settled after 29
passes it logs an error, and after 31 it gives up:

```text
Active bonus loop exceeded reasonable limit of 29.
```

Data can cause that. A prerequisite that depends on a value that depends on the
prerequisite never settles, and the character ends up with whatever the last pass
produced.

If you see that line in a log, it is a data problem, not a program fault.

## The bonus pass

Inside each pass, `BonusManager.buildActiveBonusMap` runs in two stages:

1. **Static bonuses first.** Anything whose value is a plain number is applied directly.
2. **Everything else, recursively.** A bonus whose value is a formula may depend on
   another bonus. `processBonus` resolves those dependencies first, guarding against
   cycles with a set of bonuses already seen.

*Source: [`BonusManager.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/BonusManager.java)*

The result is a map keyed by strings that encode the whole target:

```text
COMBAT.AC:Armor
COMBAT.AC:Armor.REPLACE
SKILL.TYPE.KNOWLEDGE
```

The bonus type is part of the key, which is how the
[stacking rules](../lst/concepts/bonuses.md) are enforced: same key, one winner; no
type, its own key.

Reading back goes through `getTotalBonusTo`, which builds a prefix and sums every
matching key.

## Prerequisites are re-tested every pass

A `PRExxx` on a bonus is not evaluated once at load. `getAllActiveBonuses` re-tests
every bonus's prerequisites on every rebuild.

A bonus that stops qualifying is absent from the next map. There is no
deactivation event and nothing is logged. The number changes and nothing says why.

`AppliedBonusFacet` tracks which bonuses currently apply, keyed by character.

*Source: [`AppliedBonusFacet.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/AppliedBonusFacet.java)*

## Two variable stores

Matching the two formula systems, variable values live in two different places.

| Written as | Stored in | Read through |
|---|---|---|
| `DEFINE:` | a `VariableKey` on the object, then `VariableFacet` | `PlayerCharacter.getVariable` |
| `MODIFY:` | a variable store inside `SolverManager` | `VariableContext` |

They are not the same store, and one does not see the other. That is the single most
useful thing to know when a `MODIFY:` value and a `DEFINE:` value of the same name
disagree.

*Source: [`SolverManagerFacet.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/SolverManagerFacet.java)*

The newer store is push-based: adding a modifier processes the affected variable
immediately. The older one is rebuild-and-poll.

## Worked trace: a skill total

```mermaid
flowchart TD
    A["PCSkillTotalTermEvaluator.resolve"] --> B["SkillRankControl.getTotalRank<br/><i>ranks, clamped</i>"]
    A --> C["SkillModifier.modifier"]
    C --> D["stat modifier"]
    C --> E["getTotalBonusTo SKILL.STAT.x"]
    C --> F["getTotalBonusTo SKILL.&lt;name&gt;"]
    C --> G["getTotalBonusTo SKILL.TYPE.x"]
    C --> H["armour check penalty"]
    B --> I["total"]
    C --> I
```

1. `PCSkillTotalTermEvaluator.resolve` is the entry point.
2. `SkillRankControl.getTotalRank` returns ranks plus rank bonuses, clamped to the
   maximum.
3. `SkillModifier.modifier` sums the stat modifier, then several bonus lookups: by stat,
   by skill name, by skill type, by list, plus the armour check penalty.
4. The two are added.

*Source: [`SkillModifier.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/analysis/SkillModifier.java)*

Every one of those bonus lookups reads the map built above. If a number is wrong, it is
wrong either in the ranks or in one key of that map, and the map is inspectable.

## Caching

| Cache | Holds | Cleared by |
|---|---|---|
| `cachedActiveBonusSumsMap` | summed results of `getTotalBonusTo` | every map rebuild |
| `VariableProcessor` cache | evaluated variable values | a serial number bumped by `setDirty` |

Both are invalidated aggressively. Neither survives a recalculation, which is part of
why the engine can afford to have no dirty tracking.

## Rule toggles take part

The convergence loop itself checks a house rule:

```java
if (Globals.checkRule(RuleConstants.RETROSKILL))
```

So an optional rule the reader ticked in preferences changes what runs inside the
calculation loop. See [rule toggles](../lst/concepts/rule-toggles.md).

## Where to put a breakpoint

| Method | Tells you |
|---|---|
| `PlayerCharacter.calcActiveBonuses` | how often recalculation runs, and whether it converges |
| `BonusManager.processBonus` | what a single bonus resolved to, and where a cycle was cut |
| `BonusManager.getTotalBonusTo` | which keys a lookup summed |
| `BonusManager.getAllActiveBonuses` | which bonuses failed their prerequisites |
| `SolverManagerFacet.addModifier` | anything driven by `MODIFY:` |

Start with the third. Most "wrong number" reports are a bonus that is present with the
wrong type, or absent because a prerequisite failed.

## Related

- [Bonuses](../lst/concepts/bonuses.md) — the data author's view of the map
- [The formula system](formula-system.md) — the newer of the two evaluators
- [The character model](facets.md) — where the inputs live
- [Rule toggles](../lst/concepts/rule-toggles.md) — optional rules the engine checks
