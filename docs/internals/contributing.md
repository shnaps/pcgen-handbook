---
title: Contributing
---

# Contributing

What a change to PCGen has to satisfy, and what nobody checks. This handbook is not run
by the PCGen project, so treat this as a reading of the repository rather than as
policy.

All paths are relative to the PCGen repository root, at commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa).

## There is no CONTRIBUTING file

`CONTRIBUTING.md` does not exist. Neither does a pull request template. The guidance is
split across two files:

| File | Covers |
|---|---|
| `README.md` | the workflow: ticket, branch, pull request |
| `AGENTS.md` | build, tests, style, and a list of things not to break |

`AGENTS.md` is the closer thing to a contributor guide, and it is maintained. It asks
that anyone using an assistant to work on the code updates it afterwards.

## The workflow

1. Open or claim a ticket in JIRA at `pcgenorg.atlassian.net`. Two projects: **CODE**
   for the program, **DATA** for game data.
2. Branch, named after the ticket. The convention in the repository is `fix_code_3444`.
3. Make the build pass before opening the pull request.
4. Open the pull request against `master` from your fork.

GitHub issues also exist, with templates for bug reports and feature requests. The bug
template asks for a `.pcg` character file that reproduces the problem. The README
treats JIRA as where work is tracked, because release notes are generated from it.

Commit subjects are not consistent. Many use `fix:` or `feat:` prefixes, many use a
JIRA identifier such as `DATA-3818:`, and almost all end with the pull request number in
brackets. Match what the recent history does rather than a written rule, because there
is not one.

## What has to build

```sh
./gradlew build
./gradlew test itest slowtest
```

`AGENTS.md` asks for both, with failing tests fixed before submission. New tests go in
the source root matching their speed:

| Root | For |
|---|---|
| `code/src/test` | fast unit tests |
| `code/src/itest` | integration tests |
| `code/src/slowtest` | slow tests |

Java 25 is required. It is set once in `gradle.properties` and applied as both a
toolchain and a compiler release level, so an older JDK fails immediately.

## Code style, as actually configured

Checkstyle's rules are short enough to list. These are the ones that reject code:

| Rule | Setting |
|---|---|
| Line length | 201 characters, tab width 4 |
| Opening brace | on its own line, for classes, methods and every block |
| Braces | required, even on a one-line `if` |
| Imports | no wildcards, no unused, no redundant |
| Long literals | `100L`, never `100l` |
| Modifier order | the order in the language specification |
| Utility classes | must hide their constructor |
| Boolean returns | no `if (x) return true; else return false;` |
| Array style | `String[] args`, not `String args[]` |
| End of file | newline required |

*Source: [`checkstyle.xml`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/standards/checkstyle.xml)*

Javadoc is configured but not required. Missing parameter and return tags are allowed.

Import order is not checked. There is an order file for IDEs —
`java`, `javax`, `gmgen`, `pcgen`, `plugin` — and following it keeps diffs small.

### System.exit is banned

```xml
<property name="format" value="System(\s*)\.(\s*)exit"/>
<property name="message" value="System.exit must not be used within the project. Use GracefulExit.exit instead."/>
```

The only file exempt is `GracefulExit` itself. The reason is in
[startup](startup.md): exit runs through interceptors that may veto it, and a direct
call skips them.

`AGENTS.md` adds a second rule of the same kind. Log through `pcgen.util.Logging`, using
`Logging.errorPrint`, rather than calling the logger with a level directly.

## Nothing runs the style checks

This is the part worth knowing.

| Tool | Wired into `build` | Fails on violation | Run in CI |
|---|---|---|---|
| Checkstyle | no | yes, when run directly | no |
| PMD | no | no | no |
| SpotBugs | yes | no | yes, but ignored |

Checkstyle and PMD are detached with `sourceSets = []`. PMD and SpotBugs both set
`ignoreFailures`. CI runs `build`, `testCoverage`, `itest`, `datatest` and `slowtest`,
and never `allReports`.

*Source: [`reporting.gradle`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/gradle/reporting.gradle)*

So a change breaking every style rule in the list above still goes green. Run the
checks yourself:

```sh
./gradlew allReports
```

SpotBugs is narrower than it looks. Its exclude file limits analysis to `pcgen.base`,
`pcgen.cdom` and `pcgen.output`. Everything else is out of scope.

There is also no branch protection, no contributor licence agreement and no developer
certificate of origin. What gates a change is a maintainer reading it.

## Adding a token

A new LST tag needs a class and a test. [Adding a tag](adding-a-tag.md) walks through
the class. The test extends a shared base:

*Source: [`AbstractTokenTestCase.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/test/plugin/lsttokens/testsupport/AbstractTokenTestCase.java)*

It requires seven methods:

| Method | Returns |
|---|---|
| `getCDOMClass()` | the object type the tag applies to |
| `getToken()` | the token under test |
| `getLoader()` | the loader for that object type |
| `isCDOMEqual(T, T)` | how to compare two loaded objects |
| `getLegalValue()`, `getAlternateLegalValue()` | two values that must both parse |
| `getConsolidationRule()` | what happens when the tag appears twice |

The base supplies `runRoundRobin`, which parses a value, unparses it, parses the result
and compares. That round trip is what makes the token tests a usable specification of
accepted syntax.

## Licence headers

Source files carry an LGPL 2.1 header with a copyright line naming the author and year.
Nothing checks for it. Copy the header from a neighbouring file in the same package.

## Structural rules

`AGENTS.md` names constraints that are not enforced by any tool and will break things
quietly:

- No new class in the main module may share a package name with `PCGen-base` or
  `PCGen-Formula`. The module system rejects split packages.
- Never re-attach a `JFXPanel`'s Scene to a Stage. Use `PanelFromResource` for a
  standalone dialog and `JFXPanelFromResource` only when embedding in Swing.
- Do not change how `ConfigurationSettings` finds the install root without
  understanding the packaged layout. See [startup](startup.md).

## Related

- [Building from source](building.md) — the tasks named here
- [Adding a tag](adding-a-tag.md) — the most common first change
- [Testing](testing.md) — which task proves what
- [Report a bug](../lst/howto/report-a-bug.md) — the data side of the same tracker
- [Running it under a debugger](running-and-debugging.md) — before you submit, watch it work
