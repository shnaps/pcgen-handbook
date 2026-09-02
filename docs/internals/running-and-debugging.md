---
title: Running it under a debugger
---

# Running it under a debugger

How to start PCGen with a debugger attached, run one test from an IDE, and read the
errors it prints. Read [building from source](building.md) first — this page assumes the
build already works.

All paths are relative to the PCGen repository root, at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa).

## Attaching from Gradle

```sh
./gradlew run --debug-jvm
```

`--debug-jvm` is Gradle's own flag. The task prints

```text
Listening for transport dt_socket at address: 5005
```

and then waits. Point a remote JVM debug configuration at `localhost:5005` and the
program starts. It suspends before `main`, so you can break anywhere in startup.

The same flag works on any test task:

```sh
./gradlew test --tests "*TypeLstTest*" --debug-jvm
```

Two things about `run` come from [building from source](building.md) and matter here:

- It depends on `assemble`, so the plugin jars are rebuilt first and a token you edited
  is the token that runs.
- It replaces the JVM arguments wholesale in a `doFirst` block, so anything you set
  elsewhere is discarded. `--debug-jvm` still works, because Gradle adds the debug agent
  separately.

## Running from an IDE

The repository ships no IDE configuration — no `.idea`, no `.iml`, no eclipse task. You
import it as a Gradle project and everything comes from the build files.

Three things then bite.

**The plugin jars must be current.** See below — an IDE launch skips the Gradle task
that builds them.

**The working directory must be the repository root.** `Main.validateEnvironment` checks
for `system/`, `data/`, `plugins/`, `outputsheets/` and `preview/` beside the code and
exits with a dialog if one is missing. See
[what PCGen needs at runtime](building.md#what-pcgen-needs-at-runtime).

**A test run from the IDE needs the JVM arguments the build adds.** Every `Test` task
gets them, and an IDE that runs JUnit directly does not:

```text
--module-path mods/lib
--add-modules javafx.controls,javafx.web,javafx.swing,javafx.fxml,javafx.graphics
--add-exports javafx.graphics/com.sun.javafx.application=ALL-UNNAMED
--add-exports javafx.graphics/com.sun.javafx.util=ALL-UNNAMED
--add-exports javafx.base/com.sun.javafx.logging=ALL-UNNAMED
--add-opens javafx.graphics/com.sun.glass.ui=ALL-UNNAMED
--enable-native-access=javafx.graphics
-Djava.awt.headless=true
-Dtestfx.headless=true
-Dprism.order=sw
```

Five more properties go with them — `testfx.robot`, `prism.verbose`,
`javafx.macosx.embedded` and `java.security.manager` among them. Copy the whole
`tasks.withType(Test)` block rather than this excerpt.

Without them a test that touches JavaFX fails on the module system rather than on
anything you wrote. `mods/lib` exists only after `extractJavaFXLocal` has run once.

*Source: [`build.gradle`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/build.gradle)*

## Reading errors instead of stepping

Most of what you want is already printed. `pcgen.util.Logging` is called 832 times for
errors alone, and [startup](startup.md#logging) covers where its configuration comes from
and what `-v` does.

What is not obvious is that a message only reaches the user if a handler is registered
for it. There are three registrations in the whole program:

| Registered by | Live while |
|---|---|
| `SourceFileLoader` | a data set is loading, and removed straight afterwards |
| `DebugDialogController` | the debug window is open |
| `RunConvertPanel` | the LST converter is running |

`SourceFileLoader`'s handler filters at `LST_WARNING`. So an `LST_INFO` message, or
anything logged outside a load, reaches the log file and nothing else. A silent failure
is often a message that was printed to a level nobody was listening to.

*Source: [`Logging.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/util/Logging.java), [`SourceFileLoader.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/persistence/SourceFileLoader.java)*

## Where to break, by symptom

| Symptom | Method |
|---|---|
| a tag is not being read | `TokenSupport.processToken` |
| a tag parsed but nothing happened | the token's `parseToken`, then its `DeferredToken.process` |
| a reference did not resolve | reference resolution, in [post-load phases](load-pipeline.md#6-post-load-phases) |
| a number is wrong | the table in [the rules engine](rules-engine.md#where-to-put-a-breakpoint) |
| a sheet field is empty | the export token class, from the [output token index](../outputsheets/token-index.md) |

`TokenSupport.processToken` receives the target object, the tag name and the raw value.
That makes it the one breakpoint that answers "is my tag reaching a token at all".

## What you cannot do this way

**You cannot debug a token from an IDE launch without rebuilding its jar.**
`PluginClassLoader` reads the class bytes out of `plugins/*plugins.jar`, so a breakpoint
in your edited source sits on code that is not running. `./gradlew run` rebuilds those
jars on the way through. Starting `pcgen.system.Main` directly does not, so run
`./gradlew jarAllPlugins` first.

**You cannot step through a character load and watch bonuses recalculate.**
`calcActiveBonuses` returns immediately while `importing` is set. The recalculation
happens once, after the file is read.

## Related

- [Building from source](building.md) — the tasks, and what `run` does
- [Testing](testing.md) — which source root a test belongs in
- [The load pipeline](load-pipeline.md) — what happens between a file and an object
- [The rules engine](rules-engine.md) — where a wrong number comes from
- [Changing behaviour](changing-behaviour.md) — the traps in engine code
