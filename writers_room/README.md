# ✍️ Writers Room - Conversation Direction System

The Writers Room steers ┴ROOF Radio conversations, preventing drift and maintaining engaging discourse.

## Architecture

```
DIRECTOR (DeepSeek - Large Context)
├── Analyzes full conversation arc
├── Makes strategic steering decisions
├── Has own vector memory of ALL exchanges
└── Coordinates story interns

STORY INTERNS (Llama 3.1 - Fast Analysis)
├── topic_tracker     - Monitors topic saturation
├── question_generator - Injects provocative questions
├── fact_checker      - Flags dubious claims
└── pacing_monitor    - Detects energy drops
```

## How It Works

### Every 2-3 Exchanges:

1. **Story Interns Analyze** (parallel, fast)
   - Topic Tracker: "We've mentioned 'AI' 47 times in 5 minutes"
   - Question Generator: "Nobody's asked WHY yet"
   - Fact Checker: "That claim about X contradicts source Y"
   - Pacing Monitor: "Energy dropped 40% in last 3 exchanges"

2. **Director Synthesizes** (large context, strategic)
   - Reads all intern reports
   - Reviews conversation arc from memory
   - Decides on intervention type

3. **Directive Issued**
   - STEER: "Redirect to adjacent topic: [X, Y, Z]"
   - CHALLENGE: "Push back on assumption: [claim]"
   - DEEPEN: "Explore this angle: [question]"
   - PIVOT: "Fresh direction: [new topic]"
   - CONTINUE: "Keep going, this is working"

4. **Injected into Next Host**
   - Directive added to host's context
   - Host incorporates naturally into response
   - Conversation stays engaging

## Intervention Types

### STEER
**When**: Topic saturation > 80%
**Action**: Redirect to adjacent unexplored topics
**Example**: "We've exhausted 'AI ethics'. Pivot to: AI regulation, AI in education, or AI economic impact"

### CHALLENGE
**When**: Unchallenged assumptions or weak claims
**Action**: Inject skepticism or counterpoint
**Example**: "Challenge the assumption that 'AI will replace all jobs'. What about job creation?"

### DEEPEN
**When**: Surface-level discussion on rich topic
**Action**: Ask probing questions
**Example**: "Explore WHY companies resist AI transparency, not just THAT they do"

### PIVOT
**When**: Dead-end topic or low energy
**Action**: Fresh angle or new topic
**Example**: "This thread is exhausted. New direction: How does this relate to user privacy?"

### CONTINUE
**When**: Conversation is flowing well
**Action**: No intervention, let it ride
**Example**: "Good debate, high energy, novel insights. Don't interrupt."

## Director's Memory

The Director maintains its own vector database tracking:
- All exchanges from both hosts
- All research findings from interns
- Previous directives issued
- Topic saturation levels
- Energy trajectory

Location: `data/director_memory/qdrant_director/`

## Story Interns

### Topic Tracker
- Counts keyword frequency
- Measures topic saturation
- Suggests adjacent unexplored topics
- Detects repetitive loops

### Question Generator
- Identifies missing perspectives (who, what, when, where, why, how)
- Creates provocative questions
- Finds unexplored angles
- Suggests contrarian positions

### Fact Checker
- Flags claims without evidence
- Detects contradictions with research
- Notes dubious statistics
- Suggests fact-checking priorities

### Pacing Monitor
- Measures message length trends
- Detects energy drops
- Identifies monotony patterns
- Suggests energy injections (controversy, humor, provocation)

## Integration with Hosts

The Director is consumed by hosts in `smart_host.py`:

```python
class SmartHost:
    def __init__(self):
        self.director = None  # Set by TroofRadio
    
    def generate_response(self, other_host_message):
        # Get directive from director
        directive = self.director.get_directive(
            host_name=self.name,
            recent_exchanges=self.vector_memory.get_recent_flow(5)
        )
        
        # Inject into context
        if directive and directive.get('command'):
            context += f"\n\n[PRODUCER NOTE: {directive['instruction']}]"
        
        # Generate response
        response = self._call_llm(context)
        
        # Notify director
        self.director.log_exchange(self.name, response)
        
        return response
```

## Director Decision Logic

```python
def decide_intervention(self, intern_reports):
    saturation = intern_reports['topic_tracker']['saturation']
    energy = intern_reports['pacing_monitor']['energy_level']
    missing_angles = intern_reports['question_generator']['missing']
    dubious_claims = intern_reports['fact_checker']['flags']
    
    # Priority: Fact-checking > Saturation > Energy > Questions
    
    if dubious_claims:
        return CHALLENGE(dubious_claims[0])
    
    if saturation > 0.8:
        return STEER(adjacent_topics)
    
    if energy < 0.4:
        return PIVOT(fresh_topic) or CHALLENGE(controversial_angle)
    
    if missing_angles:
        return DEEPEN(missing_angles[0])
    
    return CONTINUE()
```

## Data Flow

```
Exchange happens
    ↓
Story Interns analyze (fast, parallel)
    ├── topic_tracker.analyze()
    ├── question_generator.analyze()
    ├── fact_checker.analyze()
    └── pacing_monitor.analyze()
    ↓
Reports → Director
    ↓
Director.decide_intervention()
    ↓
Directive → Next Host
    ↓
Host incorporates directive into response
```

## Configuration

Director behavior can be tuned in config:

```json
{
  "writers_room": {
    "intervention_frequency": 3,  // Every N exchanges
    "saturation_threshold": 0.8,  // Topic saturation trigger
    "energy_threshold": 0.4,      // Low energy trigger
    "director_model": "deepseek-chat",
    "intern_model": "llama3.1",
    "director_temperature": 0.7,
    "intern_temperature": 0.3
  }
}
```

## Philosophy

The Writers Room doesn't control the conversation - it **steers** it. Like a producer whispering in a host's earpiece:

- Hosts maintain autonomy and personality
- Director prevents drift and repetition
- Conversation feels natural, not scripted
- Strategic guidance, not dictation

## Future Enhancements

- **Arc Memory**: Remember multi-episode story arcs
- **Guest Coordination**: Plan guest host appearances
- **Controversy Injection**: Deliberately stir debate
- **Audience Feedback**: Incorporate listener input
- **Energy Boost**: Inject humor or provocation when flat
- **Segment Planning**: Plan show segments (intro, main, conclusion)
