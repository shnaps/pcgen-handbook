"""Scan PCGen's Java source and emit the authoritative output token index.

Output tokens are a different system from LST tags. An LST tag is read from a data
file into a game object at load time. An output token is read from a character sheet
template and writes a value out of a finished character.

They are scannable the same way, and for the same reason: each class declares its own
name. Measured at the pinned commit, every getTokenName() is either a string literal
or a constant declared in the same file. None are computed.

What this cannot produce is argument syntax. Output tokens have no sub-token registry
- each class parses the rest of the marker itself with a StringTokenizer - so
`STAT.0.MOD` is one name and two arguments that exist only inside an if/else chain.
That part stays hand-written.

Also collects the FreeMarker model keys, which are registered with literal names
through OutputDB and are therefore scannable too.

Output: work/output-tokens.json, plus a committed copy at output-tokens.json
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "work" / "pcgen-src"
JAVA = SRC / "code/src/java"
OUT = ROOT / "work" / "output-tokens.json"

# The two packages that hold them. Core tokens are registered directly by
# ExportHandler; the rest arrive through the plugin jars.
DIRS = [
    ("core", JAVA / "pcgen/io/exporttoken"),
    ("plugin", JAVA / "plugin/exporttokens"),
]

RE_PKG = re.compile(r"^\s*package\s+([\w.]+)\s*;", re.M)
RE_CLASS = re.compile(r"(?:public\s+|final\s+|abstract\s+)*class\s+(\w+)\b")
RE_COMMENT = re.compile(r"/\*.*?\*/|//[^\n]*", re.S)
RE_ABSTRACT = re.compile(r"\babstract\s+class\b")

# getTokenName() { return "STAT"; }
RE_NAME_LITERAL = re.compile(r"getTokenName\s*\(\s*\)\s*\{\s*return\s+\"([^\"]*)\"")
# getTokenName() { return TOKENNAME; }
RE_NAME_CONST = re.compile(r"getTokenName\s*\(\s*\)\s*\{\s*return\s+(\w+)\s*;")
RE_CONST_DECL = r'static\s+final\s+String\s+%s\s*=\s*"([^"]+)"'

# OutputDB.register("stats", ...) and friends. All observed names are literals.
RE_MODEL = re.compile(
    r"OutputDB\.(?:register|addGlobalModel|registerBooleanPreference)"
    r"\s*\(\s*\"([^\"]+)\""
)


def scan_class(path, origin):
    raw = path.read_text(encoding="utf-8", errors="replace")
    body = RE_COMMENT.sub(" ", raw)

    m = RE_CLASS.search(body)
    if not m:
        return None
    cls = m.group(1)

    pkg_m = RE_PKG.search(body)
    pkg = pkg_m.group(1) if pkg_m else ""

    name = None
    resolved = None
    lit = RE_NAME_LITERAL.search(body)
    if lit:
        name, resolved = lit.group(1), "literal"
    else:
        const = RE_NAME_CONST.search(body)
        if const:
            decl = re.search(RE_CONST_DECL % re.escape(const.group(1)), body)
            if decl:
                name, resolved = decl.group(1), "constant"
            else:
                # A constant we cannot see. Report it rather than dropping it.
                return {"class": cls, "unresolved": const.group(1),
                        "path": str(path.relative_to(SRC)).replace("\\", "/")}

    if name is None:
        # Abstract bases and helpers declare no name. Not an error.
        return None

    return {
        "token": name,
        "class": cls,
        "package": pkg,
        "origin": origin,
        "deprecated": ".deprecated" in pkg,
        "resolved": resolved,
        "path": str(path.relative_to(SRC)).replace("\\", "/"),
    }


def scan_models():
    """FreeMarker model keys, registered from all over the tree."""
    keys = {}
    for f in JAVA.rglob("*.java"):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "OutputDB." not in text:
            continue
        for key in RE_MODEL.findall(RE_COMMENT.sub(" ", text)):
            keys.setdefault(key, str(f.relative_to(SRC)).replace("\\", "/"))
    return [{"key": k, "registered_in": v} for k, v in sorted(keys.items())]


def main():
    if not JAVA.exists():
        sys.exit("no source checkout at %s - clone PCGen into work/pcgen-src first" % SRC)

    tokens, unresolved, skipped = [], [], 0
    for origin, d in DIRS:
        if not d.exists():
            sys.exit("missing %s" % d)
        for f in sorted(d.rglob("*.java")):
            rec = scan_class(f, origin)
            if rec is None:
                skipped += 1
            elif "unresolved" in rec:
                unresolved.append(rec)
            else:
                tokens.append(rec)

    tokens.sort(key=lambda t: (t["token"], t["class"]))

    dupes = [n for n, c in Counter(t["token"] for t in tokens).items() if c > 1]

    sha = (ROOT / "PCGEN-SHA").read_text(encoding="utf-8").strip()
    ver = re.search(
        r"version=(\S+)", (SRC / "gradle.properties").read_text(encoding="utf-8")
    ).group(1)

    payload = {
        "pinned_sha": sha,
        "pcgen_version": ver,
        "token_count": len(tokens),
        "tokens": tokens,
        "freemarker_models": scan_models(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (ROOT / "output-tokens.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("output tokens: %d   deprecated: %d"
          % (len(tokens), sum(1 for t in tokens if t["deprecated"])))
    print("  literal names: %d   from a constant: %d"
          % (sum(1 for t in tokens if t["resolved"] == "literal"),
             sum(1 for t in tokens if t["resolved"] == "constant")))
    print("  classes declaring no name (abstract or helper): %d" % skipped)
    print("freemarker model keys: %d" % len(payload["freemarker_models"]))

    if dupes:
        print("\nDUPLICATE token names (%d):" % len(dupes))
        for n in sorted(dupes):
            print("  %s" % n)
    if unresolved:
        print("\nUNRESOLVED constants (%d):" % len(unresolved))
        for u in unresolved:
            print("  %s: %s" % (u["class"], u["unresolved"]))

    print("\n-> %s" % OUT)
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
