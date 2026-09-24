#!/usr/bin/env python3
"""Technische Basis-QA fuer eine gerenderte Abnahmefassung."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


def parse_rate(raw: str) -> float:
    if not raw or raw == "0/0":
        return 0.0
    if "/" in raw:
        left, right = raw.split("/", 1)
        return float(left) / float(right)
    return float(raw)


def loudness(path: Path) -> dict:
    result = run(["ffmpeg", "-hide_banner", "-i", str(path), "-filter_complex", "ebur128=peak=true", "-f", "null", "-"])
    summaries = re.findall(
        r"Integrated loudness:\s*\n\s*I:\s*([-+\d.]+) LUFS[\s\S]*?True peak:\s*\n\s*Peak:\s*([-+\d.]+) dBFS",
        result.stderr,
    )
    if not summaries:
        return {"error": "Lautheit konnte nicht gelesen werden"}
    integrated, peak = summaries[-1]
    return {"integrated_lufs": float(integrated), "true_peak_dbfs": float(peak)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Technische Basis-QA fuer Solution-Videos")
    parser.add_argument("video", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    if not args.video.is_file():
        print(f"ERROR: Datei fehlt: {args.video}", file=sys.stderr)
        return 2
    for binary in ("ffprobe", "ffmpeg"):
        if shutil.which(binary) is None:
            print(f"ERROR: {binary} ist nicht installiert oder nicht im PATH", file=sys.stderr)
            return 2

    probe = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size:stream=codec_type,codec_name,width,height,pix_fmt,avg_frame_rate,sample_rate,channels,duration",
        "-of", "json", str(args.video),
    ])
    if probe.returncode:
        print(probe.stderr, file=sys.stderr)
        return 2
    data = json.loads(probe.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    duration = float((data.get("format") or {}).get("duration", 0))
    checks = {
        "has_video": bool(video),
        "has_audio": bool(audio),
        "resolution_1920x1080": (video.get("width"), video.get("height")) == (1920, 1080),
        "fps_25": abs(parse_rate(video.get("avg_frame_rate", "0")) - 25.0) < 0.01,
        "pixel_format_yuv420p": video.get("pix_fmt") == "yuv420p",
        "audio_48khz": str(audio.get("sample_rate", "")) == "48000",
        "audio_stereo": int(audio.get("channels", 0) or 0) == 2,
    }
    vdur = float(video.get("duration", duration) or duration)
    adur = float(audio.get("duration", duration) or duration)
    checks["av_duration_aligned"] = abs(vdur - adur) <= 0.15

    report = {
        "file": str(args.video.resolve()),
        "duration_seconds": duration,
        "format_size": int((data.get("format") or {}).get("size", 0)),
        "video": video,
        "audio": audio,
        "loudness": loudness(args.video),
        "checks": checks,
        "technical_ok": all(checks.values()),
        "note": "Technische QA ersetzt nicht die vollstaendige redaktionelle Sichtung.",
    }
    if args.plan:
        report["plan"] = str(args.plan.resolve())

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if report["technical_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
