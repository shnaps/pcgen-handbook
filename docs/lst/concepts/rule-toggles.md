---
title: Rule toggles
---

# Rule toggles

An optional rule the reader switches on or off. PCGen calls them house rules, defines
them per game mode, and lets data test them with `PRERULE`.

There are **339** across the shipped game modes. Twenty modes exist and 19 carry a `rules.lst`, though only 35 distinct names — most
game modes offer the same toggles.

## Where they are defined

One file per game mode:

```
system/gameModes/35e/rules.lst
```

Each line is one toggle. Tab separated, like any [LST line](line-format.md), but field 0
carries a literal `NAME:` prefix rather than being a bare name:

```
NAME:SampleLoadPenalty	VAR:SYS_SAMPLELOAD	DEFAULT:Yes	DESC:Apply the sample load penalty
```

| Field | Does |
|---|---|
| `NAME` | an identifier for the toggle |
| `VAR` or `PARM` | the **key** data refers to |
| `DEFAULT` | `Yes` or `No`, the state before the reader touches it |
| `EXCLUDE` | another toggle this one cannot be on with |
| `DESC` | the label the reader sees |

*Source: [`plugin/lsttokens/rules/`](https://github.com/PCGen/pcgen/tree/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/rules)*

## VAR and PARM are the same mechanism

Both set the key the toggle is looked up by. Mechanically there is no difference — each
one reassociates the object's key to its value.

The difference is intent, stated in the shipped files' own comments:

| Written | Means |
|---|---|
| `VAR:` | a toggle data is expected to test with `PRERULE` |
| `PARM:` | a toggle the engine checks in Java |

Shipped game modes use `PARM:` 220 times against `VAR:` 119. The convention is not
enforced, and several `VAR:` toggles are also checked in Java, so do not read it as a
guarantee.

## EXCLUDE makes a pair

```
NAME:SampleHitPoints	VAR:SAMPLE_HP	DEFAULT:Yes	EXCLUDE:SAMPLE_VP	DESC:Use hit points
NAME:SampleVitality	VAR:SAMPLE_VP	DEFAULT:No	EXCLUDE:SAMPLE_HP	DESC:Use vitality points
```

The preferences panel renders excluded toggles as radio buttons instead of check boxes,
so choosing one clears the other. 60 of the 339 shipped entries use it.

Nothing in the loader enforces this both ways. Shipped data writes `EXCLUDE:` on **both**
lines, and that is the convention to copy.

## Testing one from data

```
PRERULE:1,SYS_SAMPLELOAD
```

`PRERULE` is an ordinary [prerequisite](prerequisites.md), so the count comes first. It
passes when at least that many of the listed toggles are on.

!!! warning "The key is the VAR, not the NAME"
    `PRERULE:1,SampleLoadPenalty` does not work. The key is the value of `VAR:` or
    `PARM:`, which is often nothing like the name.

*Source: [`PreRuleTester.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/pretokens/test/PreRuleTester.java)*

It needs no character, so it can gate anything — an ability, a bonus, a whole object.

### Almost always used inside another tag

Measured across shipped data, `PRERULE` appears **12,376 times in 123 files**. Only 134
of those are a field of their own. The rest are appended inside another tag's value:

```
Sample Feat	CATEGORY:FEAT	BONUS:SKILL|Sample Skill|2|PRERULE:1,SYS_SAMPLELOAD
```

That is the normal shape. A toggle usually switches one bonus on, not a whole object.

## What a toggle is not

**It is not a variable.** The `VAR:` value is a lookup key for the toggle, not a
character variable. `PREVAR` cannot read it, `BONUS:` cannot read it, and no formula can
reach it.

The only two ways a toggle affects anything:

1. `PRERULE` in data.
2. A hardcoded check in PCGen's Java, using a fixed constant.

The second is why some toggles work without any data referring to them. Skill maximums,
armour check penalties, weapon size rules and encumbrance all read their toggle directly
from the engine. Data cannot add a new toggle of that kind — only a Java change can.

## Where the reader sees them

Preferences, under **House Rules**. The panel lists every toggle for the loaded game
mode. A check box is labelled with its `DESC:` text; the 60 `EXCLUDE` toggles render as radio buttons labelled by key.

Choices persist. They are written to `options.ini` under `pcgen.options.ruleChecks`, as a
list of key and state pairs, and read back at startup. A toggle with no saved state falls
back to its `DEFAULT`.

!!! note "The file header is out of date"
    Shipped `rules.lst` files carry a header saying the label is looked up in
    `Language.properties` and that `DESC` is only a fallback. That is not what the code
    does. The panel reads `DESC:` directly, and no such lookup exists.

    Another instance of [the drift this handbook exists for](../../index.md).

## Rule toggles are not code controls

Two mechanisms, often confused, with no connection between them.

| | Rule toggle | [Code control](data-controls.md) |
|---|---|---|
| Set by | the reader, in preferences | the game mode, in `codeControl.lst` |
| Changed at runtime | yes | no |
| Tested from data | `PRERULE` | not tested, it changes what tags are legal |

Neither can switch the other on. They share no code.

## Gotchas

**The key is not the name.** The commonest mistake with `PRERULE`.

**A toggle only exists in its game mode.** A `PRERULE` naming a toggle that another game mode
defines never passes.

**Data cannot define a new engine-checked toggle.** Adding a line to `rules.lst` gives
you something `PRERULE` can test, and nothing more.

**`rules.lst` belongs to the game mode, not to your source.** Changing it changes the
rules system for every campaign that uses it.

**Toggles participate in the calculation loop.** At least one is checked inside the
engine's convergence loop, so a toggle can change how many passes a character takes to
settle. See [the rules engine](../../internals/rules-engine.md).

## Related

- [Prerequisites](prerequisites.md) — `PRERULE` is one of 129
- [Game modes](game-modes.md) — where `rules.lst` lives
- [Data controls](data-controls.md) — the other switch mechanism
- [The rules engine](../../internals/rules-engine.md) — what reads these at runtime
