#!/bin/bash
# Quick test script for ┴ROOF Radio setup

echo "Testing ┴ROOF Radio setup..."
echo ""

# Check Python
echo "1. Checking Python..."
python3 --version || { echo "Error: Python3 not found"; exit 1; }

# Check Ollama
echo ""
echo "2. Checking Ollama..."
ollama list || { echo "Error: Ollama not running. Start with: ollama serve"; exit 1; }

# Check for required models
echo ""
echo "3. Checking for required models..."
if ollama list | grep -q "deepseek-r1:14b"; then
    echo "   ✓ deepseek-r1:14b found"
else
    echo "   ✗ deepseek-r1:14b missing - run: ollama pull deepseek-r1:14b"
fi

if ollama list | grep -q "llama3.1:8b"; then
    echo "   ✓ llama3.1:8b found"
else
    echo "   ✗ llama3.1:8b missing - run: ollama pull llama3.1:8b"
fi

# Check Python packages
echo ""
echo "4. Checking Python packages..."
python3 -c "import ollama" 2>/dev/null && echo "   ✓ ollama package installed" || echo "   ✗ ollama package missing - run: pip install ollama"
python3 -c "import requests" 2>/dev/null && echo "   ✓ requests package installed" || echo "   ✗ requests package missing - run: pip install -r requirements.txt"
python3 -c "import bs4" 2>/dev/null && echo "   ✓ beautifulsoup4 package installed" || echo "   ✗ beautifulsoup4 package missing - run: pip install -r requirements.txt"

echo ""
echo "5. Testing import of ┴ROOF modules..."
python3 -c "from hosts import create_host; from interns import create_intern; from memory import Memory; from tts import get_tts_engine" 2>/dev/null && echo "   ✓ All modules import successfully" || echo "   ✗ Module import failed"

echo ""
echo "Setup check complete!"
echo ""
echo "To start broadcasting, run:"
echo "   python3 troof.py \"Your topic here\""
