---
title: The interface layer
---

# The interface layer

PCGen runs two toolkits at once, and the boundary between the window and the rules
engine is not where the code says it is. Both are worth knowing before changing
anything on screen.

All paths are relative to the PCGen repository root, at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa).

## Two toolkits

| Package | Toolkit | Files | Owns |
|---|---|---|---|
| `pcgen/gui2` | Swing | 241 | the main window and every character tab |
| `pcgen/gui3` | JavaFX | 54 | dialogs, the preferences panels, splash, toolbar |

The main window is Swing:

```java
public final class PCGenFrame extends JFrame implements UIDelegate, CharacterSelectionListener
```

*Source: [`PCGenFrame.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/gui2/PCGenFrame.java)*

JavaFX is started anyway during [startup](startup.md), with a bare `new JFXPanel()`,
because the parts written in JavaFX are embedded inside the Swing window.

### What JavaFX actually owns

The migration is real but partial. `gui3` holds:

- Dialogs: about, debug, calculator, export, options path, purchase method.
- The whole preferences panel set, twelve controllers.
- The startup splash screen.
- The toolbar, the status bar, and the random name generator.

The main frame, the character tabs, the source selection dialog and the LST converter
are all still Swing. Nothing suggests that is changing soon.

### Crossing between them

```java
public static JFXPanel wrapParentAsJFXPanel(Parent parent)
```

*Source: [`GuiUtility.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/gui3/GuiUtility.java)*

Swing code calls that to embed a JavaFX component. `GuiAssertions` sits beside it and checks
which thread you are on. Swing and JavaFX each have their own, and mixing them up is
the usual cause of a dialog that never appears.

23 FXML files live under `code/src/resources/pcgen/gui3/`. Controllers are found by
convention through `PanelFromResource`, which loads the FXML beside a given class and
supplies `LanguageBundle` as its resource bundle. There is no annotation scan.

## The facade layer

`pcgen/facade/core/` holds 33 interfaces meant to be the entire surface the interface
sees. The intent is written down:

> provides a key role in separation of the core and the UI layers. The UI can only
> operate on this interface, the core provides the implementation.

*Source: [`CharacterFacade.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/facade/core/CharacterFacade.java)*

| Interface | Is |
|---|---|
| `CharacterFacade` | one open character, as the window sees it |
| `DataSetFacade` | the loaded data: classes, races, skills |
| `UIDelegate` | dialogs and prompts, callable from core code |

`UIDelegate` inverts the direction. Core code sometimes has to ask a question, and this
lets it do so without importing Swing. `PCGenFrame` implements it.

### The rule is not enforced

Measured at the pinned commit:

| Measurement | Count |
|---|---|
| `gui2` Java files | 241 |
| `gui2` files importing `pcgen.core` directly | 93 |
| Of those, inside `gui2/facade/` | 26 |
| Outside it, reaching past the boundary | 67 |
| `facade/core` interface files importing `pcgen.core` | 14 of 33 |

`PCGenFrame` itself is one of the 67. So are most of the tabs.

The boundary interfaces leak too. `DataSetFacade` imports thirteen core classes, so
even code that only touches the facade layer is holding `Race`, `PCClass` and `Skill`
objects directly.

Treat the separation as an intention that was not maintained. Believing it will send
you looking for a facade method that nobody wrote. The surrounding code imports the
core class instead.

## Observable values

`pcgen/facade/util/` supplies the types the widgets bind to.

| Type | Is |
|---|---|
| `ReferenceFacade<T>` | one value that notifies on change |
| `ListFacade<T>` | a list that notifies on add and remove |
| `MapFacade<K,V>` | the same, keyed |

Concrete forms are `DefaultReferenceFacade`, `DefaultListFacade`, `SortedListFacade`
and `DelegatingListFacade`. Listener interfaces sit in `pcgen/facade/util/event/`.

Swing table models in `gui2` and JavaFX controllers in `gui3` both register as
listeners on the same objects. That is how one model feeds two toolkits.

## The main window

`PCGenUIManager` builds `PCGenFrame` and shows it. The tabs live in `pcgen/gui2/tabs/`,
and their order is fixed in one place:

*Source: [`InfoTabbedPane.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/gui2/tabs/InfoTabbedPane.java)*

Tab 0 is `SummaryInfoTab`, where a character is created. The others are race, class,
skills, abilities, domains, spells, inventory, equipping, companions, description,
temporary bonuses and the character sheet preview.

Choosing sources is not a tab. It is a modal dialog:

*Source: [`SourceSelectionDialog.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/gui2/sources/SourceSelectionDialog.java)*

That dialog is what starts the [load pipeline](load-pipeline.md).

## Settings and language

Preferences open as a Swing dialog wrapping a JavaFX tree, with JavaFX panels inside.
Values persist through `PCGenSettings`, which writes `options.ini` in the settings
directory named in [startup](startup.md).

Text comes from `LanguageBundle`, backed by
`code/src/resources/pcgen/lang/LanguageBundle.properties` and its per-locale variants:
German, Spanish, French, Italian, Japanese, Portuguese. Translations are managed
through Crowdin, so edit the base file only.

## Tests

There are no automated interface tests in the sense of driving widgets. `gui2` has five
test classes and `gui3` has nine, all ordinary JUnit checks on controllers and
resources, run by `./gradlew test`.

A change to the window is verified by running it. See [building](building.md).

## Related

- [Startup sequence](startup.md) — how the window gets built
- [The character model](facets.md) — what a `CharacterFacade` wraps
- [Load pipeline](load-pipeline.md) — what the source dialog starts
- [Contributing](contributing.md) — the standards a change has to meet
