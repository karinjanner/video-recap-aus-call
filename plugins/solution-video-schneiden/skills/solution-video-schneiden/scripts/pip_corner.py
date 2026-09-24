#!/usr/bin/env python3
"""Waehlt fuer einen Talking Head die freie Ecke einer Folie oder eines Dokumentbilds.

  pip_corner.py slides/hd-05.png slides/hd-06.png --size 400x225 --margin 40

Das Bild wird auf die Zielgroesse skaliert. Je Ecke wird der Anteil "unruhiger" Pixel
(Abweichung vom Median der Flaeche) gemessen. Bevorzugt wird oben rechts; eine Ecke gilt
als frei, wenn der Anteil unter --threshold liegt. Ist keine Ecke frei, lautet das Ergebnis
"none": dort keinen Talking Head zeigen.
"""

from __future__ import annotations

import argparse
import json

import numpy as np
from PIL import Image

ORDER = ["oben_rechts", "unten_rechts", "unten_links", "oben_links"]


def corners(fw: int, fh: int, w: int, h: int, m: int) -> dict[str, tuple[int, int]]:
    return {"oben_rechts": (fw - w - m, m), "unten_rechts": (fw - w - m, fh - h - m),
            "unten_links": (m, fh - h - m), "oben_links": (m, m)}


def busy(arr: np.ndarray, x: int, y: int, w: int, h: int, pad: int = 16) -> float:
    region = arr[max(0, y - pad):y + h + pad, max(0, x - pad):x + w + pad].reshape(-1, 3)
    med = np.median(region, axis=0)
    return float((np.abs(region - med).sum(axis=1) > 40).mean())


def main() -> int:
    ap = argparse.ArgumentParser(description="Freie Ecke fuer Talking Head bestimmen")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--frame", default="1920x1080")
    ap.add_argument("--size", default="400x225")
    ap.add_argument("--margin", type=int, default=40)
    ap.add_argument("--threshold", type=float, default=0.015)
    args = ap.parse_args()

    fw, fh = (int(v) for v in args.frame.lower().split("x"))
    w, h = (int(v) for v in args.size.lower().split("x"))
    pos = corners(fw, fh, w, h, args.margin)

    result = []
    for path in args.images:
        img = Image.open(path).convert("RGB").resize((fw, fh), Image.LANCZOS)
        arr = np.asarray(img).astype(int)
        scores = {c: round(busy(arr, *pos[c], w, h), 4) for c in ORDER}
        choice = next((c for c in ORDER if scores[c] < args.threshold), "none")
        result.append({"image": path, "corner": choice,
                       "position": list(pos[choice]) if choice != "none" else None, "busy": scores})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
