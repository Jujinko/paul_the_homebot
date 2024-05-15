# Google Calendar Management Bot

Dies ist ein Python-Skript, das einen Telegram-Bot bereitstellt, um Ereignisse im Google Kalender zu verwalten. Der Bot verwendet die Google Calendar API und Vertex AI, um Ereignisse abzurufen, hinzuzufügen und zu löschen.

## Voraussetzungen

Stelle sicher, dass du die folgenden Voraussetzungen erfüllst, bevor du mit der Einrichtung beginnst:

1. Ein Google Cloud Projekt mit aktivierter Google Calendar API.
2. Eine `credentials.json` Datei, die die Client-Geheimnisse für die Google API enthält.
3. Ein Telegram-Bot-Token. Du kannst einen neuen Bot erstellen und das Token erhalten, indem du [BotFather](https://telegram.me/BotFather) verwendest.
4. Installation des Google Cloud SDK.

## Einrichtung

### 1. Klone das Repository

```bash
git clone https://github.com/Jujinko/paul_the_homebot
cd google-calendar-management-bot
```

### 2. Virtuelle Umgebung erstellen und aktivieren

Erstelle eine virtuelle Umgebung, um Abhängigkeiten isoliert zu installieren:

Für Linux und macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Für Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Google Cloud SDK installieren

Folge den Anweisungen zur Installation des Google Cloud SDK:

- [Installationsanweisungen für Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

Für Linux und macOS:

```bash
./google-cloud-sdk/install.sh
```

Für Windows:

```bat
google-cloud-sdk\install.bat
```

### 4. Ein Google Cloud Projekt erstellen und konfigurieren

#### Erstelle ein neues Google Cloud Projekt

1. Gehe zur [Google Cloud Console](https://console.cloud.google.com/).
2. Klicke auf das Projekt-Dropdown-Menü oben in der Konsole und wähle "Neues Projekt".
3. Gib einen Projektnamen ein und klicke auf "Erstellen".

#### Aktiviere die notwendigen Dienste

Aktiviere die Google Calendar API und Vertex AI:

1. Gehe zur [API-Bibliothek](https://console.cloud.google.com/apis/library).
2. Suche nach "Google Calendar API" und klicke auf "Aktivieren".
3. Suche nach "Vertex AI API" und klicke auf "Aktivieren".

#### OAuth 2.0-Zugang einrichten und Credentials herunterladen

1. Gehe zu den [Anmeldedaten](https://console.cloud.google.com/apis/credentials).
2. Klicke auf "Anmeldedaten erstellen" und wähle "OAuth 2.0-Client-ID".
3. Wähle "Webanwendung" als Anwendungstyp.
4. Füge unter "Autorisierte Weiterleitungs-URIs" `http://localhost:8080` hinzu. (Falls ein anderer Port festgelegt wird, muss dieser in google_calendar/api.py angepasst werden)
5. Lade die `credentials.json` Datei herunter und speichere sie im Verzeichnis des Projekts.

### 5. Erstelle eine `config.json` Datei

Erstelle eine Datei namens `config.json` im selben Verzeichnis wie dein Skript und füge die folgenden Inhalte hinzu:

```json
{
  "project_id": "DEIN_PROJECT_ID_HIER",
  "location": "europe-west3",
  "calendar_id": "DEIN_KALENDER_ID_HIER@group.calendar.google.com",
  "telegram_token": "DEIN_TELEGRAM_BOT_TOKEN_HIER"
}
```

Ersetze die Platzhalterwerte durch deine spezifischen Werte. Die `calendar_id` kann nach dem ersten Start des Skripts durch Auslesen der ausgegebenen Kalender-IDs in die Konfigurationsdatei aktualisiert werden.

### 6. Installiere die Abhängigkeiten

Verwende `pip`, um die notwendigen Abhängigkeiten zu installieren:

```bash
pip install -r requirements.txt
```

### 7. Authentifiziere den Benutzer und erhalte Kalender-IDs

Führe das Skript aus, um die Authentifizierung abzuschließen und ein Token zu generieren, das in `token.json` gespeichert wird:

```bash
python main.py
```

Folge den Anweisungen im Browser, um die Authentifizierung abzuschließen. Beim ersten Ausführen des Skripts werden die Kalender-IDs ausgegeben. Notiere dir die gewünschte Kalender-ID und aktualisiere die `config.json` Datei entsprechend:

```json
{
  "project_id": "DEIN_PROJECT_ID_HIER",
  "location": "europe-west3",
  "calendar_id": "NOTIERTE_KALENDER_ID@group.calendar.google.com",
  "telegram_token": "DEIN_TELEGRAM_BOT_TOKEN_HIER"
}
```

## Nutzung

Nachdem die Einrichtung abgeschlossen ist, kannst du den Bot starten, indem du das Skript ausführst:

```bash
python main.py
```

Der Bot wird auf Telegram-Nachrichten reagieren, die mit `/paul` beginnen. Du kannst dem Bot Anweisungen geben, um Ereignisse in deinem Google Kalender zu verwalten.

### Beispielbefehle

- `/paul Füge ein Ereignis hinzu`
- `/paul Zeige meine Ereignisse für heute`
- `/paul Lösche das Ereignis mit ID xyz`

## Lizenz

Dieses Projekt ist unter der GNU-Lizenz (Version 3, 29 June 2007) lizenziert. Weitere Informationen findest du in der [LICENSE](LICENSE.html)-Datei.
