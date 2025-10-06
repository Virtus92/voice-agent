#!/bin/bash
# Setup script for Voice Agent

echo "🚀 Setting up Voice Agent..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📍 Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
fi

# Optional: Install Ollama for local LLM
read -p "🤔 Install Ollama for local LLM? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh

    echo "📥 Pulling Llama 3.1 8B model..."
    ollama pull llama3.1:8b-instruct-q4_K_M
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Edit .env and add your API keys"
echo "   2. Activate venv: source venv/bin/activate"
echo "   3. Run: python voice_agent.py"
echo ""
