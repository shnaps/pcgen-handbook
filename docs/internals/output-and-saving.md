---
title: Output and saving
---

# Output and saving

Two things happen at the far end of PCGen: a character becomes a sheet, and a character
becomes a file. They use different code and different tag systems.

All paths are relative to the PCGen repository root, at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa).

## Output tokens are not LST tags

An LST tag is read from a data file into a game object at load time. An **output token**
is read from a character sheet template and writes a value out of a finished character.

Different packages, different interfaces, no shared code. The two systems are unrelated
apart from both being uppercase words with colons in them.

| | LST tag | Output token |
|---|---|---|
| Appears in | `.lst` and `.pcc` files | character sheet templates |
| Direction | file into memory | memory into text |
| Package | `plugin/lsttokens/` | `plugin/exporttokens/` |
| Base | `CDOMToken` | `Token` |

The [tag index](../lst/reference/tag-index.md) covers LST tags only. Output tokens are
not in it.

## Picking an export engine

```java
public static ExportHandler createExportHandler(File templateFile)
```

*Source: [`ExportHandler.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/ExportHandler.java)*

The file extension decides everything. A template ending `.ftl` gets
`FreeMarkerExportHandler`. Anything else gets `PCGenExportHandler`, the older engine
that substitutes `|TOKEN|` markers.

Both handlers expose the same two entry points: write one character, or write a
collection for a party sheet.

## The legacy token engine

`PCGenExportHandler` walks the template and replaces every `|...|` marker. The name
before the first full stop selects the class:

| In a sheet | Class |
|---|---|
| `|STAT.0|` | `StatToken` |
| `|AC.Total|` | `ACToken` |
| `|EQTYPE.Weapon.0.NAME|` | `EqTypeToken` |

The rest of the marker is passed to the token as a string, which parses it itself. That
is why output token syntax varies so much between tokens — each one invents its own.

The contract:

```java
public abstract String getTokenName();
public abstract String getToken(String tokenSource, PlayerCharacter pc, ExportHandler eh);
```

*Source: [`Token.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/exporttoken/Token.java)*

`Token` is an abstract class, not an interface. Extend it.

### Extend `AbstractExportToken` instead

In almost every case this is the base to use. It implements `getToken` and hands you a
`CharacterDisplay` rather than a `PlayerCharacter`, which is the read-only path
[facets](facets.md) describes:

```java
public abstract String getToken(String tokenSource, CharacterDisplay display, ExportHandler eh);
```

*Source: [`AbstractExportToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/exporttoken/AbstractExportToken.java)*

The test goes in `code/src/slowtest/`, not `code/src/test/`. See
[testing](testing.md#output-token-tests-live-elsewhere).

Registration works two ways. A dozen core tokens are added directly in
`populateTokenMap`, and live in `pcgen/io/exporttoken/` — 17 classes. The rest are
found by the same [plugin mechanism](plugin-loading.md) that loads LST tokens:
`plugin/exporttokens/` holds 140 classes, 49 of them in a `deprecated` subpackage.

A duplicate token name is logged as an error and the second registration is refused.

## The FreeMarker engine

Newer sheets are FreeMarker templates. The handler builds a data model from the
character and hands it to FreeMarker:

```java
OutputDB.buildDataModel(aPC.getCharID());
OutputDB.buildModeDataModel(gamemode);
```

*Source: [`FreeMarkerExportHandler.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/FreeMarkerExportHandler.java)*

Note the model is built from a `CharID`, the same identifier the
[facets](facets.md) are keyed by. The model classes in `pcgen/output/model/` wrap facet
data for the template.

Six custom directives and functions bridge back to the old world:

| In a template | Does |
|---|---|
| `pcstring` | evaluate a legacy output token |
| `pcvar`, `pchasvar` | read a character variable |
| `pcboolean` | evaluate a condition |
| `loop`, `equipsetloop` | repeat a block |

*Source: [`PCStringDirective.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/freemarker/PCStringDirective.java)*

`pcstring` matters most. It means a FreeMarker sheet can call any legacy token, so the
old system is not going away while sheets still use it.

## What a template may ask an object for

The data model's 23 top-level keys hand back objects. An object then answers a second
vocabulary, and it is a different mechanism: the part after the dot in
`${skill.keyname}`.

That vocabulary is closed, and one method sets it.
`CDOMWrapperInfoFacet.initialize` registers an `OutputActor` under a class and a name:

| Property | Registered on | Gives |
|---|---|---|
| `key` | `CDOMObject` | the object's key |
| `displayname` | `CDOMObject` | the name as written |
| `outputname` | 17 named classes | the name after output formatting |
| `type` | `CDOMObject`, overridden for `Equipment` | its types |
| `source` | `CDOMObject` | a nested model of the source it came from |
| `info` | `CDOMObject` | a nested model of its info fields |
| `visibleto` | `CDOMObject` | its visibility, queried by view |
| `desc`, `benefit` | `PObject` | the description and the benefit text |

`outputname` is registered on seventeen concrete classes one at a time while `key` is
registered once, because lookup walks up the superclass chain. `getActor` tries the
object's own class, then its parent, and stops at `Object`.

### Data grows the set

`FACT:` and `FACTSET:` add properties without any Java. Loading either definition calls
`activateOutput`, which registers an actor under the fact name lowercased, on the class
the fact applies to. A game mode that defines `FACT:Region` gives every template
`${obj.region}`.

The name is not namespaced, so it can collide with a fixed property or an earlier fact.
A collision is **not merged**. The second registration is refused and the fact is dropped
from output with an error print, while the rest of the definition loads normally.

*Source: [`FactDefinition.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/content/fact/FactDefinition.java)*

### This half fails loudly

Ask for a property nothing registered and `CDOMObjectModel.proc` throws a
`TemplateModelException` naming both the type and the key. Export stops.

That is worth knowing because the other two paths do the opposite. A missing output token
substitutes an empty string, and an unknown name in a
[JEP formula](formula-system.md) reads as zero. Of the three vocabularies a sheet touches,
only this one tells you that you were wrong.

### Adding one in Java

Write an `OutputActor<T>` in `pcgen/output/actor/` — 16 classes, each a single `process`
method returning a `TemplateModel` — then register it in `CDOMWrapperInfoFacet`.
`pcgen/output/` is 42 classes across `actor`, `base`, `wrapper`, `factory` and `publish`.
Its tests are in `code/src/itest/`.

*Source: [`CDOMWrapperInfoFacet.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/facet/CDOMWrapperInfoFacet.java)*

## Where sheets live

`outputsheets/` is organised by game mode, then output type:

```
outputsheets/
  base.xml            base.xml.ftl
  d20/
    fantasy/          htmlxml/  pdf/  text/
    pathfinder_2/     htmlxml/  pdf/  text/
    5e/               ...
  killshot/           htm/  pdf/
```

A sheet is one file in one of those directories. Adding one means dropping it in the
right folder for the game mode and output type.

## Exporting with no window

`--exportsheet` runs the same code with no interface. `BatchExporter` calls
`ExportHandler.createExportHandler` exactly as the window does, then writes to the file
given by `-o`.

*Source: [`BatchExporter.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/system/BatchExporter.java)*

It needs a character. There is no way to ask it to load a data set and stop, which is
why checking data uses [the test harness](testing.md) instead.

## The save format

A saved character is a `.pcg` file: plain text, one `TAG:value` per line, `|` inside a
line for sub-fields, `#` comments marking sections.

```text
PCGVERSION:2.0
VERSION:6.09.08
CHARACTERNAME:Test Hero
STAT:STR=18
CLASS:Test Warrior|LEVEL=3
```

*Source: [`PCGVer2Creator.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/PCGVer2Creator.java)*

Two versions appear and they are not the same thing. `PCGVERSION` is the format
version, fixed at `2.0`. `VERSION` is the PCGen build that wrote the file, and the
parser splits it to decide how to read what follows.

Reading is the mirror class:

*Source: [`PCGVer2Parser.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/io/PCGVer2Parser.java)*

It resembles the LST format on the surface. It is a separate parser with its own tag
set, and none of the LST token classes are involved.

## What a save file refers to

Sources are stored by campaign key, not by path. On load, each key is looked up in the
loaded campaigns, after passing through `SourceMigration`, which remaps keys that were
renamed upstream.

A key that resolves to nothing is skipped in silence. If nothing resolves at all, the
log gets one line:

```text
Character's campaign entry was empty.
```

The character still loads. It loads without the data that defined half of it, which is
the usual cause of a character opening with items and abilities missing.

## Where characters are saved

The default is the platform documents folder, under a PCGen directory, in
`characters/`. On Windows that is `%USERPROFILE%\Documents`. The path is a setting, so
the preferences dialog can move it.

*Source: [`PCGenSettings.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/system/PCGenSettings.java)*

The `characters/` directory in the repository is unrelated. It holds sample characters
shipped with the program, and the integration tests use them.

## Related

- [Output token index](../outputsheets/token-index.md) — all 154, read from the source
- [The character model](facets.md) — what the export reads
- [Plugin loading](plugin-loading.md) — how output tokens are registered
- [Startup sequence](startup.md) — the headless path
- [Testing](testing.md) — what the sample characters are for
