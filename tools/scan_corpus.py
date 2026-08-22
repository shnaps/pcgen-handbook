"""Record which tag-argument forms PCGen's shipped data actually uses.

check_examples.py validates tag NAMES against tags.json. It cannot catch a wrong
ARGUMENT - BONUS:COMBAT|BAB has a valid tag name and a removed argument. Every
error found in this handbook so far has been of that kind.

This builds a corpus of the argument forms real data uses, so check_examples.py can
flag a form that appears nowhere upstream.

Output: corpus-forms.json (committed - CI has no data checkout)
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "work" / "pcgen-src" / "data"
OUT = ROOT / "corpus-forms.json"

# A field is TAG:value. Capture the tag and up to two pipe-separated segments.
FIELD = re.compile(r"^([A-Z][A-Z0-9_]*(?::[A-Z][A-Z0-9_]*)?):(.*)$", re.S)
# Structural arguments are uppercase keywords. Content names (skills, spells,
# monsters) are not, and including them made the file 1.4 MB of no validation value.
KEYWORD = re.compile(r"^[A-Z][A-Z0-9_.]*$")

MIN_COUNT = 2  # a form seen once may be a typo in the data itself

# Tags whose arguments are structural rather than content names. These are the ones
# where a wrong argument is a real error rather than an unknown proper noun.
STRUCTURAL = {
    "BONUS", "CHOOSE", "ADD", "AUTO", "ABILITY", "REMOVE", "TEMPBONUS", "QUALIFY",
    "MODIFY", "MODIFYOTHER", "DEFINE", "SPELLKNOWN", "SPELLLEVEL", "VISIBLE",
    "ACHECK", "MOVE", "SIZE", "TYPE", "CAST", "KNOWN", "FACT", "FACTSET",
    "SPELLCASTER", "KIT", "CSKILL", "CCSKILL", "MEMORIZE", "MODTOSKILLS",
}


def main():
    if not DATA.exists():
        raise SystemExit("no data checkout at %s - widen the sparse checkout first" % DATA)

    forms = Counter()
    files = 0
    for p in DATA.rglob("*.lst"):
        files += 1
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            for field in line.split("\t"):
                field = field.strip()
                if not field:
                    continue
                m = FIELD.match(field)
                if not m:
                    continue
                tag, value = m.group(1), m.group(2)
                head = tag.split(":")[0]
                if head not in STRUCTURAL and not head.startswith("PRE"):
                    continue
                segs = value.split("|")
                # level 1: TAG:firstsegment
                if segs and KEYWORD.match(segs[0]):
                    forms[tag + ":" + segs[0]] += 1
                    # level 2: TAG:first|second
                    if len(segs) > 1 and KEYWORD.match(segs[1]):
                        forms[tag + ":" + segs[0] + "|" + segs[1]] += 1

    kept = {k: v for k, v in forms.items() if v >= MIN_COUNT}
    sha = (ROOT / "PCGEN-SHA").read_text(encoding="utf-8").strip()
    OUT.write_text(
        json.dumps({"pinned_sha": sha, "lst_files": files,
                    "form_count": len(kept), "forms": dict(sorted(kept.items()))},
                   indent=0),
        encoding="utf-8")

    print("scanned %d .lst files" % files)
    print("kept %d forms seen >= %d times (from %d distinct)" % (len(kept), MIN_COUNT, len(forms)))
    print("-> %s  (%.1f KB)" % (OUT, OUT.stat().st_size / 1024))
    for probe in ["BONUS:COMBAT|BASEAB", "BONUS:COMBAT|BAB", "CHOOSE:SKILL|ALL",
                  "ABILITY:FEAT|AUTOMATIC", "BONUS:HP|CURRENTMAX"]:
        print("   %-26s %s" % (probe, kept.get(probe, "ABSENT")))


if __name__ == "__main__":
    main()
