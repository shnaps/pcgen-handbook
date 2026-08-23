---
title: Set up
---

# Set up

Goal: PCGen running, and a folder of your own where your data will survive upgrades.

## Install PCGen

Get a build from [pcgen.org](https://pcgen.org) or from the
[nightly builds](https://github.com/PCGen/pcgen/releases).

!!! tip "Prefer a nightly"
    The newest tagged release is `7.00.001`, from February 2026. Development continues
    on `master`, so most people working on PCGen data run a nightly build. This handbook
    documents `6.09.08.RC1`.

PCGen needs Java. Recent builds bundle it, so try running it before installing Java
separately.

## Find the install folder

Everything you care about lives in the folder PCGen was installed to.

| Folder | Holds |
|---|---|
| `data/` | all game data, one folder per game mode |
| `system/` | game mode rules — stats, sizes, load limits |
| `outputsheets/` | character sheet templates |
| `docs/` | PCGen's own documentation |
| `pcgen.log` | error output — you will need this |

Open `data/`. Each subfolder is a game mode: `35e`, `pathfinder`, `5e` and others.

## Make your own folder

PCGen ships a homebrew starter set at `data/35e/homebrew/my_homebrew/`. Look at it —
it has a template file for every data type, each with notes inside.

**Do not work in it directly.** Copy it, and rename the copy:

```
data/35e/homebrew/my_homebrew/    <- shipped template, leave alone
data/35e/homebrew/testburg/       <- your copy, work here
```

Renaming matters. A reinstall or upgrade can overwrite anything PCGen ships, and
`my_homebrew` is a folder PCGen ships. Work in a folder with your own name on it and
an upgrade cannot touch it.

Inside your copy you will find:

- `my__campaign.pcc` — the campaign file. Lists which data files to load.
- `my_feats.lst`, `my_classes.lst`, `my_races.lst` and so on — one file per data type.

Rename these too if you like. The `.pcc` is what names the others, so change it and
keep the names matching.

## Get a text editor

Any plain text editor works. You need two things from it:

- **Visible whitespace.** Fields are separated by tabs, and a tab that became spaces
  is the most common reason a file fails to load. You want to see the difference.
- **No auto-formatting.** Do not let it convert tabs to spaces, wrap long lines, or
  add a byte order mark.

VS Code, Notepad++ and Sublime Text all do this. So does anything else with a
whitespace toggle.

!!! warning "Word processors will corrupt your data"
    Do not use Word, WordPad or Google Docs. They rewrite quotes, insert formatting and
    save the wrong file type.

## Check it works

Start PCGen. Go to the source selection screen and look for your campaign under
**Homebrew**. If it is listed, PCGen has found your `.pcc` and you are set up.

If it is not listed, PCGen either did not find the file or rejected it. Check that
your folder is under a game mode folder inside `data/`.

## Next

[Your first change](first-change.md) — write a feat and see it in PCGen.
