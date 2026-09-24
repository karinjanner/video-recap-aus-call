# Lernschleife nach jeder Folge

Nach einer freigegebenen oder bewusst abgeschlossenen Folge die tatsächlichen Korrekturen aus Projektlog, Versionsverlauf und Abnahme auswerten. Ziel ist ein besserer nächster Erstschnitt, nicht das Ansammeln aller Einzelfälle.

## Änderungen erfassen

- Was war in der ersten Fassung anders als im freigegebenen Ergebnis?
- War das Problem redaktionell, visuell, akustisch, technisch oder Teil des Abnahmeprozesses?
- Welche Änderung hat verbessert?
- Ist die Ursache auch in künftigen Folgen oder anderen Reihen relevant?

## Genau eine Ebene wählen

### Allgemeine Dauerregel

Technische oder redaktionelle Regel mit hohem Wiederholungsrisiko über verschiedene Reihen hinweg, etwa vollständige Wortanfänge, richtige Sprecherbilder, faire Bedeutung oder unveränderte Tonspur bei reiner Bildkorrektur. Nur solche Regeln gehören in den neutralen Skill.

### Stabile Serienpräferenz

Wiederkehrende Entscheidung nur für diese Solution, etwa Rollen, Farben, Musik, Titeltexte, Zielgruppe oder bevorzugte Dramaturgie. Diese gehört in das lokale `series-profile.md`, wenn sie ausdrücklich künftig gelten soll oder sich in mehreren Folgen bewährt hat.

### Entscheidung nur für diese Folge

Zeitcodes, konkrete Statements, Namenskorrekturen, einzelne Folien, Crops, einmalige Ausschlüsse und Freigaben. Diese bleiben im Projektlog.

## Beim nächsten Video prüfen

- Welche früheren Korrekturen waren bereits gelöst?
- Welche manuellen Änderungen blieben nötig?
- Hat eine Regel zu einer unpassenden Verallgemeinerung geführt?

Zu breite Regeln eingrenzen oder zurücknehmen. Erfolg bedeutet weniger vermeidbare Korrekturen bei gleichbleibender redaktioneller Flexibilität.

## Gemeinsame Bausteine

`zoom-technik.md`, `vorab-fragen.md`, `folien-und-dokumente.md`, `startbild-und-veroeffentlichung.md` und die Skripte `sync_check.py`, `snap_edges.py`, `pip_corner.py` sind in allen Schnitt-Skills dieser Familie wortgleich. Eine allgemeine technische Regel dort in allen Skills gleich übernehmen. Im Vibe-Editing-Projekt liegen die Quellen in `skill-development/claude-skills/_shared/`; `python3 skill-development/claude-skills/sync_skills.py` verteilt sie, prüft die Skills, gleicht die installierten Kopien ab und baut die Upload-ZIP-Dateien neu.
