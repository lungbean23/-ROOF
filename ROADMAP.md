# ┴ROOF Radio Roadmap 🗺️

## 🎯 Vision

Transform ┴ROOF Radio from a proof-of-concept into a production-ready AI podcast platform with professional audio quality, fact-checking capabilities, and extensible architecture.

---

## 🚀 Phase 1: Audio & Production Quality

### **1.1 Intro Theme Song** 🎵
**Priority**: HIGH  
**Status**: Planned  
**Complexity**: Low

**Problem**: Awkward silence during 60s initial generation  
**Solution**: Play intro music/theme during startup

**Implementation**:
```python
# In broadcast.py
def play_intro_theme():
    """Play intro music during initial setup"""
    theme_file = "assets/intro_theme.mp3"
    if os.path.exists(theme_file):
        play_audio_async(theme_file)
```

**Requirements**:
- [ ] Create/license intro theme music (~30-45s)
- [ ] Add async audio playback during initialization
- [ ] Fade out when first host starts speaking
- [ ] Make theme customizable in config.json

**Estimated Time**: 2-4 hours  
**Impact**: Significantly improves listener experience

---

### **1.2 Improved TTS Voices** 🎙️
**Priority**: MEDIUM  
**Status**: Planned  
**Complexity**: Medium

**Current State**: Edge-TTS voices are functional but robotic  
**Goal**: More natural, expressive voices

**Options**:
1. **ElevenLabs API** (paid, highest quality)
   - Pro: Extremely natural voices
   - Con: Cost per character, API dependency

2. **Coqui TTS** (open-source, local)
   - Pro: Free, customizable, local
   - Con: Requires training/fine-tuning

3. **Bark** (open-source, local)
   - Pro: Free, very natural
   - Con: Slower generation, higher resource usage

**Implementation Path**:
- [ ] Add voice engine abstraction layer
- [ ] Implement ElevenLabs backend (optional)
- [ ] Implement Coqui TTS backend
- [ ] Add voice selection to config.json
- [ ] A/B test voice quality

**Estimated Time**: 8-12 hours  
**Impact**: Major improvement in podcast professionalism

---

### **1.3 Audio Mixing & Effects** 🎚️
**Priority**: LOW  
**Status**: Future  
**Complexity**: High

**Features**:
- Background music during conversation
- Audio ducking (lower music when hosts speak)
- Reverb/EQ for broadcast quality
- Intro/outro jingles
- Transition sound effects

**Tools**: pydub, ffmpeg

---

## 🔬 Phase 2: Intelligence & Accuracy

### **2.1 Fact-Checker Intern Flow** ✓
**Priority**: HIGH  
**Status**: Planned  
**Complexity**: High

**Problem**: Hosts may state inaccurate information from web search  
**Solution**: Third intern fact-checks claims in real-time

**Architecture**:
```
┴ROOF Radio
├── Hosts (Goku, Homer)
├── Research Interns (Taco, Clunt)
└── Fact-Checker Intern (NEW!)
    ├── Claim extraction
    ├── Source verification
    ├── Contradiction detection
    └── Confidence scoring
```

**Implementation**:
```python
class FactCheckerIntern:
    """
    Extracts claims from host statements and verifies them
    """
    def extract_claims(self, message):
        """Use LLM to extract factual claims"""
        pass
    
    def verify_claim(self, claim):
        """
        Search for contradicting/confirming sources
        Return: {verified: bool, confidence: float, sources: []}
        """
        pass
    
    def flag_uncertainty(self, claim, confidence):
        """
        If confidence < threshold, inject correction
        into next host's context
        """
        pass
```

**Workflow**:
1. Host makes statement: "The Great Wall is visible from space"
2. Fact-checker extracts claim
3. Searches for verification
4. Finds contradiction
5. Injects into other host's context: "[FACT CHECK: This is actually false...]"
6. Other host acknowledges: "Actually, I should correct that..."

**Requirements**:
- [ ] Claim extraction (LLM-based)
- [ ] Multi-source verification search
- [ ] Confidence scoring algorithm
- [ ] Context injection mechanism
- [ ] Graceful correction flow

**Estimated Time**: 16-24 hours  
**Impact**: Significantly improves information accuracy

---

### **2.2 Editor Room / Production Assistant** 📝
**Priority**: MEDIUM  
**Status**: Planned  
**Complexity**: Medium

**Concept**: AI "producer" who monitors conversation quality

**Responsibilities**:
- Detect when conversation is going in circles
- Suggest new angles when topic is exhausted
- Identify good stopping points
- Flag low-quality exchanges
- Generate episode summaries

**Implementation**:
```python
class ProductionAssistant:
    def analyze_conversation_quality(self, last_n_exchanges):
        """
        Returns:
        - quality_score: float
        - repetition_detected: bool
        - topic_exhaustion: float
        - suggested_actions: [str]
        """
        pass
    
    def suggest_topic_shift(self, current_topic, conversation_history):
        """Generate natural topic transition"""
        pass
    
    def generate_episode_summary(self, full_conversation):
        """Create episode description"""
        pass
```

**Features**:
- [ ] Conversation quality metrics
- [ ] Repetition detection (semantic + structural)
- [ ] Topic exhaustion scoring
- [ ] Natural transition suggestions
- [ ] Episode summary generation
- [ ] Timestamp key moments

**Estimated Time**: 12-16 hours  
**Impact**: Improves overall conversation quality

---

### **2.3 Multi-Model Host Support** 🤖
**Priority**: LOW  
**Status**: Future  
**Complexity**: Medium

**Goal**: Allow different LLM backends per host

**Use Cases**:
- Goku: Fast model (llama3.2:3b) for quick responses
- Homer: Slower, deeper model (llama3.1:70b) for synthesis
- Compare reasoning quality across models

**Implementation**:
- [ ] Abstract LLM interface
- [ ] Support: Ollama, OpenAI API, Anthropic API, local transformers
- [ ] Per-host model configuration
- [ ] Cost tracking for API models

---

## 🎨 Phase 3: User Experience

### **3.1 Web UI Dashboard** 🖥️
**Priority**: MEDIUM  
**Status**: Future  
**Complexity**: High

**Features**:
- Live conversation view (web interface)
- Topic queue
- Start/stop/pause controls
- Host configuration
- Conversation history browser
- Analytics (buffer hit rate, research quality, etc.)

**Tech Stack**: FastAPI + React or Streamlit

---

### **3.2 Mobile App** 📱
**Priority**: LOW  
**Status**: Future  
**Complexity**: Very High

**Concept**: Podcast app for ┴ROOF Radio

**Features**:
- Generate episodes on demand
- Download for offline listening
- Speed controls
- Bookmarking key moments
- Topic suggestions

---

### **3.3 Conversation Bookmarking** 🔖
**Priority**: MEDIUM  
**Status**: Future  
**Complexity**: Low

**Features**:
- Save favorite exchanges
- Tag interesting moments
- Export highlighted segments
- Search conversation history

---

## 🧪 Phase 4: Research & Quality

### **4.1 Source Quality Scoring** 📊
**Priority**: MEDIUM  
**Status**: Planned  
**Complexity**: Medium

**Problem**: Not all web sources are equal  
**Solution**: Score sources by reliability

**Implementation**:
```python
SOURCE_RELIABILITY = {
    "*.edu": 0.9,
    "*.gov": 0.9,
    "wikipedia.org": 0.7,
    "medium.com": 0.5,
    "reddit.com": 0.3,
}

def score_source(url, content):
    domain_score = get_domain_score(url)
    content_score = analyze_content_quality(content)
    return weighted_average(domain_score, content_score)
```

**Features**:
- [ ] Domain reputation database
- [ ] Content quality analysis (citations, depth, etc.)
- [ ] Recency scoring
- [ ] Author credibility (if available)
- [ ] Show source quality in context

---

### **4.2 Multi-Source Synthesis** 🔗
**Priority**: MEDIUM  
**Status**: Future  
**Complexity**: High

**Goal**: Combine multiple sources for comprehensive understanding

**Features**:
- Detect conflicting information
- Synthesize consensus view
- Highlight areas of disagreement
- Track source diversity

---

### **4.3 Citation Tracking** 📚
**Priority**: LOW  
**Status**: Future  
**Complexity**: Medium

**Goal**: Track which sources influenced which statements

**Features**:
- Source attribution in transcript
- "Show sources" for any claim
- Detect unsourced claims
- Generate bibliography

---

## ⚙️ Phase 5: Technical Improvements

### **5.1 Improved Buffer Strategy** ⚡
**Priority**: MEDIUM  
**Status**: Planned  
**Complexity**: Medium

**Current**: Buffer one response at a time  
**Goal**: Adaptive buffering based on conversation patterns

**Improvements**:
- [ ] Buffer multiple responses ahead
- [ ] Predict conversation branching
- [ ] Cancel outdated buffers on topic shift
- [ ] Priority-based generation queue
- [ ] Smart buffer invalidation

---

### **5.2 Conversation Persistence** 💾
**Priority**: LOW  
**Status**: Future  
**Complexity**: Low

**Goal**: Resume conversations across restarts

**Features**:
- Save conversation state
- Resume from specific exchange
- Fork conversations at any point
- Conversation versioning

---

### **5.3 Performance Optimization** 🚀
**Priority**: LOW  
**Status**: Future  
**Complexity**: Medium

**Targets**:
- Reduce first response latency (<30s)
- Improve buffer hit rate (>90%)
- Optimize vector database queries
- Reduce memory footprint
- GPU acceleration for embeddings

---

## 🌍 Phase 6: Platform & Distribution

### **6.1 Podcast RSS Feed** 📡
**Priority**: MEDIUM  
**Status**: Future  
**Complexity**: Medium

**Goal**: Publish ┴ROOF episodes as real podcast

**Features**:
- Auto-generate RSS feed
- Episode artwork
- Metadata (topic, duration, etc.)
- Submit to Apple Podcasts, Spotify
- Scheduling

---

### **6.2 YouTube Integration** 🎥
**Priority**: LOW  
**Status**: Future  
**Complexity**: High

**Features**:
- Auto-upload episodes to YouTube
- Generated visualization (waveforms, text overlays)
- Timestamps in description
- Automatic chapters

---

### **6.3 Social Media Clips** 📱
**Priority**: LOW  
**Status**: Future  
**Complexity**: Medium

**Features**:
- Extract interesting 30-60s clips
- Generate captions/transcripts
- Auto-post to Twitter/TikTok
- Viral moment detection

---

## 🔮 Phase 7: Advanced Features

### **7.1 Guest Hosts** 🎭
**Priority**: LOW  
**Status**: Future  
**Complexity**: High

**Concept**: Additional AI personalities join conversation

**Implementation**:
- Rotating third host
- Special guest episodes
- Multi-host roundtable discussions
- Personality marketplace

---

### **7.2 Interactive Mode** 🎮
**Priority**: LOW  
**Status**: Future  
**Complexity**: Medium

**Features**:
- Listener can ask questions mid-conversation
- Real-time topic steering
- Fact-check requests
- "Explain like I'm 5" mode

---

### **7.3 Multilingual Support** 🌐
**Priority**: LOW  
**Status**: Future  
**Complexity**: Very High

**Features**:
- Translate topics to any language
- Multilingual TTS
- Cross-language research
- Subtitle generation

---

## 📊 Success Metrics

### **Conversation Quality**
- [ ] Average buffer hit rate >80%
- [ ] Host response relevance score >0.85
- [ ] Repetition detection <5% false positives
- [ ] Fact-check accuracy >90%

### **User Experience**
- [ ] First response latency <30s
- [ ] Audio generation latency <5s
- [ ] Conversation startup <60s total
- [ ] Zero crashes in 1-hour session

### **Content Quality**
- [ ] Source quality score >0.7 average
- [ ] Topic coverage depth >3 levels
- [ ] Natural conversation flow (human evaluation)
- [ ] Listener engagement (when distributed)

---

## 🎯 Immediate Next Steps (Priority Order)

1. **Intro theme song** - Quick win, improves UX immediately
2. **Fact-checker intern** - Critical for accuracy
3. **Source quality scoring** - Improves research reliability
4. **Editor room/production assistant** - Improves conversation quality
5. **Improved TTS voices** - Major production quality boost

---

## 🤝 Contribution Opportunities

Want to help? These are great starting points:

- **Intro theme music** - Musicians welcome!
- **Voice testing** - Compare TTS engines
- **Fact-checking logic** - Algorithm design
- **UI design** - Web dashboard mockups
- **Testing** - Run conversations, report issues
- **Documentation** - Improve guides

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📅 Release Planning

### **v0.3.0** (Current)
- ✅ Vector memory
- ✅ Response buffering
- ✅ Natural conversation flow

### **v0.4.0** (Next, ~2-4 weeks)
- Intro theme song
- Improved buffer strategy
- Source quality scoring

### **v0.5.0** (~1-2 months)
- Fact-checker intern
- Production assistant
- Better TTS voices

### **v1.0.0** (Production Ready, ~3-6 months)
- All Phase 1-2 features complete
- Web UI
- RSS feed generation
- Comprehensive testing

---

Built with curiosity 🎙️
