#!/usr/bin/env python3
"""Validate, render, loudness-master, and frame-lint a Nick-style reel."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
DEFAULT_ENGINE = Path(__file__).resolve().parent.parent  # repo root


def run(command: list[str], cwd: Path, dry_run: bool) -> None:
    print("+", " ".join(shlex.quote(part) for part in command))
    if not dry_run:
        subprocess.run(command, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument(
        "--engine",
        type=Path,
        default=Path(os.environ.get("REEL_ENGINE", DEFAULT_ENGINE)),
    )
    args = parser.parse_args()
    engine = args.engine.expanduser().resolve()
    raw = engine / f"out/{args.slug}-raw.mp4"
    final = engine / f"out/{args.slug}-final.mp4"

    run(
        [
            sys.executable,
            str(SKILL / "scripts/register_beats.py"),
            "--engine",
            str(engine),
        ],
        engine,
        args.dry_run,
    )
    run(
        [
            sys.executable,
            str(SKILL / "scripts/validate_job.py"),
            args.slug,
            "--engine",
            str(engine),
        ],
        engine,
        args.dry_run,
    )
    run(["npx", "tsc", "--noEmit", "-p", "."], engine, args.dry_run)
    if not args.skip_render:
        raw.parent.mkdir(parents=True, exist_ok=True)
        run(
            [
                "npx",
                "remotion",
                "render",
                "src/index.ts",
                args.slug,
                str(raw),
                "--concurrency=2",
                "--timeout=120000",
            ],
            engine,
            args.dry_run,
        )
    elif not raw.exists() and not args.dry_run:
        raise SystemExit(f"--skip-render requested but raw render is missing: {raw}")

    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(raw),
            "-c:v",
            "copy",
            "-af",
            "loudnorm=I=-14:TP=-1.2:LRA=7",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(final),
        ],
        engine,
        args.dry_run,
    )
    run(
        [
            sys.executable,
            "tools/lint_frames.py",
            args.slug,
            "--video",
            str(final),
        ],
        engine,
        args.dry_run,
    )
    run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_name,width,height,avg_frame_rate",
            "-of",
            "default=noprint_wrappers=1",
            str(final),
        ],
        engine,
        args.dry_run,
    )
    print(f"final: {final}")


if __name__ == "__main__":
    main()
