---
title: Testing
---

# Testing

Two kinds of test matter for data work. Token tests pin down what a tag accepts. Data
tests load real datasets and require them clean.

## Token tests

`code/src/test/plugin/lsttokens/` mirrors the token packages — about 398 files, one
per tag.

They are the most precise statement of what syntax a tag accepts, often more precise
than the documentation. When this handbook needed to know exactly what a tag takes,
these were the place to look.

### What they assert

The shared bases live in `code/src/test/plugin/lsttokens/testsupport/`:

| Base | For |
|---|---|
| `AbstractTokenTestCase` | the general case |
| `AbstractGlobalTokenTestCase` | tags on `CDOMObject` |
| `AbstractCampaignTokenTestCase` | PCC tags |
| `AbstractChooseTokenTestCase` | `CHOOSE:` variants |
| `AbstractQualifierTokenTestCase`, `AbstractPrimitiveTokenTestCase` | chooser parts |

The core assertion is a **round trip**: parse a string, unparse it, require the result
to match. That is why `unparse` exists on every token, and why the tests are reliable
as a syntax reference.

They also assert what must *fail* — empty values, bad separators, malformed arguments.
Reading the rejection cases is usually faster than reading the parser.

`code/src/testcommon/plugin/lsttokens/testsupport/` holds `TokenRegistration` and
`CDOMTokenLoader`, which let a test register tokens directly instead of going through
the jar loader.

### Output token tests live elsewhere

Output token tests are not under `code/src/test/`. They live in `code/src/slowtest/`,
extend `AbstractCharacterTestCase`, and run under `./gradlew slowtest`. A test placed in
`code/src/test/` will not find them and will not run alongside them.

## Data tests

```sh
./gradlew datatest
```

Runs `DataTest` and `DataLoadTest` from `code/src/slowtest/`.

`DataLoadTest` loads datasets through the production `SourceFileLoader` and asserts
**zero errors and zero warnings**. Warnings count, so a deprecation notice fails it.

This is what PCGen's CI runs, and it is the strongest check available for a dataset.

### Pointing it at your own data

Put a `config.ini` at the repository root:

```ini
pccFilesPath=/absolute/path/to/your/data
```

!!! warning "SHOWINMENU is required"
    `DataLoadTest` selects campaigns shown in the menu, or belonging to a game mode's
    default set. A `.pcc` without `SHOWINMENU:YES` is skipped **silently** — the test
    passes without testing anything.

    A green run proves nothing until you have confirmed your campaign was selected.

Narrow the run with the usual Gradle filter:

```sh
./gradlew datatest --tests "*DataLoadTest*"
```

`DataTest` is separate and checks hygiene rather than correctness — path lengths, and
a variable report.

## Which source root a test belongs in

The classpath decides this, not how long the test takes.

| Source root | Compiles against |
|---|---|
| `code/src/test` | `main` and `testcommon` |
| `code/src/itest`, `code/src/slowtest` | the same, plus everything in `test` |

`AbstractCharacterTestCase` lives in `code/src/slowtest/pcgen/`. So any test that needs a
built character has to live in `slowtest` or `itest` as well. Put it in `code/src/test/`
and it will not compile.

Its `setUp` resets static state — `SettingsHandler.setGame("3.5")` and
`Globals.emptyLists()` among it. That state is global, which is why both slow tasks set
`forkEvery = 1`.

*Source: [`build.gradle`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/build.gradle), [`AbstractCharacterTestCase.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/slowtest/pcgen/AbstractCharacterTestCase.java)*

## The export tests compare against checked-in XML

`inttest` and the per-game-mode tasks all run `PcgenFtlTestCase.runTest`. For one named
character it:

1. loads `code/testsuite/PCGfiles/<name>.pcg`,
2. exports it through `code/testsuite/base-xml.ftl` by calling `Main.main` with
   `--character` and `--exportsheet`,
3. XML-diffs the output against `code/testsuite/csheets/<name>.xml` and fails on any
   difference.

Those `.xml` files are checked into the repository. A deliberate change to how a number
is computed fails here by design, and the fix is to regenerate them.

*Source: [`PcgenFtlTestCase.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/slowtest/pcgen/inttest/PcgenFtlTestCase.java)*

## What does not exist

**There is no command that validates a single PCC.** The headless CLI
(`--exportsheet` with `--character` or `--party`) only exports characters. Data
validation goes through the test harness or not at all.

For a single tag rather than a dataset, the cheaper route is a token test: parse the
string, assert success, assert the round trip.

## Other Gradle tasks

| Task | Runs |
|---|---|
| `test` | unit tests |
| `itest` | integration tests, including edit-context round trips |
| `slowtest` | slow tests |
| `inttest` | every character export test at once |
| `pfinttest` and similar | per-game-mode end-to-end character export |

The per-game-mode tasks export a character and compare the output, which catches
changes in behaviour that a load test cannot see.

## How this handbook uses them

Every tag in an example here is checked against a generated index, and argument forms
are checked against the shipped data corpus. Neither is a substitute for `datatest`,
which is why the examples are written to be loadable rather than only syntactically
valid.

See [verification](https://github.com/shnaps/pcgen-handbook#how-it-stays-correct).

## Related

- [The token system](token-system.md) — why round-tripping is the core assertion
- [Adding a tag](adding-a-tag.md) — writing a token and its test
- [When it breaks](../start/when-it-breaks.md) — diagnosing a failing load
