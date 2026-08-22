"""Verify every tag used in the handbook actually exists in PCGen.

Extracts TAG:value from fenced code blocks in docs/ and checks each against
tags.json. Catches tags invented from a misheard transcript, tags removed from
upstream, and typos.

Exit 1 on any unknown tag.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = ROOT / "tags.json"

# Fenced blocks we treat as PCGen data. Untagged fences count too, since most
# examples in this handbook are LST lines.
FENCE = re.compile(r"^```(\w*)\n(.*?)^```", re.M | re.S)

# A tag at the start of a field: line start, tab, or after a pipe in a PCC path.
TAG = re.compile(r"(?:^|\t)([A-Z][A-Z0-9_]*(?::[A-Z][A-Z0-9_]*)?)\s*:")

SKIP_LANGS = {"java", "mermaid", "python", "sh", "bash", "ini", "yaml", "yml", "json", "text"}

# Written as illustrations of things that do NOT exist, or non-tag uppercase words.
ALLOW = {
    "ACVALUE", "BABABBREV", "DISPLAYVARIABLE", "ACABBREV",  # removed upstream, cited as such
    "NAME", "TAG", "PRE", "PREXXX", "NOTE", "WARNING", "INFO", "TIP", "DANGER",
}


CORPUS = ROOT / "corpus-forms.json"

# Argument forms this handbook uses that shipped data does not. Each has been checked
# against the implementing class by hand. Anything not listed here is a finding.
ALLOW_FORMS = {
    # Valid SkillArmorCheck member. Real data omits the tag instead of writing NONE.
    "ACHECK:NONE",
}


def known_tags():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    tags = set()
    for t in d["tokens"]:
        tags.add(t["full_tag"].upper())
        tags.add(t["tag"].upper())
        if t["parent"]:
            tags.add(t["parent"].upper())
    return tags, d["pcgen_version"], d["pinned_sha"]


def corpus_forms():
    if not CORPUS.exists():
        return None
    return json.loads(CORPUS.read_text(encoding="utf-8"))["forms"]


KEYWORD = re.compile(r"^[A-Z][A-Z0-9_.]*$")
STRUCTURAL = {
    "BONUS", "CHOOSE", "ADD", "AUTO", "ABILITY", "REMOVE", "TEMPBONUS", "QUALIFY",
    "MODIFY", "MODIFYOTHER", "DEFINE", "SPELLKNOWN", "SPELLLEVEL", "VISIBLE",
    "ACHECK", "MOVE", "SIZE", "TYPE", "CAST", "KNOWN", "FACT", "FACTSET",
    "SPELLCASTER", "KIT", "CSKILL", "CCSKILL", "MEMORIZE", "MODTOSKILLS",
}


def check_form(field, forms):
    """Return a form string that upstream data never uses, or None."""
    if forms is None:
        return None
    m = re.match(r"^([A-Z][A-Z0-9_]*(?::[A-Z][A-Z0-9_]*)?):(.*)$", field, re.S)
    if not m:
        return None
    tag, value = m.group(1), m.group(2)
    head = tag.split(":")[0]
    if head not in STRUCTURAL and not head.startswith("PRE"):
        return None
    segs = value.split("|")
    if not segs or not KEYWORD.match(segs[0]):
        return None
    one = tag + ":" + segs[0]
    if one not in forms and one not in ALLOW_FORMS:
        return one
    if len(segs) > 1 and KEYWORD.match(segs[1]):
        two = one + "|" + segs[1]
        if two not in forms and two not in ALLOW_FORMS:
            return two
    return None


def main():
    if not DATA.exists():
        sys.exit("tags.json missing - run tools/scan_tokens.py first")
    tags, ver, sha = known_tags()

    forms = corpus_forms()
    problems = []
    unseen = []
    checked = 0
    for md in sorted(DOCS.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for lang, block in FENCE.findall(text):
            if lang.lower() in SKIP_LANGS:
                continue
            for line in block.splitlines():
                line = line.strip("\r")
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                # Argument forms: a valid tag name can still carry a removed
                # argument, which is how every error here has actually happened.
                for field in line.split("\t"):
                    bad = check_form(field.strip(), forms)
                    if bad:
                        unseen.append((md.relative_to(ROOT), bad, line.strip()[:56]))
                for m in TAG.finditer(line):
                    tag = m.group(1).upper()
                    checked += 1
                    if tag in ALLOW or tag in tags:
                        continue
                    # BONUS:X and ADD:X style - check the parent alone
                    head = tag.split(":")[0]
                    if head in tags:
                        continue
                    problems.append((md.relative_to(ROOT), line.strip()[:70], tag))

    n_forms = len(forms) if forms else 0
    print("checked %d tag uses against PCGen %s (%s)" % (checked, ver, sha[:12]))
    if forms is None:
        print("NOTE: corpus-forms.json missing - argument forms not checked")
    else:
        print("checked argument forms against %d forms from shipped data" % n_forms)

    if unseen:
        print("\n%d argument form(s) that shipped data never uses:" % len(unseen))
        for path, form, line in unseen:
            print("  %s" % path)
            print("      %s   <- %s" % (form, line))
        print("\n  A form absent from 6,311 shipped files is usually a removed or")
        print("  misremembered argument. Verify it, then add it to ALLOW_FORMS if")
        print("  it is deliberate.")

    if problems:
        print("\n%d unknown tag(s):\n" % len(problems))
        for path, line, tag in problems:
            print("  %s" % path)
            print("      %s   <- %s" % (tag, line))
        return 1
    print("all tags exist upstream")
    return 0


if __name__ == "__main__":
    sys.exit(main())
