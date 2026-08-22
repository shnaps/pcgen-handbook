---
title: What changed since the videos
---

# What changed since the videos

The [video lessons](credits.md) were recorded against PCGen 6.05 and 6.06. So were
the homebrew template files PCGen still ships. Both teach things that have since been
deprecated or removed.

**This page is the only place in the handbook where those appear.** Everywhere else
documents what is current. If a tag is listed here, do not write new data with it.

Read it if you are following a video, adapting old data, or wondering why a tag from a
tutorial produces a warning.

Checked against PCGen `6.09.08.RC1`, commit
[`d262f8b4`](https://github.com/PCGen/pcgen/tree/d262f8b44952860ff857132035fb32d8d11361fa).

## Feats became abilities

This is the single biggest change, and it touches nearly every video.

A feat is now one **category** of ability. The whole family of feat-specific tags is
deprecated in favour of the ability equivalents. PCGen's message when it sees one says
plainly that feat-based tokens are deprecated and to use ability-based ones.

| Old | Current |
|---|---|
| `FEAT:file.lst` in a PCC | `ABILITY:file.lst` |
| no category on the line | `CATEGORY:FEAT` on the line |
| `FEAT:` on a race, template, domain or kit | `ABILITY:` with a category |
| `VFEAT:` | `ABILITY:` granted as virtual |
| `ADD:FEAT`, `ADD:VFEAT` | `ADD:ABILITY` |
| `AUTO:FEAT` | `AUTO:ABILITY` |
| `REMOVE:FEAT` | `REMOVE:ABILITY` |
| `CHOOSE:FEAT`, `CHOOSE:FEATSELECTION` | `CHOOSE:ABILITY` |
| `MODIFYFEATCHOICE` | — |

Old data still loads. PCGen logs a deprecation warning for each one.

See [ability files](../lst/files/ability.md) for how to write the current form.

## Removed outright

These do not merely warn. They no longer exist, and PCGen reports an error.

| Gone | Use instead |
|---|---|
| `BONUS:COMBAT\|BAB` | `BONUS:COMBAT\|BASEAB` |
| `ACVALUE` | — |
| `ACABBREV` | — |
| `BABABBREV` | — |
| `DISPLAYVARIABLE` | — |

`BONUS:COMBAT|BAB` is the one most likely to bite, because base attack progression
appears in every class tutorial. It was removed over its behaviour around epic class
levels. Shipped data uses `BASEAB` about 2,100 times and `BAB` not at all.

!!! warning "The official docs still list some of these"
    `ACVALUE`, `ACABBREV`, `BABABBREV` and `DISPLAYVARIABLE` are still in PCGen's
    published tag documentation. They are not in the code. This handbook's
    [tag index](../lst/reference/tag-index.md) is generated from the source, so it does
    not list them.

## DEFINE lost two forms

`DEFINE` is still current, but two of its argument forms are rejected at parse time. Both
handled stats, and both moved to `DEFINESTAT`.

| Gone | Use instead |
|---|---|
| `DEFINE:LOCK.<stat>` | `DEFINESTAT:LOCK` or `DEFINESTAT:NONSTAT` |
| `DEFINE:UNLOCK.<stat>` | `DEFINESTAT:STAT` or `DEFINESTAT:UNLOCK` |

`DEFINESTAT` takes six subtokens: `LOCK`, `UNLOCK`, `NONSTAT`, `STAT`, `MINVALUE` and
`MAXVALUE`.

The error text for the `LOCK` case names `DEFINESTAT:LOCL|`, which is a typo in the
source. There is no `LOCL` subtoken. Read it as `LOCK`.

A third form still loads but warns. `DEFINE` with a non-zero value logs a deprecation
notice asking for a `DEFINE` of 0 and a bonus instead. `MAXLEVELSTAT=` is exempt. See
[declaring a variable](../lst/concepts/declaring-variables.md) for the form to write.

*Source: [`DefineLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/DefineLst.java)*

## REMOVE has no current form

`REMOVE:` registers one subtoken, `REMOVE:FEAT`, and both its parent and its subtoken sit
in `plugin/lsttokens/deprecated/`. The subtoken reports that feat-based tokens are
deprecated in favour of ability-based ones.

There is no `REMOVE:ABILITY`. The feat-to-ability move gave `ADD:FEAT` a successor in
`ADD:ABILITY` and left `REMOVE` without one.

Shipped data uses it 35 times, all `REMOVE:FEAT`. See
[granting things](../lst/concepts/granting.md) for the tags that are current.

*Source: [`RemoveLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/deprecated/RemoveLst.java)*

## Deprecated by file type

| File type | Deprecated tags |
|---|---|
| Class | `ABB`, `CLASSTYPE`, `SPELLTYPE`, `DOMAIN` |
| Deity | `APPEARANCE`, `PANTHEON`, `RACE`, `SYMBOL`, `TITLE`, `WORSHIPPERS` |
| Race | `FEAT`, `CHOOSE` (language auto form) |
| Template | `FEAT`, `APPLIEDNAME`, `CHOOSE` (language auto form) |
| Ability | `APPLIEDNAME`, `MODIFYFEATCHOICE` |
| Equipment | `RATEOFFIRE` |
| Stat | `PENALTYVAR` |
| Campaign (PCC) | `FEAT` |

23 distinct tags are marked deprecated in the source, across 32 token classes.

The deity group is the one to watch if you are following the deity video — six of that
file type's tags are deprecated. The source marks them without naming a replacement, so
check current shipped deity data before writing new files.

## Added, and not documented upstream

The reverse case. PCGen 6.07 shipped a new formula system. Two of its tags exist in the
code and are absent from the official documentation:

| Tag | Applies to |
|---|---|
| `MODIFY` | objects holding variables |
| `MODIFYOTHER` | objects holding variables |

The [ORDEREDPAIR video](https://www.youtube.com/watch?v=Oicxs-dI7gU) covers an early
part of this system.

## Why this drift exists

PCGen's tag documentation mostly stopped carrying version markers around 6.03. Its last
stable release is from February 2023, while development continues on `master`. Nobody
has resolved a documentation ticket since 2018.

That is the reason this handbook reads the Java source rather than the docs, and why a
scheduled job re-reads it weekly. See [decisions](https://github.com/shnaps/pcgen-handbook/blob/main/DECISIONS.md).

## Related

- [Credits](credits.md) — the playlist, and why it is not a syntax source
- [Tag index](../lst/reference/tag-index.md) — every tag currently implemented
- [Credits](credits.md)
