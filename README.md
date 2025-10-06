# 🎙️ Voice Agent mit LangGraph

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-ReAct_Agent-orange.svg)
![ElevenLabs](https://img.shields.io/badge/ElevenLabs-Flash_v2.5-purple.svg)

Produktionsreifer Voice Agent mit deutscher Sprachunterstützung, lokaler Spracherkennung, Cloud-basiertem LLM mit Tool-Support und hochwertiger Text-to-Speech-Synthese.

## ✨ Features

- **🎤 Lokale Spracherkennung**: faster-whisper für datenschutzfreundliches STT (~300ms)
- **🧠 Intelligenter Agent**: LangGraph ReAct Agent mit Groq LLM (Llama 4 Maverick)
- **🔊 Premium TTS**: ElevenLabs Flash v2.5 für natürliche Sprachsynthese (~75ms)
- **🛠️ Tool-Unterstützung**: Web-Suche, Wikipedia, Rechner, Zeit, Website-Abruf
- **💬 Telegram-Integration**: Volle Sprachnachrichten-Unterstützung für mobiles Testen
- **🔄 Konversationsspeicher**: Zustandsbehaftete Gespräche mit LangGraph
- **🌍 Deutsche Sprache**: Native deutsche Unterstützung mit natürlichem Gesprächsstil

## 🏗️ Architektur

```
🎤 Audio-Eingabe
   ↓
🗣️  STT: faster-whisper (lokal, ~300ms)
   ↓
🧠 LLM: Groq Llama 4 + LangGraph ReAct (cloud, ~50ms)
   ├─ 🔍 Web-Suche (DuckDuckGo)
   ├─ 📚 Wikipedia
   ├─ 🌐 Website-Abruf
   ├─ 🧮 Rechner
   └─ 📅 Aktuelle Zeit
   ↓
🔊 TTS: ElevenLabs Flash v2.5 (cloud, ~75ms)
   ↓
🔈 Audio-Ausgabe

Gesamtlatenz: ~425ms
```

## 🚀 Schnellstart

### Voraussetzungen

- Python 3.9+
- API-Keys:
  - [Groq API Key](https://console.groq.com) (Free Tier verfügbar)
  - [ElevenLabs API Key](https://elevenlabs.io) (Free Tier: 10k Zeichen/Monat)
  - [Telegram Bot Token](https://t.me/BotFather) (Optional, für Telegram-Integration)

### Installation

```bash
# Repository klonen
git clone https://github.com/dinelk/voice-agent.git
cd voice-agent

# Setup-Skript ausführen
chmod +x setup.sh
./setup.sh

# Oder manuelle Installation:
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Konfiguration

```bash
# Environment-Vorlage kopieren
cp .env.example .env

# .env bearbeiten und API-Keys hinzufügen
nano .env
```

Erforderliche Umgebungsvariablen:
```env
GROQ_API_KEY=dein_groq_api_key
ELEVENLABS_API_KEY=dein_elevenlabs_api_key
TELEGRAM_BOT_TOKEN=dein_telegram_token  # Optional
```

### Verwendung

#### Kommandozeile

```python
from voice_agent import VoiceAgent

# Agent initialisieren
agent = VoiceAgent(
    whisper_model="small",
    groq_model="meta-llama/llama-4-maverick-17b-128e-instruct",
    language="de"
)

# Text-Chat
response = agent.chat("Was ist Python?")
print(response)

# Sprachverarbeitung
result = agent.process(
    audio_path="input.wav",
    stream_audio=False
)
print(f"Transkription: {result['transcription']}")
print(f"Antwort: {result['response']}")
```

#### Telegram Bot

```bash
# Telegram Bot starten
python telegram_bot.py
```

Dann einfach Sprachnachrichten oder Text an den Bot senden!

## 🛠️ Tools & Fähigkeiten

Der Agent verfügt über folgende integrierte Tools:

- **🔍 Web-Suche**: Echtzeit-Websuche mit DuckDuckGo
- **📚 Wikipedia**: Zugriff auf Wikipedia-Wissensdatenbank
- **🌐 Website-Abruf**: Inhalte von jeder URL extrahieren
- **🧮 Rechner**: Mathematische Ausdrücke und Berechnungen
- **📅 Aktuelle Zeit**: Datum und Uhrzeit in jeder Zeitzone

## 📊 Performance

### Latenz-Aufschlüsselung

| Komponente | Latenz | Modell |
|-----------|---------|-------|
| STT | ~300ms | faster-whisper small |
| LLM | ~50ms | Groq Llama 4 Maverick |
| TTS | ~75ms | ElevenLabs Flash v2.5 |
| **Gesamt** | **~425ms** | ✅ Echtzeitfähig |

### Kostenschätzung

Monatliche Kosten für 1000 Interaktionen (~30s Audio, ~100 Wörter Antwort):

- STT: **0€** (lokal)
- LLM: **0€** (Groq Free Tier)
- TTS: **~22€** (ElevenLabs)
- **Gesamt: ~22€/Monat**

Vergleich zu vollständig Cloud-basiert: ~58-78€/Monat
**Einsparung: 62-72%**

## 🔧 Konfiguration

### Whisper-Modell-Auswahl

```python
agent = VoiceAgent(
    whisper_model="small",  # Optionen: tiny, small, medium, large
)
```

Modell-Vergleich:
- `tiny`: Am schnellsten, geringere Genauigkeit
- `small`: **Empfohlen** - Gute Balance
- `medium`: Höhere Genauigkeit, langsamer
- `large`: Beste Genauigkeit, am langsamsten

### LLM-Modell-Auswahl

```python
agent = VoiceAgent(
    groq_model="meta-llama/llama-4-maverick-17b-128e-instruct",
)
```

Verfügbare Modelle:
- `meta-llama/llama-4-maverick-17b-128e-instruct`: **Empfohlen** - Beste Tool-Nutzung
- `llama-3.1-8b-instant`: Schneller, gute allgemeine Performance
- `llama-3.3-70b-versatile`: Höchste Qualität, langsamer

### Stimmen-Auswahl

```python
result = agent.process(
    audio_path="input.wav",
    voice_id="z1EhmmPwF0ENGYE8dBE6",  # ElevenLabs Voice ID
)
```

Voice IDs findest du in der [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)

## 📱 Telegram Bot

Der enthaltene Telegram Bot bietet:

- ✅ Sprachnachrichten-Transkription und -Antwort
- ✅ Text-Nachrichten-Unterstützung
- ✅ Benutzerspezifische Gesprächshistorie
- ✅ Generierung von Sprachantworten

**Befehle:**
- `/start` - Willkommensnachricht
- `/help` - Hilfeinformationen
- `/reset` - Gesprächshistorie zurücksetzen

## 🧪 Testen

```bash
# Agent testen
python voice_agent.py

# Telegram Bot testen (benötigt Bot-Token)
python telegram_bot.py
```

## 🔒 Datenschutz & Sicherheit

- **STT**: 100% lokale Verarbeitung (faster-whisper)
- **LLM**: Cloud-basiert (Groq) - Daten werden an API gesendet
- **TTS**: Cloud-basiert (ElevenLabs) - Text wird an API gesendet

Für vollständigen Datenschutz können lokale LLM-Alternativen (z.B. Ollama) verwendet werden.

## 📚 Dokumentation

### API-Dokumentation

**VoiceAgent Klasse:**

```python
class VoiceAgent:
    def __init__(
        self,
        groq_api_key: Optional[str] = None,
        elevenlabs_api_key: Optional[str] = None,
        whisper_model: str = "small",
        groq_model: str = "meta-llama/llama-4-maverick-17b-128e-instruct",
        language: str = "de",
        max_history: int = 10
    )

    def chat(self, message: str) -> str:
        """Nur-Text-Chat ohne Audio"""

    def process(
        self,
        audio_path: str,
        voice_id: str = "z1EhmmPwF0ENGYE8dBE6",
        stream_audio: bool = False
    ) -> Dict[str, Any]:
        """Vollständige Pipeline: Audio → Text → Agent → Sprache"""

    def reset_history(self):
        """Gesprächshistorie löschen"""
```

### Tools API

Eigene Tools hinzufügen durch Erstellen von LangChain Tools:

```python
from langchain_core.tools import tool

@tool
def mein_custom_tool(query: str) -> str:
    """Tool-Beschreibung für den Agent"""
    # Deine Implementierung
    return result

# Zu tools.py TOOLS-Liste hinzufügen
```

## 🤝 Beitragen

Beiträge sind willkommen! Bitte siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

## 🙏 Danksagungen

- [ElevenLabs](https://elevenlabs.io) für Premium-TTS
- [Groq](https://groq.com) für schnelle LLM-Inferenz
- [LangChain](https://www.langchain.com) & [LangGraph](https://www.langchain.com/langgraph) für Agent-Framework
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) für effizientes STT

## 🔗 Links

- **Repository**: [GitHub](https://github.com/dinelk/voice-agent)
- **Issues**: [Bug-Reports & Feature-Requests](https://github.com/dinelk/voice-agent/issues)
- **Diskussionen**: [Community-Forum](https://github.com/dinelk/voice-agent/discussions)

## 📧 Kontakt

- **Autor**: Dinel Kurtovic
- **Email**: info@dinel.at
- **GitHub**: [@dinelk](https://github.com/dinelk)

---

**Mit ❤️ für die AI-Community entwickelt**
