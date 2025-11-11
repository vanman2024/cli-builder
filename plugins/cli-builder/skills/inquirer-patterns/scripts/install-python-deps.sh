#!/bin/bash

# install-python-deps.sh
# Install Python dependencies for questionary patterns

set -e

echo "📦 Installing Python dependencies for questionary patterns..."
echo

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed"
    echo "Please install Python 3.7 or higher first"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 7 ]); then
    echo "⚠️  Warning: Python 3.7 or higher is recommended"
    echo "Current version: $(python3 --version)"
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    echo "Please install pip3 first"
    exit 1
fi

# Upgrade pip
echo "🔄 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install core dependencies
echo "📥 Installing questionary..."
pip3 install "questionary>=2.0.0"

echo "📥 Installing prompt_toolkit..."
pip3 install "prompt_toolkit>=3.0.0"

# Optional: Install colorama for colored output on Windows
echo "📥 Installing colorama (optional, for Windows support)..."
pip3 install colorama

echo
echo "✅ All Python dependencies installed successfully!"
echo
echo "📚 Installed packages:"
echo "  - questionary>=2.0.0"
echo "  - prompt_toolkit>=3.0.0"
echo "  - colorama"
echo
echo "🚀 You can now run the examples:"
echo "  python3 templates/python/text_prompt.py"
echo "  python3 templates/python/list_prompt.py"
echo "  python3 templates/python/checkbox_prompt.py"
echo "  python3 templates/python/password_prompt.py"
echo "  python3 templates/python/autocomplete_prompt.py"
echo "  python3 templates/python/conditional_prompt.py"
echo
