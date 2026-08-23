---
title: The character model
---

# The character model

Loaded game data lives in [`CDOMObject` instances](cdom-model.md). A character is a
different thing: a set of choices, plus everything those choices imply. PCGen holds it
in 234 facet classes, and almost none of it in the character object.

All paths are relative to the PCGen repository root, at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa).

## PlayerCharacter holds a number

`PlayerCharacter.java` is 9,910 lines, which suggests it holds the character. It does
not. It holds an identifier and about 107 facet references:

```java
private final RaceFacet raceFacet = FacetLibrary.getFacet(RaceFacet.class);
```

*Source: [`PlayerCharacter.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/PlayerCharacter.java)*

Its methods are mostly thin. `setRace` calls a facet and then recalculates bonuses.

The identifier is a `CharID`:

```java
public final class CharID implements TypeSafeConstant, PCGenIdentifier
```

*Source: [`CharID.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/enumeration/CharID.java)*

## Where the state actually is

One static map, at the root of the facet hierarchy:

```java
private static final DoubleKeyMap<PCGenIdentifier, Class<?>, Object> CACHE
```

*Source: [`AbstractStorageFacet.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/base/AbstractStorageFacet.java)*

Keyed by character and by facet class. So a facet is a singleton holding no fields of
its own. Asking it for a value means passing the `CharID` of the character you mean:

```java
raceFacet.get(id)
```

Two characters open at once share every facet object and keep separate slots in that
map.

`copyContents` is abstract on the storage base, so each facet must state how its data
is copied. Cloning a character otherwise shares mutable structures between the copy and
the original.

## The shapes of facet

Fourteen base classes in `pcgen/cdom/facet/base/`. Four cover most cases.

| Base | Holds | Example |
|---|---|---|
| `AbstractItemFacet` | one value or none | `RaceFacet`, `DeityFacet` |
| `AbstractListFacet` | several values, no source tracking | `LanguageFacet` |
| `AbstractSourcedListFacet` | several values, remembering what granted each | `CDOMObjectConsolidationFacet` |
| `AbstractQualifiedListFacet` | the same, for things gated by prerequisites | ability facets |

Source tracking is the interesting one. If a race and a template both grant the same
language, a sourced list holds one entry with two sources. It reports the addition once,
and reports removal only when the last source goes away.

That is what stops a character losing a language they still have another reason to know.

### The other ten

The fourteen form a tree, and the split that matters is one level up.
`AbstractStorageFacet` stores. `AbstractDataFacet` extends it and adds the event
broadcast. **A facet that does not extend `AbstractDataFacet` cannot be listened to.**

| Base | Extends | Holds |
|---|---|---|
| `AbstractStorageFacet` | — | the root. Cache access, and nothing else |
| `AbstractDataFacet` | storage | the root of everything that fires events |
| `AbstractSingleSourceListFacet` | data | several values, each with exactly one source |
| `AbstractItemConvertingFacet` | data | several values, converted on the way in |
| `AbstractCNASEnforcingFacet` | data | ability selections, with their own ordering rules |
| `AbstractScopeFacet` | storage | values keyed by a scope as well as an id |
| `AbstractAssociationFacet` | scope | one association per source |
| `AbstractSubScopeFacet` | storage | the same, two scopes deep |
| `AbstractSubAssociationFacet` | scope | one association, two scopes deep |
| `AbstractScopeFacetConsolidator` | list | flattens a scoped facet into a plain list |

The difference between `AbstractSourcedListFacet` and `AbstractSingleSourceListFacet` is
the one to get right. Both track where a value came from. The single-source version
assumes one owner and replaces it. The sourced version keeps a set, and that is what
makes the removal behaviour above work.

## Adding a facet

Four things, in order:

1. **Pick the base by how the value is held**, not by what it means. One or none, a
   list, a list with sources, a list gated by prerequisites.
2. **Implement `copyContents(source, copy)`.** It is the one abstract method on
   `AbstractStorageFacet`. Copying a character calls it, and the contract is a deep
   copy — after it returns, changing one character must not touch the other.
3. **Register it with Spring**, so `FacetLibrary` finds a bean rather than falling back
   to reflection and logging an error.
4. **Wire the listeners** in `FacetInitialization`, by hand, alongside the other fifty.

*Source: [`AbstractStorageFacet.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/base/AbstractStorageFacet.java)*

## Getting a facet

```java
FacetLibrary.getFacet(RaceFacet.class)
```

The library looks in its own map first, then asks Spring for a bean. Only if Spring has
no bean does it construct the class by reflection, and it logs an error when it does.
Spring wiring is the intended path.

*Source: [`FacetLibrary.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/FacetLibrary.java)*

## How facets are wired together

Facets react to each other through events. The wiring itself is not annotations or
configuration — it is a long method that runs once at startup:

```java
raceFacet.addDataFacetChangeListener(bioSetTrackingFacet);
raceFacet.addDataFacetChangeListener(charObjectFacet);
```

*Source: [`FacetInitialization.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/FacetInitialization.java)*

Around fifty facets are fetched and connected there by hand. Reading that method is the
fastest way to see the dependency graph.

### The order events arrive in

Listeners are held in a `TreeMap` keyed by an integer priority, so priorities fire in
ascending order. Within one priority, listeners fire in the order they registered — the
list is built by prepending and read back to front.

Almost everything uses the default priority of zero. Four places do not, and they are
the ordering rules of the character model stated in code:

| Priority | Facet | Why it waits |
|---|---|---|
| 1 | `NaturalEquipSetFacet` | after natural weapons exist |
| 1000 | `BonusActiviationFacet` | after the granting facets have run |
| 2000 | `MovementResultFacet` | after bonuses are active |
| 5000 | `CalcBonusFacet` | last, once everything else settled |

A new listener at the default priority runs before all four. If it depends on bonuses
being active, it needs a number above 1000.

*Source: [`AbstractDataFacet.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/base/AbstractDataFacet.java)*

The event contract is two methods and two constants:

```java
public interface DataFacetChangeListener<IDT, T>
{
    void dataAdded(DataFacetChangeEvent<IDT, T> dfce);
    void dataRemoved(DataFacetChangeEvent<IDT, T> dfce);
}
```

*Source: [`DataFacetChangeListener.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/event/DataFacetChangeListener.java)*

## A worked trace: setting a race

```mermaid
flowchart TD
    A["PlayerCharacter.setRace"] --> B["RaceInputFacet.set<br/><i>resolve any CHOOSE</i>"]
    B --> C["RaceFacet.set<br/><i>stores it, fires DATA_ADDED</i>"]
    C --> D["BioSetTrackingFacet<br/><i>age, height, weight</i>"]
    C --> E["CharacterConsolidationFacet<br/><i>all native objects</i>"]
    E --> F["CDOMObjectConsolidationFacet<br/><i>plus equipment-borne</i>"]
    F --> G["VisionFacet, NaturalWeaponProfFacet,<br/>ArmorProfFacet, VarScopedFacet, ..."]
```

1. `PlayerCharacter.setRace` calls `raceInputFacet.set(id, race)`.
2. `RaceInputFacet` resolves a `CHOOSE:` on the race if there is one, then calls
   `RaceFacet.set`.
3. `RaceFacet` stores the value and fires `DATA_ADDED`.
4. `BioSetTrackingFacet` updates age, height and weight for the new race.
5. `CharacterConsolidationFacet` folds the race into one list of every game object the
   character has natively, and fires its own event.
6. `CDOMObjectConsolidationFacet` merges that list with objects coming from equipment,
   and fires again.
7. Everything derived listens to that last one: vision, natural weapons, armour
   proficiencies, special abilities, variable scopes.

`PlayerCharacter` orchestrates none of steps 4 to 7. It calls one facet and then
recalculates bonuses.

The two consolidation facets carry the closest thing to a stated reason for the
design. Gathering every object into one place lets a downstream facet listen to a
single source. Without it, each would need to know every kind of thing that grants
something.

*Source: [`CDOMObjectConsolidationFacet.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/CDOMObjectConsolidationFacet.java)*

There is no design document, no `package-info.java` and no note in `AGENTS.md`
explaining the architecture as a whole. The class comments are what exists.

## CharacterDisplay

`CharacterDisplay` is a read-only view over the same facet cache. It holds a `CharID`,
reads about forty facets, and exposes queries with no setters.

*Source: [`CharacterDisplay.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/display/CharacterDisplay.java)*

Output tokens, term evaluators and prerequisite tests go through
`PlayerCharacter.getDisplay()` rather than the character itself. Anything that only
reads should do the same.

## What this means when you change something

**A value is wrong on the sheet.** Find the facet that owns it, not the place the tag
was parsed. The tag stored data on a `CDOMObject` long before this point.

**Something is not appearing after a choice.** Check the listener wiring in
`FacetInitialization`. A facet with no registered listener silently does nothing.

**A new derived value needs adding.** The pattern is a new facet listening to
`CDOMObjectConsolidationFacet`, registered in `FacetInitialization` and fetched through
`FacetLibrary`.

## Related

- [The object model](cdom-model.md) — what facets store
- [The interface layer](ui-layer.md) — how the window reads a character
- [Output and saving](output-and-saving.md) — what reads through `CharacterDisplay`
- [Load pipeline](load-pipeline.md) — where the objects came from
