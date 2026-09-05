---
title: When it breaks
---

# When it breaks

Data that fails to load is the normal state of writing data. This page is how to find
out why.

## Read the log first

PCGen writes to **`pcgen.log`**. Read it before changing anything. It names the file
and usually the line.

The file is written to PCGen's working directory. That is the install folder for a
normal start, and somewhere else if you launched from a script.

Cannot find it? PCGen keeps the same messages in memory and shows them in its own log
window. That is the reliable way to read them.

*Source: [`LoggingRecorder.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/system/LoggingRecorder.java)*

## What the levels mean

PCGen adds three levels of its own for data problems, on top of the usual ones:

| Level in the log | Means |
|---|---|
| `LSTERROR` | the line failed. That data is not loaded. |
| `LSTWARN` | the line loaded, but something is wrong or deprecated |
| `LSTINFO` | informational, usually safe to ignore |

Search the log for those spellings. The Java constants are named `LST_ERROR`,
`LST_WARNING` and `LST_INFO`, but the log writes the shorter names above. PCGen's own
log window labels them Data Errors, Data Warnings and Data Info.

Data loading logs at `LSTWARN` by default, so errors and warnings both appear without
you changing anything.

Deprecation notices arrive as warnings, when the preference for them is on. They mean
your data works today and will not forever — see [what changed](../appendix/whats-changed.md).

*Source: [`Logging.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/util/Logging.java)*

## Turning up the detail

Levels are set in `logging.properties`. PCGen looks beside `options.ini` first, then in the install folder. The `pcgen` and `plugin`
entries control data loading.

Raising the detail is worth it when a load succeeds but the result is wrong, because
the interesting messages are below warning level.

## Two kinds of failure

This distinction saves the most time.

**Parse failures** happen at the line. A tag name PCGen does not know, or a value it
cannot read. The message names your file and line, and the fix is usually there.

**Reference failures** happen after everything is loaded. A name that matched nothing
— a skill, feat or class that does not exist under that name. The message may name a
*different* file, because the complaint comes from whatever pointed at the missing
thing.

So an error naming a file you never edited usually means your file spelled something
wrongly, or did not load at all.

## The common causes

In rough order of how often they catch people. The middle column is the message text as
the loader writes it, so it can be searched for.

| Symptom | What the log says | Cause |
|---|---|---|
| Nothing loaded, no error | nothing | the PCC does not name your file, or the line is commented out |
| Campaign not in the source list | nothing | PCGen did not find the `.pcc`, or the game mode name is wrong |
| A tag name is not recognised | `Illegal Token '<tag>'` | a misspelt tag, or one not legal on that line type |
| One field rejected | `Invalid Token - does not contain a colon` | a stray word, or spaces where a tab belongs |
| One field rejected | `Invalid Token - starts with a colon` | a missing tag name before the colon |
| A line named with its number | `Error parsing file <file> line <n>` | the tag was found but its value would not parse |
| A tag still works but complains | `<tag> deprecated. Tag was <text> in <object>` | the tag has a successor. See [what changed](../appendix/whats-changed.md) |
| Object loads but does nothing | nothing | wrong [`TYPE`](../lst/concepts/types.md) |
| An ability is missing entirely | `A Category is required for an Ability` | no `CATEGORY:` on the line, so it was rejected |
| Reference not found | names a file you may not have edited | name mismatch, including a trailing space |
| Worked yesterday, fails now | varies | you edited a file PCGen ships and an update replaced it |

*Source: [`LstUtils.java`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/java/pcgen/persistence/lst/LstUtils.java)*

## Lines that are skipped, not failed

Three cases drop your line and carry on. The load finishes, so it looks like it worked.

| Message | Means |
|---|---|
| `PObject <name> not found; .COPY skipped.` | the object you copied from did not load |
| `PObject <name> not found; .MOD skipped.` | the object you modified did not load |
| `WARNING: Duplicate object name: <key>` | two objects share a key. One of them is dropped |

The first two usually mean a load-order problem rather than a spelling one. The object
has to exist before the line that changes it runs. See
[sources](../lst/concepts/sources.md) for the order files load in, and
[keys and names](../lst/concepts/keys-and-names.md) for which duplicate survives.

*Source: [`LanguageBundle.properties`](https://github.com/PCGen/pcgen/blob/d4ade6d509f4206b1c1789848752e633ec3c134c/code/src/resources/pcgen/lang/LanguageBundle.properties)*

## Narrowing it down

When the message is not enough:

1. **Comment out your new lines.** Confirm it loads clean without them. If it does not,
   the problem is older than you think.
2. **Add them back one at a time.** Restart between each. The first failure names the
   line.
3. **Cut the failing line down.** Remove tags until it loads, then add them back. The
   tag that breaks it is the one to look up.
4. **Check the name resolves.** Copy the exact name from the object being referenced.
   Do not retype it.

Restarting matters. Data is read once at load time, so editing a file while PCGen runs
changes nothing until you reload.

## Whitespace

Worth its own mention because it is invisible.

- Fields are separated by **tabs**. A run of spaces is not a separator.
- A space before a tab becomes part of the value. `Sample Feat ` and `Sample Feat` are
  different names, and only one of them matches.
- A tab-to-space conversion by your editor breaks every line in the file at once.

Turn on visible whitespace. See [Set up](setup.md).

## Checking a whole data set

PCGen has no command that validates a dataset on its own. The nearest thing is the
test harness its own CI runs, which loads data through the production loader and
requires zero errors and zero warnings.

That is covered in [testing](../internals/testing.md), which owns the harness and the one
trap that makes a green run meaningless.

## Related

- [How loading works](how-loading-works.md) — why reference errors surface late
- [Line format](../lst/concepts/line-format.md) — tabs, fields and comments
- [What changed](../appendix/whats-changed.md) — deprecation warnings explained
- Video: [Debugging Tips and Demo](https://www.youtube.com/watch?v=7yr-q27WeKY),
  recorded against 6.05/6.06
