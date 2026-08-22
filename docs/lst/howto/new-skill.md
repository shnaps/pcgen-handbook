---
title: Add a skill
---

# Add a skill

Goal: a working skill a character can put ranks into.

Skills are smaller than most file types — seven tags of their own. Most of the work is
deciding how they interact with classes.

## Before you start

- A working folder and a campaign that loads — see [Set up](../../start/setup.md).
- `SKILL:my_skills.lst` uncommented in your `.pcc`.

## The simplest skill

```
Sample Skill	KEYSTAT:INT	USEUNTRAINED:YES	TYPE:General	DESC:An example skill.
```

Four decisions, and they are the four you make every time:

| Decision | Tag |
|---|---|
| Which ability score applies | `KEYSTAT` |
| Can an untrained character try it | `USEUNTRAINED` |
| How it groups, for prerequisites and choosers | `TYPE` |
| Does armour interfere | `ACHECK` |

## KEYSTAT is game mode dependent

The value is a stat abbreviation *defined by the game mode*, not a fixed list. In
`35e` those are the familiar six. A different game mode may define others.

```
Sample Athletics	KEYSTAT:STR	USEUNTRAINED:YES	ACHECK:YES	TYPE:General
```

The stat is stored as a reference, so a name that does not exist is reported after
loading rather than on the line itself. An error naming a stat usually means a typo
here.

*Source: [`KeystatToken.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/plugin/lsttokens/skill/KeystatToken.java)*

## Armour check

```
ACHECK:NONE     armour never matters
ACHECK:YES      the normal armour check penalty applies
ACHECK:NONPROF  penalty only when not proficient with the armour worn
ACHECK:DOUBLE   double the normal penalty
ACHECK:WEIGHT   penalty scales with weight carried, not armour
```

`YES` is the one you want almost every time — 253 of the 262 uses in shipped data.

*Source: [`SkillArmorCheck.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/cdom/enumeration/SkillArmorCheck.java)*

## Trained-only and exclusive skills

Two different restrictions that get confused:

```
Sample Craft	KEYSTAT:INT	USEUNTRAINED:NO	EXCLUSIVE:YES	TYPE:General.Craft
```

- `USEUNTRAINED:NO` — a character with zero ranks cannot attempt it at all.
- `EXCLUSIVE:YES` — restricts which classes may buy ranks at class-skill cost.

They are independent. A skill can be either, both or neither.

## Situational variants

`SITUATION` names variants of one skill without making them separate skills:

```
Sample Skill	KEYSTAT:INT	USEUNTRAINED:YES	SITUATION:In darkness	SITUATION:While climbing
```

Repeat the tag for each variant.

## Making it a class skill

Two places can declare this, and picking one matters.

From the skill's side:

```
Sample Skill	KEYSTAT:INT	CLASSES:Sample Class
```

Or from the class's side, which is what most shipped data does. Declaring it in both
places means the same relationship is defined twice, and the two can drift apart.

**Pick one direction and keep to it across your data set.** From the class side is the
usual choice, because a class is where someone looks to see what it can do.

## The finished file

```
# my_skills.lst - example skills
# Invented content. Nothing from a published book.

Sample Skill	KEYSTAT:INT	USEUNTRAINED:YES	ACHECK:NONE	TYPE:General	DESC:An example skill.
Sample Athletics	KEYSTAT:STR	USEUNTRAINED:YES	ACHECK:YES	TYPE:General	DESC:An example skill affected by armour.
Sample Craft	KEYSTAT:INT	USEUNTRAINED:NO	ACHECK:NONE	EXCLUSIVE:YES	TYPE:General.Craft	DESC:An example trained-only skill.
```

## Check it worked

1. Restart PCGen and load your campaign.
2. Make a character and open the skill tab.
3. Confirm `Sample Skill` is listed and takes ranks.
4. Put the character in armour and confirm `Sample Athletics` picks up the penalty.
5. Confirm `Sample Craft` cannot be used at zero ranks.

## When it does not work

| Symptom | Cause |
|---|---|
| Skill missing entirely | PCC line still commented out |
| Error naming a stat | `KEYSTAT` typo, or a stat this game mode does not define |
| Skill present but unusable at 0 ranks | `USEUNTRAINED:NO` — that is what it means |
| Armour penalty not applied | `ACHECK:NONE`, or the skill is not armour-affected |
| Skill not a class skill anywhere | nothing declares it, from either side |
| Skill invisible | `VISIBLE:NO` |

## Related

- [Skill files](../files/skill.md) — every skill tag
- [Add a feat](new-feat.md) — feats that grant skill bonuses
- Video: [Homebrew Basics 2 — Simple Feats & Skills](https://www.youtube.com/watch?v=9tha4tQ1zNk),
  recorded against PCGen 6.05
