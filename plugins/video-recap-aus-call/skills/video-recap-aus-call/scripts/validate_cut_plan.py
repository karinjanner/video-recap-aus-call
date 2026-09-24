#!/usr/bin/env python3
"""Prueft Struktur, Zeiten und Rollenlogik eines Recap-Schnittplans."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def seconds(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        raise ValueError(f"ungueltige Zeit: {value!r}")
    parts = value.split(":")
    if len(parts) == 1:
        return float(parts[0])
    if len(parts) == 2:
        minutes, secs = parts
        return float(minutes) * 60 + float(secs)
    if len(parts) == 3:
        hours, minutes, secs = parts
        return float(hours) * 3600 + float(minutes) * 60 + float(secs)
    raise ValueError(f"ungueltige Zeit: {value!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Recap-Schnittplan validieren")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--skip-file-check", action="store_true")
    args = parser.parse_args()

    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: Plan kann nicht gelesen werden: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    if args.profile:
        if not args.profile.is_file():
            errors.append(f"Serienprofil fehlt: {args.profile}")
        else:
            profile_text = args.profile.read_text(encoding="utf-8")
            if "noch offen" in profile_text.lower():
                warnings.append("Serienprofil enthaelt noch offene Angaben")

    project = plan.get("project") or {}
    sources = plan.get("sources") or {}
    segments = plan.get("segments") or []
    music = plan.get("music") or []
    moderator = str(project.get("moderator") or "").strip()
    presenter = str(project.get("main_presenter") or "").strip()
    music_mode = str(project.get("music_mode") or "none").strip().lower()
    transition_music_allowed = project.get("transition_music_allowed") is True
    try:
        source_duration = float(project.get("source_duration_seconds", 0) or 0)
    except (TypeError, ValueError):
        source_duration = 0.0

    if not isinstance(sources, dict) or not sources:
        errors.append("sources fehlt oder ist leer")
    if not isinstance(segments, list) or not segments:
        errors.append("segments fehlt oder ist leer")
    if not moderator:
        warnings.append("Moderator:in ist im Projekt nicht benannt")
    if source_duration <= 0:
        warnings.append("Dauer der vollstaendigen Meeting-Quelle fehlt")
    if project.get("source_review_complete") is not True:
        warnings.append("Vollstaendige Transkript- und Themenlandkartenpruefung ist nicht bestaetigt")
    if music_mode not in {"none", "own"}:
        errors.append("music_mode muss 'none' oder 'own' sein")

    if not args.skip_file_check:
        for key, raw in sources.items():
            if not Path(raw).expanduser().is_file():
                errors.append(f"Quelle {key!r} existiert nicht: {raw}")

    duration = 0.0
    seen: dict[tuple, str] = {}
    cold_open: list[dict] = []
    title_index: int | None = None
    clip_indexes: list[int] = []

    for index, seg in enumerate(segments):
        if not isinstance(seg, dict):
            errors.append(f"Segment {index + 1}: muss ein Objekt sein")
            continue
        label = seg.get("id") or f"Segment {index + 1}"
        kind = seg.get("type")
        if kind == "clip":
            clip_indexes.append(index)
            source = seg.get("source")
            if source not in sources:
                errors.append(f"{label}: unbekannte Quelle {source!r}")
                continue
            try:
                start, end = seconds(seg.get("start")), seconds(seg.get("end"))
            except Exception as exc:
                errors.append(f"{label}: {exc}")
                continue
            if end <= start:
                errors.append(f"{label}: end muss groesser als start sein")
                continue
            duration += end - start
            fingerprint = (source, round(start, 3), round(end, 3))
            if fingerprint in seen and not seg.get("allow_repeat"):
                errors.append(f"{label}: wiederholt exakt {seen[fingerprint]}")
            seen[fingerprint] = label
            if seg.get("complete_sentence") is not True:
                warnings.append(f"{label}: complete_sentence ist nicht true")
            if not str(seg.get("quote", "")).strip():
                warnings.append(f"{label}: quote fehlt")
            if not str(seg.get("reason", "")).strip():
                warnings.append(f"{label}: redaktionelle Begruendung fehlt")
            if seg.get("role") == "cold_open":
                cold_open.append(seg)
        elif kind == "card":
            try:
                card_duration = float(seg.get("duration", 0))
            except (TypeError, ValueError):
                card_duration = 0
            if card_duration <= 0:
                errors.append(f"{label}: Kartenlaenge fehlt oder ist ungueltig")
            duration += max(card_duration, 0)
            if seg.get("role") == "title":
                if title_index is not None:
                    warnings.append("Mehr als eine Titelkarte gefunden")
                title_index = index
        else:
            errors.append(f"{label}: unbekannter type {kind!r}")

    if not cold_open:
        warnings.append("Cold Open fehlt")
    else:
        speakers = {str(s.get("speaker", "")).strip() for s in cold_open if s.get("speaker")}
        if len(speakers) < 2:
            warnings.append("Cold Open enthaelt weniger als zwei unterschiedliche Personen")
        if moderator and moderator not in speakers:
            warnings.append(f"Moderator:in {moderator!r} fehlt im Cold Open")
        elif moderator and str(cold_open[0].get("speaker") or "").strip() != moderator:
            warnings.append(f"Cold Open beginnt nicht mit Moderator:in {moderator!r}")
        if presenter and presenter not in speakers:
            warnings.append(f"Hauptvortragsperson {presenter!r} fehlt im Cold Open")

    if title_index is None:
        warnings.append("Titelkarte fehlt")
    elif presenter:
        first_after_title = next(
            (seg for idx, seg in enumerate(segments) if idx > title_index and isinstance(seg, dict) and seg.get("type") == "clip"),
            None,
        )
        if not first_after_title:
            warnings.append("Nach der Titelkarte folgt kein Sprachclip")
        elif str(first_after_title.get("speaker") or "").strip() != presenter:
            warnings.append(f"Nach der Titelkarte beginnt nicht die Hauptvortragsperson {presenter!r}")

    if clip_indexes:
        last_clip = segments[clip_indexes[-1]]
        if last_clip.get("complete_sentence") is not True:
            warnings.append("Letztes Sprachsegment ist nicht als vollstaendige Aussage markiert")
        if last_clip.get("role") != "closing_statement":
            warnings.append("Letztes Sprachsegment ist nicht als Abschlussaussage eingeordnet")
        if moderator and str(last_clip.get("speaker") or "").strip() != moderator:
            warnings.append(f"Letztes Sprachsegment stammt nicht von Moderator:in {moderator!r}")

    if music_mode == "none":
        if music:
            errors.append("music_mode ist 'none', aber music enthaelt Eintraege")
    elif music_mode == "own":
        roles: set[str] = set()
        if not music:
            errors.append("music_mode ist 'own', aber music ist leer")
        for index, item in enumerate(music):
            if not isinstance(item, dict):
                errors.append(f"Musikeintrag {index + 1} muss ein Objekt sein")
                continue
            role = str(item.get("role") or "").strip()
            if role:
                roles.add(role)
            if item.get("usage_confirmed") is not True:
                errors.append(f"Musikeintrag {index + 1}: usage_confirmed muss true sein")
            raw_path = str(item.get("path") or "").strip()
            if not raw_path:
                errors.append(f"Musikeintrag {index + 1}: path fehlt")
            elif not args.skip_file_check and not Path(raw_path).expanduser().is_file():
                errors.append(f"Musikdatei existiert nicht: {raw_path}")
            if role == "transition":
                if not transition_music_allowed:
                    errors.append(f"Musikeintrag {index + 1}: Uebergangsmusik ist im Projekt nicht freigegeben")
                if item.get("transition_usage_confirmed") is not True:
                    errors.append(f"Musikeintrag {index + 1}: transition_usage_confirmed muss true sein")
                if not item.get("phrase_end"):
                    warnings.append(f"Musikeintrag {index + 1}: Ende der Uebergangsphrase fehlt")
        for expected in ("intro", "outro"):
            if expected not in roles:
                warnings.append(f"Musikeinsatz {expected!r} fehlt")

    target = project.get("target_seconds", [420, 600])
    if isinstance(target, list) and len(target) == 2:
        if duration < float(target[0]) or duration > float(target[1]):
            warnings.append(f"geplante Segmentdauer {duration:.1f}s liegt ausserhalb {target[0]}–{target[1]}s")

    compression_ratio = round(source_duration / duration, 2) if source_duration > 0 and duration > 0 else None
    report = {
        "ok": not errors,
        "source_seconds": round(source_duration, 3) if source_duration > 0 else None,
        "estimated_seconds": round(duration, 3),
        "compression_ratio": compression_ratio,
        "music_mode": music_mode,
        "transition_music_allowed": transition_music_allowed,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
