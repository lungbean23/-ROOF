# Writers Room Guide System - Implementation Roadmap

## Overview

The Guide system introduces gravitational conversation dynamics to ┴ROOF Radio. At its core is **The Point** - an independent attractor that evolves with the conversation and influences host behavior through the Director.

**Key Philosophy:**
- The Point exists independently of hosts
- Director becomes "The Keeper of The Point"
- Hosts maintain independent arcs but gravitate toward The Point
- Interns provide research fuel for both arcs and Point evolution

---

## Architecture Vision

```
┌─────────────────────────────────────────┐
│    DIRECTOR (The Keeper)                │
│    - Guards The Point                   │
│    - Decides when/where to shift Point  │
│    - Issues gravitational corrections   │
└──────────────┬──────────────────────────┘
               │ Controls
               ↓
        🌟 THE POINT 🌟
        (Evolves independently)
         ↗️  ↖️  
       ↗️      ↖️  Gravity
     ↗️          ↖️
   🚂 Goku        🚂 Homer
   Arc Tracker    Arc Tracker
```

**File Structure:**
```
writers_room/
├── director.py                    # Enhanced as Keeper
├── director_logic_circuit.py      # Tactical rules
├── guide/                         # NEW
│   ├── __init__.py
│   ├── the_point.py              # Gravitational attractor
│   ├── arc_tracker.py            # Per-host arc tracking
│   └── GUIDE_PLAN.md             # This document
└── story_interns/                 # Intelligence layer
```

---

## Phase 1: The Point (Observation Mode)
**Duration:** Week 1  
**Goal:** Collect data without changing behavior  
**Risk:** None - purely observational

### Components to Build

#### 1.1 `writers_room/guide/__init__.py`
```python
"""
Writers Room Guide System
Strategic conversation guidance through The Point and arc tracking
"""

from .the_point import ThePoint

__all__ = ['ThePoint']
```

#### 1.2 `writers_room/guide/the_point.py`
**Mode:** Observation only - no influence on directives

**Key Features:**
- Tracks conversation essence from exchanges
- Identifies facets (multiple aspects of The Point)
- Calculates saturation (how exhausted current Point is)
- Measures coherence (how well exchanges align)
- **DOES NOT** issue directives yet

**Metrics to Log:**
- Point essence over time
- Facet evolution
- Saturation curve
- (Future) Host distances once calculated

**Data Output:**
```json
{
  "current_point": {
    "essence": "troubleshooting methodology",
    "facets": ["systematic diagnosis", "intuition vs process", "tool selection"],
    "strength": 0.75,
    "saturation": 0.42,
    "emerged_at": 5
  },
  "exchange_count": 25
}
```

#### 1.3 Update `broadcast.py`
**Changes:**
```python
# Add import
from writers_room.guide import ThePoint

# In __init__:
self.the_point = ThePoint(topic)

# In _run_broadcast(), after each exchange:
self.the_point.update_point_from_exchange(
    host_name=current_speaker.name,
    message=message,
    research_context=research
)
```

**No changes to:**
- Director
- Hosts
- Any directive logic

### Success Criteria
- [ ] The Point initializes with topic
- [ ] Updates after each exchange without errors
- [ ] Creates `data/the_point.json`
- [ ] Essence and facets evolve logically
- [ ] Saturation increases over time
- [ ] No impact on conversation quality

### Testing Protocol
1. Run 5 conversations on different topics
2. Review `data/the_point.json` after each
3. Verify:
   - Essence makes sense
   - Facets are relevant
   - Saturation reaches ~0.8 by end
   - No crashes or errors

### Data Analysis
- Plot saturation over exchange count
- Review facet evolution patterns
- Identify if algorithmic shift triggers make sense
- Note any edge cases or weird behavior

---

## Phase 2: Director Integration (Monitoring)
**Duration:** Week 2  
**Goal:** Director sees The Point but doesn't act on it  
**Risk:** Low - adds logging only

### Components to Build

#### 2.1 Update `writers_room/director.py`

**Add to Director.__init__:**
```python
# The Point (Director monitors this)
self.the_point = None  # Set by broadcast.py
self.point_monitoring = True  # Flag for monitoring mode
```

**Add method:**
```python
def set_the_point(self, the_point):
    """Director monitors The Point"""
    self.the_point = the_point
    print(f"[Director: Monitoring Point - '{the_point.current_point['essence']}']")

def _log_point_status(self, host_name):
    """Log Point status (Phase 2: monitoring only)"""
    if not self.the_point:
        return
    
    point_summary = self.the_point.get_point_summary()
    
    # Log key metrics
    print(f"[Point Status: Essence='{point_summary['essence']}' "
          f"Saturation={point_summary['saturation']:.0%} "
          f"Strength={point_summary['strength']:.0%}]")
    
    # Log if shift would be triggered
    if point_summary.get('should_shift'):
        print(f"[⚠️  Point shift threshold reached - saturation {point_summary['saturation']:.0%}]")
```

**Update get_directive:**
```python
def get_directive(self, host_name, recent_exchanges):
    # NEW: Log Point status (no action)
    if self.the_point and self.point_monitoring:
        self._log_point_status(host_name)
    
    # Continue with existing logic circuit
    directive = self._decide_intervention(host_name, recent_exchanges)
    
    print(f"[✍️  Directive issued: {directive['command']}]")
    return directive
```

#### 2.2 Update `broadcast.py`

**Add after Director initialization:**
```python
# Connect Director to The Point
self.director.set_the_point(self.the_point)
```

### Success Criteria
- [ ] Director logs Point status every exchange
- [ ] Logs show when shift threshold reached
- [ ] **Directives remain unchanged** (logic circuit still in control)
- [ ] No performance impact
- [ ] Logs are readable and informative

### Testing Protocol
1. Run 3 conversations with Point monitoring
2. Verify Director logs appear
3. Check that directives are identical to Phase 1
4. Review logs for insights about Point behavior

### Data Analysis
- When do shift triggers fire?
- Are thresholds too sensitive/conservative?
- Does Point essence make sense to human observer?
- Prepare threshold tuning for Phase 3

---

## Phase 3: Gravitational Pull (Conservative)
**Duration:** Week 3  
**Goal:** Director issues Point-based corrections for EXTREME drift only  
**Risk:** Medium - changes directive behavior

### Components to Build

#### 3.1 Add distance calculation to `the_point.py`

**Already exists in the_point.py:**
```python
def calculate_host_distance(self, host_name: str, host_arc_theme: str) -> float
def get_gravitational_pull(self, host_name: str) -> Optional[Dict]
```

**Tune thresholds:**
```python
# In get_gravitational_pull:
if distance < 0.7:  # Phase 3: Very conservative
    return None  # Allow wide orbit
elif distance < 0.85:
    strength = "gentle"
else:
    strength = "strong"  # Only for extreme drift
```

#### 3.2 Update `director.py`

**Modify get_directive:**
```python
def get_directive(self, host_name, recent_exchanges):
    # NEW: Check for EXTREME gravitational pull
    if self.the_point and not self.point_monitoring:
        # Calculate distance (need host arc theme)
        host = self._get_host_by_name(host_name)
        
        if host and hasattr(host, 'current_topic_focus'):
            distance = self.the_point.calculate_host_distance(
                host_name, 
                host.current_topic_focus
            )
            
            pull = self.the_point.get_gravitational_pull(host_name)
            
            # Only act on STRONG pull (distance > 0.85)
            if pull and pull["strength"] == "strong":
                print(f"[Director: STRONG gravitational pull - {distance:.0%} from Point]")
                return {
                    "verb": "FOCUS",
                    "noun": "INTERN",
                    "command": "FOCUS INTERN",
                    "instruction": pull["instruction"],
                    "reason": f"Gravitational pull: {distance:.0%} from Point",
                    "rule_triggered": "point_gravity"
                }
    
    # Continue with logic circuit (handles 95% of cases)
    directive = self._decide_intervention(host_name, recent_exchanges)
    return directive

def _get_host_by_name(self, host_name):
    """Get host reference by name"""
    if hasattr(self, 'goku') and self.goku.name == host_name:
        return self.goku
    if hasattr(self, 'homer') and self.homer.name == host_name:
        return self.homer
    return None
```

#### 3.3 Add simple topic focus to hosts

**In `smart_host.py`:**
```python
class SmartHost:
    def __init__(self, ...):
        # ... existing code ...
        self.current_topic_focus = None  # For Point distance calculation
    
    def speak(self, topic, ...):
        # ... existing code ...
        
        # Update current focus (simple version)
        self.current_topic_focus = topic
        
        # ... rest of speak method ...
```

#### 3.4 Switch mode in broadcast.py

```python
# After connecting Point to Director:
self.director.point_monitoring = False  # Phase 3: Enable active mode
```

### Success Criteria
- [ ] Gravitational pull fires only for extreme drift (distance > 0.85)
- [ ] Logic circuit still handles majority of directives
- [ ] Conversations feel natural (not over-corrected)
- [ ] Pull directives successfully bring hosts back to Point
- [ ] No degradation in conversation quality

### Testing Protocol
1. Run 10 conversations
2. Track:
   - How often gravitational pull fires
   - Host distances before/after pull
   - Whether pulls feel natural or jarring
3. Compare to Phase 2 (monitoring only) conversations
4. A/B test: some with pull enabled, some disabled

### Metrics to Collect
- Gravitational pull frequency (target: <10% of directives)
- Average distance at pull trigger (should be >0.85)
- Success rate (does host return to Point after pull?)
- Subjective quality (do conversations feel better/worse?)

### Tuning Criteria
If pull fires too often (>20%):
- Increase distance threshold to 0.9
- Require multiple exchanges of high distance

If pull never fires:
- Lower threshold to 0.8
- Verify distance calculation is working

---

## Phase 4: Arc Trackers (Parallel Development)
**Duration:** Week 4 (can overlap with Phase 3)  
**Goal:** Hosts track their own narrative arcs  
**Risk:** Low - passive tracking initially

### Components to Build

#### 4.1 `writers_room/guide/arc_tracker.py`

**Copy from conversation_arc_tracker.py with adjustments:**
- ConversationArcTracker class
- Methods for arc management
- Question alignment detection (for Phase 5)
- JSON persistence

**Key Features:**
- Track current arc theme
- Detect arc energy
- Identify when ready to pivot
- Calculate question-response alignment
- Detect arc drift

#### 4.2 Update `hosts/smart_host.py`

**Add to imports:**
```python
from writers_room.guide import ConversationArcTracker
```

**Add to __init__:**
```python
self.arc_tracker = ConversationArcTracker(name)
```

**Add to speak() method:**
```python
def speak(self, topic, research_brief, other_host_message=None, ...):
    # ... existing generation code ...
    
    message = self._generate_response(...)
    
    # NEW: Update arc tracker (passive)
    theme = self._detect_arc_theme(message, topic)
    energy_delta = self._estimate_energy_delta(message)
    
    self.arc_tracker.add_to_current_arc(
        key_point=theme,
        energy_delta=energy_delta,
        question_received=other_host_message if '?' in (other_host_message or '') else None,
        my_response=message
    )
    self.arc_tracker.increment_exchange()
    
    # Update current topic focus for Point distance
    self.current_topic_focus = theme
    
    # ... rest of method ...
    return message

def _detect_arc_theme(self, message, topic):
    """Simple theme detection from message"""
    # Phase 4: Simple keyword-based detection
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['systematic', 'method', 'process', 'step']):
        return f"{topic}_methodical_approach"
    elif any(word in message_lower for word in ['intuition', 'feel', 'experience', 'sense']):
        return f"{topic}_intuitive_approach"
    elif any(word in message_lower for word in ['tool', 'equipment', 'instrument']):
        return f"{topic}_tools_focus"
    elif any(word in message_lower for word in ['learn', 'training', 'practice', 'skill']):
        return f"{topic}_learning_focus"
    else:
        return topic  # Default to main topic

def _estimate_energy_delta(self, message):
    """Estimate energy change from message content"""
    # Simple heuristics
    energy = 0.0
    
    # Questions increase energy
    if '?' in message:
        energy += 0.1
    
    # Specific examples increase energy
    if any(word in message.lower() for word in ['for example', 'specifically', 'like when']):
        energy += 0.1
    
    # Generic agreement decreases energy
    if any(phrase in message.lower() for phrase in ['i agree', 'that\'s right', 'exactly']):
        energy -= 0.1
    
    return energy
```

#### 4.3 Update `writers_room/guide/__init__.py`

```python
from .the_point import ThePoint
from .arc_tracker import ConversationArcTracker

__all__ = ['ThePoint', 'ConversationArcTracker']
```

### Success Criteria
- [ ] Each host has own arc tracker
- [ ] Arcs persist to JSON files
- [ ] Themes evolve logically
- [ ] Energy levels correlate with conversation quality
- [ ] Arc data is useful for analysis
- [ ] No performance impact

### Testing Protocol
1. Run 5 conversations with arc tracking
2. Review `data/goku_arc_map.json` and `data/homer_arc_map.json`
3. Verify:
   - Arc themes make sense
   - Energy levels seem accurate
   - Pivot triggers fire appropriately
4. Compare arc evolution to manual observation

### Data Collection
- Arc theme distribution
- Average arc length
- Energy patterns over time
- Pivot frequency
- Question alignment scores

---

## Phase 5: Full Integration
**Duration:** Week 5  
**Goal:** Complete system with all components working together  
**Risk:** High - major behavioral changes

### Components to Build

#### 5.1 Enhanced Director Priority System

**Update `director.py` get_directive with full hierarchy:**

```python
def get_directive(self, host_name, recent_exchanges):
    """
    Full priority hierarchy:
    1. Point shift execution (highest)
    2. Strong gravitational pull
    3. Arc drift detection (question dodging)
    4. Gentle gravitational pull
    5. Logic circuit tactical
    """
    
    # Priority 1: Execute planned Point shift
    if hasattr(self, 'point_shift_intent') and self.point_shift_intent:
        return self._execute_point_shift()
    
    # Priority 2: Strong gravitational pull (distance > 0.85)
    if self.the_point:
        host = self._get_host_by_name(host_name)
        if host and hasattr(host, 'arc_tracker') and host.arc_tracker.current_arc:
            arc_theme = host.arc_tracker.current_arc.get('theme', 'unknown')
            distance = self.the_point.calculate_host_distance(host_name, arc_theme)
            
            pull = self.the_point.get_gravitational_pull(host_name)
            if pull and pull["strength"] == "strong":
                print(f"[Director: Strong pull - {distance:.0%} from Point]")
                return {
                    "verb": "FOCUS",
                    "noun": "INTERN",
                    "command": "FOCUS INTERN",
                    "instruction": pull["instruction"],
                    "reason": f"Gravitational: {distance:.0%}",
                    "rule_triggered": "point_gravity_strong"
                }
    
    # Priority 3: Arc drift (question dodging)
    if host and hasattr(host, 'arc_tracker'):
        drift_signal = host.arc_tracker.get_arc_drift_signal()
        if drift_signal and drift_signal.get("severity") == "high":
            print(f"[Director: Arc drift - {drift_signal['alignment_score']:.0%} alignment]")
            return {
                "verb": "FOCUS",
                "noun": "QUESTION",
                "command": "FOCUS QUESTION",
                "instruction": f"Arc drift! You shifted topics. The question was: {drift_signal['question'][:80]}. Answer it directly.",
                "reason": f"Arc alignment {drift_signal['alignment_score']:.0%}",
                "rule_triggered": "arc_drift_correction"
            }
    
    # Priority 4: Gentle gravitational pull (distance 0.7-0.85)
    if self.the_point and pull and pull["strength"] == "gentle":
        print(f"[Director: Gentle pull - {distance:.0%} from Point]")
        return {
            "verb": "FOCUS",
            "noun": "INTERN",
            "command": "FOCUS INTERN",
            "instruction": pull["instruction"],
            "reason": f"Gravitational: {distance:.0%}",
            "rule_triggered": "point_gravity_gentle"
        }
    
    # Priority 5: Logic circuit tactical decisions
    directive = self._decide_intervention(host_name, recent_exchanges)
    
    # After directive, assess if Point should shift
    if self.exchange_count % 10 == 0:
        self._assess_point_status()
    
    print(f"[✍️  Directive issued: {directive['command']}]")
    return directive
```

#### 5.2 Director Point Shifting Logic

**Add to `director.py`:**

```python
def _assess_point_status(self):
    """
    Director's independent assessment of Point
    Decides if/when/where to shift
    """
    if not self.the_point:
        return
    
    point_summary = self.the_point.get_point_summary()
    
    # Algorithmic triggers
    if point_summary["should_shift"]:
        self.point_shift_intent = {
            "reason": "algorithmic_saturation",
            "new_direction": None,
            "planned_at": self.exchange_count
        }
        return
    
    # Director's independent judgment (every 10 exchanges)
    # Use DeepSeek to reason about shift
    if self._director_wants_shift(point_summary):
        # Determine new direction
        new_direction = self._determine_new_direction(point_summary)
        
        self.point_shift_intent = {
            "reason": "director_strategic_judgment",
            "new_direction": new_direction,
            "planned_at": self.exchange_count
        }
        print(f"[Director: Planning Point shift to '{new_direction}']")

def _director_wants_shift(self, point_summary):
    """Ask DeepSeek if shift would be productive"""
    prompt = f"""You're directing a conversation. Current Point: {point_summary['essence']}
Saturation: {point_summary['saturation']:.0%}
Facets explored: {point_summary['facets']}

Should we shift to new territory? Reply YES or NO with 1 sentence reason."""

    try:
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response['message']['content']
        return 'yes' in answer.lower()[:20]
    except:
        return False

def _determine_new_direction(self, point_summary):
    """Ask DeepSeek where to shift"""
    prompt = f"""Current Point exhausted: {point_summary['essence']}
Suggest a fresh but related direction to explore. One phrase only."""

    try:
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()[:100]
    except:
        return f"{point_summary['essence']}_evolved"

def _execute_point_shift(self):
    """Execute planned Point shift"""
    if not self.point_shift_intent:
        return None
    
    intent = self.point_shift_intent
    new_essence = intent["new_direction"] or "evolved_discussion"
    
    # Shift The Point
    self.the_point.shift_point(new_essence, reason=intent["reason"])
    
    # Clear intent
    self.point_shift_intent = None
    
    print(f"[🌟 POINT SHIFTED: '{new_essence}']")
    
    return {
        "verb": "FOCUS",
        "noun": "INTERN",
        "command": "FOCUS INTERN",
        "instruction": f"The Point has shifted! New center: {new_essence}. Explore this fresh territory.",
        "reason": intent["reason"],
        "rule_triggered": "point_shift"
    }
```

### Success Criteria
- [ ] All 5 priority levels work correctly
- [ ] Point shifts happen naturally
- [ ] Arc drift catches question dodging
- [ ] Gravitational pull keeps conversation coherent
- [ ] Logic circuit still handles baseline
- [ ] Conversations feel guided but not robotic

### Testing Protocol
1. Run 20 conversations across diverse topics
2. Track directive distribution:
   - Point shift: ~5% of exchanges
   - Strong gravity: ~5-10%
   - Arc drift: ~3-5%
   - Gentle gravity: ~10-15%
   - Logic circuit: ~65-75%
3. Subjective quality assessment
4. Compare to pre-Guide baseline

### Metrics
- Directive type distribution
- Point shift frequency and timing
- Host distance patterns over conversation
- Arc energy correlations with quality
- Question dodging detection accuracy

---

## Testing & Validation

### Automated Tests
```bash
# Unit tests
pytest tests/test_the_point.py
pytest tests/test_arc_tracker.py
pytest tests/test_director_guide.py

# Integration tests
pytest tests/test_guide_system_integration.py
```

### Manual Testing Checklist

**For each phase:**
- [ ] Run on 3 different topic types (technical, philosophical, practical)
- [ ] Verify logs are clean and informative
- [ ] Check JSON persistence files
- [ ] Compare conversation quality to baseline
- [ ] Review edge cases (very short/long conversations)

**Specific scenarios to test:**
- Host gets completely off-topic (should trigger strong pull)
- Host dodges direct question (should trigger arc drift)
- Point gets saturated (should trigger shift)
- Both hosts cluster near Point (should trigger shift for tension)
- Rapid back-and-forth questions (arc tracker should handle)

---

## Rollback Plan

**Each phase is independently reversible:**

### Phase 1 Rollback:
```python
# In broadcast.py, comment out:
# from writers_room.guide import ThePoint
# self.the_point = ThePoint(topic)
# self.the_point.update_point_from_exchange(...)
```

### Phase 2 Rollback:
```python
# In director.py:
self.point_monitoring = True  # Keep in monitoring-only mode
```

### Phase 3 Rollback:
```python
# In director.py get_directive, comment out gravitational pull block
```

### Phase 4 Rollback:
```python
# In smart_host.py, comment out arc tracker initialization and updates
```

### Phase 5 Rollback:
```python
# Revert to Phase 3 or 4 state
```

**Complete rollback:**
```bash
# Delete guide directory
rm -rf writers_room/guide

# Revert broadcast.py and director.py to git state
git checkout broadcast.py writers_room/director.py hosts/smart_host.py
```

---

## Success Metrics

### Quantitative Goals

**Phase 1:**
- Point tracks essence accurately (manual review)
- Saturation reaches 70-90% by conversation end
- No crashes or errors

**Phase 2:**
- Director logs appear consistently
- Shift triggers fire 1-3 times per conversation
- Zero impact on directive distribution

**Phase 3:**
- Gravitational pull fires 5-15% of exchanges
- Host distances decrease after pull
- Conversation quality maintained or improved

**Phase 4:**
- Arc themes make logical sense
- Energy correlates with engagement
- Question dodging detected with >70% accuracy

**Phase 5:**
- All directive types used appropriately
- Point shifts feel natural (not forced)
- Conversations have clear narrative arcs
- Hosts maintain independence while staying coherent

### Qualitative Goals

- Conversations feel **guided but not scripted**
- The Point emerges **naturally from content**
- Hosts maintain **distinct perspectives**
- Director feels like a **producer, not a controller**
- Topic evolution feels **organic**
- Listeners can sense **narrative momentum**

---

## Future Enhancements (Post-Phase 5)

### Short Term
- SharedConversationGraph (track arc relationships between hosts)
- Enhanced theme detection (use embeddings instead of keywords)
- Point visualization dashboard
- Arc energy prediction model

### Medium Term
- Multiple simultaneous Points (parallel discussion threads)
- Point merging/splitting dynamics
- Host personality influence on arc behavior
- Listener feedback integration

### Long Term
- Machine learning for optimal Point shifting
- Predictive arc modeling
- Multi-host support (3+ hosts with complex dynamics)
- Real-time Point adjustment based on audience engagement

---

## Notes & Observations

### Implementation Notes
- Keep phases separate in git branches during development
- Tag each phase completion for easy rollback
- Maintain changelog of behavioral changes
- Document any unexpected emergent behaviors

### Performance Considerations
- The Point calculations are lightweight (string operations)
- Arc tracking adds minimal overhead (<5ms per exchange)
- Director's DeepSeek calls happen infrequently (every 10 exchanges)
- JSON persistence is async-safe

### Known Limitations
- Simple keyword-based theme detection (Phase 4-5)
- No semantic understanding of Point essence
- Director judgment limited by prompt engineering
- Arc drift detection may have false positives

### Research Questions
- What's the optimal gravitational pull threshold?
- How often should Point shift ideally?
- Do certain topics naturally resist Point formation?
- Can we predict arc energy from message content?
- Does Point strength correlate with conversation quality?

---

## Changelog

**Version 1.0 (Current)**
- Initial roadmap created
- 5-phase implementation plan defined
- Testing protocols established
- Success criteria documented

---

**Last Updated:** 2026-02-10  
**Status:** Phase 0 (Planning Complete)  
**Next Step:** Implement Phase 1
