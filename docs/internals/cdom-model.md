---
title: The object model
---

# The object model

What a race, a skill or a feat actually is once PCGen has read it. Every one of them is
a `CDOMObject`, and none of them has a field for the tags you write.

Read [the token system](token-system.md) first. This page explains what those tokens
write into.

All paths are relative to the PCGen repository root, at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa).

## CDOMObject

`CDOMObject` is the base class for every loaded game object.

```java
public abstract class CDOMObject extends ConcretePrereqObject
    implements BonusContainer, Loadable, Reducible, PCGenScoped, VarHolder
```

*Source: [`CDOMObject.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/base/CDOMObject.java)*

It has two ordinary fields: the display name, and the URI of the file it was read from.
Everything else is stored in maps.

That is the design worth understanding. `Race` has no `hands` field. `Skill` has no
`keyStat` field. A tag writes its value into a map under a typed key, and reads it back
the same way.

## The keys

Each map takes one kind of key, and the key carries the value type.

| Key type | Holds | On `CDOMObject` |
|---|---|---|
| `IntegerKey` | one number | `getSafe(IntegerKey)`, `put(IntegerKey, Integer)` |
| `StringKey` | one string | `get(StringKey)`, `put(StringKey, String)` |
| `ObjectKey<T>` | one typed object, often a reference | `get(ObjectKey<T>)`, `put(ObjectKey<T>, T)` |
| `ListKey<T>` | an ordered list, duplicates allowed | `addToListFor`, `getSafeListFor` |
| `MapKey<K,V>` | a keyed map inside the object | `addToMapFor`, `get(MapKey, K)` |
| `FormulaKey` | one formula | `get(FormulaKey)` |
| `VariableKey` | a `DEFINE:` variable and its formula | `put(VariableKey, Formula)` |
| `FactKey<T>` | one `FACT:` value, resolved later | `get`, `getResolved` |
| `FactSetKey<T>` | a `FACTSET:` collection | `addToSetFor`, `getSafeSetFor` |

The accessors are generic and `final`, so no subclass can change how storage works:

```java
public final <OT> OT get(ObjectKey<OT> key)
public final <OT> OT put(ObjectKey<OT> key, OT value)
```

Every map starts null and is allocated on first write. An object that uses three tags
carries three small maps, not thirty empty fields.

### Tags picking keys

`RACE` files write the number of hands through an `IntegerKey`:

```java
protected IntegerKey integerKey() { return IntegerKey.CREATURE_HANDS; }
```

*Source: [`race/HandsToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/race/HandsToken.java)*

`TYPE:` adds to a list:

```java
context.getObjectContext().addToList(cdo, ListKey.TYPE, type);
```

*Source: [`TypeLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/TypeLst.java)*

`DEFINE:` creates a variable key from the name in the data, at load time:

```java
context.getObjectContext().put(obj, VariableKey.getConstant(firstItem), f);
```

*Source: [`DefineLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/DefineLst.java)*

## Why keys instead of fields

Adding a tag adds a class. It does not touch `CDOMObject`, and it does not touch the
class of the thing the tag applies to.

`IntegerKey`, `FactKey`, `FactSetKey` and `VariableKey` go further: they mint new
constants at run time from a name, through `getConstant`. That is how `FACTDEF` lets a
data set declare its own fields with no Java change at all.

`StringKey`, `ListKey` and `MapKey` have hand-declared constants, so a new one means
editing that key class. That is still one small central file rather than a field and a
pair of accessors on every game object.

## The concrete types

Most game objects go through one intermediate class:

```java
public class PObject extends CDOMObject
```

*Source: [`PObject.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/PObject.java)*

Extending `PObject`, in `pcgen/core/`: `Ability`, `Race`, `Skill`, `Equipment`,
`EquipmentModifier`, `Deity`, `Domain`, `Spell`, `PCTemplate`, `PCClass`, `Kit`,
`Language`, `WeaponProf`, `ArmorProf`, `PCStat`, `PCAlignment`, `SizeAdjustment`,
`Campaign`.

Extending `CDOMObject` directly, mostly in `pcgen/cdom/inst/`: `PCClassLevel`,
`EquipmentHead`, `CodeControl`, `GlobalModifiers`.

`PCClassLevel` is the one to know. A class line's per-level data becomes one object
per level. That is why `2` in a `CLASS` file's level line behaves like a record and
not like a number.

## Names and keys

Two identities, and data authors meet both.

| Java | From the file |
|---|---|
| `getDisplayName()` | field 0 of the line |
| `getKeyName()` | the `KEY:` tag, or field 0 when there is no `KEY:` |

```java
po.setName(colToken.nextToken());
```

*Source: [`GenericLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/GenericLoader.java)*

`setName` sets the display name. `getKeyName` reads `StringKey.KEY_NAME` and falls back
to the display name. So every object has a key whether or not the file
gives one. Setting `KEY:` is what lets you rename the display name later without
breaking references.

## Comparing two objects

Three ways to ask whether two objects are the same, and they do not agree.

| Method | Compares |
|---|---|
| `==` | identity. Two loads of the same file give two objects |
| `equals` | the key name, ignoring case |
| `isCDOMEqual` | every key, list and map the object holds |

`isCDOMEqual` is the deep one. `AbstractReferenceManufacturer` uses it to decide whether a
duplicate key is a real conflict. The token round-trip tests use it to prove a parse and
an unparse agree.

### equals and hashCode disagree

`PObject.equals` matches key names across **any** `PObject`, and the matching `hashCode`
is commented out:

```java
@Override
public boolean equals(final Object obj)
{
    return obj instanceof PObject && getKeyName().equalsIgnoreCase(((PObject) obj).getKeyName());
}

//Temporarily commented out since unit tests are badly behaved, see COD#E-1895
//	@Override
//	public int hashCode()
//	{
//		return getKeyName().hashCode();
//	}
```

Which way this bites depends on the type.

**Neither method overridden.** `PCClass`, `Deity`, `Domain`, `PCTemplate`, `Campaign` and
`Kit` take value equality from `PObject` and identity hashing from `Object`. Two objects
that are `equals` hash differently.

**A `hashCode` restored.** `Skill`, `Spell`, `Ability`, `Equipment`, `Language`,
`ArmorProf`, `ShieldProf` and `WeaponProf` override both, and `Race` overrides only the
`hashCode`. Every one returns `getKeyName().hashCode()`, which is case-sensitive, against
an `equals` that is not. A skill keyed `Sample Athletics` and one keyed `sample athletics`
are equal and hash to different buckets.

Nothing normalises case on the way in. `setKeyName` stores the string it is handed.

So do not use a CDOM object as a `HashMap` key or put one in a `HashSet`. The engine does
not either — `AbstractReferenceManufacturer` holds objects in a `KeyMap` keyed by string,
and tracks duplicates under a `CaseInsensitiveString` wrapper.

*Source: [`PObject.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/PObject.java), [`CDOMObject.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/base/CDOMObject.java), [`AbstractReferenceManufacturer.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/reference/AbstractReferenceManufacturer.java)*

## References

A tag naming another object cannot look it up while loading, because the target may not
have been read yet. Files load in an order nobody controls.

So tokens store a `CDOMReference` — a promise, not a pointer.

| Class | Is |
|---|---|
| `CDOMSingleRef<T>` | one named target |
| `CDOMGroupRef<T>` | a group, such as `TYPE=Martial` or `ALL` |

Each object type has a `ReferenceManufacturer` that hands out references and remembers
which names were asked for. After every file is read, `SourceFileLoader` calls:

```java
refContext.resolveReferences(validator);
```

*Source: [`SourceFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/SourceFileLoader.java)*

Every reference is matched to a real object at that moment. A name nobody constructed
produces the error data authors see most often:

```text
Unconstructed Reference: Skill Test Awareness
```

*Source: [`CDOMFactory.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/reference/CDOMFactory.java)*

A group reference that matches nothing reports separately, naming the type that was
requested and never loaded.

This is why an error can name a file you did not touch. The complaint comes from
whatever pointed at the missing object, not from the object itself.

## The objects a character holds are clones

Nothing a character holds is the object the reference context loaded. That matters before
you edit `PCClass`, `PCClassLevel` or `Equipment`.

### A class is cloned once, and its levels again

Adding a class calls `globalClass.clone()`, with the comment `//Still required :(`. Level
data then exists twice. `PCClass.getOriginalClassLevel` lazily builds a `PCClassLevel` in
the class's own map, while `PlayerCharacter.getActiveClassLevel` returns a per-character
clone held by `ClassFacet`.

Edit the original level and a loaded character never sees it. Edit the globally shared
class and the change leaks into every character built from it afterwards.

### Cloning a class re-owns bonuses on the shared map first

`PCClass.clone` calls `super.clone()`, which calls `ownBonuses`, which the override runs
over the original class levels. The clone's own level map is not substituted until
afterwards. Every clone therefore swaps the global levels' `BonusObj` instances for fresh
ones, and anything holding a bonus by identity goes stale.

That matters because bonuses are counted by identity — see
[the rules engine](rules-engine.md#what-bites-when-you-change-a-calculation).

### `CLASS:Foo.MOD` re-enters the same object

`PCClassLoader` fetches the constructed `PCClass` rather than building a new one, and the
level lines after it write onto the same `PCClassLevel`. A `.MOD` adds to existing level
data rather than replacing it, so applying one twice doubles it.

### Equipment has three names, and a modifier rewrites two

`getName()` is neither `getDisplayName()` nor `getKeyName()` — it concatenates the display
name with a modifier suffix. `nameItemFromModifiers` rebuilds both the name and the key
from the applied modifiers and calls `setKeyName`.

So a customised item has a key derived from its modifier list. A lookup by the base item's
key misses it.

### `Equipment.isType` answers for whichever head was asked about last

`bonusPrimary` is a private field that selects the primary or secondary head of a double
weapon. `bonusTo` and `canAddModifier` assign it as a side effect, and `isType(String)`
reads it.

A prerequisite or an `EQMOD=` check on a double weapon answers for whichever head an
unrelated earlier call left selected.

*Source: [`PlayerCharacter.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/PlayerCharacter.java), [`PCClass.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/PCClass.java), [`PCClassLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/PCClassLoader.java), [`Equipment.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/Equipment.java)*

## Abilities are keyed by category

Every other object type is identified by its key. `Ability` is identified by category
plus key.

```java
public final class Ability extends PObject implements Categorized<Ability>, AbilityFacade
```

*Source: [`Ability.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/Ability.java)*

`Categorized` overrides the object's class identity so the category takes part in it.
`AbilityCategory` is both the category value and the factory that builds abilities for
it.

Two abilities may share a key when they sit in different categories. Nothing else in
the model works that way, and it is the reason `CATEGORY:` is not optional on the tags
that grant abilities.

## Related

- [The token system](token-system.md) — what writes into these keys
- [Load pipeline](load-pipeline.md) — when resolution happens
- [The character model](facets.md) — what happens to these objects on a character
- [Line format](../lst/concepts/line-format.md) — field 0, from the data side
