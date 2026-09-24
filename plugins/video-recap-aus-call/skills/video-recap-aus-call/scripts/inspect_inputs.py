#!/usr/bin/env python3
"""Inventarisiert lokale Meeting-Medien mit ffprobe, ohne Inhalte hochzuladen."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

MEDIA_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4a", ".wav", ".mp3", ".aac"}
TEXT_EXTS = {".vtt", ".srt", ".txt"}


def classify(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if suffix in {".vtt", ".srt"}:
        return "transcript"
    if suffix == ".txt" and "chat" in name:
        return "chat"
    if suffix in {".mp3", ".wav", ".m4a", ".aac"}:
        return "audio"
    if "_avo_" in name or "active" in name or "speaker" in name:
        return "active_speaker"
    if "_gvo_" in name or "gallery" in name or "galerie" in name:
        return "gallery"
    if "_as_" in name or "screen" in name or "share" in name or "folie" in name:
        return "screen_share"
    if "recording" in name or "aufnahme" in name:
        return "combined_main"
    return "other_media" if suffix in MEDIA_EXTS else "text"


def ffprobe(path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size:stream=index,codec_type,codec_name,width,height,avg_frame_rate,sample_rate,channels",
        "-of", "json", str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        return {"error": (result.stderr or "ffprobe failed").strip()}
    return json.loads(result.stdout)


def discover(inputs: list[Path]) -> list[Path]:
    found: set[Path] = set()
    for item in inputs:
        if item.is_dir():
            for path in item.rglob("*"):
                if path.is_file() and path.suffix.lower() in MEDIA_EXTS | TEXT_EXTS:
                    found.add(path.resolve())
        elif item.is_file() and item.suffix.lower() in MEDIA_EXTS | TEXT_EXTS:
            found.add(item.resolve())
    return sorted(found, key=lambda p: str(p).lower())


def main() -> int:
    parser = argparse.ArgumentParser(description="Lokales Medieninventar fuer Call- und Meeting-Aufnahmen")
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    if shutil.which("ffprobe") is None:
        print("ERROR: ffprobe ist nicht installiert oder nicht im PATH", file=sys.stderr)
        return 2

    files = discover(args.inputs)
    payload = {"inputs": [str(p.resolve()) for p in args.inputs], "files": []}
    for path in files:
        item = {"path": str(path), "name": path.name, "kind": classify(path)}
        if path.suffix.lower() in MEDIA_EXTS:
            item["probe"] = ffprobe(path)
        else:
            item["size"] = path.stat().st_size
        payload["files"].append(item)

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if files else 1


if __name__ == "__main__":
    raise SystemExit(main())
