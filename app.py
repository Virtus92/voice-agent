"""
Gradio Web-UI für Voice Agent
Push-to-Talk wie ChatGPT Voice Mode
"""

import gradio as gr
import tempfile
import os
import numpy as np
import soundfile as sf
import scipy.signal as signal
from voice_agent import VoiceAgent

# Globaler Agent
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
    """Noise Reduction für laute Umgebungen"""
    # High-pass filter (100 Hz cutoff)
    sos = signal.butter(10, 100, 'hp', fs=sample_rate, output='sos')
    filtered = signal.sosfilt(sos, audio_data)

    # Normalisierung
    if np.abs(filtered).max() > 0:
        filtered = filtered / np.abs(filtered).max()

    return filtered


def voice_chat(audio):
    """
    AUTOMATISCH getriggert wenn Recording stoppt
    Audio → Transkription → Agent → Antwort
    """
    if audio is None:
        return None, "🎤 Bereit - drücke Record und sprich!", None

    try:
        agent = initialize_agent()

        sample_rate, audio_data = audio

        # Konvertiere zu Float32 wenn nötig
        if audio_data.dtype == np.int16:
            audio_data = audio_data.astype(np.float32) / 32768.0
        elif audio_data.dtype == np.int32:
            audio_data = audio_data.astype(np.float32) / 2147483648.0

        # Noise Reduction
        print("🔇 Reduziere Hintergrundgeräusche...")
        audio_data = reduce_noise(audio_data, sample_rate)

        # Speichere temporär
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
            temp_path = f.name
            sf.write(temp_path, audio_data, sample_rate)

        print(f"🗣️ Verarbeite Sprache...")

        # Verarbeiten
        result = agent.process(audio_path=temp_path, stream_audio=False)

        os.unlink(temp_path)

        # Audio-Antwort speichern
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            response_path = f.name
            f.write(result['audio'])

        transcription_text = f"**🗣️ Du:** {result['transcription']}"
        response_text = f"**🤖 Agent:** {result['response']}"

        print(f"✅ Fertig!")

        return response_path, transcription_text, response_text

    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return None, f"❌ Fehler bei Aufnahme", f"Details: {str(e)}"


def reset():
    """Reset Konversation"""
    global agent
    if agent:
        agent.reset_history()
    return None, "🔄 Neue Konversation gestartet", ""


# Custom CSS
custom_css = """
#audio-input {
    border: 3px dashed #6366f1;
    border-radius: 16px;
    padding: 24px;
    background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
}

#status-text {
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    padding: 16px;
    border-radius: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin: 16px 0;
}

.transcription-box {
    background: #1e293b;
    border-left: 4px solid #3b82f6;
    padding: 16px;
    margin: 12px 0;
    border-radius: 8px;
    color: #f0f9ff !important;
}

.response-box {
    background: #1e293b;
    border-left: 4px solid #22c55e;
    padding: 16px;
    margin: 12px 0;
    border-radius: 8px;
    color: #f0fdf4 !important;
}
"""

# Gradio Interface
with gr.Blocks(css=custom_css, title="🎙️ Voice Agent", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🎙️ Voice Agent - Push-to-Talk wie ChatGPT

    ### 🚀 So einfach wie ChatGPT Voice Mode!

    **Anleitung:**
    1. 🔴 Drücke **"Record"**
    2. 🗣️ **Sprich** deine Frage
    3. ⏹️ Drücke **"Stop"**
    4. ⚡ Agent verarbeitet **automatisch** und antwortet!

    **Keine Extra-Buttons nötig** - genau wie bei ChatGPT!
    """)

    # Status Anzeige
    status = gr.Markdown(
        "### 🎤 Bereit - drücke Record und sprich!",
        elem_id="status-text"
    )

    with gr.Row():
        with gr.Column(scale=1):
            # HAUPTELEMENT: Audio Input
            audio_input = gr.Audio(
                label="🎙️ Push-to-Talk: Record → Sprechen → Stop",
                type="numpy",
                sources=["microphone"],
                elem_id="audio-input",
                streaming=False,
                show_label=True,
                format="wav"
            )

            gr.Markdown("""
            **💡 Funktioniert auch bei Lärm!**
            Einfach deutlich sprechen - Rauschunterdrückung läuft automatisch.
            """)

        with gr.Column(scale=1):
            # Transkription
            transcription = gr.Markdown(
                "",
                elem_classes=["transcription-box"]
            )

            # Agent Antwort
            response = gr.Markdown(
                "",
                elem_classes=["response-box"]
            )

    # Audio Output (Auto-Play)
    audio_output = gr.Audio(
        label="🔊 Agent Antwort (spielt automatisch ab)",
        type="filepath",
        autoplay=True,
        visible=True
    )

    # Reset Button
    with gr.Row():
        reset_btn = gr.Button(
            "🔄 Neue Konversation starten",
            variant="secondary",
            size="lg"
        )

    # EVENT: Automatisch triggern wenn Recording stoppt
    audio_input.stop_recording(
        fn=voice_chat,
        inputs=[audio_input],
        outputs=[audio_output, transcription, response]
    )

    # Reset Event
    reset_btn.click(
        fn=reset,
        inputs=[],
        outputs=[audio_output, transcription, response]
    )

    # Beispiele
    gr.Markdown("""
    ---

    ## 💡 Beispiel-Fragen:

    - **"Was ist künstliche Intelligenz?"** - Wikipedia-Suche
    - **"Suche aktuelle Nachrichten über KI"** - Web-Suche
    - **"Wie spät ist es?"** - Aktuelle Uhrzeit
    - **"Was ist 15 mal 23?"** - Rechner
    - **"Finde Restaurants in Leonding"** - Lokale Suche

    ---

    ## 🛠️ Features:

    ✅ **Lokale Spracherkennung** (faster-whisper) - Datenschutz!
    ✅ **Intelligentes LLM** (Groq Llama 4 Maverick) - Schnell & Smart!
    ✅ **Premium Stimme** (ElevenLabs Flash v2.5) - Natürlich!
    ✅ **Rauschunterdrückung** (Scipy) - Funktioniert überall!
    ✅ **Web-Tools** - Suche, Wikipedia, Rechner, Zeit

    ---

    **Entwickelt von Dinel Kurtovic** | [GitHub](https://github.com/Virtus92/voice-agent) | info@dinel.at

    Mit ❤️ für die AI-Community
    """)


if __name__ == "__main__":
    print("🚀 Starte Voice Agent Push-to-Talk UI...")
    initialize_agent()

    demo.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860
    )
