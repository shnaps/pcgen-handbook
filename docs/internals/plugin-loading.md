---
title: Plugin loading
---

# Plugin loading

Tags are not registered anywhere. There is no list of tokens, no annotation scan, no
configuration file. Adding a tag means adding a class.

Worth understanding before writing one. It explains why the token classes are the only
authoritative statement of what tags exist, and why this handbook reads them.

## Jarred by package

`code/gradle/plugins.gradle` builds one jar per plugin package rather than bundling
them with the program:

```
plugins/lstplugins.jar      plugin/lsttokens/**
plugins/preplugins.jar      plugin/pretokens/**
plugins/bonusplugins.jar    plugin/bonustokens/**
```

The same pattern covers the converter, modifier, primitive, qualifier, function,
grouping, jepcommands and export packages.

## Found at startup

`Main` builds a class loader pointed at the plugins directory. That loader scans it for
files matching `*plugins.jar`, loads every class it finds, and offers each one to the
registered plugin loaders.

Anything matching the pattern is picked up. Nothing names the individual jars.

*Source: [`PluginClassLoader.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/system/PluginClassLoader.java)*

## Claimed by TokenLibrary

`TokenLibrary` implements `PluginLoader`. It declares which types it wants, and each
offered class is routed by what it implements:

| Implements | Goes to |
|---|---|
| `LstToken` | the token map, keyed by name and target class |
| `BonusObj` | the bonus map, for `BONUS:` subtypes |
| `PrerequisiteParserInterface` | the prerequisite parsers |
| `ModifierFactory` | the formula system operators |
| `GroupingDefinition` | groupings |

Sub-tokens are keyed by three values — target class, parent token, token name — which
is how `ADD:ABILITY` and `CHOOSE:ABILITY` stay distinct.

*Source: [`TokenLibrary.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/rules/persistence/TokenLibrary.java)*

## What this means in practice

**Adding a tag is one file.** Put a class implementing `CDOMPrimaryToken` in the right
package. It is jarred, loaded and registered with no other change.

**Deleting a class removes the tag.** There is no stale registry entry left behind,
which is why removed tags such as `ACVALUE` vanish completely rather than lingering as
errors.

**The package a class sits in decides its jar.** A token in the wrong package is not
loaded, and nothing complains. The tag is unknown at load time.

**A scan of the classes is exhaustive.** Since registration is by class rather than by
list, reading every class under `plugin/` gives the complete tag set. That is what
`tools/scan_tokens.py` in this repository does.

## The test that guards it

`PluginBuildTest` checks that the packages on disk match the jar tasks in the build.
It carries a hardcoded list of the plugin packages. That list is the closest thing
PCGen has to a registry. It exists to catch a new package added without a matching jar
task.

If you add a plugin package, that test is what will tell you the build does not know
about it.

## Related

- [The token system](token-system.md) — what those classes implement
- [Adding a tag](adding-a-tag.md) — writing one
- [Repository layout](architecture.md) — where the packages sit
