# ┴ROOF Radio 🎙️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

> **Truth with a speech impediment**

An AI-powered podcast system featuring two dimension-traversing hosts who explore topics through intelligent conversation, powered by **vector-based semantic memory**, **live web research**, and **response buffering**.

**Break free from algorithmic rage-bait.** Instead of doom-scrolling or watching "edutainment," tune into ┴ROOF Radio and listen to AI hosts genuinely explore topics with curiosity and intellectual honesty.

---

## 🎯 What Makes ┴ROOF Special

### **🧠 Semantic Conversation Memory (Qdrant Vector DB)**
- Hosts remember context across **entire conversations** using vector embeddings
- Retrieves semantically relevant exchanges, not just recent chronological ones
- Natural conversation flow without repetitive cold opens or "That's interesting" loops
- **Example**: Topic "morning routines" → Recalls exchange about "sunrise practices" from 20 exchanges ago

### **🔍 Smart Research Interns**
- Taco and Clunt autonomously research topics **during** conversation
- Multi-angle analysis: "which", "how", "when", "why" questions
- Live web search with DuckDuckGo
- Research strategy evolves as conversation develops

### **⚡ Pipeline Response Buffering**
- Pre-generates responses while audio plays in background
- Reduces wait time from 2 minutes → **instant** (when buffered)
- Hit rates improve during conversation: 0% → 33% → 67% → **75%+**
- Async background generation for seamless listening experience

### **🌊 Topic Evolution**
- Conversations naturally progress through stages
- Topics deepen and branch organically
- Hosts build on previous points rather than restarting

---

## 📊 Current Performance

```
Exchange 1:  60s generation (no buffer, cold start)
Exchange 2:  30s generation (buffer building)
Exchange 3:  1-2s response (buffer hit! ✓)
Exchange 4+: Instant responses (67-75% hit rate)

Vector Memory Performance:
├─ Embedding generation: 10ms per exchange
├─ Similarity search: 5ms for n=3 results
├─ Storage overhead: ~1.5KB per exchange
└─ Total latency: ~15ms (negligible vs 30-120s LLM generation)

Conversation Quality:
✓ No repetitive greetings ("Ahoy" → varied natural openings)
✓ Direct answers to questions
✓ Specific engagement with co-host's ideas
✓ Natural transitions and flow
```

---

## 🎙️ The Philosophy

Web research **broadens** conversation context by introducing new perspectives, but it doesn't **ground** conversations in verified truth. Sources may be biased, outdated, or incorrect. The hosts acknowledge uncertainty and explore ideas collaboratively rather than pretending to have all the answers.

This is your antidote to consumer media.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12, 3.13, or **3.14** (fully compatible!)
- [Ollama](https://ollama.ai) with `llama3.2:3b` model
- ~4GB RAM for models
- Audio player (Linux: mpg123/mpv, macOS/Windows: built-in)

### Installation

```bash
# 1. Clone repo
git clone https://github.com/lungbean23/-ROOF.git
cd ┴ROOF

# 2. Install Ollama model
ollama pull llama3.2:3b

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run!
python3 troof.py "waking up early"

python3 troof.py --fresh "your new topic"
```

### First Run Output
```
[Qdrant: Created collection 'goku_conversation']
[Vector Memory (Qdrant) initialized for Goku]
[Pipeline Buffer initialized]

────────────────────────────────────────────────
🎙️ Goku
────────────────────────────────────────────────
Let's explore waking up early...

[Qdrant: Stored exchange #1]
[Qdrant: Retrieved 0 relevant exchanges]

────────────────────────────────────────────────
🎙️ Homer
────────────────────────────────────────────────
You're right about consistency...

[Buffer HIT! ✓]
[Qdrant: Stored exchange #2]
[Qdrant: Retrieved 1 relevant exchanges (avg similarity: 73%)]
```

---

## 🏗️ Architecture

```
┴ROOF Radio
│
├── Hosts (Smart Conversation)
│   ├── Vector Memory (Qdrant + FastEmbed)
│   │   ├── Semantic retrieval (cosine similarity)
│   │   ├── Recent flow tracking
│   │   └── Repetition detection
│   ├── Response Buffer
│   │   ├── Pre-generation (async)
│   │   ├── Queue management
│   │   └── Hit rate tracking
│   └── LLM (Ollama llama3.2:3b)
│
├── Interns (Research)
│   ├── Angle identification (which/how/when/why)
│   ├── Web search (DuckDuckGo)
│   ├── Finding digest
│   └── Brief generation
│
└── Pipeline
    ├── Topic evolution
    ├── TTS (edge-tts)
    ├── Async orchestration
    └── Error handling
```

---

## 📁 Project Structure

```
┴ROOF/
├── troof.py                    # Main entry point
├── broadcast.py                # Core orchestration
│
├── hosts/
│   ├── smart_host.py           # Vector-based intelligent hosts
│   ├── response_buffer.py      # Response pre-generation
│   ├── conversation_memory.py  # Legacy (replaced by vector_memory.py)
│   └── base_host.py            # Host base class
│
├── interns/
│   ├── smart_interns.py        # Multi-angle research system
│   └── base_intern.py          # Intern base class
│
├── vector_memory.py            # Qdrant vector database integration
├── pipeline_buffer.py          # Async response pipeline
├── topic_evolver.py            # Topic progression logic
├── tts.py                      # Text-to-speech (edge-tts)
├── config.json                 # Host personalities & config
├── requirements.txt            # Python dependencies
│
├── data/
│   └── conversation_vectors/   # Persistent Qdrant storage
│       ├── qdrant_goku/
│       └── qdrant_homer/
│
└── logs/
    ├── conversations/          # JSON conversation transcripts
    ├── hosts/                  # Host activity logs
    └── interns/                # Research logs
```

---

## 🎭 The Cast

### **Goku (The Explorer)**
- **Voice**: Philosophical, curious, exploratory
- **Archetype**: "Always seeking, always questioning"
- **Research Intern**: Taco (breadth-first, latest trends)
- **Approach**: Questions assumptions, seeks new perspectives
- **Model**: llama3.2:3b

### **Homer (The Synthesizer)**  
- **Voice**: Connects patterns, weaves narratives
- **Archetype**: "Connects dots across reality"
- **Research Intern**: Clunt (depth-first, contrarian angles)
- **Approach**: Synthesizes insights, finds hidden connections
- **Model**: llama3.2:3b

---

## 🔧 Configuration

Edit `config.json` to customize host personalities:

```json
{
  "hosts": {
    "goku": {
      "name": "Goku",
      "personality": "Always seeking, always questioning",
      "style": "Philosophical and exploratory",
      "voice_archetype": "The Explorer",
      "model": "llama3.2:3b",
      "intern": "taco"
    }
  }
}
```

### Voice Customization

Edit `VOICE_MAP` in `tts.py`. Available Edge-TTS voices:
- `en-US-GuyNeural` (energetic)
- `en-US-ChristopherNeural` (conversational) 
- `en-GB-RyanNeural` (British male)
- `en-US-JennyNeural` (friendly female)
- More at: https://speech.microsoft.com/portal/voicegallery

---

## 📝 Key Technologies

### **Vector Memory** (`vector_memory.py`)
- **Database**: Qdrant (local persistent storage)
- **Embedding**: FastEmbed with `all-MiniLM-L6-v2` (384 dimensions)
- **Distance Metric**: Cosine similarity
- **Features**: 
  - Semantic context retrieval
  - Chronological recent flow
  - Repetition detection (>85% similarity threshold)

### **Response Buffer** (`response_buffer.py`)
- **Strategy**: Pre-generate next response while current audio plays
- **Queue**: Async background generation via ThreadPoolExecutor
- **Hit Rate**: Tracks successful buffer retrievals
- **Optimization**: Adaptive buffering based on conversation flow

### **Smart Interns** (`smart_interns.py`)
- **Multi-angle research**: which, how, when, why questions
- **Topic evolution**: Adapts queries to conversation stage
- **Web search**: Live DuckDuckGo integration
- **Brief generation**: Digestible 3-4 finding summaries

### **Pipeline** (`pipeline_buffer.py`)
- **Async orchestration**: Research + Generation in parallel
- **TTS integration**: edge-tts for natural voice output
- **Error handling**: Graceful degradation on failures
- **Logging**: Comprehensive activity tracking

---

## 🎯 Recent Achievements

- ✅ **Vector-based semantic memory** (Qdrant + FastEmbed)
- ✅ **Python 3.14 compatibility** (upgraded from ChromaDB)
- ✅ **Natural conversation flow** (eliminated "That's interesting" loops)
- ✅ **Response buffering** (achieving 67-75% hit rate)
- ✅ **Smart research interns** (multi-angle analysis)
- ✅ **Topic evolution system** (conversation progression)
- ✅ **Persistent conversation memory** (survives restarts)
- ✅ **Direct question answering** (hosts actually listen!)

---

## 🐛 Known Issues

- First exchange takes ~60s (no buffer available yet)
- Buffer occasionally misses on complex topic shifts
- TTS voices could be more expressive
- No intro music (silence during startup)
- Interns sometimes repeat similar queries

---

## 📚 Example Topics

```bash
python3 troof.py "waking up early"
python3 troof.py "Are LLMs actually reasoning?"
python3 troof.py "What is consciousness?"
python3 troof.py "Should we colonize Mars?"
python3 troof.py "the philosophy of breakfast"
python3 troof.py "why do cats purr"
```

---

## 🔄 How It Works

1. **You provide a topic**
2. **Vector memory initializes** (loads past conversations if any)
3. **Pipeline starts**: First host generates opening (60s)
4. **Research begins**: Intern searches web while host speaks
5. **Audio plays**: TTS converts text to speech
6. **Buffer activates**: Next response pre-generated in background
7. **Second host responds**: Instant (from buffer) or 30s (if buffer miss)
8. **Loop continues**: Conversation flows with improving buffer hit rate
9. **Memory stores**: Each exchange saved to vector database
10. **Semantic retrieval**: Hosts recall relevant past exchanges

Press `Ctrl+C` to save and exit gracefully.

---

## Writers Room Guide System 🎬

The Guide system keeps conversations on-track through 4 layers:

**Phase 1 - The Point** 📍
Tracks the essence of what's being discussed, evolving facets as the conversation develops.

**Phase 2 - Director Monitoring** 👁️
The Director observes The Point's saturation and strength, logging metrics every 5 exchanges.

**Phase 3 - Gravitational Pull** 🌟
When hosts drift >85% away from The Point, the Director issues a correction directive.

**Phase 4 - Arc Trackers** 🎯
Individual host arc tracking detects question dodging and topic misalignment.

### Usage
```bash
# Fresh start (clears vector memory)
python3 troof.py --fresh "your topic"

# Continue with memory
python3 troof.py "follow-up topic"

# Inspect database contamination
python3 inspect_db.py
```

**Result:** Natural, coherent conversations that stay focused without being rigid.
## 🤝 Contributing

Found a bug? Have an idea? PRs welcome!

See [ROADMAP.md](ROADMAP.md) for planned features.

---

## 📜 License

MIT License - Do whatever you want with this. It's yours.

---

## 🌟 Spread the Troof

If ┴ROOF Radio helped you escape the algorithm:
- ⭐ Star this repo
- 🐦 Share with #TroofRadio
- 🔊 Record your favorite exchanges
- 💡 Suggest new topics

Let truth spread across the trooftops!

---

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai) for local LLM inference
- Voices powered by [Edge-TTS](https://github.com/rhasspy/edge-tts)
- Web research via [DuckDuckGo](https://duckduckgo.com)
- Vector DB by [Qdrant](https://qdrant.tech)
- Embeddings by [FastEmbed](https://qdrant.github.io/fastembed/)

---

Made with curiosity and a speech impediment 🎙️
