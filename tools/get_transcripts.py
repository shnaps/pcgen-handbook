"""Fetch YouTube auto-captions for the PCGen homebrew playlist and clean them to text.

Output goes to work/transcripts/NN-slug.md  (gitignored research notes, not wiki content).
Captions are ASR: prose is usable, tag syntax is NOT. Never trust a tag spelling from here.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "work" / "raw"
OUT = ROOT / "work" / "transcripts"
PLAYLIST = "https://www.youtube.com/playlist?list=PLLa5A1qjBOPekqEC_R9BAZW-8q5IT-klM"


def slug(s):
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s_-]+", "-", s).strip("-")[:60]


def playlist():
    r = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "%(playlist_index)s\t%(id)s\t%(duration)s\t%(title)s", PLAYLIST],
        capture_output=True, text=True, check=True)
    out = []
    for line in r.stdout.strip().splitlines():
        idx, vid, dur, title = line.split("\t", 3)
        out.append({"index": int(idx), "id": vid, "duration": int(float(dur)), "title": title})
    return out


def fetch(vid):
    dest = RAW / f"{vid}.en-orig.vtt"
    if dest.exists():
        return dest
    subprocess.run(["yt-dlp", "--write-auto-subs", "--sub-langs", "en-orig", "--sub-format", "vtt",
                    "--skip-download", "-o", str(RAW / "%(id)s.%(ext)s"),
                    f"https://www.youtube.com/watch?v={vid}"],
                   capture_output=True, text=True, check=True)
    return dest if dest.exists() else None


def vtt_to_blocks(path, bucket=60):
    """Collapse VTT rolling captions into plain text, bucketed into ~1 minute chunks."""
    txt = re.sub(r"<[^>]+>", "", path.read_text(encoding="utf-8", errors="replace"))
    blocks, cur_t, seen = {}, 0, None
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        m = re.match(r"(\d\d):(\d\d):(\d\d)\.\d+\s+-->", line)
        if m:
            h, mi, s = map(int, m.groups())
            cur_t = h * 3600 + mi * 60 + s
            continue
        if "-->" in line or line == seen:
            continue
        seen = line
        blocks.setdefault((cur_t // bucket) * bucket, []).append(line)
    return blocks


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    vids = playlist()
    (ROOT / "work" / "playlist.json").write_text(json.dumps(vids, indent=2), encoding="utf-8")
    manifest = []
    for v in vids:
        name = f"{v['index']:02d}-{slug(v['title'])}"
        try:
            vtt = fetch(v["id"])
        except subprocess.CalledProcessError as e:
            print(f"FAIL {v['index']:02d} {v['id']}: {e.stderr[-200:]}", file=sys.stderr)
            manifest.append({**v, "file": None, "words": 0}); continue
        if not vtt:
            print(f"NOCAP {v['index']:02d} {v['id']}", file=sys.stderr)
            manifest.append({**v, "file": None, "words": 0}); continue
        blocks = vtt_to_blocks(vtt)
        body = [f"# {v['title']}", "",
                f"- video: https://www.youtube.com/watch?v={v['id']}",
                f"- length: {v['duration'] // 60}m{v['duration'] % 60:02d}s",
                "- source: YouTube auto-captions (ASR). Prose is usable; tag spellings are NOT.",
                ""]
        words = 0
        for t in sorted(blocks):
            text = " ".join(blocks[t])
            words += len(text.split())
            body.append(f"**[{t // 60:02d}:{t % 60:02d}]** {text}\n")
        (OUT / f"{name}.md").write_text("\n".join(body), encoding="utf-8")
        manifest.append({**v, "file": f"{name}.md", "words": words})
        print(f"OK   {v['index']:02d} {words:5d}w  {name}")
    (ROOT / "work" / "transcripts.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    tot = sum(m["words"] for m in manifest)
    print(f"\n{sum(1 for m in manifest if m['file'])}/{len(manifest)} videos, {tot:,} words total")


if __name__ == "__main__":
    main()
