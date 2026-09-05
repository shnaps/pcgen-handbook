---
title: Building from source
---

# Building from source

Getting PCGen to compile and run on your own machine, and what each Gradle task is
for. Read [repository layout](architecture.md) first if you have not seen the tree.

All paths are relative to the PCGen repository root, at commit
[`d4ade6d5`](https://github.com/PCGen/pcgen/tree/d4ade6d509f4206b1c1789848752e633ec3c134c).

## What you need

| Requirement | Version | Why |
|---|---|---|
| JDK | 25 | the toolchain version the build asks Gradle for |
| Gradle | none | the repository ships a wrapper |
| Git | any | shallow clones are fine for reading, not for building |

The Java version lives in one place:

```properties
javaVersion=25
javafxVersion=25.0.4
```

*Source: [`gradle.properties`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/gradle.properties)*

`build.gradle` reads that value into a Java toolchain block. No toolchain resolver is
configured, so Gradle does not download a JDK for you — it fails with `PCGen requires
JDK 25 to build, but Gradle could not find one`. Install that version yourself. The JavaFX major version must match
the Java major version, and the file says so in a comment.

You never install Gradle. `./gradlew` on Linux and macOS, `gradlew.bat` on Windows,
downloads Gradle 9.7.0 on first run.

## The three commands that matter

```sh
./gradlew build      # compile, jar the plugins, run the unit tests
./gradlew run        # start PCGen
./gradlew datatest   # load the shipped data and require it clean
```

`build` is the one CI runs on every push. It takes a few minutes cold, because it also
runs SpotBugs.

`run` is the fastest way to see a change. Its configuration is split across two files.
`build.gradle` names the entry point:

```groovy
application {
    mainClass.set('pcgen.system.Main')
}
```

`code/gradle/distribution.gradle` does the rest:

```groovy
tasks.named("run") {
    dependsOn assemble, extractJavaFXLocal

    doFirst {
        jvmArgs = ["-ea", "--enable-preview",
                   "--module-path", modsLibPath,
                   "--add-modules", "javafx.controls,javafx.web,javafx.swing,javafx.fxml,javafx.graphics",
                   "--enable-native-access", "javafx.graphics,javafx.web"]
    }
}
```

It replaces the JVM arguments rather than adding to them, because the application plugin
sets a module path that does not work. The comment in the file says so.

Two consequences worth knowing. `run` depends on `assemble`, so it rebuilds the plugin
jars every time — a token edit takes effect. And it runs with assertions enabled, so an
`assert` in the code you are editing will fire.

`mods/lib` is not in the repository. `extractJavaFXLocal` unzips the JavaFX SDK into it,
downloading from gluonhq first, and every `JavaCompile` task depends on that too. A fresh
clone therefore needs one network fetch before it compiles anything.

*Source: [`distribution.gradle`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/gradle/distribution.gradle), [`build.gradle`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/build.gradle)*

## What the build produces

| Path | Holds |
|---|---|
| `build/classes/java/main` | compiled classes |
| `plugins/*.jar` | one jar per plugin package, written into the source tree |
| `output/` | a runnable layout, from `copyToOutput` or `qbuild` |
| `build/jpackage/` | the native installer, from `fullJpackage` |

The plugin jars landing in `plugins/` rather than under `build/` surprises people. That
directory is build output, not source. See [plugin loading](plugin-loading.md) for why
they are separate jars at all.

## What PCGen needs at runtime

Compiled code alone will not start. `Main.validateEnvironment` checks for the data
directories and exits with an error dialog if one is missing:

`system/` · `data/` · `plugins/` · `outputsheets/` · `preview/`

*Source: [`Main.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/system/Main.java)*

Running from a checkout works because those directories are already beside the code.
Running from a copied jar with nothing else fails at startup, not at load time.

## Task reference

Read from `build.gradle` and `code/gradle/*.gradle`.

| Task | Does |
|---|---|
| `build` | compile, jar plugins, run unit tests, run SpotBugs |
| `assemble` | build the artifacts without running tests |
| `run` | start PCGen from the checkout |
| `test` | unit tests only |
| `itest` | integration tests |
| `slowtest` | slow tests, one JVM fork per test class |
| `datatest` | `DataTest` and `DataLoadTest` — the data authors' check |
| `inttest` | full end-to-end character tests |
| `pfinttest`, `srdinttest`, `sfinttest` and others | the same, per game mode |
| `jarAllPlugins` | rebuild the plugin jars |
| `allReports` | Checkstyle, PMD and SpotBugs together |
| `testCoverage` | Jacoco report |
| `qbuild` | copy the jar into `output/` for a quick manual run |
| `fullJpackage` | native installer bundle |
| `buildDist` | the five release zips |

`./gradlew tasks` lists the rest.

## Quality gates

Three tools are configured, and only one of them runs during a normal build.

| Tool | Config | In `build`? | Fails the build? |
|---|---|---|---|
| Checkstyle | `code/standards/checkstyle.xml` | no | only when run directly |
| PMD | `code/standards/ruleset.xml` | no | no, `ignoreFailures` is set |
| SpotBugs | `code/standards/spotbugs_ignore.xml` | yes | no, `ignoreFailures` is set |

Checkstyle and PMD are detached from the normal build by `sourceSets = []`, which
unhooks them from `check`. So a change that breaks the style rules still builds
locally and still passes CI.

The task graph bears this out. `./gradlew build --dry-run` lists five SpotBugs tasks —
one per source set, including `spotbugsSlowtest` and `spotbugsTestcommon` — and no
Checkstyle or PMD task at all.

Two things that graph also shows, which the task names do not suggest:

- `build` **compiles** the integration and slow tests without running them. A compile
  error in `code/src/slowtest/` fails `./gradlew build`. A failing assertion there does
  not.
- `build` runs the `PCGen-base` and `PCGen-Formula` unit tests as well as PCGen's own.

Run them yourself before submitting:

```sh
./gradlew allReports
```

*Source: [`reporting.gradle`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/gradle/reporting.gradle)*

## What CI runs

`.github/workflows/gradle-test.yml` fires on every push to `master` and every pull
request, as two parallel jobs:

1. `./gradlew build`, then `./gradlew testCoverage`, then a coverage comment on the
   pull request.
2. `./gradlew itest datatest slowtest`.

A third workflow, `.github/workflows/codeql-analysis.yml`, runs CodeQL on the same
events and weekly. It is the one gate that can flag a change without any test failing.

They are split because the first takes about four minutes and the second about
sixteen. Running them in sequence would put the short job behind the long one.

## Gotchas

**The configuration cache is on.** `gradle.properties` enables it, with problems set
to warn rather than fail. A task that misbehaves after an edit to the build files
usually needs `--no-configuration-cache` to confirm the cache is the cause.

**Heap is preset.** `org.gradle.jvmargs=-Xmx4096m`. Lower it if your machine cannot
spare four gigabytes.

**`distZip` and `distTar` are disabled.** The build defines its own release zips
instead. Do not expect the standard application plugin output.

**`build` does not run the data tests.** A change that breaks data loading passes
`./gradlew build` and fails in CI's second job. Run `datatest` yourself.

**A token runs from its jar, not from your compiled class.** Eleven tasks in
`code/gradle/plugins.gradle` jar the token packages into `plugins/*plugins.jar`, and
`PluginClassLoader` reads the class bytes back out of those jars at startup.

`./gradlew run` handles this, because it depends on `assemble` and `jar` depends on
`jarAllPlugins`. Launching `pcgen.system.Main` any other way does not. Run
`./gradlew jarAllPlugins` before starting PCGen from an IDE.

**A new third-party dependency needs a second edit.** Adding a library to
`dependencies` is enough to compile and run. `fullJpackage` also needs it in the jlink
block's `forceMerge` list, and the merged module's `requires` list is maintained by
hand. Miss that and the failure appears only when someone builds an installer.

*Source: [`plugins.gradle`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/gradle/plugins.gradle), [`PluginClassLoader.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/system/PluginClassLoader.java)*

## Related

- [Repository layout](architecture.md) — what is in the tree
- [Startup sequence](startup.md) — what `Main` does once it runs
- [Testing](testing.md) — which test task proves what
- [Contributing](contributing.md) — the standards a change has to meet
- [Running it under a debugger](running-and-debugging.md) — attaching to `run`, and to one test
