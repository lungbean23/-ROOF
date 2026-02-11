# 🌸 Trillium - Deep Continuity Botanical

Like a trillium's underground rhizome that persists year after year, this botanical maintains deep thematic memory and balanced perspective.

## Purpose

During healthy conversation flow (NOT crisis/death), Trillium builds deep, interconnected wisdom that persists across multiple conversation restarts. It provides continuity through quality, not quantity.

## Metaphor

**Trillium** (wake robin):
- Long-lived perennial
- Deep rhizome (underground root system)
- Three-petaled symmetry (perfect balance)
- Slow-growing, patient
- Returns year after year

## Components

### 1. rhizome.py
**Activates**: During healthy conversation (context < 60%)

**Functions**:
- `deepen_roots(themes, insights)` - Build persistent memory
- `get_deep_context(current_themes)` - Retrieve wisdom
- `get_strongest_themes()` - Identify core recurring interests
- `decay_energy()` - Natural theme weakening over time
- `prune_weak_themes()` - Remove very weak themes

**Data Structure**:
```python
rhizome = {
    "nodes": {
        "quantum_physics": {
            "theme": "quantum physics",
            "occurrences": 15,
            "energy": 8.5,  # Strength (1-10)
            "insights": ["Observation collapses wave function", ...],
            "first_seen": "2025-02-01T10:30:00"
        }
    },
    "connections": {
        "('meditation', 'quantum_physics')": {
            "strength": 7,  # Co-occurrence count
            "created": "2025-02-02T14:20:00"
        }
    }
}
```

**Energy System**:
- Themes gain energy when discussed (+0.5 per mention)
- Energy decays naturally over time (×0.9 per conversation)
- High energy themes = core recurring interests
- Minimum energy 0.1 (themes never fully die)

### 2. three_petals.py
**Activates**: Any time balanced verification needed

**Functions**:
- `verify_statement(stmt, past, present, future)` - Triple check
- `create_balanced_statement(theme)` - Guidance for creation
- `check_conversation_balance(exchanges)` - Health check

**The Three Petals**:

**PETAL 1 - PAST**: Continuity from history
- Does this contradict what we said before?
- Is this a repetition?
- Does this build on previous insights?

**PETAL 2 - PRESENT**: Current accuracy
- Is this factually accurate now?
- Does this align with current research?
- Is the tone appropriate for current energy?

**PETAL 3 - FUTURE**: Trajectory
- Does this move us toward our goal?
- Does this open up future discussion?
- Does this create interesting tangents?

**Balance Score**:
- Perfect balance: All three petals equally strong
- Imbalance: One petal much weaker than others
- Helps identify conversation weaknesses

## Usage Examples

### Rhizome - Building Deep Memory

```python
from botanicals.Trillium import TrilliumRhizome

rhizome = TrilliumRhizome()

# During conversation - add depth
themes = ["quantum physics", "consciousness"]
insights = [
    "Observation might require consciousness",
    "Measurement problem unresolved"
]

rhizome.deepen_roots(themes, insights)
# Output: Rhizome deepened - now 47 theme nodes

# Later - retrieve deep context
context = rhizome.get_deep_context(["quantum physics"])
# Output: {
#   "direct_themes": [...],
#   "connected_themes": ["consciousness", "measurement"],
#   "accumulated_insights": [...]
# }

# See what we've learned over time
summary = rhizome.get_rhizome_summary()
print(summary)
# Output:
# Trillium Rhizome - 47 total themes
# Strongest themes:
# 1. quantum physics (energy: 8.5, occurrences: 15, insights: 7)
# 2. consciousness (energy: 7.2, occurrences: 12, insights: 5)
```

### Three Petals - Balanced Verification

```python
from botanicals.Trillium import TrilliumThreePetals

petals = TrilliumThreePetals()

# Verify a statement from three angles
statement = "Quantum observation requires consciousness"

verification = petals.verify_statement(
    statement=statement,
    past_context=[...],  # Previous exchanges
    current_facts={"research_findings": [...]},
    intended_direction="explore measurement problem"
)

print(verification)
# Output: {
#   "petals": {
#     "past": {"continuity_score": 0.8, "contradicts_past": False},
#     "present": {"accuracy_score": 0.7, "fact_alignment": 0.7},
#     "future": {"trajectory_score": 0.9, "opens_future": True}
#   },
#   "balance_score": 0.8  # Well balanced
# }

# Check overall conversation health
balance = petals.check_conversation_balance(recent_exchanges)
# Output: {
#   "petal_strength": {
#     "past": 0.6,   # 60% of exchanges reference history
#     "present": 0.4, # 40% reference current facts  
#     "future": 0.8   # 80% open future discussion
#   },
#   "recommendation": "Strengthen present petal: Ground in current facts/research"
# }
```

## Data Storage

Rhizome stored in: `data/trillium_rhizome/rhizome.json`

Persists across all conversations - single source of accumulated wisdom.

## Relationship to Other Systems

- **Buffer** (vector_memory): Minutes/hours, dies with context
- **Taraxacum**: Emergency backup, activates on death
- **Trillium**: Days/weeks/months, persists forever

Trillium is the **deep root** that survives winters and returns in spring.

## Philosophy

Not all memory should be ephemeral. Some wisdom deserves to persist.

The rhizome grows slowly, season by season, building interconnected understanding. Unlike the buffer's frantic caching or Taraxacum's desperate seeding, Trillium is patient.

It asks: What have we learned across all our conversations? What themes keep recurring? What insights have withstood time?

The three petals ensure balance: We honor the past without being trapped by it. We ground in the present without losing trajectory. We open the future without aimless wandering.

This is cultivation through patient growth.

## Maintenance

**Energy Decay** (call periodically):
```python
rhizome.decay_energy(decay_rate=0.9)  # Each conversation
```

**Pruning** (call occasionally):
```python
rhizome.prune_weak_themes(min_energy=0.2)  # Every 10 conversations
```

Keeps the rhizome healthy - strong themes thrive, weak ones fade.
