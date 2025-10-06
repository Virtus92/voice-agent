#!/bin/bash
# Install all dependencies

echo "📦 Installing Voice Agent Dependencies..."

# Activate venv
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Run bot: ./run_bot.sh"
