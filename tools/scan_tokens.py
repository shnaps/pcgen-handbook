"""Scan PCGen's Java source and emit the authoritative LST tag index.

The token classes ARE the specification. getTokenName() gives the literal tag
string; getTokenClass() gives the object type that accepts it. Everything else in
the handbook defers to what this produces.

Output: work/tokens.json
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "work" / "pcgen-src"
JAVA = SRC / "code/src/java"
OUT = ROOT / "work" / "tokens.json"

RE_PKG = re.compile(r"^\s*package\s+([\w.]+)\s*;", re.M)
RE_CLASS = re.compile(
    r"(?:public\s+|final\s+|abstract\s+)*class\s+(\w+)\s*(?:<[^{]*?>)?\s*"
    r"(?:extends\s+([\w.]+)\s*(?:<[^{]*?>)?\s*)?"
    r"(?:implements\s+([^{]+?))?\s*\{",
    re.S,
)
RE_COMMENT = re.compile(r"/\*.*?\*/|//[^\n]*", re.S)


def m_literal(body, name):
    """A method returning a plain string literal."""
    m = re.search(name + r"\s*\(\s*\)\s*\{\s*return\s+\"([^\"]*)\"", body)
    return m.group(1) if m else None


def m_const(body, name):
    """A method returning a constant, e.g. CControl.FACE or CControl.FACE.getName()."""
    m = re.search(name + r"\s*\(\s*\)\s*\{\s*return\s+([\w.]+?)(?:\.getName\(\))?\s*;", body)
    return m.group(1) if m else None


def m_class(body, name="getTokenClass"):
    m = re.search(name + r"\s*\(\s*\)\s*\{\s*return\s+([\w.]+)\.class", body)
    return m.group(1).split(".")[-1] if m else None


def m_strarray(body, name):
    """kindsHandled() -> new String[]{"RACE", ...}"""
    m = re.search(name + r"\s*\(\s*\)\s*\{\s*return\s+new\s+String\[\]\s*\{(.*?)\}", body, re.S)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []


def build_ccontrol():
    """CControl.java holds the constant tag names used by gamemode/codecontrol."""
    f = JAVA / "pcgen/cdom/util/CControl.java"
    if not f.exists():
        return {}
    t = f.read_text(encoding="utf-8", errors="replace")
    out = {}
    for name, val in re.findall(r'static\s+final\s+String\s+(\w+)\s*=\s*"([^"]+)"', t):
        out["CControl." + name] = val
    for name, val in re.findall(
        r'static\s+final\s+CControl\s+(\w+)\s*=[^;]*?"([A-Z][A-Z0-9_]*)"', t, re.S
    ):
        out.setdefault("CControl." + name, val)
    return out


def parse_file(path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    body = RE_COMMENT.sub("", raw)
    pm = RE_PKG.search(body)
    cm = RE_CLASS.search(body)
    if not cm:
        return None
    impls = (cm.group(3) or "").replace("\n", " ")
    return {
        "file": str(path.relative_to(SRC)).replace("\\", "/"),
        "package": pm.group(1) if pm else "",
        "class": cm.group(1),
        "extends": (cm.group(2) or "").split(".")[-1] or None,
        "implements": [
            i.strip().split("<")[0].split(".")[-1] for i in impls.split(",") if i.strip()
        ],
        "body": body,
    }


def main():
    if not JAVA.exists():
        sys.exit("missing source clone at " + str(JAVA))

    ccontrol = build_ccontrol()
    print("CControl constants: %d" % len(ccontrol))

    # Keyed by PATH, not class name: the same class name appears in many packages
    # (race/TypeToken, skill/TypeToken, ...) and name-keying silently drops them.
    all_infos = []
    files = {}  # class name -> info, for superclass resolution only
    for sub in [
        "plugin/lsttokens",
        "plugin/pretokens",
        "plugin/bonustokens",
        "plugin/qualifier",
        "plugin/primitive",
        "plugin/modifier",
        "pcgen/rules/persistence/token",
    ]:
        d = JAVA / sub
        if not d.exists():
            continue
        for p in d.rglob("*.java"):
            info = parse_file(p)
            if info:
                all_infos.append(info)
                # Prefer abstract bases as the inheritance target for a given name.
                prev = files.get(info["class"])
                if prev is None or "abstract" in info["body"][:400]:
                    files[info["class"]] = info

    print("parsed files: %d   distinct class names: %d" % (len(all_infos), len(files)))

    def inherited(info, getter, depth=0):
        """Walk the superclass chain for a value the class does not declare itself."""
        if info is None or depth > 6:
            return None
        v = getter(info["body"])
        if v:
            return v
        return inherited(files.get(info["extends"] or ""), getter, depth + 1)

    tokens = []
    unresolved = []

    for info in all_infos:
        pkg = info["package"]
        body = info["body"]
        impls = info["implements"]
        if not pkg.startswith("plugin."):
            continue

        # PRExxx: one parser class can declare several kinds.
        # kindsHandled() casing is inconsistent in the source ("ability", "RACE"), but
        # PreParserFactory lowercases for lookup, so matching is case-insensitive.
        # Data and convention are uppercase, so normalise to that.
        if pkg.startswith("plugin.pretokens.parser"):
            for k in m_strarray(body, "kindsHandled"):
                tokens.append(
                    {
                        "tag": "PRE" + k.upper(),
                        "family": "pre",
                        "parent": None,
                        "applies_to": "any",
                        "class": info["class"],
                        "source": info["file"],
                        "deprecated": False,
                        "deprecated_version": None,
                        "note": None,
                    }
                )
            continue

        family = None
        parent = None
        tag = None
        applies = None

        if pkg.startswith("plugin.bonustokens"):
            tag = m_literal(body, "getBonusHandled")
            if not tag:
                continue
            family, parent, applies = "bonus", "BONUS", "any"

        elif pkg.startswith("plugin.lsttokens"):
            family = "lst"
            tag = m_literal(body, "getTokenName")
            if tag is None:
                c = m_const(body, "getTokenName")
                if c:
                    tag = ccontrol.get(c)
                    if tag is None:
                        # Fall back to a constant declared in this same file.
                        local = re.search(
                            r'static\s+final\s+String\s+' + c.split(".")[-1]
                            + r'\s*=\s*"([^"]+)"', body)
                        tag = local.group(1) if local else None
                    if tag is None:
                        unresolved.append((info["class"], c))
                        continue
            if tag is None:
                tag = inherited(info, lambda b: m_literal(b, "getTokenName"))
            if tag is None:
                continue
            parent = inherited(info, lambda b: m_literal(b, "getParentToken"))
            if "GameModeLstToken" in impls:
                applies = "gamemode-file"
            else:
                applies = inherited(info, m_class) or "any"

        elif pkg.startswith(("plugin.qualifier", "plugin.primitive", "plugin.modifier")):
            tag = m_literal(body, "getTokenName")
            if not tag:
                continue
            family = pkg.split(".")[1]
            applies = inherited(info, m_class) or "any"
        else:
            continue

        # Deprecation: three orthogonal signals in the source.
        dep_ver = None
        lvl = re.search(r"compatibilityLevel\s*\(\s*\)\s*\{\s*return\s+(\d+)", body)
        sub_lvl = re.search(r"compatibilitySubLevel\s*\(\s*\)\s*\{\s*return\s+(\d+)", body)
        if lvl and sub_lvl:
            dep_ver = lvl.group(1) + "." + sub_lvl.group(1)
        note = None
        nm = re.search(r'getMessage\s*\([^)]*\)\s*\{\s*return\s+"([^"]+)"', body)
        if nm:
            note = nm.group(1)
        deprecated = bool(dep_ver) or "DeprecatedToken" in impls \
            or ".deprecated" in pkg or "CDOMCompatibilityToken" in impls

        tokens.append(
            {
                "tag": tag,
                "family": family,
                "parent": parent,
                "applies_to": applies,
                "class": info["class"],
                "source": info["file"],
                "deprecated": deprecated,
                "deprecated_version": dep_ver,
                "note": note,
            }
        )

    for t in tokens:
        t["full_tag"] = (t["parent"] + ":" + t["tag"]) if t["parent"] else t["tag"]
    tokens.sort(key=lambda t: (t["family"], t["full_tag"], t["applies_to"] or ""))

    sha = (ROOT / "PCGEN-SHA").read_text(encoding="utf-8").strip()
    ver = re.search(
        r"version=(\S+)", (SRC / "gradle.properties").read_text(encoding="utf-8")
    ).group(1)

    payload = {
        "pinned_sha": sha,
        "pcgen_version": ver,
        "token_count": len(tokens),
        "tokens": tokens,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # Committed copy. CI needs the tag facts without cloning PCGen, and this is
    # also what ingest.py diffs a fresh scan against to detect drift.
    (ROOT / "tags.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    fam = Counter(t["family"] for t in tokens)
    uniq = len({t["full_tag"] for t in tokens})
    print("\ntokens: %d   unique tags: %d" % (len(tokens), uniq))
    for k in sorted(fam):
        print("  %-10s %5d" % (k, fam[k]))
    print("  %-10s %5d" % ("deprecated", sum(1 for t in tokens if t["deprecated"])))
    if unresolved:
        print("\nUNRESOLVED constants (%d):" % len(unresolved))
        for c, k in unresolved[:15]:
            print("  %s: %s" % (c, k))
    print("\n-> %s" % OUT)


if __name__ == "__main__":
    main()
