"""Re-derive every measured number the handbook states.

WIKI-SCHEMA.md says a usage figure must be measured, never recalled, and then
says the honest part: "No tool validates a number, so the method is the only
guard." This is that tool.

Counts have been the largest error class in every audit this project has run.
Rounded estimates on day one. Comment-inclusive counts on 2026-08-23, which
moved every figure they touched. Wrong-scope counts on 2026-09-01, where a
figure for the whole source tree was published as a figure for one file.

Each entry below pairs a published number with the command that derives it.
Two things fail the check:

  - the source no longer produces the number, so the page is stale
  - the number is no longer on the page, so this registry is stale

Skips without the pinned clone, as lint_wiki.py and check_srd.py do.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SRC = ROOT / "work" / "pcgen-src"
JAVA = SRC / "code" / "src" / "java"


def files(under, pattern="*.java", recursive=True):
    """Count files matching a glob."""
    base = SRC / under
    if not base.is_dir():
        return 0
    return len(list(base.rglob(pattern) if recursive else base.glob(pattern)))


def occurrences(needle, under, pattern="*.java"):
    """Count occurrences of a literal string across a tree."""
    base = SRC / under
    total = 0
    for path in base.rglob(pattern):
        total += path.read_text(encoding="utf-8", errors="replace").count(needle)
    return total


def lines_matching(regex, under, pattern="*.java"):
    """Count lines matching a regex across a tree."""
    rx = re.compile(regex)
    base = SRC / under
    total = 0
    for path in base.rglob(pattern):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if rx.search(line):
                total += 1
    return total


def files_matching(regex, under, pattern="*.java", exclude=None):
    """Count files containing a regex match."""
    rx = re.compile(regex)
    base = SRC / under
    total = 0
    for path in base.rglob(pattern):
        if exclude and exclude in path.name:
            continue
        if rx.search(path.read_text(encoding="utf-8", errors="replace")):
            total += 1
    return total


def in_file(regex, relpath):
    """Count lines matching a regex in one file."""
    path = SRC / relpath
    if not path.exists():
        return -1
    rx = re.compile(regex)
    return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
               if rx.search(line))


def data_fields(tag):
    """Count tag fields in shipped data, by the method WIKI-SCHEMA.md pins.

    Scope is data/**/*.lst. Skip a line starting '#'. Split on tabs, strip
    each field, then test the prefix. Never a substring match.
    """
    total = 0
    for path in (SRC / "data").rglob("*.lst"):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line[:1] == "#":
                continue
            for field in line.split("\t"):
                if field.strip().startswith(tag):
                    total += 1
    return total


def data_field_values(tag):
    """The same, returning the whole field so values can be counted."""
    found = []
    for path in (SRC / "data").rglob("*.lst"):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line[:1] == "#":
                continue
            for field in line.split("\t"):
                field = field.strip()
                if field.startswith(tag):
                    found.append(field)
    return found


# page, what the number counts, the figure on the page, how to derive it.
REGISTRY = [
    ("internals/facets.md", "facet classes",
     234, lambda: files("code/src/java/pcgen/cdom/facet", "*Facet.java")),

    ("lst/concepts/data-controls.md", "code controls declared",
     54, lambda: in_file(r"static final", "code/src/java/pcgen/cdom/util/CControl.java")),

    ("lst/concepts/types.md", "GROUP: fields in shipped data",
     22, lambda: data_fields("GROUP:")),
    ("lst/concepts/types.md", "GROUP:RaceType_Humanoid",
     12, lambda: data_field_values("GROUP:").count("GROUP:RaceType_Humanoid")),
    ("lst/concepts/types.md", "GROUP:UNSELECTED",
     10, lambda: data_field_values("GROUP:").count("GROUP:UNSELECTED")),
    ("lst/concepts/types.md", "isUnselected call sites",
     13, lambda: lines_matching(r"isUnselected\(\)|::isUnselected", "code/src/java")
                 - lines_matching(r"public final boolean isUnselected", "code/src/java")),

    ("lst/concepts/variables-and-formulas.md", "MODIFYOTHER fields in shipped data",
     192, lambda: data_fields("MODIFYOTHER:")),
    ("lst/concepts/variables-and-formulas.md", "of those naming the Walk mode",
     189, lambda: sum(1 for f in data_field_values("MODIFYOTHER:")
                      if f.split("|")[1:2] == ["Walk"])),

    ("internals/output-and-saving.md", "classes in plugin/exporttokens",
     140, lambda: files("code/src/java/plugin/exporttokens")),
    ("internals/output-and-saving.md", "of those, deprecated",
     49, lambda: files("code/src/java/plugin/exporttokens/deprecated")),
    ("internals/output-and-saving.md", "live top-level export classes",
     91, lambda: files("code/src/java/plugin/exporttokens", recursive=False)),
    ("internals/output-and-saving.md", "live classes extending Token directly",
     42, lambda: sum(1 for p in (JAVA / "plugin/exporttokens").glob("*.java")
                     if re.search(r"extends Token\b", p.read_text(encoding="utf-8")))),
    ("internals/output-and-saving.md", "live classes extending AbstractExportToken",
     22, lambda: sum(1 for p in (JAVA / "plugin/exporttokens").glob("*.java")
                     if "extends AbstractExportToken" in p.read_text(encoding="utf-8"))),

    ("internals/testing.md", "token test classes",
     363, lambda: len([p for p in (SRC / "code/src/test/plugin/lsttokens").rglob("*Test.java")
                       if "testsupport" not in p.parts])),

    ("internals/design.md", "game modes",
     20, lambda: len([d for d in (SRC / "system" / "gameModes").iterdir() if d.is_dir()])),

    ("internals/changing-behaviour.md", "lines naming setDirty( in PlayerCharacter",
     59, lambda: in_file(r"setDirty\(", "code/src/java/pcgen/core/PlayerCharacter.java")),
    ("internals/changing-behaviour.md", "of those, commented out",
     6, lambda: in_file(r"^\s*//.*setDirty\(",
                        "code/src/java/pcgen/core/PlayerCharacter.java")),
    ("internals/changing-behaviour.md", "setDirty( across the source",
     87, lambda: occurrences("setDirty(", "code/src/java")),
    ("internals/changing-behaviour.md", "GuiAssertions calls",
     47, lambda: lines_matching(r"GuiAssertions\.\w+\(", "code/src/java")),
    ("internals/changing-behaviour.md", "files calling them",
     26, lambda: files_matching(r"GuiAssertions\.\w+\(", "code/src/java",
                                exclude="GuiAssertions.java")),

    ("internals/running-and-debugging.md", "Logging.errorPrint calls",
     832, lambda: occurrences("Logging.errorPrint", "code/src/java")),
    ("internals/running-and-debugging.md", "log handler registrations",
     3, lambda: occurrences("Logging.registerHandler(", "code/src/java")),

    ("internals/startup.md", "initProperty family call sites",
     44, lambda: sum(occurrences(n, "code/src/java")
                     for n in ("initProperty(", "initInt(", "initBoolean("))
                 - sum(in_file(r"public \w+ " + n,
                               "code/src/java/pcgen/system/PropertyContext.java")
                       for n in ("initProperty", "initInt", "initBoolean"))),
    ("internals/startup.md", "PCGenSettings references",
     222, lambda: occurrences("PCGenSettings.", "code/src/java")),
    ("internals/startup.md", "ConfigurationSettings references",
     115, lambda: occurrences("ConfigurationSettings.", "code/src/java")),

    ("internals/ui-layer.md", "DefaultReferenceFacade fields in CharacterFacadeImpl",
     32, lambda: in_file(r"private(?!.*\bclass\b).*DefaultReferenceFacade",
                         "code/src/java/pcgen/gui2/facade/CharacterFacadeImpl.java")),
    ("internals/ui-layer.md", "facets bridged to the interface layer",
     6, lambda: occurrences("addDataFacetChangeListener", "code/src/java/pcgen/gui2")),
]


WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
    8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
    14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
    19: "nineteen", 20: "twenty",
}


def on_page(number, text):
    """Is the figure stated on the page, as digits or as a word?

    The handbook spells small numbers out, so "three registrations" has to
    satisfy an entry registered as 3.
    """
    flat = text.replace(",", "")
    if re.search(r"(?<![\d])%d(?![\d])" % number, flat):
        return True
    word = WORDS.get(number)
    return bool(word) and re.search(r"(?i)\b%s\b" % word, flat) is not None


def main():
    if not SRC.is_dir():
        print("no source checkout at work/pcgen-src, skipping")
        return 0

    wrong = []
    missing = []
    for page, label, stated, measure in REGISTRY:
        actual = measure()
        if actual != stated:
            wrong.append((page, label, stated, actual))

        text = (DOCS / page).read_text(encoding="utf-8")
        if not on_page(stated, text):
            missing.append((page, label, stated))

    if wrong:
        print("%d number(s) the source no longer produces:" % len(wrong))
        for page, label, stated, actual in wrong:
            print("  %-44s %s" % (page, label))
            print("      page says %s, source says %s" % (stated, actual))

    if missing:
        print("\n%d registry entr(ies) whose number is not on the page:" % len(missing))
        for page, label, stated in missing:
            print("  %-44s %s (%s)" % (page, label, stated))
        print("\nEither the page was reworded or the entry is stale. Fix the registry.")

    if wrong or missing:
        return 1

    print("checked %d measured number(s) against the source" % len(REGISTRY))
    print("every published figure re-derives")
    return 0


if __name__ == "__main__":
    sys.exit(main())
