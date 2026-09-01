---
title: Adding a tag
---

# Adding a tag

Writing a new LST tag is one class and one test. Two neighbouring systems are not. A
`PRExxx` is three classes, and a game mode tag or a `BONUS:` subtype uses a different
contract entirely. See [three contracts](#three-contracts).

Read [the token system](token-system.md) first — this page assumes the interfaces.

!!! warning "This page covers one of three contracts"
    Everything below is the **CDOM token** contract, used by data tags and by the
    object-scoped packages. Game mode tokens and `BONUS:` subtypes are different
    classes with different method names and a different registry. See
    [three contracts](#three-contracts) before you start on either.

## Before you start

Most things do not need a new tag. `BONUS`, `ADD`, `CHOOSE` and the formula system
cover a great deal, and a new tag is a maintenance burden on everyone. Reach for one
when the behaviour genuinely has no expression in what exists.

## 1. Pick the package

The package decides which jar the class lands in, and nothing else registers it.

| Tag kind | Package |
|---|---|
| a data or game mode tag | `plugin/lsttokens/` |
| scoped to one object type | `plugin/lsttokens/<type>/` — `skill`, `race`, `pcclass` |
| a `PRExxx` | `plugin/pretokens/{parser,test,writer}/` |
| a `BONUS:` subtype | `plugin/bonustokens/` |
| a chooser primitive or qualifier | `plugin/primitive/` or `plugin/qualifier/` |

A class in the wrong package is not loaded, and nothing reports it. The tag is just
unknown.

### Three contracts

The table above routes by package. Two of those destinations do not use the interfaces
the rest of this page describes.

| Writing | Extends or implements | Its methods | Found through |
|---|---|---|---|
| a data tag | `AbstractNonEmptyToken`, `CDOMPrimaryToken` | `parseNonEmptyToken`, `unparse`, `getTokenClass` | `TokenLibrary` |
| a game mode tag | `GameModeLstToken` | `parse(GameMode, String, URI)` | `TokenStore` |
| a `BONUS:` subtype | `BonusObj` | `parseToken`, `unparseToken`, `getBonusHandled` | `Bonus` |

The game mode tree holds 157 classes — 66 at its top level and the rest in eleven
subdirectories, `codecontrol` the largest at 43. `plugin/bonustokens/` holds 55, and none
of those declares a `parseNonEmptyToken`. The game mode side is not so uniform: 33 of its
157 classes declare one.

The game mode side is a separate registry, not a separate base class on the same one.
`GameModeLoader` reads `TokenStore`, which `TokenLibrary` knows nothing about.

*Source: [`GameModeLstToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/lst/GameModeLstToken.java)*

*Source: [`BonusObj.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/bonus/BonusObj.java)*

## 2. Pick a base class

Rarely implement the interface directly. The shared bases handle the tedious parts:

| Base | Use when |
|---|---|
| `AbstractNonEmptyToken` | any tag that requires a value |
| `AbstractTokenWithSeparator` | the value uses `\|` or another separator |
| `AbstractIntToken` | the value is a single number |
| `AbstractStringToken` | the value is a single string |
| `AbstractYesNoToken` | the value is `YES` or `NO` |

`AbstractNonEmptyToken` is the common choice. It rejects an empty value before your
code runs.

## 3. Write the class

The shape, using a single-value tag on skills as the example:

```java
public class ExampleToken extends AbstractNonEmptyToken<Skill>
        implements CDOMPrimaryToken<Skill>
{
    @Override
    public String getTokenName()
    {
        return "EXAMPLE";
    }

    @Override
    protected ParseResult parseNonEmptyToken(LoadContext context, Skill skill, String value)
    {
        context.getObjectContext().put(skill, StringKey.EXAMPLE, value);
        return ParseResult.SUCCESS;
    }

    @Override
    public String[] unparse(LoadContext context, Skill skill)
    {
        String v = context.getObjectContext().getString(skill, StringKey.EXAMPLE);
        return v == null ? null : new String[]{v};
    }

    @Override
    public Class<Skill> getTokenClass()
    {
        return Skill.class;
    }
}
```

### The key does not exist yet

`StringKey.EXAMPLE` in that example has to be declared before the class compiles.
`StringKey` is an enum in `pcgen/cdom/enumeration/`, so declaring one means adding a word
to the list.

The key classes have different shapes, which matters when you copy an example:

| Class | Shape | Holds |
|---|---|---|
| `StringKey` | an enum | a plain string |
| `IntegerKey` | an enum | a number |
| `ObjectKey` | `public static final` fields, typed | anything else |

`getString` takes a `StringKey` and nothing else. Passing an `ObjectKey` does not
compile, which is the mistake to expect when moving between the two.

**Consider a `FACT:` instead.** `StringKey`'s own javadoc says a `FACT:` token is
preferred over a new `StringKey` token. A fact is declared in data with `FACTDEF` and
needs no Java at all. Reach for a new key only when the value has behaviour attached.

*Source: [`StringKey.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/enumeration/StringKey.java)*

## 4. Four things to get right

1. **`getTokenName()` returns a literal.** The scanner in this repository, and anything
   else reading the tags, depends on it being readable without running the code.
2. **`getTokenClass()` decides where the tag is legal.** `Skill.class` means skill
   files only. `CDOMObject.class` means nearly everywhere.
3. **Write through the context**, not to the object. See
   [the token system](token-system.md).
4. **`unparse` returns `null` when nothing was set.** Not an empty array.

## 5. Make failure useful

The message in a `Fail` is what a data author sees in the log:

```java
return new ParseResult.Fail(getTokenName() + " expected a number, found: " + value);
```

Name the tag and show the offending value. Most of the diagnosis in
[when it breaks](../start/when-it-breaks.md) comes down to whether this message was
written well.

## 6. Write the test

Mirror the package under `code/src/test/plugin/lsttokens/` and extend the matching base.

**You write no `@Test` methods.** The bases carry them, including the round trip. What
you write is overrides that tell the base what it is testing:

```java
public class ExampleTokenTest extends AbstractStringTokenTestCase<Skill>
{
    static ExampleToken token = new ExampleToken();
    static CDOMTokenLoader<Skill> loader = new CDOMTokenLoader<>();

    @Override
    public Class<Skill> getCDOMClass() { return Skill.class; }

    @Override
    public CDOMLoader<Skill> getLoader() { return loader; }

    @Override
    public CDOMPrimaryToken<Skill> getToken() { return token; }

    @Override
    public StringKey getStringKey() { return StringKey.EXAMPLE; }

    @Override
    public boolean isClearLegal() { return true; }
}
```

**Match the base to the tag.** `AbstractStringTokenTestCase` fits a string tag and asks
for `getStringKey` and `isClearLegal`. `AbstractIntegerTokenTestCase` fits a number and
asks instead for `getIntegerKey`, `isZeroAllowed`, `isNegativeAllowed` and
`isPositiveAllowed`. Picking the wrong one leaves abstract methods unimplemented.

Underneath both, `AbstractTokenTestCase` declares the hooks every test supplies:
`getCDOMClass`, `getLoader`, `getToken`, `isCDOMEqual`, `getLegalValue`,
`getAlternateLegalValue` and `getConsolidationRule`. The last says what happens when the
tag appears twice — `ConsolidationRule.OVERWRITE` keeps the second, `SEPARATE` keeps
both.

The round trip is the assertion that matters, and it is inherited. It catches an
`unparse` that does not match the parse.

*Source: [`AbstractStringTokenTestCase.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/test/plugin/lsttokens/testsupport/AbstractStringTokenTestCase.java)*

## 7. Check the build knows the package

If you added a **new package** rather than a class in an existing one, add a jar task
in `code/gradle/plugins.gradle`. `PluginBuildTest` fails when a package has no
matching task, which is the signal you missed it.

A class in an existing package needs no build change.

## Deprecating a tag

Moving the class to `plugin/lsttokens/deprecated/` marks it. It does not help anyone whose
data already uses it.

For that there is the converter. `plugin/converter/` holds 28 classes that rewrite old
data into its current form, each implementing `TokenProcessorPlugin`:

```java
public interface TokenProcessorPlugin extends TokenProcessor
{
    public Class<? extends CDOMObject> getProcessedClass();

    public String getProcessedToken();
}
```

A plugin names the object type and the tag it rewrites. The tool that runs them is
`pcgen/gui2/converter/`, 9 classes, launched from `PCGenDataConvert.main`.

Neither package has a behaviour test. `plugin/converter` is covered only by
`code/src/slowtest/plugin/PluginBuildTest.java`, which checks that the package is jarred,
not that a plugin rewrites anything. Write the plugin when a deprecation has a mechanical
replacement, and skip it when the fix needs a human decision.

*Source: [`TokenProcessorPlugin.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/gui2/converter/event/TokenProcessorPlugin.java)*

## Two-level tags

For `PARENT:CHILD` form, implement `CDOMSecondaryToken` and add `getParentToken()`:

```java
@Override public String getParentToken() { return "ADD"; }
@Override public String getTokenName()   { return "EXAMPLE"; }
```

That gives `ADD:EXAMPLE`. Nothing composes the full string for you.

## Work that must wait

If the tag references something that may not be loaded yet, implement `DeferredToken`
alongside and do that part in `process`. Parsing still happens at the line; validation
happens once everything exists.

## Deprecating instead of deleting

Removing a tag breaks existing data. The established route is to move the class to
`plugin/lsttokens/deprecated/` and keep it working. Log a message naming the
replacement. That is what `FEAT:` and the rest of the feat family do.

See [what changed](../appendix/whats-changed.md) for how that looks from the data side.

## Related

- [The token system](token-system.md) — the interfaces
- [Plugin loading](plugin-loading.md) — why one class is enough
- [Testing](testing.md) — the test harness
- [Changing behaviour](changing-behaviour.md) — for a change the token framework does not cover
