# Zoom-Technik: feste technische Regeln

<!-- Gemeinsamer Baustein: wird aus skill-development/claude-skills/_shared/ in alle Schnitt-Skills kopiert. Nur dort ändern. -->

Diese Regeln betreffen Probleme, die bei jeder Zoom- oder Meeting-Aufnahme auftreten können. Sie gelten unabhängig von Dramaturgie und Serie. Konkrete Pixel- und Sekundenwerte gehören ins Projektlog, nicht in den Skill.

Die Hilfsskripte liegen im Ordner `scripts/` dieses Skills und brauchen `python3` mit `numpy` und `Pillow` (im Vibe-Editing-Projekt: `plugins/vibe-editing/.venv/bin/python`).

## 1. Perspektiven synchronisieren

- Eine maßgebliche Tonspur festlegen, meist die separate Audiodatei oder die kombinierte Hauptaufnahme.
- Vor dem Schnitt jede Bildperspektive per Kreuzkorrelation gegen diese Tonspur prüfen:

  ```bash
  python3 scripts/sync_check.py MASTER_AUDIO PERSPEKTIVE.mp4 [WEITERE.mp4 …] --at 600 3600 7000
  ```

  Mehrere über die Aufnahme verteilte Zeitpunkte messen. Abweichungen unter einem Bildintervall (40 ms bei 25 fps) gelten als synchron. Einen konstanten Versatz einmal korrigieren; einen zunehmenden Drift melden und nicht stillschweigend überdecken.
- Alle Bildquellen danach mit denselben Originalzeitcodes schneiden.

## 2. Transkript

- Das Zoom-Transkript (VTT) ist ein guter Überblick, hat aber oft Lücken, falsche Sprecherzuordnungen und ungenaue Zeiten.
- Für alle Passagen, die ins Video kommen können, lokal mit Whisper (mindestens Modell `medium`, Wortzeitstempel) nachtranskribieren. Cloud-Transkription nur nach ausdrücklicher Zustimmung.
- Namen nie aus dem Transkript raten; mit sichtbaren Zoom-Namen und Anreden abgleichen.

## 3. Schnittkanten

- Whisper-Wortzeiten nicht direkt als Schnittkante verwenden. Sie weichen bis etwa 0,3 s ab.
- Jede Kante auf die leiseste Stelle im Originalton zwischen den Nachbarwörtern legen und danach alle Kanten automatisch prüfen:

  ```bash
  python3 scripts/snap_edges.py MASTER_AUDIO --plan 10_WORK/02-cut-plan.json --out 10_WORK/03-kanten.json
  ```

  Das Skript schlägt korrigierte Kanten vor und markiert Kanten mit hohem Pegel als Verdacht auf ein angeschnittenes Wort. Markierte Kanten im Original anhören; das Ergebnis ersetzt keine Hörkontrolle.
- Vor harten Anfangskonsonanten und nach dem letzten bedeutungstragenden Laut lieber etwas mehr stehen lassen.

## 4. Richtige Person im Bild

- Die aktive Sprecheransicht schaltet oft 0,3–0,5 s verspätet um. Zeigt sie am Anfang noch die falsche Person, eine synchrone Kachel aus der Galerieansicht als Bildbrücke verwenden und erst danach umschalten.
- Kachelpositionen in der Galerie ändern sich, wenn Personen beitreten, gehen oder die Kamera ein- und ausschalten. Die Lage der gewünschten Kachel in kurzen Abständen (etwa alle 0,4 s) prüfen und das Segment an jedem Layoutwechsel teilen.

## 5. Bildausschnitt der Webcam

- Den Ausschnitt pro Aufnahme und Kameraposition neu bestimmen; nie ungeprüft aus einer früheren Folge übernehmen.
- Vor dem Rendern an Standbildern mehrerer Stellen prüfen: Kinn und Hals nicht abgeschnitten, kein unnötiger Kopfraum, keine störenden Gegenstände am oberen Rand, Gestik nicht verloren.
- Sitzt die Person tief im Bild, lieber oben enger und unten bis zur Bildkante schneiden als das Kinn opfern. Je stärker vergrößert wird, desto unschärfer; einen Ausschnitt so groß wie möglich halten.
- Eingebrannte Zoom-Einblendungen (Zeitstempel, Namensfelder, Symbole) im gewünschten Ausschnitt nicht durch engeren Zuschnitt wegschneiden, wenn dabei Kinn oder Gesicht verloren gehen. Stattdessen das betroffene Rechteck mit dem passenden, synchronen Stück aus der Galeriekachel derselben Person ersetzen (skaliert, weiche Maske, Layoutwechsel beachten).
- Einen freigegebenen Ausschnitt konsistent auf alle passenden Auftritte derselben Person anwenden, solange das Ausgangsbild gleich bleibt.

## 6. Talking Head (falls in den Vorab-Fragen gewählt)

- Größe als Orientierung: etwa ein Fünftel der Bildbreite (400 × 225 bei 1920 × 1080), abgerundete Ecken, schmaler heller Rand, weicher Schatten, 0,25 s Ein- und Ausblendung.
- Die Ecke je Folie automatisch nach Freifläche wählen:

  ```bash
  python3 scripts/pip_corner.py FOLIE.png [WEITERE.png …]
  ```

  Bevorzugt oben rechts; nur wenn dort Inhalt liegt, eine andere Ecke. Ist keine Ecke frei (Doppelseiten, Übersichten, große Dokumentausschnitte), keinen Talking Head zeigen.
- Nur auf Folienpassagen ab etwa 1,5 s, und nur solange die gezeigte Person spricht. Der Ausschnitt darf das Kinn nicht abschneiden.
- Lippensynchron wie jedes Sprecherbild: Bildzeit folgt der Tonzeit.

## 7. Lippensynchronität der Endfassung

- Eine gleiche Bild- und Tondauer ist kein Nachweis. An mehreren Stellen (Anfang, erste Sprecherpassage nach der Titelkarte, nach Übergängen, kurz vor Schluss) den Ton der Endfassung gegen die Originalzeitachse kreuzkorrelieren (`sync_check.py` mit `--offset` für die Position im Schnitt) und stichprobenartig ansehen.
- Abweichungen getrennt einordnen: konstanter Versatz, Sprung an einer Naht, zunehmender Drift.

## 8. Effizient überarbeiten

- Jedes Segment einzeln als Zwischendatei (Bild und Ton getrennt, verlustarm) rendern und in einem versionierten Ordner cachen. Bei einer Korrektur nur die betroffenen Segmente neu rendern und danach zusammensetzen.
- Nie eine frühere Fassung überschreiben; `v1`, `v2` … fortlaufend.

## 9. Reine Bildänderungen isolieren

Verlangt die Nutzerin oder der Nutzer ausdrücklich nur eine Bildänderung:

- Inhalt, Schnittzeiten, Reihenfolge, Musik und Ton unverändert lassen.
- Die dekodierte Tonspur der alten und neuen Fassung hashen; sie muss identisch sein.
- Unveränderte Bildbereiche stichprobenartig per PSNR vergleichen.
- Wird vorne etwas eingefügt (etwa ein Startbild), den Ton exakt um diese Dauer verschieben und den Versatz nachmessen.
