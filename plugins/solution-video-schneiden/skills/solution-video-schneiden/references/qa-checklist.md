# QA-Checkliste

## Inhalt und Rollen

- Wurde die vollständige Meeting-Aufzeichnung analysiert und als Themenlandkarte dokumentiert?
- Stammen die ausgewählten Aussagen aus einer echten Prüfung des gesamten Meetings statt nur eines kurzen Ausschnitts?
- Ist das Ergebnis eine zusammenhängende 7–10-minütige Folge und nicht bloß eine Sammlung unabhängiger Highlights?
- Themenversprechen der Folge in einem Satz dokumentiert?
- Versteht eine außenstehende Person nach Cold Open und Titelbrücke das Thema?
- Beginnt der Cold Open mit einer klaren, vollständigen Aussage der Moderation?
- Bei Hauptvortrag: vortragende Person im Cold Open und direkt nach der Titelbrücke?
- Fragen, Einwände und Reaktionen inhaltlich wertvoll und fair zugeordnet?
- Wirkt der Vortrag interaktiv, ohne künstliche oder irreführende Anschlüsse?
- Ergänzen sich Statements statt sich zu wiederholen?
- Konkretes Beispiel oder Ergebnis enthalten, wenn das Material eines bietet?
- Organisatorische und technische Nebenpfade entfernt, sofern nicht Thema?
- Schließt die Moderation die Folge mit einem vollständigen, tragfähigen Statement?
- Falls keine geeignete Moderationsaussage existiert: Ausnahme vor dem Rendern offengelegt, freigegeben und begründet?

## Bild

- Kein doppelter erster Frame und keine unbeabsichtigte Wiederholung.
- Richtige Person sichtbar, solange ihre bereinigte Passage läuft.
- Folienwechsel passen semantisch zum Gesagten.
- Lower Third zeigt bestätigten Namen ohne E-Mail-Adresse.
- Crops entfernen störende Ränder, ohne Gesicht, Gestik oder wichtige Objekte abzuschneiden.
- Keine privaten Tabs, Benachrichtigungen, Adressen oder sensiblen Projektnamen.
- Titel-, Themen- und Abschlusskarten ausreichend lange lesbar.
- Design folgt dem Serienprofil; ein aus Folien abgeleitetes Design wurde per Vorschau bestätigt, eine neutrale Gestaltung ist als vorläufig gekennzeichnet; keine fremden Logos übernommen.

## Ton und Musik

- Lippenbewegung und Sprache synchron.
- Keine abgeschnittenen Konsonanten, Atmer oder Wortenden.
- Kritische Grenzen im Originalton kontrolliert.
- Sprachlautheit zwischen Personen ausgeglichen.
- Bei `ohne Musik`: keine Platzhalter- oder fremde Musik enthalten; Übergänge akustisch sauber.
- Bei bereitgestellter Musik: Datei wurde für die aktuelle Solution ausdrücklich ausgewählt und ihre Nutzung bestätigt; Sprache bleibt verständlich; keine willkürlich abgeschnittene Phrase; Intro und Outro hörend geprüft.
- Musik an Themenübergängen nur bei separat bestätigter Übergangsnutzung; jeder geplante Musikeinsatz ist im fertigen Übergang tatsächlich hörbar und vollständig geprüft.
- Musik unter Sprache nur bei ausdrücklichem Wunsch und eindeutig leiser als Sprache.
- Kein Lautheitssprung, bei dem Musik die angrenzende Sprache überdeckt.

## Übergänge

- Nur echte Themenwechsel markiert?
- Verhindert jeder Übergang falsche Kontinuität?
- Letzter Satz davor und erster Satz danach vollständig?
- Nummerierter Prüfclip mit Kontext für jede neue Übergangslösung vorhanden?

## Technik

- Quell- und Arbeitsdateien liegen im Vibe-Editing-Projekt; finale Fassung liegt in `20_DELIVER/`.
- Ausgabe entspricht Format, Auflösung und Bildrate des Serienprofils.
- H.264/yuv420p und AAC Stereo 48 kHz, sofern Profil nichts anderes vorgibt.
- Video- und Audiodauer ausgerichtet.
- Datei an Anfang, Übergängen und Ende abspielbar.
- `ffprobe`, Lautheitsprüfung und Kontrollclips erzeugt.
- Vollständige Datei ohne Dekodierfehler geprüft.
- Bei reiner Bildänderung Renderplan nur visuell verändert und Hash der dekodierten Tonspur identisch.

## Übergabe

- Kandidatentabelle, Schnittplan, Render-Skript, QA-Bericht und Projektlog vorhanden.
- Dateiname enthält Datum und Versionsnummer.
- Vollständige Fassung in Echtzeit angesehen.
- Upload oder Veröffentlichung erst nach separater Freigabe.
- Learnings als allgemeine Regel, Serienpräferenz oder Einzelfall eingeordnet.
