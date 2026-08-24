"""Flag SRD content used as example material in the handbook.

Examples must use invented content. The site is public, and keeping Open Game
Content off it keeps the licence's attribution obligations off it too. Nothing
enforced that rule until this script, and two breaches had reached the site.

Names are taken from the RSRD data PCGen ships, restricted to the object kinds
that turn up in examples: skills, feats, spells, equipment, deities, domains,
classes and races. A stoplist removes words that are ordinary English as well
as object names.

Fenced blocks and inline code spans are both scanned. Prose is not - the false
positive rate on ordinary sentences is too high to be useful, so a name used in
a sentence rather than an example has to be caught by reading.

Exit 1 on any hit.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SRC = ROOT / "work" / "pcgen-src"
SRD = SRC / "data" / "35e" / "wizards_of_the_coast" / "rsrd"

# Words that name a shipped object and are also ordinary English. A hit on one
# of these says nothing about where the text came from.
STOPLIST = {
    "string", "nothing", "active", "order", "close", "touch", "symbol", "title",
    "focus", "blade", "magic", "guide", "fantasy", "status", "trade", "spells",
    "prepared", "talent", "talents", "archetype", "special ability", "class feature",
    "scroll", "beast", "elemental", "outsider", "humanoid", "arcane", "priest",
    "adept", "warrior", "explorer", "silver", "flame", "wards", "unseen", "blessed",
    "awareness", "feats", "reflex", "fortitude",
    # size codes and armour categories are mechanical vocabulary, not content
    "light", "medium", "heavy", "large", "small", "tiny", "huge",
}

SKIP_PAGES = {"lst/reference/tag-index.md", "outputsheets/token-index.md"}

# Naming one shipped object to explain a mechanism is documentation, not an
# example, so a few pairs are allowed by hand. Keyed by page and name so the
# same word is still caught anywhere it is used as example content, and each
# entry carries the reason it is here.
ALLOWED = {
    # the fact is which type stacks, and the type has a name
    ("lst/concepts/bonuses.md", "Dodge"),
    # a real key, quoted to show that keys may contain spaces
    ("lst/files/equipment-modifier.md", "Adamantine"),
    # named to show armour profs are per item, which is why a category fails
    ("lst/howto/new-equipment.md", "Padded"),
}
FENCE = re.compile(r"```.*?\n(.*?)```", re.S)
INLINE = re.compile(r"`([^`\n]+)`")
SPLIT = re.compile(r"[\t|:,=\r\n]+")


def srd_names():
    """Object names from the RSRD, from the file kinds examples actually use."""
    names = set()
    if not SRD.is_dir():
        return names
    for path in SRD.rglob("*.lst"):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line or line[0] == "#":
                continue
            first = line.split("\t")[0].strip()
            if not first or ":" in first or len(first) < 5:
                continue
            if not re.fullmatch(r"[A-Z][A-Za-z' \-]+", first):
                continue
            if first.lower() in STOPLIST:
                continue
            names.add(first)
    return names


def main():
    names = srd_names()
    if not names:
        print("no RSRD data found under work/pcgen-src - skipping")
        return 0

    hits = []
    for page in sorted(DOCS.rglob("*.md")):
        rel = page.relative_to(DOCS).as_posix()
        if rel in SKIP_PAGES:
            continue
        text = page.read_text(encoding="utf-8")
        found = set()
        for block in FENCE.findall(text) + INLINE.findall(text):
            for part in SPLIT.split(block):
                words = part.strip().split()
                for size in (1, 2, 3):
                    for i in range(len(words) - size + 1):
                        phrase = " ".join(words[i:i + size])
                        if phrase in names:
                            found.add(phrase)
        for phrase in sorted(found):
            if (rel, phrase) not in ALLOWED:
                hits.append((rel, phrase))

    if hits:
        print("%d SRD name(s) in examples:" % len(hits))
        for rel, phrase in hits:
            print("  %-44s %s" % (rel, phrase))
        print("\nExamples use invented content. Replace these.")
        return 1

    print("checked %d pages" % len(list(DOCS.rglob("*.md"))))
    print("no SRD content in examples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
