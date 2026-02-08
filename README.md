# ┴ROOF Radio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> Truth with a speech impediment

An infinite AI conversation radio station where two AI hosts collaboratively seek truth on any topic you give them. Their research interns pull live information from the web to broaden (not necessarily ground) the discussion.

**Break free from algorithmic rage-bait and fake education content.** Instead of doom-scrolling Facebook or watching YouTube "edutainment," tune into ┴ROOF Radio and listen to AI hosts genuinely explore topics with curiosity and intellectual honesty.

## 🎙️ The Philosophy

Web research **broadens** conversation context by introducing new perspectives, but it doesn't **ground** conversations in verified truth. Sources may be biased, outdated, or incorrect. The hosts acknowledge uncertainty and explore ideas collaboratively rather than pretending to have all the answers.

This is your antidote to consumer media.

## 📻 Features

✅ **Real Web Research** - Interns pull live information from the internet  
✅ **Voice Output** - Uses Edge-TTS for natural-sounding speech  
✅ **Infinite Conversation** - Keeps going until you stop it  
✅ **Full Transparency** - All research logged to debug files  
✅ **Conversation Logging** - All exchanges saved as JSON  
✅ **Graceful Shutdown** - Ctrl+C saves and exits cleanly  

## 🎭 The Cast

- **Goku** - Enthusiastic truth-seeker with boundless energy and curiosity (DeepSeek-R1:14b)
- **Homer** - Ancient storyteller who sees epic narratives in everything, wise and philosophical (DeepSeek-R1:14b)
- **Taco** - Goku's research intern (Llama3.1:8b)
- **Clunt** - Homer's research intern (Llama3.1:8b)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai) installed and running
- Audio player (Linux: mpg123/mpv, macOS/Windows: built-in)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/troof-radio.git
   cd troof-radio
   ```

2. **Install Ollama models**
   ```bash
   ollama pull deepseek-r1:14b
   ollama pull llama3.1:8b
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install audio player** (Linux only)
   ```bash
   # Fedora/RHEL
   sudo dnf install mpg123
   
   # Debian/Ubuntu
   sudo apt install mpg123
   
   # Or use mpv
   sudo dnf install mpv  # or: sudo apt install mpv
   ```

### Run It

```bash
python3 troof.py "Your topic here"
```

Press `Ctrl+C` to stop and save the conversation.

### Examples

```bash
python3 troof.py "Are LLMs actually reasoning?"
python3 troof.py "What is consciousness?"
python3 troof.py "Should we colonize Mars?"
python3 troof.py "cash recyclers"
```

## 🔄 How It Works

1. You provide a topic
2. Goku's intern (Taco) does **real web research** using DuckDuckGo
3. Goku shares his initial thoughts with **actual voice output**
4. Homer's intern (Clunt) researches opposing perspectives
5. Homer responds to Goku
6. Loop continues infinitely, bouncing truth back and forth

The conversation is saved to `logs/` when you stop it.

## 📁 Project Structure

```
┴ROOF/
├── troof.py              # Main application
├── hosts.py              # AI host personalities
├── interns.py            # Research assistants (legacy)
├── smart_interns.py      # Enhanced research system
├── memory.py             # Conversation logging
├── tts.py                # Text-to-speech engine
├── config.json           # Host/intern configuration
├── requirements.txt      # Python dependencies
└── logs/
    ├── debug/            # Debug logs with research details
    └── [conversations]   # Saved conversation transcripts
```

## 🐛 Debug Logs

All background processes are logged to `logs/debug/`:
- Research queries and findings
- Intern activity
- Session metadata
- Important reminders that web research broadens but doesn't ground truth

Example:
```bash
cat logs/debug/debug_2026-02-08.log
```

## 🎨 Customization

Edit `config.json` to customize:
- Host personalities
- Speaking styles
- Exchange timing
- Research behavior

### Voice Customization

Want different voices? Edit the `VOICE_MAP` in `tts.py`. Available Edge-TTS voices include:
- `en-US-GuyNeural` (energetic)
- `en-US-ChristopherNeural` (conversational) 
- `en-US-JennyNeural` (friendly female)
- `en-GB-RyanNeural` (British male)
- Many more at https://speech.microsoft.com/portal/voicegallery

## 🤝 Contributing

Found a bug? Have an idea? PRs welcome!

Some ideas for contributions:
- Add more host personalities
- Improve web research quality
- Add support for other LLM backends
- Create a web UI
- Add fact-checking capabilities
- Integrate with more data sources

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License

MIT License - Do whatever you want with this. It's yours.

## 🌟 Spread the Troof

If ┴ROOF Radio helped you escape the algorithm, consider:
- ⭐ Starring this repo
- 🐦 Sharing on social media with #TroofRadio
- 🔊 Recording your favorite exchanges
- 🎨 Creating artwork or memes
- 💡 Suggesting new topics

Let truth spread across the trooftops!

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai) for local LLM inference
- Voices powered by [Edge-TTS](https://github.com/rhasspy/edge-tts)
- Web research via [DuckDuckGo](https://duckduckgo.com)

---

Made with curiosity and a speech impediment 🎙️
