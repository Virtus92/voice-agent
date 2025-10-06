"""
Telegram Bot Interface for Voice Agent
Voice message support for easy mobile testing
"""

import os
import asyncio
from pathlib import Path
from typing import Optional
import tempfile

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from voice_agent import VoiceAgent
from dotenv import load_dotenv

load_dotenv()


class TelegramVoiceBot:
    """Telegram Bot wrapper for Voice Agent"""

    def __init__(
        self,
        telegram_token: str,
        whisper_model: str = "small",
        groq_model: str = "meta-llama/llama-4-maverick-17b-128e-instruct"
    ):
        """
        Initialize Telegram Bot

        Args:
            telegram_token: Telegram Bot Token
            whisper_model: Whisper model size
            groq_model: Groq model name
        """
        self.token = telegram_token

        print("🔄 Initializing Voice Agent for Telegram...")
        self.agent = VoiceAgent(
            whisper_model=whisper_model,
            groq_model=groq_model,
            language="de"
        )

        self.user_agents = {}

        print("✅ Telegram Bot ready!")

    def get_user_agent(self, user_id: int) -> VoiceAgent:
        """Get or create agent for user"""
        if user_id not in self.user_agents:
            self.user_agents[user_id] = VoiceAgent(
                whisper_model="small",
                groq_model="meta-llama/llama-4-maverick-17b-128e-instruct",
                language="de"
            )
        return self.user_agents[user_id]

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🎙️ **Voice Agent - Dein KI-Assistent**

Ich kann:
✅ Sprachnachrichten verstehen (einfach Voice Message senden!)
✅ Text-Nachrichten beantworten
✅ Im Web suchen 🔍
✅ Wikipedia konsultieren 📚
✅ Websites abrufen 🌐
✅ Rechnen 🧮
✅ Zeit & Datum abrufen 📅

**Befehle:**
/start - Diese Nachricht
/reset - Konversation zurücksetzen
/help - Hilfe

**Einfach losschreiben oder Voice Message senden! 🎤**
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 **Hilfe**

**Voice Messages:**
- Einfach Voice Message senden 🎤
- Ich transkribiere und antworte mit Voice!

**Text Messages:**
- Normale Fragen stellen
- Ich antworte mit Text

**Beispiel-Anfragen:**
• "Suche aktuelle Nachrichten über KI"
• "Was ist Python?" (Wikipedia)
• "Was ist 123 * 456?"
• "Wie spät ist es?"
• "Öffne https://example.com"

**Befehle:**
/reset - Konversation neu starten
/help - Diese Hilfe
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reset command"""
        user_id = update.effective_user.id
        agent = self.get_user_agent(user_id)
        agent.reset_history()
        await update.message.reply_text("🔄 Konversation zurückgesetzt!")

    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_id = update.effective_user.id
        message_text = update.message.text

        print(f"📝 Text from {user_id}: {message_text}")

        await update.message.chat.send_action("typing")

        try:
            agent = self.get_user_agent(user_id)
            response = agent.chat(message_text)
            await update.message.reply_text(response)

        except Exception as e:
            print(f"❌ Error: {e}")
            await update.message.reply_text(f"❌ Fehler: {str(e)}")

    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages"""
        user_id = update.effective_user.id

        print(f"🎤 Voice message from {user_id}")

        await update.message.chat.send_action("typing")

        try:
            voice_file = await update.message.voice.get_file()

            with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_audio:
                temp_path = temp_audio.name
                await voice_file.download_to_drive(temp_path)

            print(f"📥 Downloaded voice: {temp_path}")

            agent = self.get_user_agent(user_id)

            result = agent.process(
                audio_path=temp_path,
                stream_audio=False
            )

            await update.message.reply_text(
                f"🗣️ Du: {result['transcription']}\n\n💬 Ich: {result['response']}"
            )

            if result['audio']:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_response:
                    response_path = temp_response.name
                    temp_response.write(result['audio'])

                print(f"🔊 Sending voice response: {response_path}")

                with open(response_path, 'rb') as audio_file:
                    await update.message.reply_voice(voice=audio_file)

                os.remove(response_path)

            os.remove(temp_path)

        except Exception as e:
            print(f"❌ Error processing voice: {e}")
            import traceback
            traceback.print_exc()
            await update.message.reply_text(f"❌ Fehler bei Voice-Verarbeitung: {str(e)}")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        print(f"❌ Error: {context.error}")
        if update and update.message:
            await update.message.reply_text("❌ Ein Fehler ist aufgetreten. Bitte versuche es erneut.")

    def run(self):
        """Start the bot"""
        print(f"🚀 Starting Telegram Bot...")

        app = Application.builder().token(self.token).build()

        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("reset", self.reset_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
        app.add_handler(MessageHandler(filters.VOICE, self.handle_voice_message))

        app.add_error_handler(self.error_handler)

        print("✅ Bot is running! Press Ctrl+C to stop.")
        app.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Run Telegram Bot"""

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not set!")
        print("\n📝 Setup Instructions:")
        print("1. Talk to @BotFather on Telegram")
        print("2. Create new bot with /newbot")
        print("3. Copy token and add to .env:")
        print("   TELEGRAM_BOT_TOKEN=your_token_here")
        return

    bot = TelegramVoiceBot(
        telegram_token=token,
        whisper_model="small",
        groq_model="meta-llama/llama-4-maverick-17b-128e-instruct"
    )

    bot.run()


if __name__ == "__main__":
    main()
