---
title: Repository layout
---

# Repository layout

Where things are in the PCGen repository, for someone landing in it for the first
time.

Paths are from the repository root, at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa)
(version `6.09.08.RC1`).

## Top level

| Path | Holds |
|---|---|
| `code/` | all Java source, build logic and tests |
| `data/` | shipped game data, by game mode then publisher |
| `system/` | game mode definitions, in `system/gameModes/` |
| `docs/` | the user documentation, served as-is by GitHub Pages |
| `outputsheets/` | character sheet templates |
| `plugins/` | build output — the plugin jars, not source |
| `PCGen-base/`, `PCGen-Formula/` | the formula system, as separate Gradle subprojects |
| `installers/` | packaging |

`AGENTS.md` at the root is the de facto contributor guide, and covers Java work only.
It says nothing about documentation.

## Source roots

`code/src/` is split by what the code is for, not by module:

| Root | Contains |
|---|---|
| `java` | the program. Packages `pcgen.*`, `plugin.*`, `gmgen.*` |
| `test` | fast unit tests |
| `itest` | integration tests |
| `slowtest` | slow tests, including the data-loading tests |
| `testcommon` | helpers shared between test roots |
| `resources` | bundled resources |

Note it is `code/src/test`, not `utest`.

## The packages that matter for data

[The overview](overview.md#four-top-level-packages) sets out the four package trees.
Nearly everything in this handbook's [tag index](../lst/reference/tag-index.md) lives
under `plugin/`. These are the parts of `pcgen.*` a data change passes through:

| Package | Does |
|---|---|
| `pcgen/persistence/lst/` | reads `.lst` and `.pcc` files |
| `pcgen/rules/persistence/` | dispatches tags to tokens |
| `pcgen/rules/persistence/token/` | the token interfaces and shared bases |
| `pcgen/rules/context/` | `LoadContext` and the object and reference contexts |
| `pcgen/cdom/` | the object model, and the keys tokens write through |

## Build

Gradle, with a wrapper. `settings.gradle` is three lines and pulls in the two formula
subprojects.

Build logic is split into `code/gradle/*.gradle` rather than living in one file:

| File | Does |
|---|---|
| `plugins.gradle` | builds the plugin jars, one per package |
| `distribution.gradle` | assembles the release, including copying `docs/**` verbatim |
| `release.gradle`, `reporting.gradle` | releases and reports |

`code/standards/` holds the Checkstyle, PMD and SpotBugs configuration.

The toolchain targets Java 25.

## Tests

Six Gradle tasks run them, and [testing](testing.md) lists all six. `datatest` is the
one worth knowing as a data author: it loads the shipped data and requires it clean.

## Documentation is not built

`docs/` is hand-written XHTML, served directly by GitHub Pages from `master` and
copied verbatim into the distribution. There is no documentation build step and no CI
touching it.

That is convenient, since a documentation change cannot break the build. It is also why
the documentation drifted from the code with nothing noticing.

## Related

- [Load pipeline](load-pipeline.md) — how a file becomes an object
- [The token system](token-system.md) — how tags are implemented
- [Plugin loading](plugin-loading.md) — how the jars are found at startup
