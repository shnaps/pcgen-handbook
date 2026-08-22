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


def known_tags():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    tags = set()
    for t in d["tokens"]:
        tags.add(t["full_tag"].upper())
        tags.add(t["tag"].upper())
        if t["parent"]:
            tags.add(t["parent"].upper())
    return tags, d["pcgen_version"], d["pinned_sha"]


def main():
    if not DATA.exists():
        sys.exit("tags.json missing - run tools/scan_tokens.py first")
    tags, ver, sha = known_tags()

    problems = []
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

    print("checked %d tag uses against PCGen %s (%s)" % (checked, ver, sha[:12]))
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
