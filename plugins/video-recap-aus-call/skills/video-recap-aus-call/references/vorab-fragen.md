# Vorab-Fragen vor dem ersten Schnitt

<!-- Gemeinsamer Baustein: wird aus skill-development/claude-skills/_shared/ in alle Schnitt-Skills kopiert. Nur dort ändern. -->

Ziel: wenige, gezielte Entscheidungen einholen, die Aufwand, Rechenzeit oder Vertraulichkeit betreffen. Alles andere entscheidet der Skill selbst und dokumentiert es. Höchstens vier Fragen auf einmal stellen, jeweils mit Empfehlung. Bereits aus Auftrag, Dateien oder Serienprofil eindeutig erkennbare Antworten nicht erneut erfragen, sondern als Vorschlag bestätigen lassen.

Die Fragen stellen, sobald das Material erfasst ist und bevor Kandidaten ausgewählt oder aufwendige Arbeitsschritte gestartet werden. Offene Antworten blockieren die Inhaltsanalyse nicht, wohl aber das Rendern.

## 1. Folien

> „Gibt es eine saubere oder neuere Fassung der Folien (PDF oder Bilder), die ich statt der Bildschirmfreigabe aus der Aufnahme verwenden soll?“

- **Ja:** Die Folien in `00_SOURCE/` ablegen, einzeln in Zielauflösung rastern und den gesprochenen Stellen inhaltlich zuordnen. Die Bildschirmfreigabe dient dann nur noch als Zeitreferenz, wann welche Folie gezeigt wurde.
- **Nein oder noch nicht:** Folien aus der Bildschirmfreigabe der Aufnahme verwenden, sauber zuschneiden und Zoom-Oberfläche, Mauszeiger und Benachrichtigungen vermeiden. Hinweisen, dass eine bessere Fassung später reine Bildänderung ist und den Ton nicht verändert.
- Weichen neue Folien inhaltlich von den gezeigten ab, nur Folien verwenden, deren Aussage zum gesprochenen Ton passt.

## 2. Talking Head auf Folien

> „Soll auf längeren Folienpassagen eine kleine Einblendung der sprechenden Person (Talking Head) zu sehen sein? Das braucht deutlich mehr Rechenzeit.“

Drei Stufen anbieten:

- **Aus:** Folien im Vollbild. Schnellste Variante.
- **Einfach:** feste Ecke, Ausschnitt aus der aktiven Sprecheransicht; nur wo die Person tatsächlich spricht. Mittlerer Aufwand.
- **Voll:** Kachel aus der Galerieansicht, deren Lage bei Layoutwechseln laufend nachgeführt wird, und je Folie die freie Ecke automatisch gewählt ([Zoom-Technik](zoom-technik.md)). Höchster Aufwand, sauberstes Ergebnis, wenn die Sprecheransicht zu tief sitzt oder Einblendungen enthält.

Die Antwort gilt für diese Folge. Nicht ungefragt die volle Stufe wählen.

## 3. Referenzdokument

> „Gibt es ein Dokument, an dem sich das Video inhaltlich orientieren oder prüfen lassen soll, etwa Whitepaper, Konzept, Handout oder Protokoll?“

- **Ja:** Das Dokument nach `00_SOURCE/paper/` kopieren (Original unverändert lassen) und als Faktenbasis verwenden. Aussagen, die ihm widersprechen oder nur Geplantes als Ist-Stand darstellen, nicht verwenden oder im Bild richtigstellen.
- **Nein:** Die Aufnahme selbst ist die Grundlage.

## 4. Originaldokumente und Vertraulichkeit

> „Welche Originaldokumente oder Live-Bilder darf ich zeigen, und was muss unkenntlich bleiben (Kundennamen, Personen, Preise, Adressen)?“

- Gezeigte Originale in `10_WORK/…/material/` kopieren; Originale nie verändern.
- Unklare Stellen standardmäßig unscharf machen und in der Übergabe benennen.
- Kundennamen, Namen Dritter ohne Kamera, E-Mail-Adressen, private Tabs und Benachrichtigungen nie sichtbar lassen.

## 5. Startbild

> „Soll das Video mit einem Startbild beginnen, das gleichzeitig als Vorschaubild für YouTube oder WhatsApp dient?“

Bei Ja nach [Startbild und Veröffentlichung](startbild-und-veroeffentlichung.md) vorgehen. Ohne Antwort kein Startbild einbauen.

## Dokumentation

Die Antworten oben im Projektlog festhalten, getrennt nach **bestätigt**, **aus dem Material abgeleitet** und **noch offen**. Ändert sich eine Antwort später (zum Beispiel neue Folien liegen vor), ist das eine reine Bildänderung nach den Isolationsregeln der [Zoom-Technik](zoom-technik.md).
