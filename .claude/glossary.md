# Glossary

Fixed vocabulary for the handbook. ASD-STE100's base dictionary is aerospace
maintenance vocabulary and has no words for any of this, so these are declared as
project Technical Names and Technical Verbs.

Use these exact words. Do not rotate synonyms.

## Core terms

| Term | Means | Not |
|---|---|---|
| tag | `TAG:value` as written in a data file | token, field, attribute, property |
| token | the Java class implementing a tag | tag, handler |
| field | one tab-separated part of a line | column, cell, tag |
| line | one record in an LST file | row, entry |
| LST file | a `.lst` data file | list file, lst-file |
| PCC file | a `.pcc` campaign file | pcc, campaign file (in syntax contexts) |
| campaign | what a PCC defines: a book or data set | module, source |
| game mode | a rules system such as `35e` or `Pathfinder` | ruleset, system |
| key | the unique identifier for an object | name, id |
| load order | the sequence files are read in | loading order, order of loading |
| prerequisite | a `PRExxx` condition | prereq, requirement |
| bonus | a `BONUS:` modifier | buff, modifier |
| chooser | `CHOOSE:`, and the selection it drives | choice, selector |
| homebrew | user-made data | custom content, mods |

## Verbs

| Verb | Use for |
|---|---|
| load | reading a file into PCGen |
| parse | turning a line or tag into data |
| resolve | connecting a reference to its target |
| set | giving a value |
| grant | giving an ability, feat or bonus to a character |
| apply | putting a template or modifier into effect |
| override | replacing an earlier value |

Avoid **process**, **handle**, **manage** — pick the specific verb above.

## General IT words, allowed

comment, delimiter, directory, encoding, file, folder, path, plain text, syntax, tab,
whitespace, case-sensitive, build, class, method, package, repository, commit, branch.

## Capitalisation

- **PCGen** — one word, capital P and G. Never "PcGen", "pcgen" in prose, "PC Gen".
- **LST**, **PCC** — always uppercase in prose. Lowercase only in file extensions
  (`.lst`, `.pcc`).
- Tag names always uppercase exactly as written in a file: `KEYSTAT`, `PRERACE`.
