#!/usr/bin/env python3
"""Frame-lint: automated pre-delivery QC pass over a rendered reel.

Usage:
    python3 tools/lint_frames.py <slug> [--video out/<slug>.mp4]

Reads src/beats/<slug>.json + the rendered mp4, then:
  1. Extracts a labeled still at each scene's start (+0.35s) and midpoint into
     out/<slug>-lint/ (NN-<type>-start.png / -mid.png).
  2. Builds a contact sheet (lint-sheet-*.jpg) for the vision CRITIC pass.
  3. Runs programmatic checks per still and prints a report:
       - DEAD SPACE: fraction of near-uniform dark or bright area > 30%
       - DUPLICATE: consecutive scenes whose mid-frames are near-identical
         (repetition — same treatment/clip reused back-to-back)
       - EDGE TEXT: high-contrast content hugging the left/right frame edge
         (likely cropped mid-word screenshot)
  4. Prints the manual CRITIC checklist (from SKILL.md STEP 6) with the beats
     metadata each item needs (kinetic/headline/caption overlap windows).

Programmatic flags are HINTS for the critic, not verdicts — always eyeball the
sheet. Exit code is 0 unless the video/beats are missing.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def extract(video, t, out, label):
    # NB: this ffmpeg build has no drawtext filter — label via PIL below.
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(video),
        "-frames:v", "1", "-vf", "scale=540:-1", str(out),
    ])
    if HAVE_PIL:
        from PIL import ImageDraw, ImageFont
        img = Image.open(out).convert("RGB")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except OSError:
            font = ImageFont.load_default()
        x0, y0, x1, y1 = draw.textbbox((12, 10), label, font=font)
        draw.rectangle((x0 - 8, y0 - 6, x1 + 8, y1 + 6), fill=(0, 0, 0))
        draw.text((12, 10), label, fill=(255, 255, 255), font=font)
        img.save(out)


def grid_stats(img, cells=12):
    """Per-cell (mean, stddev) on grayscale for dead-space detection."""
    g = img.convert("L")
    w, h = g.size
    cw, ch = w // cells, h // cells
    out = []
    for r in range(cells):
        for c in range(cells):
            cell = g.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
            hist = cell.histogram()
            n = sum(hist)
            mean = sum(i * v for i, v in enumerate(hist)) / n
            var = sum(v * (i - mean) ** 2 for i, v in enumerate(hist)) / n
            out.append((mean, var ** 0.5))
    return out


def dead_space_frac(img):
    cells = grid_stats(img)
    flat_dark = sum(1 for m, s in cells if s < 6 and m < 38)
    flat_bright = sum(1 for m, s in cells if s < 6 and m > 218)
    return max(flat_dark, flat_bright) / len(cells)


def ahash(img, size=16):
    g = img.convert("L").resize((size, size))
    px = list(g.getdata())
    avg = sum(px) / len(px)
    return [p > avg for p in px]


def hash_dist(a, b):
    return sum(1 for x, y in zip(a, b) if x != y) / len(a)


def edge_text_score(img):
    """Detect high-frequency content hugging L/R edges (cropped text)."""
    g = img.convert("L")
    w, h = g.size
    band = 8
    score = 0.0
    for x0 in (0, w - band):
        strip = g.crop((x0, int(h * 0.2), x0 + band, int(h * 0.8)))
        px = list(strip.getdata())
        mean = sum(px) / len(px)
        var = sum((p - mean) ** 2 for p in px) / len(px)
        score = max(score, var ** 0.5)
    return score


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    video = ROOT / (
        sys.argv[sys.argv.index("--video") + 1]
        if "--video" in sys.argv
        else f"out/{slug}.mp4"
    )
    beats_path = ROOT / f"src/beats/{slug}.json"
    if not video.exists():
        sys.exit(f"missing video: {video}")
    if not beats_path.exists():
        sys.exit(f"missing beats: {beats_path}")

    beats = json.loads(beats_path.read_text())
    scenes = beats["scenes"]
    lint_dir = ROOT / f"out/{slug}-lint"
    lint_dir.mkdir(parents=True, exist_ok=True)
    for old in lint_dir.glob("*.png"):
        old.unlink()

    # -- 1. extract labeled stills ------------------------------------------
    stills = []  # (idx, type, phase, path, t)
    cursor = 0.0
    for i, s in enumerate(scenes):
        dur = s["durationSec"]
        marks = [("start", cursor + min(0.35, dur * 0.3)),
                 ("mid", cursor + dur / 2)]
        for phase, t in marks:
            label = f"{i:02d} {s['type']} {phase} @{t:.1f}s"
            p = lint_dir / f"{i:02d}-{s['type']}-{phase}.png"
            extract(video, t, p, label)
            stills.append((i, s["type"], phase, p, t))
        cursor += dur

    # contact sheets (mids only, 4 per row)
    mids = [p for (_, _, ph, p, _) in stills if ph == "mid"]
    for si in range(0, len(mids), 12):
        chunk = mids[si:si + 12]
        sheet = lint_dir / f"lint-sheet-{si // 12}.jpg"
        inputs = []
        for p in chunk:
            inputs += ["-i", str(p)]
        n = len(chunk)
        cols = min(4, n)
        rows = -(-n // cols)
        run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
             f"concat=n={n}:v=1:a=0,tile={cols}x{rows}", "-frames:v", "1",
             str(sheet)])

    # -- 2. programmatic checks ---------------------------------------------
    flags = []
    if HAVE_PIL:
        imgs = {}
        for (i, typ, phase, p, t) in stills:
            if phase != "mid":
                continue
            img = Image.open(p)
            imgs[i] = img
            frac = dead_space_frac(img)
            if frac > 0.30:
                flags.append(
                    f"[DEAD SPACE] scene {i:02d} ({typ}): "
                    f"{frac:.0%} of frame is flat/empty")
            if typ in ("receipt", "floatcard") and edge_text_score(img) > 34:
                flags.append(
                    f"[EDGE TEXT] scene {i:02d} ({typ}): busy pixels at frame "
                    "edge — screenshot likely cropped mid-word")
        hashes = {i: ahash(img) for i, img in imgs.items()}
        for i in sorted(hashes)[1:]:
            if i - 1 in hashes and hash_dist(hashes[i - 1], hashes[i]) < 0.08:
                a, b = scenes[i - 1]["type"], scenes[i]["type"]
                flags.append(
                    f"[DUPLICATE] scenes {i-1:02d}({a}) → {i:02d}({b}) look "
                    "near-identical — repeated treatment/clip back-to-back")
    else:
        flags.append("[SKIP] PIL not installed — auto checks skipped")

    # PACING (universal rule 2026-07-31): no held layout > ~2s.
    FOOTAGE_TYPES = {"footage", "split"}  # real motion may run longer
    VIDEO_EXT = (".mp4", ".webm", ".mov")
    def is_motion(sc):
        if sc["type"] in FOOTAGE_TYPES:
            return True
        src = str(sc.get("src") or sc.get("mediaSrc") or "")
        return sc["type"] in ("floatcard", "deviceframe") and src.endswith(VIDEO_EXT)
    for i, sc in enumerate(scenes):
        d = sc["durationSec"]
        if i == 0 and d > 2.2:
            flags.append(
                f"[PACING] scene 00 ({sc['type']}): hook layout held {d:.1f}s"
                " — HARD LIMIT 2s (user rule, blocking)")
        elif not is_motion(sc) and d > 2.6:
            flags.append(
                f"[PACING] scene {i:02d} ({sc['type']}): held layout {d:.1f}s"
                " — split across visuals or cut to footage")

    # CLIP REUSE (universal rule 2026-08-01): no source clip may carry more
    # than one footage beat — reusing the same shot reads as "limited footage".
    from collections import Counter
    used = Counter()
    for sc in scenes:
        src = str(sc.get("src") or "")
        if sc.get("type") == "footage" and src and "avatar-master" not in src:
            used[src] += 1
    for src, n in used.items():
        if n > 1:
            flags.append(
                f"[CLIP REUSE] {src.split('/')[-1]} used in {n} beats — every "
                "footage beat needs its OWN shot (blocking)")

    # caption-overlap advisory: display-type scenes that force chips ON
    for i, s in enumerate(scenes):
        display = s["type"] in ("typecard", "wordcascade") or "kinetic" in s
        if display and s.get("hideCaptions") is False:
            flags.append(
                f"[DOUBLE TEXT?] scene {i:02d} ({s['type']}) has display type "
                "but hideCaptions:false — verify chips don't duplicate it")

    # -- 3. report -----------------------------------------------------------
    print(f"\n=== frame-lint: {slug} — {len(scenes)} scenes ===")
    print(f"stills + sheets: {lint_dir}/")
    if flags:
        print("\nAUTO FLAGS (hints, verify by eye):")
        for f in flags:
            print("  " + f)
    else:
        print("\nno auto flags.")
    print("""
CRITIC CHECKLIST (review the lint sheets against the beat map):
  1. script-visual match: does each frame show what the VO claims?
  2. ONE TEXT SYSTEM: no karaoke chip while display type speaks the words
  3. no text collisions (headline vs card vs chip), captions off the face
  4. receipts: highlight framed big, box AROUND the data (never covering it)
  5. no content cropped mid-word at frame edges; screenshots card-framed
  6. every number carries units/labels; credits present; no app chrome
  7. display type legible on its actual backdrop (frame AT landing moment)
  8. dead space <30% of frame; no flat-black surrounds around small assets
  9. hook frame passes the sound-off test (names the subject visually)""")


if __name__ == "__main__":
    main()
