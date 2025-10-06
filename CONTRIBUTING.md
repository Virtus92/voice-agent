# Beitragen zum Voice Agent Projekt

Vielen Dank für dein Interesse, zum Voice Agent beizutragen! Wir freuen uns über jede Art von Beitrag.

## 🚀 Wie kann ich beitragen?

### Bugs melden

Wenn du einen Bug findest:

1. Prüfe, ob der Bug bereits in den [Issues](https://github.com/dinelk/voice-agent/issues) gemeldet wurde
2. Wenn nicht, erstelle ein neues Issue mit:
   - Klarer Beschreibung des Problems
   - Schritten zur Reproduktion
   - Erwartetes vs. tatsächliches Verhalten
   - System-Informationen (OS, Python-Version, etc.)
   - Relevante Logs oder Screenshots

### Features vorschlagen

Hast du eine Idee für ein neues Feature?

1. Prüfe die [Issues](https://github.com/dinelk/voice-agent/issues) auf ähnliche Vorschläge
2. Erstelle ein Issue mit:
   - Klarer Beschreibung des Features
   - Anwendungsfall und Nutzen
   - Mögliche Implementierungsansätze (optional)

### Code beitragen

1. **Fork** das Repository
2. **Clone** deinen Fork:
   ```bash
   git clone https://github.com/dein-username/voice-agent.git
   cd voice-agent
   ```

3. **Branch** erstellen:
   ```bash
   git checkout -b feature/dein-feature-name
   ```

4. **Änderungen** vornehmen:
   - Folge dem bestehenden Code-Stil
   - Füge Docstrings hinzu
   - Teste deine Änderungen gründlich

5. **Commit** deine Änderungen:
   ```bash
   git add .
   git commit -m "feat: Kurze Beschreibung der Änderung"
   ```

6. **Push** zum Fork:
   ```bash
   git push origin feature/dein-feature-name
   ```

7. **Pull Request** erstellen:
   - Gehe zu deinem Fork auf GitHub
   - Klicke auf "New Pull Request"
   - Beschreibe deine Änderungen ausführlich
   - Verlinke relevante Issues

## 📋 Code-Richtlinien

### Python Style Guide

- Folge [PEP 8](https://pep8.org/)
- Verwende aussagekräftige Variablennamen
- Halte Funktionen klein und fokussiert
- Docstrings für alle öffentlichen Funktionen und Klassen

### Commit Messages

Verwende das [Conventional Commits](https://www.conventionalcommits.org/) Format:

- `feat:` Neues Feature
- `fix:` Bug-Fix
- `docs:` Dokumentationsänderungen
- `style:` Code-Formatierung (keine funktionalen Änderungen)
- `refactor:` Code-Refactoring
- `test:` Tests hinzufügen oder ändern
- `chore:` Wartungsarbeiten

Beispiele:
```
feat: Add support for English language
fix: Resolve audio playback issue on Windows
docs: Update installation instructions
```

### Dokumentation

- Aktualisiere die README.md bei neuen Features
- Füge Docstrings zu neuen Funktionen hinzu
- Kommentiere komplexe Logik
- Aktualisiere die API-Dokumentation bei Bedarf

### Testing

- Teste deine Änderungen lokal
- Stelle sicher, dass bestehende Tests weiterhin laufen
- Füge Tests für neue Features hinzu (wenn möglich)

## 🛠️ Entwicklungsumgebung einrichten

```bash
# Repository klonen
git clone https://github.com/dinelk/voice-agent.git
cd voice-agent

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# API Keys konfigurieren
cp .env.example .env
# .env mit deinen Keys bearbeiten

# Agent testen
python voice_agent.py
```

## 🤝 Verhaltenskodex

- Sei respektvoll und konstruktiv
- Begrüße neue Contributors
- Hilf anderen bei Fragen
- Halte Diskussionen professionell und sachlich

## 📞 Fragen?

Bei Fragen kannst du:

- Ein Issue erstellen
- Eine Diskussion starten
- Eine E-Mail an info@dinel.at senden

## 🎉 Danke!

Jeder Beitrag, egal wie klein, ist wertvoll und wird geschätzt. Danke, dass du das Projekt unterstützt!
