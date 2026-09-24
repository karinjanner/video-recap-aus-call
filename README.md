# Video-Recap aus Call

Ein Skill für **Claude Code**, der aus einer langen Call- oder Meeting-Aufzeichnung (typisch 1–3 Stunden Zoom, etwa ein Workshop, eine Arbeitsgruppe oder ein Community-Treffen) einen zusammenhängenden **7–10-minütigen Recap im Querformat (16:9)** schneidet: mit Cold Open, verschiedenen Stimmen der Runde, Titel- und Abschlusskarte, Themenübergängen und technischer Qualitätsprüfung.

> [!IMPORTANT]
> **Dieser Skill funktioniert nur zusammen mit dem Vibe-Editing-Repo.**
>
> Der Skill ist die redaktionelle Anleitung: was ausgewählt wird, in welcher Reihenfolge, wie das Video aufgebaut ist. Die eigentlichen Schnitt-, Transkriptions- und Renderwerkzeuge kommen aus dem kostenlosen, öffentlichen Projekt **Vibe Editing**:
>
> 👉 **https://github.com/maddexritter-rgb/vibe-editing**
>
> Ohne Vibe Editing kann der Skill nur planen und Texte vorschlagen, aber kein Video schneiden. Vibe Editing ist ein eigenständiges Projekt von einem anderen Autor und nicht Teil dieses Repos.

## Was du brauchst

1. **Claude Code**, zum Beispiel die Claude-Desktop-App (Bereich „Code“). Im normalen Chat auf claude.ai kann der Skill nicht schneiden, weil er dort keinen Zugriff auf Videodateien und Werkzeuge auf deinem Rechner hat.
2. **Vibe Editing** auf deinem Rechner (siehe oben).
3. **Diesen Skill.**

Du musst nichts im Terminal eintippen. Claude übernimmt die Einrichtung und fragt dich vorher.

## Installation

### Am einfachsten: Claude machen lassen

Öffne Claude Code und schreibe:

> Installiere mir bitte den Skill von https://github.com/karinjanner/video-recap-aus-call und richte Vibe Editing ein, falls es noch fehlt.

### Als Plugin (für alle, die mit Claude Code vertraut sind)

In Claude Code nacheinander eingeben:

```
/plugin marketplace add karinjanner/video-recap-aus-call
/plugin install video-recap-aus-call@video-recap-aus-call
```

### Von Hand

Unter [Releases](https://github.com/karinjanner/video-recap-aus-call/releases) die Datei `video-recap-aus-call.zip` herunterladen und entpacken. Den Ordner `video-recap-aus-call` nach `~/.claude/skills/` legen.

## Was beim ersten Start passiert

Wenn Vibe Editing noch nicht auf deinem Rechner ist, erklärt Claude dir das und **fragt ausdrücklich, ob es Vibe Editing herunterladen und einrichten darf.** Erst nach deinem Ja passiert etwas. Das gilt auch dann, wenn deine Claude-Einstellungen das Herunterladen ohne Rückfrage erlauben würden. Sagst du Nein, wird nichts heruntergeladen.

Claude holt Vibe Editing dabei ausschließlich von der Originaladresse oben, nie von einer Kopie.

## Loslegen

Leg die Aufnahme in einen Ordner und schreibe Claude zum Beispiel:

> Mach mir einen Video-Recap aus dem Call in diesem Ordner.

Beim ersten Mal stellt Claude ein paar kurze Fragen: Name und Thema eurer Runde oder Reihe, wer moderiert, ob ihr ein eigenes Design oder eigene Musik habt. Ohne eigenes Design leitet der Skill eines aus euren Folien ab und zeigt dir vorher eine Vorschau. Musik wird nur verwendet, wenn du selbst eine Datei bereitstellst.

## Datenschutz

Alles läuft lokal auf deinem Rechner. Die Transkription passiert standardmäßig offline. Videos, Stimmen oder Transkripte werden nicht hochgeladen, außer du verlangst das ausdrücklich.

## Lizenz und Dank

Dieser Skill steht unter der [MIT-Lizenz](LICENSE). Die Produktionswerkzeuge stammen aus [Vibe Editing](https://github.com/maddexritter-rgb/vibe-editing) (ebenfalls MIT-Lizenz). Dieses Repo ist ein unabhängiger Zusatz und kein offizieller Teil von Vibe Editing.
