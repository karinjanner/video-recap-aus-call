#!/usr/bin/env python3
"""Misst per Kreuzkorrelation, wie weit Tonspuren gegenueber einer Master-Tonspur versetzt sind.

Beispiele:
  # Zoom-Perspektiven vor dem Schnitt pruefen (gleiche Zeitachse erwartet)
  sync_check.py 06-audio-only.m4a 01-speaker.mp4 05-gallery.mp4 --at 600 3600 7000

  # Endfassung pruefen: Masterzeit 1234.5 s liegt im Schnitt bei 42.0 s
  sync_check.py 06-audio-only.m4a fassung-v3.mp4 --pairs 1234.5:42.0 2210:318.4

Positiver Versatz = die gepruefte Datei liegt spaeter als der Master.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

import numpy as np

SR = 8000


def load(path: str, start: float, dur: float) -> np.ndarray:
    start = max(0.0, start)
    out = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", path,
         "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.float32)


def lag_seconds(ref: np.ndarray, probe: np.ndarray, search: float) -> tuple[float, float]:
    """Verschiebung von ref innerhalb von probe (probe beginnt search Sekunden frueher)."""
    if len(ref) < SR or len(probe) < len(ref):
        return float("nan"), 0.0
    ref = (ref - ref.mean()) / (ref.std() + 1e-9)
    probe = (probe - probe.mean()) / (probe.std() + 1e-9)
    n = 1 << int(np.ceil(np.log2(len(probe) + len(ref))))
    corr = np.fft.irfft(np.fft.rfft(probe, n) * np.conj(np.fft.rfft(ref, n)), n)[: len(probe) - len(ref) + 1]
    k = int(np.argmax(corr))
    score = min(1.0, float(corr[k] / len(ref)))
    return k / SR - search, score


def main() -> int:
    ap = argparse.ArgumentParser(description="Tonversatz per Kreuzkorrelation messen")
    ap.add_argument("master")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--at", nargs="*", type=float, default=[], help="Masterzeiten (s), gleiche Zeitachse")
    ap.add_argument("--pairs", nargs="*", default=[], help="MASTERZEIT:DATEIZEIT fuer geschnittene Fassungen")
    ap.add_argument("--window", type=float, default=15.0, help="Laenge des Vergleichsfensters (s)")
    ap.add_argument("--search", type=float, default=2.0, help="Suchbereich +/- (s)")
    ap.add_argument("--fps", type=float, default=25.0)
    args = ap.parse_args()

    pairs = [(t, t) for t in args.at]
    for raw in args.pairs:
        try:
            m, c = raw.split(":")
            pairs.append((float(m), float(c)))
        except ValueError:
            print(f"ERROR: ungueltiges Paar {raw!r}", file=sys.stderr)
            return 2
    if not pairs:
        print("ERROR: --at oder --pairs angeben", file=sys.stderr)
        return 2

    frame = 1.0 / args.fps
    report = []
    for path in args.files:
        for m_t, c_t in pairs:
            ref = load(args.master, m_t, args.window)
            probe = load(path, c_t - args.search, args.window + 2 * args.search)
            lag, score = lag_seconds(ref, probe, args.search if c_t - args.search >= 0 else c_t)
            ok = bool(np.isfinite(lag) and abs(lag) < frame and score > 0.3)
            report.append({"file": path, "master_s": m_t, "file_s": c_t,
                           "offset_ms": None if not np.isfinite(lag) else round(lag * 1000, 1),
                           "correlation": round(score, 3), "within_one_frame": ok})
    print(json.dumps(report, ensure_ascii=False, indent=2))
    bad = [r for r in report if not r["within_one_frame"]]
    if bad:
        print(f"\n{len(bad)} von {len(report)} Messungen ausserhalb eines Bildintervalls "
              f"oder mit schwacher Korrelation – anhoeren und einordnen.", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
