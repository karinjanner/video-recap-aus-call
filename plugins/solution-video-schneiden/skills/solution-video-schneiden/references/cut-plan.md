# Schnittplan-Format

Vor jedem Rendern eine JSON-Datei anlegen. Zeiten dürfen Sekunden oder `HH:MM:SS.mmm` sein.

```json
{
  "project": {
    "date": "2026-09-02",
    "title": "Name der Solution",
    "source_duration_seconds": 7200,
    "source_review_complete": true,
    "target_seconds": [420, 600],
    "resolution": [1920, 1080],
    "fps": 25,
    "moderator": "Bestätigter Name",
    "main_presenter": "Bestätigter Name oder null",
    "music_mode": "none",
    "transition_music_allowed": false
  },
  "sources": {
    "main": "/absolute/path/main.mp4",
    "speaker": "/absolute/path/active-speaker.mp4",
    "slides": "/absolute/path/screen-share.mp4"
  },
  "segments": [
    {
      "id": "cold-open-01",
      "type": "clip",
      "role": "cold_open",
      "source": "speaker",
      "start": "00:12:03.400",
      "end": "00:12:14.600",
      "speaker": "Bestätigter Name",
      "meeting_role": "main_presenter",
      "quote": "Vollständige Aussage …",
      "complete_sentence": true,
      "visual": "speaker_full",
      "reason": "Eröffnet den fachlichen Kern"
    },
    {
      "id": "title",
      "type": "card",
      "role": "title",
      "duration": 5
    }
  ],
  "music": []
}
```

Bei ausdrücklich bereitgestellter Musik:

```json
{
  "role": "intro",
  "path": "/absolute/path/bereitgestellter-track.wav",
  "phrase_start": "00:00:00.000",
  "phrase_end": "00:00:09.500",
  "duck_under_speech": true,
  "usage_confirmed": true
}
```

Für Übergangsmusik zusätzlich:

```json
{
  "role": "transition",
  "path": "/absolute/path/bereitgestellter-track.wav",
  "phrase_start": "00:00:24.000",
  "phrase_end": "00:00:28.500",
  "duck_under_speech": false,
  "usage_confirmed": true,
  "transition_usage_confirmed": true
}
```

## Regeln

- Reihenfolge in `segments` entspricht der Ausgabereihenfolge.
- `source` verweist auf einen Schlüssel in `sources`.
- `start` und `end` sind Originalzeitcodes.
- Karten besitzen `duration` statt `start` und `end`.
- `quote` enthält die tatsächlich verwendete vollständige Aussage.
- `reason` dokumentiert die redaktionelle Begründung.
- `complete_sentence` muss bewusst gesetzt werden.
- Identische Quellintervalle nicht doppelt verwenden; bewusste Wiederholungen mit `allow_repeat: true` begründen.
- Bei `music_mode: none` bleibt `music` leer.
- `source_duration_seconds` enthält die Dauer der vollständigen Meeting-Aufzeichnung; `source_review_complete` darf erst nach Transkript- und Themenlandkartenprüfung `true` sein.
- Bei `music_mode: own` müssen Musikdatei und Nutzungsbestätigung vorhanden sein; Anfangs- und Endmusik können aus derselben oder aus getrennten Dateien stammen. Vollständige musikalische Phrasen statt pauschal vollständiger Tracks planen.
- Musikeinträge mit `role: transition` sind nur erlaubt, wenn `project.transition_music_allowed` und `transition_usage_confirmed` ausdrücklich `true` sind.
- Bei Hauptvortrag muss die Person im Cold Open vorkommen und der erste Sprachclip nach der Titelkarte von ihr stammen. Bewusste Abweichungen im Projektlog begründen.
- Das letzte Sprachsegment vor der Abschlusskarte muss eine vollständige Aussage der Moderation mit `role: closing_statement` sein. Fehlt eine geeignete Moderationsaussage im Material, die belegte Ausnahme vor dem Rendern freigeben und im Projektlog begründen.
