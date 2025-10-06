"""
Gradio Web-UI für Voice Agent
Echtzeit-Sprachinteraktion mit Noise-Handling
"""

import gradio as gr
import tempfile
import os
from pathlib import Path
import numpy as np
import soundfile as sf
from voice_agent import VoiceAgent

# Agent initialisieren (wird beim Start geladen)
agent = None

def initialize_agent():
    """Initialisiere Agent beim ersten Start"""
    global agent
    if agent is None:
        print("🔄 Initialisiere Voice Agent...")
        agent = VoiceAgent(
            whisper_model="small",
            groq_model="meta-llama/llama-4-maverick-17b-128e-instruct",
            language="de"
        )
        print("✅ Voice Agent bereit!")
    return agent


def reduce_noise(audio_data, sample_rate):
    """
    Einfache Noise Reduction für laute Umgebungen
    Verwendet High-Pass Filter und Normalisierung
    """
    import scipy.signal as signal

    # High-pass filter um Rauschen zu reduzieren
    sos = signal.butter(10, 100, 'hp', fs=sample_rate, output='sos')
    filtered = signal.sosfilt(sos, audio_data)

    # Normalisierung
    if np.abs(filtered).max() > 0:
        filtered = filtered / np.abs(filtered).max()

    return filtered


def process_audio(audio_input, chat_history):
    """
    Verarbeite Audio-Eingabe und generiere Antwort

    Args:
        audio_input: Tuple (sample_rate, audio_data) von Gradio
        chat_history: Bisherige Konversationshistorie

    Returns:
        Tuple (chat_history, audio_output)
    """
    if audio_input is None:
        return chat_history, None

    try:
        # Agent initialisieren
        agent = initialize_agent()

        # Audio extrahieren
        sample_rate, audio_data = audio_input

        # Noise Reduction für laute Umgebungen
        print("🔇 Reduziere Hintergrundgeräusche...")
        audio_data = reduce_noise(audio_data, sample_rate)

        # Temporäre Datei für Audio erstellen
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            temp_path = temp_audio.name
            sf.write(temp_path, audio_data, sample_rate)

        print(f"📥 Verarbeite Audio: {temp_path}")

        # Audio verarbeiten
        result = agent.process(
            audio_path=temp_path,
            stream_audio=False
        )

        # Temporäre Eingabe-Datei löschen
        os.unlink(temp_path)

        # Chat-Historie aktualisieren
        user_message = result['transcription']
        bot_message = result['response']

        if chat_history is None:
            chat_history = []

        chat_history.append((user_message, bot_message))

        # Audio-Antwort als temporäre Datei speichern
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_response:
            response_path = temp_response.name
            temp_response.write(result['audio'])

        print(f"✅ Antwort generiert: {response_path}")

        return chat_history, response_path

    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()

        error_msg = f"Fehler bei der Verarbeitung: {str(e)}"
        if chat_history is None:
            chat_history = []
        chat_history.append(("Fehler", error_msg))

        return chat_history, None


def text_chat(message, chat_history):
    """
    Verarbeite Text-Eingabe (ohne Audio)

    Args:
        message: Text-Nachricht
        chat_history: Bisherige Konversationshistorie

    Returns:
        Updated chat_history
    """
    if not message:
        return chat_history

    try:
        # Agent initialisieren
        agent = initialize_agent()

        # Antwort generieren
        response = agent.chat(message)

        # Chat-Historie aktualisieren
        if chat_history is None:
            chat_history = []

        chat_history.append((message, response))

        return chat_history

    except Exception as e:
        print(f"❌ Fehler: {e}")
        error_msg = f"Fehler: {str(e)}"
        if chat_history is None:
            chat_history = []
        chat_history.append((message, error_msg))
        return chat_history


def reset_conversation():
    """Setze Konversation zurück"""
    global agent
    if agent:
        agent.reset_history()
    return [], None


# Gradio Interface
with gr.Blocks(title="🎙️ Voice Agent - Deutscher Sprachassistent", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🎙️ Voice Agent - Deutscher Sprachassistent

    Sprechen Sie mit dem KI-Assistenten! Der Agent nutzt:
    - 🗣️ Lokale Spracherkennung (faster-whisper)
    - 🧠 Intelligentes LLM (Groq Llama 4 Maverick mit Tools)
    - 🔊 Natürliche Sprachsynthese (ElevenLabs Flash v2.5)
    - 🔇 Automatische Rauschunterdrückung für laute Umgebungen

    **Funktionen:** Web-Suche, Wikipedia, Rechner, Uhrzeit, Website-Abruf
    """)

    with gr.Row():
        with gr.Column(scale=2):
            # Chat-Anzeige
            chatbot = gr.Chatbot(
                label="Konversation",
                height=400,
                show_label=True
            )

            # Audio-Ausgabe
            audio_output = gr.Audio(
                label="🔊 Agent Antwort (Audio)",
                type="filepath",
                autoplay=True
            )

        with gr.Column(scale=1):
            # Tabs für Sprache und Text
            with gr.Tab("🎤 Spracheingabe"):
                gr.Markdown("""
                ### Anleitung:
                1. Klicke auf das Mikrofon
                2. Sprich deine Frage
                3. Warte auf Transkription und Antwort

                **Tipp:** Funktioniert auch in lauter Umgebung dank Rauschunterdrückung!
                """)

                audio_input = gr.Audio(
                    label="🎤 Sprich mit dem Agent",
                    type="numpy",
                    sources=["microphone"]
                )

                submit_audio_btn = gr.Button("📤 Audio senden", variant="primary", size="lg")

            with gr.Tab("💬 Texteingabe"):
                gr.Markdown("""
                ### Text-Chat
                Schreibe deine Frage als Text.
                """)

                text_input = gr.Textbox(
                    label="✍️ Deine Nachricht",
                    placeholder="Was möchtest du wissen?",
                    lines=3
                )

                submit_text_btn = gr.Button("📤 Text senden", variant="primary", size="lg")

            # Reset Button
            reset_btn = gr.Button("🔄 Konversation zurücksetzen", variant="secondary")

    # Event Handler
    submit_audio_btn.click(
        fn=process_audio,
        inputs=[audio_input, chatbot],
        outputs=[chatbot, audio_output]
    )

    submit_text_btn.click(
        fn=text_chat,
        inputs=[text_input, chatbot],
        outputs=[chatbot]
    ).then(
        fn=lambda: "",
        outputs=[text_input]
    )

    text_input.submit(
        fn=text_chat,
        inputs=[text_input, chatbot],
        outputs=[chatbot]
    ).then(
        fn=lambda: "",
        outputs=[text_input]
    )

    reset_btn.click(
        fn=reset_conversation,
        inputs=[],
        outputs=[chatbot, audio_output]
    )

    # Beispiele
    gr.Markdown("""
    ## 💡 Beispiel-Fragen:

    - "Was ist künstliche Intelligenz?"
    - "Suche aktuelle Nachrichten über Technologie"
    - "Wie spät ist es?"
    - "Was ist 123 mal 456?"
    - "Finde die besten Restaurants in Leonding"
    """)

    # Footer
    gr.Markdown("""
    ---
    **Entwickelt von Dinel Kurtovic** | [GitHub](https://github.com/Virtus92/voice-agent) | info@dinel.at

    Mit ❤️ für die AI-Community
    """)


if __name__ == "__main__":
    # Agent beim Start initialisieren (optional, für schnellere erste Anfrage)
    print("🚀 Starte Voice Agent Web-UI...")
    initialize_agent()

    # Demo starten
    demo.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860
    )
