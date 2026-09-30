# Geführter Ablauf: erst fragen, dann planen, dann rendern

<!-- Gemeinsamer Baustein: wird aus skill-development/claude-skills/_shared/ in alle Schnitt-Skills kopiert. Nur dort ändern. -->

Rendern dauert lange. Deshalb führt der Skill die Person Schritt für Schritt durch drei Haltepunkte. An jedem Haltepunkt wird gewartet, bis eine Antwort da ist. **Ohne ausdrücklich freigegebenen Schnittplan wird nichts gerendert**, auch kein „schneller erster Entwurf“.

Fragen immer in einfacher Sprache, höchstens vier auf einmal, jede mit Empfehlung. Was aus Auftrag, Dateien oder Serienprofil schon eindeutig hervorgeht, nicht erneut offen fragen, sondern kurz als Vorschlag bestätigen lassen.

## Haltepunkt 1: Material klären (vor der Transkription)

Sobald die Dateien erfasst sind (`inspect_inputs.py`), kurz zusammenfassen, was gefunden wurde: Dauer, Bildquellen, Tonspuren, Transkript, Chat, Folien. Dann fragen:

### Mehrere Ansichten oder Kameras

> „Ich habe folgende Bildquellen gefunden: … Gibt es noch weitere Aufnahmen desselben Termins? Zum Beispiel bei Zoom weitere Ansichten (Sprecheransicht, Galerie, Bildschirmfreigabe) oder, bei einem Vortrag oder Workshop, eine zweite Kamera, die von einer anderen Seite gefilmt hat? Die kann ich mit dem Ton synchronisieren und abwechselnd einsetzen.“

- Bei Zoom gezielt nach fehlenden Ansichten fragen: Die Cloud-Aufnahme kann Sprecheransicht, Galerie, Bildschirmfreigabe und Ton getrennt liefern. Liegt nur eine davon vor, darauf hinweisen, dass weitere Ansichten Sprecherbilder und Folien deutlich verbessern.
- Zusätzliche Kameras oder Handyaufnahmen haben meist einen eigenen Startzeitpunkt. Den Versatz über den Ton messen ([Zoom-Technik](zoom-technik.md), `sync_check.py`) und nur synchron geprüfte Quellen verwenden.
- Weitere Dateien nach `00_SOURCE/` kopieren; Originale nie verändern.

### Transkript

Liegt ein Transkript bei (etwa Zoom-VTT), stichprobenartig gegen den Ton prüfen und das Ergebnis in einem Satz sagen („Das Zoom-Transkript ist brauchbar“ oder „hat viele Lücken und falsche Namen“). Ist es lückenhaft oder fehlt es, **vor** einer eigenen Volltranskription fragen:

> „Das vorhandene Transkript ist an vielen Stellen ungenau. Hast du noch ein zweites Transkript, zum Beispiel aus einem anderen Tool, das du mir geben kannst? Dann gleiche ich beide ab. Oder soll ich das Gespräch selbst neu transkribieren? Das dauert länger und kostet mehr Rechenzeit beziehungsweise Tokens.“

- **Zweites Transkript:** in `00_SOURCE/` ablegen, beide abgleichen, und nur strittige Stellen oder Passagen, die ins Video kommen, lokal nachtranskribieren.
- **Selbst transkribieren:** lokal mit Whisper nach [Zoom-Technik](zoom-technik.md). Cloud-Transkription nur nach ausdrücklicher Zustimmung.
- Die Wahl im Projektlog festhalten.

Außerdem an dieser Stelle die noch offenen [Vorab-Fragen](vorab-fragen.md) stellen (saubere Folien, Talking Head, Referenzdokument, Vertraulichkeit, Startbild), sofern das Serienprofil sie nicht schon beantwortet.

## Haltepunkt 2: Schnittplan vorschlagen und freigeben lassen

Erst nachdem das **ganze** Meeting gesichtet und kartiert ist (Themenlandkarte, Kandidatentabelle), einen Vorschlag zeigen. Er ist knapp und für Menschen ohne Schnitterfahrung lesbar:

1. **Worum es geht:** das Themenversprechen in einem Satz.
2. **Vorgeschlagene Länge:** eine konkrete Zahl mit kurzer Begründung innerhalb der Standardlänge dieses Skills (siehe SKILL.md und Serienprofil), zum Beispiel „ungefähr 8 Minuten, weil …“. Ausdrücklich als Vorschlag kennzeichnen.
3. **Schnittplan als Tabelle** in Ausgabereihenfolge: Nr., Teil (Cold Open, Titel, Thema …), wer spricht, Kernaussage in wenigen Worten, Originalzeit, Bild (Sprecher, Folie, Galerie …), Dauer, dazu die Spalten, die SKILL.md für diesen Skill zusätzlich verlangt. Darunter die geplante Gesamtdauer.
4. **Prioritäten:** was unbedingt drin sein sollte und was bei einer kürzeren Fassung zuerst wegfallen würde, jeweils mit eingesparter Zeit.
5. **Bewusst weggelassen:** Themen oder Beiträge, die nicht vorkommen, mit Grund.
6. **Offene Punkte**, etwa Unschärfe, Abschlusskarte oder unklare Namen.

Danach fragen:

> „Passt das so? Oder möchtest du etwas ändern, zum Beispiel eine andere Reihenfolge, andere Schwerpunkte (etwas soll unbedingt rein oder raus) oder eine andere Länge? Sag mir einfach, was anders sein soll.“
>
> „Hast du eigene Folien oder Hintergrundbilder, die ich verwenden soll? Die kannst du mir jetzt hochladen.“

- Die Frage nach Folien und Hintergrundbildern entfällt, wenn sie in Haltepunkt 1 schon beantwortet wurde. Hochgeladene Dateien nach `00_SOURCE/` legen und im Plan zuordnen: Folien den passenden Tonstellen, Hintergrundbilder etwa Titel-, Kapitel- oder Abschlusskarte.
- Änderungswünsche einarbeiten und den **überarbeiteten Plan erneut zeigen** (Änderungen kurz markieren). So lange wiederholen, bis die Person ausdrücklich zustimmt („passt“, „los“, „freigegeben“ oder ähnlich).
- Schweigen, eine Rückfrage oder eine Teilzustimmung ist keine Freigabe.
- Erst nach der Freigabe im Schnittplan das Freigabefeld setzen und die Freigabe mit Datum und Wortlaut in `project.plan_approval_note` festhalten ([Schnittplan](cut-plan.md)). Ohne Freigabefeld meldet `validate_cut_plan.py` einen Fehler. Die Längenangabe aus der Freigabe als `target_seconds` übernehmen.

Die Freigabe des Plans ersetzt nicht die Abnahme der fertigen Fassung.

## Haltepunkt 3: Abnahme der Fassung

Nach dem Rendern und der eigenen QA die Fassung zeigen und fragen, ob sie so passt oder was geändert werden soll. Bei Änderungen unterscheiden: nur Bild (Ton bleibt unverändert), Inhalt oder Reihenfolge (Plan anpassen, betroffene Segmente neu rendern).

## Wann Haltepunkte entfallen dürfen

Nur wenn die Person es ausdrücklich verlangt („frag nicht, schneid einfach“). Dann den Plan trotzdem kurz zeigen, die Begründung im Projektlog festhalten und `plan_approval_note` entsprechend ausfüllen.
