#!/bin/bash

# Post-create script for EIA Daily Dashboard devcontainer
# This script sets up the Python virtual environment and installs dependencies

set -e

echo "🔧 Setting up EIA Daily Dashboard development environment..."

# Create virtual environment in .venv if it doesn't exist
if [ ! -d .venv ]; then
    echo "📦 Creating virtual environment in .venv..."
    python -m venv .venv
else
    echo "📦 Virtual environment .venv already exists, skipping creation..."
fi

# Activate virtual environment for this script only; VS Code/devcontainer
# configuration (python.defaultInterpreterPath / VIRTUAL_ENV) handles
# terminal activation for interactive sessions.
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements from requirements.txt..."
pip install -r requirements.txt

# Create .env from example if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Remember to add your EIA API key to .env file!"
fi

echo "✅ Development environment setup complete!"
echo ""
echo "🚀 To run the dashboard:"
echo "   streamlit run app.py"
echo ""
echo "🔑 Don't forget to add your EIA API key to .env:"
echo "   EIA_API_KEY=your_api_key_here"
