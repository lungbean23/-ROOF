# 🌿 Botanicals - Complementary Memory Systems

Botanical tools used by hosts and interns to manage memory across the lifecycle of conversations.

## Overview

These botanicals **complement** the primary buffer system (`vector_memory_qdrant.py`). They don't replace it - they work alongside it like herbs in a medicine cabinet.

### The Three-Layer Memory Architecture

```
┴ROOF Radio Memory System:

┌─────────────────────────────────────────────────────────────┐
│ BUFFER (vector_memory_qdrant.py)                           │
│ • Short-term: Seconds to minutes                           │
│ • Purpose: Fast response caching (67-75% hit rate)         │
│ • Scope: Current conversation only                         │
│ • Dies with: Context window overflow                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ TRILLIUM (botanicals/Trillium/)                            │
│ • Long-term: Days, weeks, months                           │
│ • Purpose: Deep thematic wisdom                            │
│ • Scope: All conversations (persistent rhizome)            │
│ • Survives: Forever (slow decay, pruning)                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ TARAXACUM (botanicals/Taraxacum/)                          │
│ • Genetic: Survives death events                           │
│ • Purpose: Continuity across context restarts              │
│ • Scope: Single conversation lineage                       │
│ • Activates: On death (>80% context) and startup           │
└─────────────────────────────────────────────────────────────┘
```

## The Two Botanicals

### 🌼 Taraxacum (Dandelion) - Emergency Diversification

**Activates when**: Context pressure > 80% (death approaching)

**Strategy**: Quantity, diversity, rapid dispersal

**Components**:
- `seed_spreader.py` - Extracts DNA, generates variant seeds
- `germinator.py` - Selects and activates seeds on startup

**Use case**: "We're about to die from context overflow. Scatter seeds with different continuation strategies so something survives."

**Metaphor**: Short-lived dandelion spreading hundreds of seeds before death

### 🌸 Trillium - Deep Continuity

**Activates when**: Healthy conversation flow (context < 60%)

**Strategy**: Quality, persistence, balance

**Components**:
- `rhizome.py` - Deep persistent memory (themes, insights, connections)
- `three_petals.py` - Triple verification (past, present, future)

**Use case**: "We're having a good conversation. Let's remember the deep themes and build lasting wisdom that survives across all future conversations."

**Metaphor**: Long-lived perennial returning year after year from deep rhizome

## Usage by Hosts and Interns

Hosts and interns are the **practitioners** who decide when to use which botanical:

```python
from botanicals.Taraxacum import TaraxacumSeedSpreader, TaraxacumGerminator
from botanicals.Trillium import TrilliumRhizome, TrilliumThreePetals

class SmartHost:
    def __init__(self):
        self.buffer = VectorConversationMemory()
        
        # Botanicals on the shelf
        self.taraxacum_spreader = TaraxacumSeedSpreader()
        self.taraxacum_germinator = TaraxacumGerminator()
        self.trillium_rhizome = TrilliumRhizome()
        self.trillium_petals = TrilliumThreePetals()
    
    def startup(self):
        # Try to germinate seeds from last death
        seed = self.taraxacum_germinator.select_seed(self.name)
        if seed:
            context = self.taraxacum_germinator.germinate_seed(seed)
            print(f"Starting from seed: {context}")
        
        # Load deep wisdom
        wisdom = self.trillium_rhizome.get_strongest_themes()
        print(f"Core themes: {wisdom}")
    
    def during_conversation(self):
        # Use buffer for immediate responses
        context = self.buffer.get_relevant_context(topic)
        
        # Build deep memory (Trillium)
        if self.conversation_depth > 3:
            self.trillium_rhizome.deepen_roots(themes, insights)
        
        # Verify balance
        verification = self.trillium_petals.verify_statement(
            statement, past_context, current_facts, direction
        )
    
    def approaching_death(self):
        # Emergency seed spreading (Taraxacum)
        if self.context_pressure > 0.8:
            conversation_state = {
                "host_name": self.name,
                "recent_exchanges": self.buffer.get_recent_flow(5),
                "themes": self.current_themes,
                "unanswered_questions": self.open_questions
            }
            
            self.taraxacum_spreader.prepare_for_death(conversation_state)
            print("Seeds scattered - ready for next generation")
```

## When to Use What

| Situation | Use | Don't Use |
|-----------|-----|-----------|
| Normal response | Buffer | Botanicals |
| Building themes over time | Trillium rhizome | Taraxacum |
| Verifying statement balance | Trillium three petals | Buffer |
| Context death imminent (>80%) | Taraxacum spreader | Trillium |
| Starting new conversation | Taraxacum germinator | - |
| Want deep historical themes | Trillium rhizome | Buffer |

## File Structure

```
botanicals/
├── __init__.py                 # Main package
├── README.md                   # This file
│
├── Taraxacum/                  # Emergency diversification
│   ├── __init__.py
│   ├── README.md
│   ├── seed_spreader.py        # Death response: scatter seeds
│   └── germinator.py           # Startup: activate seeds
│
└── Trillium/                   # Deep continuity
    ├── __init__.py
    ├── README.md
    ├── rhizome.py              # Persistent wisdom network
    └── three_petals.py         # Triple verification
```

## Data Storage

```
data/
├── conversation_vectors/       # Buffer (vector_memory)
├── taraxacum_seeds/           # Taraxacum seed bank
│   └── {host}_{timestamp}.json
└── trillium_rhizome/          # Trillium deep memory
    └── rhizome.json
```

## Philosophy: Yin and Yang

These botanicals balance each other:

| Taraxacum (Yang) | Trillium (Yin) |
|------------------|----------------|
| Death response | Life continuity |
| Quantity (many seeds) | Quality (deep roots) |
| Fast, desperate | Slow, patient |
| Diversification | Consolidation |
| Emergency mode | Healthy mode |
| Scatter | Gather |
| Mutation | Preservation |

Together they form a complete lifecycle:
1. **Trillium** builds deep during healthy times
2. **Taraxacum** scatters seeds when death approaches  
3. Seeds can grow into new **Trillium** rhizomes
4. The cycle continues

Neither replaces the other. Neither replaces the buffer. They're all essential parts of a complete memory ecology.

## Testing

```bash
# Test Taraxacum
python3 -c "
from botanicals.Taraxacum import TaraxacumSeedSpreader
spreader = TaraxacumSeedSpreader()
report = spreader.prepare_for_death({'host_name': 'Test', 'themes': ['testing']})
print(report)
"

# Test Trillium  
python3 -c "
from botanicals.Trillium import TrilliumRhizome
rhizome = TrilliumRhizome()
rhizome.deepen_roots(['testing', 'botanicals'])
print(rhizome.get_rhizome_summary())
"
```

## Integration Status

- [x] Botanicals created
- [x] Documentation complete
- [ ] Integration with smart_host.py
- [ ] Integration with vector_memory_qdrant.py
- [ ] Testing in full conversation flow

## Next Steps

1. Test botanicals independently
2. Integrate Trillium rhizome calls into smart_host.py
3. Add Taraxacum death detection to context monitor
4. Add Taraxacum germination to conversation startup
5. Monitor effectiveness over multiple conversation cycles
