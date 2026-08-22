---
title: Adding a tag
---

# Adding a tag

Writing a new LST tag is one class and one test. There is no registry to update.

Read [the token system](token-system.md) first — this page assumes the interfaces.

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
        context.getObjectContext().put(skill, ObjectKey.EXAMPLE, value);
        return ParseResult.SUCCESS;
    }

    @Override
    public String[] unparse(LoadContext context, Skill skill)
    {
        String v = context.getObjectContext().getString(skill, ObjectKey.EXAMPLE);
        return v == null ? null : new String[]{v};
    }

    @Override
    public Class<Skill> getTokenClass()
    {
        return Skill.class;
    }
}
```

Four things to get right:

1. **`getTokenName()` returns a literal.** The scanner in this repository, and anything
   else reading the tags, depends on it being readable without running the code.
2. **`getTokenClass()` decides where the tag is legal.** `Skill.class` means skill
   files only. `CDOMObject.class` means nearly everywhere.
3. **Write through the context**, not to the object. See
   [the token system](token-system.md).
4. **`unparse` returns `null` when nothing was set.** Not an empty array.

## 4. Make failure useful

The message in a `Fail` is what a data author sees in the log:

```java
return new ParseResult.Fail(getTokenName() + " expected a number, found: " + value);
```

Name the tag and show the offending value. Most of the diagnosis in
[when it breaks](../start/when-it-breaks.md) comes down to whether this message was
written well.

## 5. Write the test

Mirror the package under `code/src/test/plugin/lsttokens/`, extend the matching base,
and assert three things:

- valid input parses
- the round trip reproduces the input exactly
- invalid input fails, one case per way of being wrong

The round trip is the important one, and it is what will catch an `unparse` that does
not match the parse.

## 6. Check the build knows the package

If you added a **new package** rather than a class in an existing one, add a jar task
in `code/gradle/plugins.gradle`. `PluginBuildTest` fails when a package has no
matching task, which is the signal you missed it.

A class in an existing package needs no build change.

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
