#!/bin/bash
# Quick start script for Telegram Bot

echo "🚀 Starting Voice Agent Telegram Bot..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv venv"
    exit 1
fi

# Activate venv
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import telegram" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check API keys
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Copy .env.example to .env and add your API keys"
    exit 1
fi

# Run bot
echo "✅ Starting bot..."
python telegram_bot.py
