---
title: Granting things
---

# Granting things

Two tags hand something to a character. `AUTO` grants it outright. `ADD` asks the player
to choose.

Shipped data writes `AUTO:` **7,449** times and `ADD:` **3,678** times. Both take a
subtoken naming what is granted.

| Tag | The player | Use it for |
|---|---|---|
| `AUTO:` | gets it, no prompt | what the race, class or template always provides |
| `ADD:` | is asked to pick | a choice the character makes on gaining the object |

## AUTO

```
AUTO:LANG|Sample Tongue
AUTO:WEAPONPROF|TYPE.Simple
```

Five current subtokens. A sixth, `AUTO:FEAT`, is deprecated and used once:

| Subtoken | Uses | Grants |
|---|---|---|
| `LANG` | 3,491 | a language |
| `WEAPONPROF` | 3,115 | a weapon proficiency |
| `EQUIP` | 457 | a piece of equipment |
| `ARMORPROF` | 236 | an armour proficiency |
| `SHIELDPROF` | 149 | a shield proficiency |

Arguments are separated by `|`. List several in one tag.

### A prerequisite must come last

```
AUTO:LANG|Sample Tongue|PRELEVEL:MIN=5
```

Put a `PRExxx` anywhere but the end and the line fails with `PRExxx must be at the END
of the Token`. The parser reads the prerequisite, then treats everything before it as the
list of things to grant.

### `.CLEAR` must come first

```
AUTO:LANG|.CLEAR
```

Anywhere else it fails with `When used, .CLEAR must be the first argument`.

### `%LIST` grants what a chooser picked

```
AUTO:WEAPONPROF|%LIST
```

`%LIST` stands for the selection made by the [chooser](choosers.md) on the same object.
The grant happens once the player has picked. With a prerequisite attached, the grant
becomes conditional on that choice.

*Source: [`auto/LangToken.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/auto/LangToken.java)*

## ADD

```
ADD:ABILITY|FEAT|NORMAL|Sample Feat,Sample Other Feat
```

Eight classes register **seven** distinct current subtokens — `ClassSkillsToken` and
`ClassSkillsLevelToken` both answer to `CLASSSKILLS`. Two more forms in the table below
are deprecated:

| Subtoken | Uses | Offers |
|---|---|---|
| `SPELLCASTER` | 2,587 | caster levels in another class |
| `ABILITY` | 969 | one or more abilities |
| `LANGUAGE` | 66 | a language |
| `CLASSSKILLS` | 26 | skills that become class skills |
| `EQUIP` | 10 | equipment |
| `SKILL` | 9 | a skill |
| `TEMPLATE` | 1 | a template |
| `FEAT` | 9 | deprecated, use `ABILITY` |
| `VFEAT` | 1 | deprecated, use `ABILITY` with `VIRTUAL` |

### The shape of `ADD:ABILITY`

```
ADD:ABILITY|<count>|<category>|<nature>|<ability>,<ability>
```

The count is optional and comes first. Leave it out and the character picks one:

```
ADD:ABILITY|FEAT|NORMAL|Sample Feat
ADD:ABILITY|2|FEAT|NORMAL|Sample Feat,Sample Other Feat
```

The parser tells the two apart by counting pipes. A count must resolve above zero.

**Nature** must be `NORMAL` or `VIRTUAL`. `AUTOMATIC` and `ANY` are both rejected by
name. A virtual ability is granted without spending from the pool.

PCGen builds the prompt title itself. The category is followed by `Choice`, and the
nature is prepended only when it is not `NORMAL`. So `NORMAL` gives `FEAT Choice` and
`VIRTUAL` gives `VIRTUAL FEAT Choice`. There is no tag to override it.

### Repeats

Add `STACKS` to the ability list to let the same choice be taken more than once, or
`STACKS=<n>` to cap it. Two stacking specifications in one tag is an error.

*Source: [`add/AbilityToken.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/plugin/lsttokens/add/AbilityToken.java)*

## REMOVE is not a current tag

`REMOVE:` has one subtoken, `REMOVE:FEAT`, and it is deprecated. The token class states
that feat-based tokens are deprecated in favour of ability-based ones.

Shipped data uses it 35 times, all of them `REMOVE:FEAT`. There is no current
replacement tag that takes something away the way `ADD` gives it.

[What changed](../../appendix/whats-changed.md) carries the detail. Do not write it.

## What breaks

**A prerequisite in the middle of an `AUTO`.** Hard failure, with the message naming the
end of the token.

**A count of zero.** `ADD:ABILITY|0|FEAT|NORMAL|Sample Feat` fails with `Count in
ADD:ABILITY must be > 0`.

**`AUTOMATIC` as a nature.** Rejected by name. `AUTO:` is how something is granted
without a choice.

**Mixing `ANY` with a named ability.** Fails with `Contains ANY and a specific
reference`.

**Expecting `ADD` to grant silently.** It does not. It queues a choice the player answers
when the object is gained.

## Where to look

| Task | Class |
|---|---|
| the `ADD:` tag and its dispatch | `plugin/lsttokens/add/` — 8 classes, 8 tests |
| the `AUTO:` tag and its dispatch | `plugin/lsttokens/auto/` — 5 classes, 5 tests |
| the deprecated `REMOVE:` | `plugin/lsttokens/deprecated/RemoveLst.java` |
| what a nature means | `pcgen/cdom/enumeration/Nature.java` |
| accepted and rejected syntax | `code/src/test/plugin/lsttokens/{add,auto}/` |

## Related

- [Choosers](choosers.md) — `CHOOSE:`, and the `%LIST` selection `AUTO` can read
- [Prerequisites](prerequisites.md) — the `PRExxx` that must sit at the end of an `AUTO`
- [Ability files](../files/ability.md) — what `ADD:ABILITY` hands out
- [Types](types.md) — `TYPE.Simple` and matching a group instead of naming one
- [What changed](../../appendix/whats-changed.md) — `REMOVE:`, and the feat-to-ability move
