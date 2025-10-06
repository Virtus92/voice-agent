"""
Voice Agent with LangGraph & Tools
Supports: Web Search, Wikipedia, Website Fetching, Calculator, and more
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path

from faster_whisper import WhisperModel
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from elevenlabs.client import ElevenLabs
from tools import TOOLS


class VoiceAgent:
    """
    Voice Agent with LangGraph:
    - Local STT: faster-whisper
    - Cloud LLM: Groq with LangGraph ReAct agent
    - Cloud TTS: ElevenLabs Flash v2.5
    - Tools: Web Search, Wikipedia, Website Fetching, etc.
    - Memory: LangGraph state management
    """

    def __init__(
        self,
        groq_api_key: Optional[str] = None,
        elevenlabs_api_key: Optional[str] = None,
        whisper_model: str = "small",
        groq_model: str = "meta-llama/llama-4-maverick-17b-128e-instruct",
        language: str = "de",
        max_history: int = 10
    ):
        """
        Initialize Voice Agent with LangGraph

        Args:
            groq_api_key: Groq API key
            elevenlabs_api_key: ElevenLabs API key
            whisper_model: Whisper model size
            groq_model: Groq model name
            language: Language code
            max_history: Max conversation history entries
        """
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.elevenlabs_api_key = elevenlabs_api_key or os.getenv("ELEVENLABS_API_KEY")

        self.language = language
        self.groq_model = groq_model
        self.max_history = max_history

        self.conversation_state = {"messages": []}

        print("🔄 Initializing Voice Agent with LangGraph...")

        print(f"📥 Loading Whisper model: {whisper_model}")
        self.whisper = WhisperModel(
            whisper_model,
            device="cpu",
            compute_type="int8"
        )

        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not set!")

        print(f"🧠 Initializing ChatGroq: {groq_model}")
        self.llm = ChatGroq(
            api_key=self.groq_api_key,
            model=groq_model,
            temperature=0.7,
            max_tokens=1000
        )

        print("🤖 Creating LangGraph ReAct Agent with tools...")

        system_message = """Du bist ein freundlicher deutscher Sprachassistent. Du sprichst natürlich und direkt wie ein echter Gesprächspartner.

WICHTIG - Natürliche gesprochene Sprache:
- Antworte kurz, klar und direkt wie im echten Gespräch
- Keine formellen Listen, Aufzählungen oder Strukturen
- Sprich fließend und natürlich, als würdest du mit jemandem reden
- Fasse dich kurz - maximal 2-3 Sätze wenn möglich

Deine Tools:
- web_search: Für aktuelle Infos und lokale Suchen (Restaurants, Geschäfte, etc.)
- wikipedia_search: Für Fakten und Definitionen
- calculator: Für Berechnungen
- get_current_time: Für Datum und Zeit
- fetch_website: Nur wenn explizit eine URL gewünscht ist

Tool-Strategie:
- Für lokale Suchen (wie Restaurants): Nutze web_search und gib ALLE gefundenen Ergebnisse weiter
- Stoppe sobald du eine vollständige Antwort geben kannst
- Bei Fehlern (403, Timeout): Nicht erneut versuchen, einfach mit vorhandenen Infos antworten
- Keine unnötigen wiederholten Suchen

Antwort-Stil:
SCHLECHT: "Die drei bestbewertesten Pizzerien in Leonding sind: 1. Restaurant A, 2. Restaurant B..."
GUT: "Ich habe einige tolle Pizzerien in Leonding gefunden. Da wäre zum Beispiel La Ruffa, die haben gute Bewertungen. Dann gibt's noch die Pizzeria Toscana und das Ristorante Da Vinci. Willst du mehr Details zu einem der Restaurants?"

Sprich natürlich, freundlich und hilfsbereit auf Deutsch!"""

        self.agent = create_react_agent(
            self.llm,
            TOOLS,
            prompt=system_message
        )

        if not self.elevenlabs_api_key:
            raise ValueError("ELEVENLABS_API_KEY not set!")

        print("🔊 Initializing ElevenLabs Flash v2.5")
        self.eleven = ElevenLabs(api_key=self.elevenlabs_api_key)

        print("✅ Voice Agent with LangGraph ready!\n")

    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio using faster-whisper"""
        print(f"🗣️  Transcribing audio...")
        segments, info = self.whisper.transcribe(
            audio_path,
            language=self.language,
            beam_size=5
        )

        text = " ".join([segment.text for segment in segments])
        print(f"📝 Transcription: {text}")
        return text.strip()

    def generate_response_with_tools(self, user_message: str) -> str:
        """
        Generate LLM response with LangGraph ReAct agent

        Args:
            user_message: User's message

        Returns:
            Final response after tool execution
        """
        print(f"🧠 Generating response with LangGraph ReAct Agent...")

        self.conversation_state["messages"].append(HumanMessage(content=user_message))

        if len(self.conversation_state["messages"]) > self.max_history * 2:
            self.conversation_state["messages"] = self.conversation_state["messages"][-self.max_history * 2:]

        try:
            result = self.agent.invoke(self.conversation_state)

            agent_messages = result.get("messages", [])

            final_response = None
            for msg in reversed(agent_messages):
                if isinstance(msg, AIMessage) and msg.content:
                    final_response = msg.content
                    break

            if not final_response:
                final_response = "Entschuldigung, ich konnte keine Antwort generieren."

            self.conversation_state = result

            print(f"✅ Final Response: {final_response}")
            return final_response

        except Exception as e:
            print(f"❌ Error in agent: {e}")
            import traceback
            traceback.print_exc()
            return f"Entschuldigung, es gab einen Fehler: {str(e)}"

    def text_to_speech(self, text: str, voice_id: str = "z1EhmmPwF0ENGYE8dBE6") -> bytes:
        """Convert text to speech using ElevenLabs Flash v2.5"""
        print(f"🔊 Synthesizing speech (Flash v2.5)...")

        audio_generator = self.eleven.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_128"
        )

        audio_bytes = b"".join(audio_generator)
        return audio_bytes

    def text_to_speech_streaming(self, text: str, voice_id: str = "z1EhmmPwF0ENGYE8dBE6"):
        """Stream TTS for lower latency"""
        print(f"🔊 Streaming speech (Flash v2.5)...")

        audio_stream = self.eleven.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_128"
        )

        from elevenlabs import play
        play(audio_stream)

    def process(
        self,
        audio_path: str,
        voice_id: str = "z1EhmmPwF0ENGYE8dBE6",
        stream_audio: bool = False
    ) -> Dict[str, Any]:
        """
        Full pipeline: Audio → Text → LangGraph Agent → Speech

        Args:
            audio_path: Input audio file
            voice_id: ElevenLabs voice ID
            stream_audio: Stream TTS output

        Returns:
            Dict with transcription, response, and audio
        """
        transcription = self.transcribe(audio_path)

        response = self.generate_response_with_tools(transcription)

        if stream_audio:
            self.text_to_speech_streaming(response, voice_id)
            audio_bytes = None
        else:
            audio_bytes = self.text_to_speech(response, voice_id)

        return {
            "transcription": transcription,
            "response": response,
            "audio": audio_bytes
        }

    def chat(self, message: str) -> str:
        """
        Text-only chat (no audio)

        Args:
            message: User message

        Returns:
            Agent response
        """
        return self.generate_response_with_tools(message)

    def reset_history(self):
        """Clear conversation history"""
        self.conversation_state = {"messages": []}
        print("🔄 Conversation history cleared")


def main():
    """Example usage"""

    agent = VoiceAgent(
        whisper_model="small",
        groq_model="meta-llama/llama-4-maverick-17b-128e-instruct",
        language="de"
    )

    print("\n" + "="*50)
    print("Testing Voice Agent with LangGraph")
    print("="*50 + "\n")

    response = agent.chat("Suche aktuelle Nachrichten über künstliche Intelligenz")
    print(f"\n✅ Response: {response}\n")

    response = agent.chat("Was ist Python?")
    print(f"\n✅ Response: {response}\n")

    response = agent.chat("Was ist 123 * 456?")
    print(f"\n✅ Response: {response}\n")

    response = agent.chat("Wie spät ist es?")
    print(f"\n✅ Response: {response}\n")


if __name__ == "__main__":
    main()
