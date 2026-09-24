#!/usr/bin/env python3
"""Legt Schnittkanten auf die leiseste Stelle im Originalton und markiert verdaechtige Kanten.

Liest alle Clip-Segmente eines Schnittplans (start/end, optional "parts": [[a, b], ...])
auf der gemeinsamen Originalzeitachse und schlaegt korrigierte Kanten vor:
  - Anfang: spaeteste leise Stelle kurz vor dem ersten Wort,
  - Ende: frueheste leise Stelle kurz nach dem letzten Wort.
Eine Kante mit hohem Pegel deutet auf ein angeschnittenes Wort hin und muss angehoert werden.

  snap_edges.py 00_SOURCE/06-audio-only.m4a --plan 10_WORK/02-cut-plan.json --out 10_WORK/03-kanten.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

SR = 16000
HOP = 0.01
WIN = 0.02


def seconds(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    parts = [float(p) for p in str(value).split(":")]
    total = 0.0
    for p in parts:
        total = total * 60 + p
    return total


def envelope(audio: str, t0: float, t1: float) -> np.ndarray:
    t0 = max(0.0, t0)
    out = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", audio,
         "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(out, dtype=np.float32)
    n, w = int(HOP * SR), int(WIN * SR)
    if len(x) <= w:
        return np.array([-120.0])
    return np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + w] ** 2)) + 1e-9) for i in range(0, len(x) - w, n)])


def snap_start(audio: str, s: float, before: float, after: float) -> tuple[float, float, float]:
    lo = max(0.0, s - before)
    env = envelope(audio, lo, s + after)
    quiet = np.where(env <= env.min() + 6)[0]
    new = lo + max(int(quiet.max()) - 1, 0) * HOP
    edge = env[min(int(round((s - lo) / HOP)), len(env) - 1)]
    return round(new, 3), float(edge), float(env.min())


def snap_end(audio: str, e: float, before: float, after: float) -> tuple[float, float, float]:
    lo = max(0.0, e - before)
    env = envelope(audio, lo, e + after)
    quiet = np.where(env <= env.min() + 6)[0]
    new = lo + int(quiet.min()) * HOP + 0.025
    edge = env[min(int(round((e - lo) / HOP)), len(env) - 1)]
    return round(new, 3), float(edge), float(env.min())


def speech_level(audio: str, a: float, b: float) -> float:
    env = envelope(audio, a, min(b, a + 20))
    return float(np.percentile(env, 80))


def main() -> int:
    ap = argparse.ArgumentParser(description="Schnittkanten auf Pegelminimum legen und pruefen")
    ap.add_argument("audio", help="maßgebliche Tonspur auf der Originalzeitachse")
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--reach", type=float, default=0.45, help="Suchweite ausserhalb des Clips (s)")
    ap.add_argument("--inside", type=float, default=0.10, help="Suchweite in den Clip hinein (s)")
    args = ap.parse_args()

    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: Plan kann nicht gelesen werden: {exc}", file=sys.stderr)
        return 2

    rows = []
    for seg in plan.get("segments", []):
        if not isinstance(seg, dict) or seg.get("type") != "clip":
            continue
        spans = seg.get("parts") or [[seg.get("start"), seg.get("end")]]
        for k, (a_raw, b_raw) in enumerate(spans):
            a, b = seconds(a_raw), seconds(b_raw)
            level = speech_level(args.audio, a, b)
            na, head, qa = snap_start(args.audio, a, args.reach, args.inside)
            nb, tail, qb = snap_end(args.audio, b, args.inside, args.reach)
            flags = []
            if head > qa + 8 and head > level - 12:
                flags.append("ANFANG")
            if tail > qb + 8 and tail > level - 12:
                flags.append("ENDE")
            rows.append({"id": seg.get("id"), "part": k + 1, "start": a, "end": b,
                         "suggested_start": na, "suggested_end": nb,
                         "shift_start_ms": round((na - a) * 1000), "shift_end_ms": round((nb - b) * 1000),
                         "speech_db": round(level, 1), "edge_start_db": round(head, 1),
                         "edge_end_db": round(tail, 1), "flags": flags})

    for r in rows:
        mark = " ".join(r["flags"]) or "-"
        print(f"{str(r['id'])[:28]:28} {r['part']:>2}  {r['start']:9.2f} -> {r['suggested_start']:9.2f}  "
              f"{r['end']:9.2f} -> {r['suggested_end']:9.2f}  {mark}")
    flagged = sum(1 for r in rows if r["flags"])
    print(f"\n{flagged} von {len(rows)} Teilstuecken mit auffaelliger Kante (vor Uebernahme anhoeren).")
    if args.out:
        args.out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
