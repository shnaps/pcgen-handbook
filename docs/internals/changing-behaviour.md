---
title: Changing behaviour
---

# Changing behaviour

Five mechanisms in PCGen's engine that a change has to respect. Each one is invisible in
the class you are editing, and each one fails quietly rather than throwing.

[Adding a tag](adding-a-tag.md) covers the common change, where the framework holds your
hand. This page covers the changes it does not.

All paths are relative to the PCGen repository root, at commit
[`d4ade6d5`](https://github.com/PCGen/pcgen/tree/d4ade6d509f4206b1c1789848752e633ec3c134c).

## A cached number goes stale unless the serial moves

`PlayerCharacter.setDirty` reads as a save flag. It is also the cache invalidator for the
whole character:

```java
public void setDirty(final boolean dirtyState)
{
    if (dirtyState)
    {
        serial++;
        cache = new ObjectCache();
        variableProcessor.setSerial(serial);
        cabFacet.update(id);
        cAvSpellFacet.update(id);
        cKnSpellFacet.update(id);
        condLangFacet.update(id);
        bonusSkillRankChangeFacet.reset(id);
    }

    dirtyFlag = dirtyState;
}
```

Readers such as `getBaseCheck` and `baseAttackBonus` return a cached `Float` keyed by
that serial. Mutate character state without calling `setDirty(true)` and they keep
serving the old number until something unrelated invalidates the cache. The character
sheet is then wrong in a way no exception marks.

`PlayerCharacter.java` names `setDirty(` on **59** lines: 52 live calls, the declaration,
and **six commented out** rather than deleted. One carries its reason — a re-load of every
tab — written above it. Those comments are the record of an earlier fight with this
mechanism. Across `code/src/java` the call appears 87 times.

The method's own javadoc warns it is "not a 'safe' call" and must not run during
character cloning, because conditional abilities get dropped.

*Source: [`PlayerCharacter.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/core/PlayerCharacter.java)*

## Half the engine has two implementations

A **code control** is a switch a game mode sets. On the data side it turns features on
and off, and [data controls](../lst/concepts/data-controls.md#code-controls) covers that
view. On the code side it selects which of two implementations runs.

The shape is always the same. Ask for the control token. Null means the hardcoded path:

```java
public int getBaseCheck(final PCCheck check)
{
    String checkVar = ControlUtilities.getControlToken(Globals.getContext(), CControl.BASESAVE);
    if (checkVar != null)
    {
        return ((Number) this.getLocal(check, checkVar)).intValue();
    }
    // ... the cached, hardcoded computation
}
```

Fix a saving-throw bug in the lower half of that method and you fix it for every game
mode that leaves `BASESAVE` unset. Any mode that sets it keeps the bug. Both branches are
live at once, in the same build.

`isFeatureEnabled` is the boolean form, and it also decides what gets written to a
character file. `PCGVer2Creator` gates the domain and alignment lines on it, so turning a
feature off stops the save carrying that field. The data is not hidden, it is not written.

Note there are two implementations of that name. `PlayerCharacter.isFeatureEnabled` is the
one the save uses; `ControlUtilities.isFeatureEnabled` has a single caller.

Shipped game modes set only a handful of the controls, which is why the hardcoded branch
is the one usually exercised. [Data controls](../lst/concepts/data-controls.md#code-controls)
owns how many exist and which are used.

*Source: [`ControlUtilities.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/cdom/util/ControlUtilities.java), [`CControl.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/cdom/util/CControl.java)*

## Two toolkits, two threads, no exception

PCGen runs Swing and JavaFX in the same window. [The UI layer](ui-layer.md#two-toolkits)
covers which is which. What matters when you edit UI code is that they have **separate**
UI threads, and the wrong one does not throw.

The codebase says so explicitly. `GuiAssertions` offers six checks — the JavaFX thread,
the Swing thread and a general GUI thread, each with a negative form. Every one throws a
`WrongThreadException` naming the thread it actually found. They are called **47** times
across 26 files.

Crossing between them is done deliberately:

| Call | Hops to |
|---|---|
| `SwingUtilities.invokeLater` | the Swing event dispatch thread |
| `Platform.runLater` | the JavaFX application thread |
| `GuiUtility.runOnJavaFXThreadNow` | the JavaFX thread, and waits for the result |

The mixing is real, not historical. `CharacterSheetPanel` *is* a `JFXPanel`, and
`GuiUtility.wrapParentAsJFXPanel` embeds JavaFX content into Swing containers throughout
the dialogs.

Touch a widget from the wrong thread and you get a missed repaint or a stale value, not a
stack trace. Add the matching assertion to any new UI method and the mistake becomes
loud.

*Source: [`GuiAssertions.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/gui3/GuiAssertions.java), [`GuiUtility.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/gui3/GuiUtility.java)*

## New character state has to survive the save

Adding a value to a character is four edits, not one. Miss any of them and the value
works until the user reopens the file.

Money is the smallest complete example.

| Step | Where | Money's version |
|---|---|---|
| declare the channel | `CControl` | `GOLDINPUT` |
| read and write it | `ChannelUtilities` | `readControlledChannel`, `setControlledChannel` |
| write it to the file | `PCGVer2Creator` | `appendMoneyLine`, using `IOConstants.TAG_MONEY` |
| read it back | `PCGVer2Parser` | `parseMoneyLine` |

The tag string is a constant in `IOConstants`, so the writer and the reader agree by
construction. Adding one without the other produces a file that saves the value and drops
it on load, silently.

**`CControl` holds two unrelated kinds of member.** A plain `String` constant is a code
control, section two's subject. A channel is a `CControl` **instance**, built with the
constructor that takes `isChannel`. Declaring the wrong one gives you a name nothing
creates a variable for.

`SourceFileLoader.enableBuiltInControl` walks `CControl.getChannelConstants()` at load
time and defines the variable, using the format string the constant declares. A wrong
format fails there rather than at your edit.

The variable is not named what you named it. `ChannelUtilities.createVarName` prefixes
`CHANNEL*`, so a sheet cannot reach it by the plain name.

Two more steps if the value is user-visible:

- **Publish it to output sheets.** `OutputDB.register(String, CControl)` names a channel
  for templates. `FacetInitialization` does this for `deity` and `alignment`.
- **Mark the character dirty when it changes.** `ChannelUtilities.setDirtyOnChannelChange`
  wires a channel to the serial mechanism above, which is how the two connect.

*Source: [`CControl.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/cdom/util/CControl.java), [`SourceFileLoader.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/persistence/SourceFileLoader.java), [`ChannelUtilities.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/output/channel/ChannelUtilities.java), [`PCGVer2Creator.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/io/PCGVer2Creator.java), [`PCGVer2Parser.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/io/PCGVer2Parser.java), [`OutputDB.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/output/publish/OutputDB.java)*

## The screen does not listen to the model

A correct fix in engine code can leave the tab showing the old number, because almost
nothing in the interface listens to a facet. See
[how a change reaches a widget](ui-layer.md#how-a-change-reaches-a-widget), which owns
this.

## Before you submit

The three checks that catch these, in the order they are cheapest to run:

1. `./gradlew test` — the token round trips.
2. `./gradlew datatest` — every shipped data set loads clean.
3. `./gradlew inttest` — characters export byte-identical to the checked-in XML. A
   deliberate maths change fails here, and the fix is to regenerate those files. See
   [testing](testing.md#the-export-tests-compare-against-checked-in-xml).

## Related

- [Adding a tag](adding-a-tag.md) — the change the framework supports directly
- [The character model](facets.md) — where character state actually lives
- [The rules engine](rules-engine.md) — the recalculation these caches sit in front of
- [Running it under a debugger](running-and-debugging.md) — watching any of this happen
- [Data controls](../lst/concepts/data-controls.md) — the data author's view of section 2
