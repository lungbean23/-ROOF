.
├── CONTRIBUTING.md
├── LICENSE
├── PROJECT_MAP.md
├── README.md
├── broadcast.py              # Broadcast orchestration & main loop
├── config.json
├── debug_ollama.py
├── hosts.py                  # Legacy host system
├── hosts/                    # HOST WING 🎙️
│   ├── __init__.py           # Package exports
│   ├── base_host.py          # Base class with logging & memory
│   ├── conversation_memory.py # Tracks topics to avoid repetition
│   ├── response_buffer.py    # Pre-buffers responses for smooth flow
│   └── smart_host.py         # Enhanced host implementation
├── interns.py                # Legacy intern system
├── interns/                  # INTERN WING 🔬
│   ├── __init__.py           # Package exports
│   ├── base_intern.py        # Base class with logging
│   ├── context_analyzer.py   # Understands conversation context
│   ├── digest.py             # Compresses web results
│   ├── fact_check_flow.py    # Fact-checking (stub)
│   └── research_flow.py      # Smart research selection
├── log_cleanup.py            # Log cleanup utility
├── memory.py                 # Conversation memory & logging
├── requirements.txt
├── setup.py                  # Initialization & validation
├── smart_interns.py          # Enhanced intern implementation
├── test_troof.sh
├── troof.py                  # Main entry point (minimal)
├── troof.sh
└── tts.py                    # Text-to-speech engine
