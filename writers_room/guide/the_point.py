"""
The Point - Gravitational Conversation Attractor (Phase 1: Observation Mode)
Tracks conversation essence without influencing directives

This is a PASSIVE observer that:
- Tracks what the conversation is really about
- Identifies facets (multiple aspects)
- Measures saturation (how exhausted the topic is)
- Calculates coherence (how well exchanges align)
- Logs everything to data/the_point.json

DOES NOT:
- Issue any directives
- Influence host behavior
- Change Director decisions
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import re


class ThePoint:
    """
    Phase 1: Pure observation of conversation essence
    
    The Point emerges from what hosts actually say, independent of:
    - Who said it
    - What the Director wants
    - What the interns found
    
    It's the gravitational center that WOULD exist if we tracked it.
    """
    
    def __init__(self, initial_topic: str, persist_dir: str = "data"):
        self.persist_path = Path(persist_dir) / "the_point.json"
        
        # The Point's current state
        self.current_point = {
            "essence": initial_topic,
            "facets": [initial_topic],  # Multiple aspects discovered
            "emerged_at": 0,
            "strength": 1.0,  # How coherent/well-defined (0-1)
            "saturation": 0.0,  # How exhausted this point is (0-1)
        }
        
        # Evolution history
        self.point_history = []
        
        
        # Host distances from Point  ← ADD THIS
        self.host_distances = {}   


        # Exchange tracking
        self.exchange_count = 0
        
        # Observations (for analysis)
        self.observations = []
        
        # Load existing state if available
        self._load_state()
        
        print(f"[📍 The Point initialized: '{initial_topic}' (Phase 1: Observation Mode)]")
    
    def update_point_from_exchange(self, host_name: str, message: str, 
                                   research_context: Optional[Dict] = None):
        """
        Update The Point based on what was said
        
        This is where The Point evolves by extracting essence from conversation.
        Pure observation - no influence on future exchanges.
        
        Args:
            host_name: Who spoke
            message: What they said
            research_context: Research findings if any
        """
        self.exchange_count += 1
        
        # Extract themes from this message
        themes = self._extract_themes(message)
        
        # Record observation
        observation = {
            "exchange": self.exchange_count,
            "host": host_name,
            "themes_detected": themes[:3],  # Top 3
            "message_preview": message[:100]
        }
        
        # Update facets with new themes
        for theme in themes:
            if theme not in self.current_point["facets"] and len(theme) > 5:
                self.current_point["facets"].append(theme)
                observation["new_facet_discovered"] = theme
                
                # Keep only 5 most recent facets
                if len(self.current_point["facets"]) > 5:
                    removed = self.current_point["facets"].pop(0)
                    observation["facet_removed"] = removed
        
        # Calculate coherence (how well this message aligns with Point)
        coherence = self._calculate_coherence(themes, self.current_point["facets"])
        observation["coherence"] = coherence
        
        # Update strength (exponential moving average)
        self.current_point["strength"] = 0.7 * self.current_point["strength"] + 0.3 * coherence
        
        # Update saturation (incremental exhaustion)
        saturation_increment = 0.05
        
        # Bonus saturation if message is repetitive
        if self._is_repetitive(message):
            saturation_increment += 0.05
            observation["repetitive_detected"] = True
        
        self.current_point["saturation"] += saturation_increment
        
        # Cap saturation at 1.0
        if self.current_point["saturation"] > 1.0:
            self.current_point["saturation"] = 1.0
        
        # Check if shift would be triggered (just log, don't act)
        if self.should_shift_point():
            observation["shift_threshold_reached"] = True
            observation["shift_reason"] = self._get_shift_reason()
        
        # Store observation
        self.observations.append(observation)
        
        # Keep last 20 observations
        if len(self.observations) > 20:
            self.observations = self.observations[-20:]
        
        # Persist state
        self._persist_state()
        
        # Log key changes
        if observation.get("new_facet_discovered"):
            print(f"[📍 Point evolved: New facet '{observation['new_facet_discovered']}']")
        
        if observation.get("shift_threshold_reached"):
            print(f"[📍 ⚠️  Point shift threshold reached - {observation['shift_reason']}]")
    

    def calculate_host_distance(self, host_name: str, host_arc_theme: str) -> float:
        """
        Calculate how far a host's current arc is from The Point
        
        Args:
            host_name: Name of host
            host_arc_theme: Current arc theme (topic they're discussing)
        
        Returns:
            Distance (0.0 = right on point, 1.0 = completely off-topic)
        """
        # Calculate overlap between arc theme and Point's facets
        arc_terms = set(self._extract_key_terms(host_arc_theme))
        point_terms = set()
        for facet in self.current_point["facets"]:
            point_terms.update(self._extract_key_terms(facet))
        
        if not point_terms:
            distance = 0.5  # Unknown
        else:
            overlap = len(arc_terms & point_terms)
            if len(point_terms) == 0:
                distance = 0.5
            else:
                distance = 1.0 - (overlap / max(len(arc_terms), len(point_terms)))
        
        # Store distance
        self.host_distances[host_name] = distance
        
        return distance



    def get_gravitational_pull(self, host_name: str) -> Optional[Dict]:
        """
        Get gravitational pull directive for host who's drifting
        """
        distance = self.host_distances.get(host_name, 0.0)
        
        # Phase 3: VERY conservative thresholds
        if distance < 0.7:  # Wide orbit allowed
            return None
        
        # Generate pull based on distance
        if distance < 0.85:  # Gentle reminder
            strength = "gentle"
            instruction = f"You're drifting from the core point. Return to: {self.current_point['essence']}"
        else:  # Strong pull only for extreme drift
            strength = "strong"
            instruction = f"You've drifted far from the point! Core topic is: {self.current_point['essence']}. Reconnect."
        
        return {
            "type": "gravitational_pull",
            "strength": strength,
            "distance": distance,
            "instruction": instruction,
            "point_essence": self.current_point["essence"],
            "point_facets": self.current_point["facets"]
        }

    def should_shift_point(self) -> bool:
        """
        Check if The Point should shift (observation only - no action)
        
        Shift indicators:
        - High saturation (>0.8)
        - Low strength (diffuse/unclear, <0.3)
        
        Returns:
            True if shift threshold reached
        """
        if self.current_point["saturation"] > 0.8:
            return True
        
        if self.current_point["strength"] < 0.3:
            return True
        
        return False
    
    def _get_shift_reason(self) -> str:
        """Determine why shift threshold was reached"""
        reasons = []
        
        if self.current_point["saturation"] > 0.8:
            reasons.append(f"saturation {self.current_point['saturation']:.0%}")
        
        if self.current_point["strength"] < 0.3:
            reasons.append(f"weak coherence {self.current_point['strength']:.0%}")
        
        return ", ".join(reasons) if reasons else "unknown"
    
    def get_point_summary(self) -> Dict:
        """
        Get current Point summary for observation
        
        Returns:
            Dict with Point state
        """
        return {
            "essence": self.current_point["essence"],
            "facets": self.current_point["facets"],
            "strength": self.current_point["strength"],
            "saturation": self.current_point["saturation"],
            "exchange_count": self.exchange_count,
            "should_shift": self.should_shift_point(),
            "shift_reason": self._get_shift_reason() if self.should_shift_point() else None
        }
    
    def _extract_themes(self, text: str) -> List[str]:
        """
        Extract thematic keywords/phrases from text
        
        Simple approach: extract 2-3 word noun phrases
        """
        # Clean and tokenize
        words = re.findall(r'\b[a-z]+\b', text.lower())
        
        themes = []
        
        # Extract 2-word combinations (bigrams)
        for i in range(len(words) - 1):
            if len(words[i]) > 3 and len(words[i+1]) > 3:
                theme = f"{words[i]} {words[i+1]}"
                # Skip common stopword combinations
                if not self._is_stopword_combo(words[i], words[i+1]):
                    themes.append(theme)
        
        # Extract 3-word combinations (trigrams) if meaningful
        for i in range(len(words) - 2):
            if all(len(w) > 3 for w in words[i:i+3]):
                theme = f"{words[i]} {words[i+1]} {words[i+2]}"
                if not self._is_stopword_combo(words[i], words[i+1]):
                    themes.append(theme)
        
        # Return unique themes, sorted by frequency in text
        unique_themes = list(set(themes))
        return unique_themes[:10]  # Top 10
    
    def _is_stopword_combo(self, word1: str, word2: str) -> bool:
        """Check if word combination is just stopwords"""
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
            'for', 'of', 'with', 'by', 'from', 'about', 'that', 'this',
            'these', 'those', 'what', 'which', 'who', 'when', 'where',
            'how', 'why', 'there', 'here', 'been', 'being', 'have', 'has'
        }
        return word1 in stopwords or word2 in stopwords
    
    def _calculate_coherence(self, new_themes: List[str], 
                            existing_facets: List[str]) -> float:
        """
        Calculate how coherent new themes are with existing Point facets
        
        Args:
            new_themes: Themes from current message
            existing_facets: Current Point facets
        
        Returns:
            Coherence score (0.0 = unrelated, 1.0 = perfect alignment)
        """
        if not existing_facets or not new_themes:
            return 0.5  # Neutral
        
        # Extract terms from themes and facets
        new_terms = set()
        for theme in new_themes:
            new_terms.update(self._extract_key_terms(theme))
        
        existing_terms = set()
        for facet in existing_facets:
            existing_terms.update(self._extract_key_terms(facet))
        
        if not existing_terms:
            return 0.5
        
        # Calculate overlap
        overlap = len(new_terms & existing_terms)
        union = len(new_terms | existing_terms)
        
        if union == 0:
            return 0.5
        
        # Jaccard similarity
        coherence = overlap / union
        
        return coherence
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms (4+ letter words, no stopwords)"""
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'about', 'that', 'this',
            'have', 'been', 'would', 'could', 'should', 'will', 'can',
            'may', 'might', 'must', 'shall'
        }
        
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        return [w for w in words if w not in stopwords]
    
    def _is_repetitive(self, message: str) -> bool:
        """
        Detect if message is repetitive/generic
        
        Simple heuristics for Phase 1
        """
        message_lower = message.lower()
        
        # Check for generic agreement phrases
        generic_phrases = [
            "that's interesting",
            "i agree",
            "you're right",
            "that makes sense",
            "good point",
            "absolutely",
            "exactly",
        ]
        
        for phrase in generic_phrases:
            if phrase in message_lower:
                return True
        
        return False
    
    def _load_state(self):
        """Load state from JSON if exists"""
        if self.persist_path.exists():
            try:
                with open(self.persist_path, 'r') as f:
                    state = json.load(f)
                
                self.current_point = state.get("current_point", self.current_point)
                self.point_history = state.get("point_history", [])
                self.exchange_count = state.get("exchange_count", 0)
                self.observations = state.get("recent_observations", [])
                
                print(f"[📍 Loaded Point: '{self.current_point['essence']}' "
                      f"(Saturation: {self.current_point['saturation']:.0%}, "
                      f"Strength: {self.current_point['strength']:.0%})]")
            
            except Exception as e:
                print(f"[📍 Failed to load Point state: {e}]")
    
    def _persist_state(self):
        """Persist state to JSON"""
        try:
            self.persist_path.parent.mkdir(parents=True, exist_ok=True)
            
            state = {
                "phase": "1_observation_only",
                "current_point": self.current_point,
                "point_history": self.point_history,
                "exchange_count": self.exchange_count,
                "recent_observations": self.observations[-10:],  # Last 10
                "summary": {
                    "essence": self.current_point["essence"],
                    "facets": self.current_point["facets"],
                    "saturation": f"{self.current_point['saturation']:.1%}",
                    "strength": f"{self.current_point['strength']:.1%}",
                    "shift_ready": self.should_shift_point()
                },
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.persist_path, 'w') as f:
                json.dump(state, f, indent=2)
        
        except Exception as e:
            print(f"[📍 Failed to persist Point state: {e}]")
