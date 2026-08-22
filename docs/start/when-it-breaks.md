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

*Source: [`LoggingRecorder.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/system/LoggingRecorder.java)*

## What the levels mean

PCGen adds three levels of its own for data problems, on top of the usual ones:

| Level | Means |
|---|---|
| `LST_ERROR` | the line failed. That data is not loaded. |
| `LST_WARNING` | the line loaded, but something is wrong or deprecated |
| `LST_INFO` | informational, usually safe to ignore |

Data loading logs at `LSTWARN` by default, so errors and warnings both appear without
you changing anything.

Deprecation notices arrive as warnings. They mean your data works today and will not
forever — see [what changed](../appendix/whats-changed.md).

*Source: [`Logging.java`](https://github.com/PCGen/pcgen/blob/d262f8b44952860ff857132035fb32d8d11361fa/code/src/java/pcgen/util/Logging.java)*

## Turning up the detail

Levels are set in `logging.properties` in the install folder. The `pcgen` and `plugin`
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

In rough order of how often they catch people:

| Symptom | Cause |
|---|---|
| Nothing loaded, no error | the PCC line is still commented out |
| Campaign not in the source list | PCGen did not find the `.pcc`, or the game mode name is wrong |
| Unknown tag error | typo, or a tag removed since the tutorial you followed |
| Everything on one line failed | fields separated by spaces instead of tabs |
| Object loads but does nothing | wrong `TYPE`, or missing `CATEGORY` on an ability |
| Reference not found | name mismatch, including a trailing space |
| Worked yesterday, fails now | you edited a file PCGen ships and an update replaced it |

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

That is covered in [the load pipeline](../internals/load-pipeline.md#verifying-a-dataset-loads).

## Related

- [How loading works](how-loading-works.md) — why reference errors surface late
- [Line format](../lst/concepts/line-format.md) — tabs, fields and comments
- [What changed](../appendix/whats-changed.md) — deprecation warnings explained
- Video: [Debugging Tips and Demo](https://www.youtube.com/watch?v=7yr-q27WeKY),
  recorded against 6.05/6.06
