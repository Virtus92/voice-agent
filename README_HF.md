---
title: Voice Agent mit LangGraph
emoji: 🎙️
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
tags:
  - voice
  - speech
  - llm
  - langgraph
  - groq
  - elevenlabs
  - whisper
  - german
  - telegram
---

# 🎙️ Voice Agent mit LangGraph

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

### Installation

```bash
git clone https://huggingface.co/spaces/Virtus92/voice-agent
cd voice-agent
pip install -r requirements.txt
```

### Konfiguration

```bash
cp .env.example .env
# Füge deine API-Keys hinzu
```

Erforderliche API-Keys:
- [Groq API Key](https://console.groq.com) - Free Tier verfügbar
- [ElevenLabs API Key](https://elevenlabs.io) - Free Tier: 10k Zeichen/Monat
- [Telegram Bot Token](https://t.me/BotFather) - Optional

### Verwendung

```python
from voice_agent import VoiceAgent

agent = VoiceAgent(
    whisper_model="small",
    groq_model="meta-llama/llama-4-maverick-17b-128e-instruct",
    language="de"
)

# Text-Chat
response = agent.chat("Was ist Python?")
print(response)

# Sprachverarbeitung
result = agent.process(audio_path="input.wav")
print(f"Transkription: {result['transcription']}")
print(f"Antwort: {result['response']}")
```

## 📊 Performance

| Komponente | Latenz | Modell |
|-----------|---------|-------|
| STT | ~300ms | faster-whisper small |
| LLM | ~50ms | Groq Llama 4 Maverick |
| TTS | ~75ms | ElevenLabs Flash v2.5 |
| **Gesamt** | **~425ms** | ✅ Echtzeitfähig |

## 🛠️ Tools

Der Agent verfügt über folgende integrierte Tools:

- 🔍 Web-Suche (DuckDuckGo)
- 📚 Wikipedia
- 🌐 Website-Abruf
- 🧮 Rechner
- 📅 Aktuelle Zeit

## 📱 Telegram Bot

```bash
python telegram_bot.py
```

Befehle:
- `/start` - Willkommensnachricht
- `/help` - Hilfeinformationen
- `/reset` - Gesprächshistorie zurücksetzen

## 🔗 Links

- **GitHub**: [Virtus92/voice-agent](https://github.com/Virtus92/voice-agent)
- **Dokumentation**: Vollständige Anleitung im Repository
- **Issues**: Bug-Reports & Feature-Requests

## 📧 Kontakt

- **Autor**: Dinel Kurtovic
- **Email**: info@dinel.at
- **GitHub**: [@Virtus92](https://github.com/Virtus92)

## 📝 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details

---

**Mit ❤️ für die AI-Community entwickelt**
