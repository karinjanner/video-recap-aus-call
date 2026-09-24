# Startbild und Veröffentlichung

<!-- Gemeinsamer Baustein: wird aus skill-development/claude-skills/_shared/ in alle Schnitt-Skills kopiert. Nur dort ändern. -->

Beides ist optional und wird nur auf ausdrücklichen Wunsch umgesetzt (siehe [Vorab-Fragen](vorab-fragen.md)).

## Startbild

Ein Standbild ganz am Anfang, das zugleich als Vorschaubild (Thumbnail) für YouTube, WhatsApp oder Newsletter dient.

### Gestaltung

- Vorlage und Farben aus dem Serienprofil verwenden. Gibt es keine Vorlage, ein ruhiges Titelbild im Seriendesign bauen: großer Serientitel, kurzer Folgentitel, Datum.
- Die Art des Videos sichtbar machen, zum Beispiel ein Etikett „RECAP“ für einen Diskussions-Recap oder „… stellt vor“ für eine Konzeptvorstellung.
- Personen nur zeigen, wenn sie in der Aufnahme sichtbar mitgewirkt haben. Namen nur in bestätigter Schreibweise. Teilnehmende ohne Kamera nicht mit fremden Bildern darstellen, höchstens als Zahl („+1“).
- Als HTML-Vorlage bauen und mit einem lokalen Browser im Headless-Modus rendern. Mindestens zwei Varianten nebeneinander zur Auswahl zeigen, wenn noch keine Vorlage freigegeben ist.

### Dateien

- Rendern in 2560 × 1440 und daraus 1280 × 720 (YouTube-Thumbnail, unter 2 MB) sowie 1920 × 1080 für das Video.
- Beide PNG-Größen zusätzlich in `20_DELIVER/` ablegen: `YYYY-MM-DD_<slug>_startbild[-Variante]_BREITExHÖHE.png`.

### Einbau ins Video

- Etwa 2,5 s stehendes Startbild ohne Ton, danach 1,0 s Überblendung in den ersten Inhalt.
- Wird das Startbild einer bereits abgenommenen Fassung vorangestellt, ist das eine reine Bildänderung: Ton exakt um die Dauer verschieben, Versatz nachmessen, übriges Bild unverändert lassen ([Zoom-Technik](zoom-technik.md), Abschnitt 9).
- Eine Namenseinblendung im Cold Open beginnt erst nach der Überblendung.

## Veröffentlichung

Upload, Titeländerung oder Thumbnail-Wechsel nur nach ausdrücklicher Freigabe für genau dieses Video und nur im eigenen Konto der Nutzerin oder des Nutzers.

- **Titel:** nach dem Titelschema des Serienprofils; ohne Schema einen Vorschlag machen und bestätigen lassen.
- **Beschreibung:** zwei bis drei Sätze zum Themenversprechen, danach die Kapitelliste.
- **Kapitel:** Zeitstempel beziehen sich auf die ausgelieferte Datei (inklusive Startbild), nicht auf die Originalaufnahme. Liste beginnt mit `0:00`.
- **Thumbnail:** die 1280 × 720-Fassung des Startbilds. Lässt sich die Dateiauswahl im Browser nicht bedienen, den genauen Dateipfad nennen und die Person bitten, das Bild selbst hochzuladen. Nichts vortäuschen: im Projektlog festhalten, was gesetzt ist und was noch offen ist.
- Nach dem Speichern prüfen, ob Titel und Vorschaubild tatsächlich übernommen wurden.
