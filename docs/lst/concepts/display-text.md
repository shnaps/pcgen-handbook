---
title: Text the player reads
---

# Text the player reads

Five tags carry the text a player sees on screen and on a character sheet. Four of them
share one placeholder grammar.

`DESC` is one of the five most-used tags in the data language. Shipped data writes it
**99,997** times, behind `TYPE`, `BONUS`, `SOURCEPAGE` and `CATEGORY`.

| Tag | Uses | Legal on | Carries |
|---|---|---|---|
| `DESC` | 99,997 | anything | the description of the object |
| `ASPECT` | 11,774 | abilities | a named value a sheet can look up |
| `SAB` | 11,297 | anything grantable | a special ability line |
| `BENEFIT` | 5,438 | abilities | what the ability gives, in one line |
| `TEMPDESC` | 1,035 | anything | the description while a temporary bonus is active |

## DESC

```
Sample Feat	CATEGORY:FEAT	TYPE:General	DESC:Grants a bonus to Climb.
```

The text runs to the first `|`. Everything after that is either a variable or a
prerequisite.

```
DESC:Grants a %1 bonus to Climb.|2
DESC:Grants a bonus while wet.|PREVAR:GTEQ,Wet,1
```

*Source: [`DescLst.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/DescLst.java)*

### The placeholder grammar

The text takes numbered placeholders and nothing else:

| In the text | Becomes |
|---|---|
| `%1`, `%2` | the first, second variable after the pipes |
| `%{1}` | the same, bracketed. Numbers only |
| `%%` | a literal `%` |

**The named forms are variables, not text.** `%NAME`, `%CHOICE`, `%LIST` and `%FEAT=` go
in the pipe list, and the text refers to them by number:

```
DESC:Adds a bonus to %1.|%CHOICE
```

| As a variable | Resolves to |
|---|---|
| `%NAME` | the object's output name |
| `%CHOICE` | what the player chose |
| `%LIST` | the full selection from a [chooser](choosers.md) |
| `%FEAT=` | a named feat |

Writing `DESC:Adds a bonus to %CHOICE.` does not work. Shipped data agrees: of the 135
`DESC` fields using `%CHOICE`, **none** puts it in the text.

`BENEFIT`, `SAB` and `TEMPDESC` all build the same object as `DESC`, so all four take the
same grammar.

**A bare `%` is caught.** A `%` with no digits after it renders as a literal `%` and logs
a warning telling you to escape it as `%%`.

*Source: [`Description.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/Description.java)*

### Clearing

```
DESC:.CLEAR
DESC:.CLEAR.Grants a bonus
```

`.CLEAR` drops every description. `.CLEAR.<pattern>` drops the ones matching. Both are
for [`.MOD`](modifying-data.md). A `.CLEAR` in the middle of a tag fails with `confused
by '.CLEAR' as a middle token`.

## ASPECT

```
Sample Feat	CATEGORY:FEAT	TYPE:General	ASPECT:Ability Benefit|Adds %1 to Climb.|2
```

Two required parts, a name and a value, then variables and prerequisites as with `DESC`.

**Nothing validates the name.** Aspect names are invented by whoever writes the data and
held in a case-insensitive map created on demand. Shipped data uses **226 distinct
names**, and the code registers none of them.

The most-used names in shipped data:

| Name | Uses |
|---|---|
| `Ability Benefit` | 1,825 |
| `ChildAbility` | 1,338 |
| `NAME` | 972 |
| `SaveBonus` | 926 |
| `CheckType` | 920 |

So a misspelt aspect name is not an error. It creates a second aspect that nothing reads,
and the sheet shows a blank where the value should be. Copy the name from data that
already works.

Several aspects may share a name. They accumulate in a list under that key.

*Source: [`AspectToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/ability/AspectToken.java)*

## BENEFIT and SAB

Both hold a line of text about what something does. They differ in where the text goes.

`BENEFIT` is for abilities. Several benefits on one ability are joined with a single
space into one string.

`SAB` is a special ability line, legal on anything that can be granted. It is refused on
an `Ungranted` object type.

Neither may consist of only a prerequisite. `SAB:PRELEVEL:MIN=5` fails with `Cannot have
only PRExxx subtoken`.

*Source: [`BenefitFormatting.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/core/BenefitFormatting.java)*

## Which one to write

| You want | Use |
|---|---|
| the description of the thing | `DESC` |
| a value a sheet reads by name | `ASPECT` |
| one line summarising what an ability gives | `BENEFIT` |
| a special ability granted by a class, race or template | `SAB` |

`DESC` is legal everywhere and is the safe default. Reach for the others when a sheet or
the interface needs the text in a particular place.

## What breaks

**A description that is only a prerequisite.** `DESC:PRELEVEL:MIN=5` fails with
`encountered only a PRExxx`.

**Unbalanced brackets.** `DESC` checks that parentheses match and fails the line if they
do not.

**A stray `%`.** Not an error, and not silent. It renders as a literal `%` and logs a
warning asking you to write `%%`.

**A named form written into the text.** `%CHOICE` in the text is not substituted. Put it
in the pipe list and write `%1`.

**A misspelt aspect name.** Not an error. The value goes into a key nothing reads.

**Invalid XML characters.** Rejected, because the text reaches sheets that are XML.

## Where to look

| Task | Class |
|---|---|
| the `DESC` tag | `plugin/lsttokens/DescLst.java` |
| placeholder substitution | `pcgen/core/Description.java` |
| the `ASPECT` tag | `plugin/lsttokens/ability/AspectToken.java` |
| aspect names | `pcgen/cdom/enumeration/AspectName.java` |
| joining several benefits | `pcgen/core/BenefitFormatting.java` |
| the `SAB` tag | `plugin/lsttokens/SabLst.java` |

## Related

- [Ability files](../files/ability.md) — where `ASPECT` and `BENEFIT` are legal
- [Choosers](choosers.md) — what `%CHOICE` and `%LIST` stand for
- [Prerequisites](prerequisites.md) — the `PRExxx` that may end any of these tags
- [Modifying existing data](modifying-data.md) — `.MOD`, which `.CLEAR` is for
- [Output sheets](../../outputsheets/token-index.md) — what reads these on the way out
