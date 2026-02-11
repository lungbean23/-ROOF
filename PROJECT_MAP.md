# ┴ROOF Radio - Project Structure
```
.
├── CONTRIBUTING.md
├── LICENSE
├── PROJECT_MAP.md
├── README.md
├── ROADMAP.md
├── qdrant_setup.md
├── broadcast.py              # Broadcast orchestration & main loop
├── config.json
├── troof.py                  # Main entry point
├── troof.sh
├── test.sh
├── setup.py                  # Initialization & validation
├── debug_ollama.py
├── fix_setup.sh
├── log_cleanup.py
├── memory.py                 # Legacy conversation memory
├── pipeline_buffer.py
├── requirements.txt
├── topic_evolver.py
├── tts.py                    # Text-to-speech engine
├── vector_memory.py          # Qdrant vector memory + botanicals
├── vector_memory_qdrant.py   # Legacy Qdrant implementation
│
├── hosts.py                  # Legacy host system
├── hosts/                    # 🎙️ HOST WING
│   ├── __init__.py           # Package exports
│   ├── base_host.py          # Base class with logging & memory
│   ├── conversation_memory.py # Tracks topics to avoid repetition
│   ├── personality.py        # Host personality definitions
│   ├── response_buffer.py    # Pre-buffers responses for smooth flow
│   ├── response_flow.py      # Response generation flow
│   └── smart_host.py         # Enhanced host implementation
│
├── interns.py                # Legacy intern system
├── interns/                  # 🔬 INTERN WING (Research Assistants)
│   ├── __init__.py           # Package exports
│   ├── base_intern.py        # Base class with logging
│   ├── context_analyzer.py   # Understands conversation context
│   ├── digest.py             # Compresses web results
│   ├── fact_check_flow.py    # Fact-checking flow
│   └── research_flow.py      # Smart research selection
│
├── smart_interns.py          # Enhanced intern implementation
│
├── botanicals/               # 🌿 BOTANICAL WING (Memory Ecology)
│   ├── __init__.py           # Package exports
│   ├── README.md             # Botanical system overview
│   ├── taraxacum/            # 🌼 Emergency seed spreading (death response)
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── seed_spreader.py  # Scatter variant seeds before death
│   │   └── germinator.py     # Activate seeds on startup
│   └── trillium/             # 🌸 Deep continuity (persistent wisdom)
│       ├── __init__.py
│       ├── README.md
│       ├── rhizome.py        # Deep persistent memory network
│       └── three_petals.py   # Triple verification (past/present/future)
│
├── writers_room/             # ✍️ WRITERS ROOM (Conversation Direction)
│   ├── __init__.py           # Package exports
│   ├── README.md             # Writers room overview
│   ├── director.py           # Main conversation director/producer
│   └── story_interns/        # Producer interns for analysis
│       ├── __init__.py
│       ├── topic_tracker.py      # Monitor topic saturation
│       ├── question_generator.py # Inject provocative questions
│       ├── fact_checker.py       # Flag dubious claims
│       └── pacing_monitor.py     # Detect energy/engagement
│
├── data/                     # Persistent data storage
│   ├── conversation_vectors/ # Qdrant vector database (per-host)
│   ├── taraxacum_seeds/      # Conversation seeds (survival)
│   └── trillium_rhizome/     # Deep wisdom network (rhizome.json)
│
├── logs/                     # Runtime logs
│   ├── CURRENT_BROADCAST.txt # Current broadcast log
│   ├── debug/                # Debug logs
│   ├── hosts/                # Per-host logs
│   └── interns/              # Per-intern logs
│
└── __pycache__/              # Python bytecode cache
```

## System Architecture

### Memory Layers (Botanical System)
1. **Buffer** (vector_memory.py) - Seconds to minutes, 67-75% hit rate
2. **Trillium Rhizome** - Days/weeks/months, persistent wisdom
3. **Taraxacum Seeds** - Genetic survival across context death

### Conversation Flow
1. **Hosts** generate responses (Goku, Homer)
2. **Interns** provide research support (Taco, Clunt)
3. **Writers Room** steers conversation direction
4. **Botanicals** maintain memory across lifecycle

### Writers Room Flow
```
Every 2-3 exchanges:
1. Director analyzes recent conversation
2. Story interns provide feedback:
   - Topic Tracker: "Too much repetition on X"
   - Question Generator: "What about angle Y?"
   - Fact Checker: "That claim is dubious"
   - Pacing Monitor: "Energy dropping, inject controversy"
3. Director decides intervention (STEER/CHALLENGE/DEEPEN/PIVOT)
4. Directive injected into next host's context
```

### Data Flow
```
User Query
    ↓
TroofRadio (broadcast.py)
    ↓
┌────────────┬──────────────┬─────────────────┐
│   Hosts    │   Interns    │  Writers Room   │
│  (speak)   │  (research)  │   (direct)      │
└─────┬──────┴──────┬───────┴─────────┬───────┘
      │             │                 │
      └─────────────┴─────────────────┘
                    ↓
              Botanicals
           (remember/survive)
```
