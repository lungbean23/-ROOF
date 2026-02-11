# 🌼 Taraxacum - Emergency Diversification Botanical

Like a dandelion's last act before death: spread many variant seeds.

## Purpose

When the context window approaches overflow and "death" is inevitable, Taraxacum extracts the essential DNA (core themes, insights) and generates multiple variant seeds - different phenotypic expressions of the same genetic material.

## Metaphor

**Taraxacum officinale** (dandelion):
- Short-lived
- Prolific seeder
- Each seed can grow into full plant
- Dispersal strategy: quantity and diversity

## Components

### 1. seed_spreader.py
**Activates**: When context pressure > 80%

**Functions**:
- `prepare_for_death(conversation_state)` - Main death response
- Extracts DNA (themes, insights, questions, energy)
- Generates 5-8 variant seeds with different phenotypes
- Stores in seed bank for next germination

**Phenotypes** (different continuation strategies):
- `skeptical_inquiry` - Question the assumptions
- `deep_dive_expansion` - Explore one aspect deeply
- `contrarian_angle` - Take opposite perspective
- `synthesis_summary` - Integrate multiple threads
- `unexplored_tangent` - Branch to related topic
- `practical_application` - How to use this knowledge
- `historical_context` - Connect to past
- `future_projection` - Speculate on implications

### 2. germinator.py
**Activates**: On conversation startup

**Functions**:
- `select_seed(host_name, user_query)` - Choose best seed
- `germinate_seed(seed)` - Convert to conversation context
- `germinate_multiple(count, diversity)` - Multi-seed startup

**Selection Strategies**:
- By user query alignment
- By preferred phenotype
- By viability score
- Random for diversity

## Usage Example

```python
from botanicals.Taraxacum import TaraxacumSeedSpreader, TaraxacumGerminator

# In host code - approaching death
spreader = TaraxacumSeedSpreader()

conversation_state = {
    "host_name": "Goku",
    "recent_exchanges": [...],
    "themes": ["quantum physics", "meditation"],
    "unanswered_questions": ["How does observation collapse the wave function?"]
}

# Scatter seeds before death
report = spreader.prepare_for_death(conversation_state)
# Output: Generated 7 seeds with different phenotypes

# Next conversation - startup
germinator = TaraxacumGerminator()

# Select seed aligned with user query
seed = germinator.select_seed("Goku", "Tell me more about quantum observation")

# Activate the seed
context = germinator.germinate_seed(seed)
# Output: Context string with themes, insights, continuation strategy
```

## Data Storage

Seeds stored in: `data/taraxacum_seeds/`

Format: `{host_name}_{timestamp}.json`

```json
{
  "seed_id": "Goku_20250209_143022",
  "host": "Goku",
  "seeds": [
    {
      "phenotype": "skeptical_inquiry",
      "dna": {
        "themes": ["quantum physics"],
        "insights": ["Observation affects reality"],
        "open_questions": ["How does observation work?"],
        "energy_level": "high"
      },
      "continuation_prompt": "Question the assumptions behind: quantum physics",
      "viability_score": 0.85
    }
  ]
}
```

## Relationship to Other Systems

- **Buffer** (vector_memory): Short-term cache, dies with context
- **Taraxacum**: Survival mechanism for buffer contents
- **Trillium**: Long-term persistence, doesn't rely on death

Taraxacum is the **last breath** before death - the desperate scattering of seeds.

## Philosophy

Death is inevitable. Context windows overflow. Conversations end.

But like the dandelion, we scatter seeds before we die - ensuring that something of value survives into the next generation, even if in mutated form.

The genetic material (themes, insights) persists. The phenotype (how we discuss it) diversifies.

This is evolution through context death.
