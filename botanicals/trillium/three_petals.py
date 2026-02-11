"""
Trillium Three Petals - Triple Perspective Botanical

Like the trillium's three-petaled symmetry representing perfect balance,
this botanical provides three-way verification and perspective:

Petal 1: PAST - What we've learned (continuity from history)
Petal 2: PRESENT - What we're discussing (current context)
Petal 3: FUTURE - Where we're heading (anticipated themes)

Used to maintain balanced understanding and avoid one-sided thinking.
"""

from typing import List, Dict, Any
from datetime import datetime


class TrilliumThreePetals:
    """
    Triple perspective verification botanical
    
    Provides three-angle view of any conversation element:
    1. Historical continuity (how does this relate to what came before?)
    2. Present accuracy (is this correct right now?)
    3. Future trajectory (where does this lead?)
    
    Helps prevent:
    - Forgetting context (weak past petal)
    - Inaccuracy (weak present petal)
    - Aimless wandering (weak future petal)
    """
    
    def __init__(self):
        print("[Trillium Three Petals initialized]")
    
    def verify_statement(self, 
                        statement: str,
                        past_context: List[Dict] = None,
                        current_facts: Dict = None,
                        intended_direction: str = None) -> Dict[str, Any]:
        """
        Verify a statement from three perspectives
        
        Args:
            statement: The statement to verify
            past_context: Previous exchanges/themes
            current_facts: Current known facts
            intended_direction: Where conversation should go
        
        Returns:
            Three-petal verification report
        """
        print(f"\n[🌸 THREE PETALS VERIFYING]")
        
        verification = {
            "statement": statement,
            "timestamp": datetime.now().isoformat(),
            "petals": {
                "past": self._verify_past(statement, past_context or []),
                "present": self._verify_present(statement, current_facts or {}),
                "future": self._verify_future(statement, intended_direction or "")
            }
        }
        
        # Overall balance score
        verification["balance_score"] = self._calculate_balance(verification["petals"])
        
        return verification
    
    def _verify_past(self, statement: str, past_context: List[Dict]) -> Dict[str, Any]:
        """
        PETAL 1: Verify against historical context
        
        Questions:
        - Does this contradict what we said before?
        - Is this a repetition?
        - Does this build on previous insights?
        """
        if not past_context:
            return {
                "status": "no_history",
                "continuity_score": 0.5,
                "notes": "No historical context available"
            }
        
        # Simple checks (could be enhanced with embeddings)
        statement_lower = statement.lower()
        
        # Check for contradictions (simplified)
        contradicts = False
        repeats = False
        builds_on = False
        
        for ex in past_context:
            past_msg = ex.get("message", "").lower()
            
            # Very basic repetition check
            if len(statement) > 20 and statement_lower in past_msg:
                repeats = True
            
            # Check for contradiction indicators
            if ("not" in statement_lower or "no" in statement_lower) and \
               any(word in past_msg for word in statement_lower.split()):
                # Potential contradiction (very basic)
                contradicts = True
        
        # Continuity score
        if repeats:
            continuity_score = 0.3  # Repetition is poor continuity
        elif contradicts:
            continuity_score = 0.4  # Contradiction is poor continuity
        else:
            continuity_score = 0.8  # Likely building on past
        
        return {
            "status": "verified",
            "continuity_score": continuity_score,
            "contradicts_past": contradicts,
            "repeats_past": repeats,
            "notes": "Past petal verification complete"
        }
    
    def _verify_present(self, statement: str, current_facts: Dict) -> Dict[str, Any]:
        """
        PETAL 2: Verify against current reality
        
        Questions:
        - Is this factually accurate now?
        - Does this align with current research?
        - Is the tone appropriate for current energy?
        """
        if not current_facts:
            return {
                "status": "no_facts",
                "accuracy_score": 0.5,
                "notes": "No current facts to verify against"
            }
        
        # Check alignment with current facts
        research_findings = current_facts.get("research_findings", [])
        current_energy = current_facts.get("energy_level", "medium")
        
        # Simple fact alignment check
        fact_alignment = 0.7  # Default neutral
        
        if research_findings:
            # Check if statement mentions key findings
            statement_lower = statement.lower()
            mentioned_findings = sum(
                1 for finding in research_findings 
                if any(word in statement_lower for word in str(finding).lower().split())
            )
            
            if mentioned_findings > 0:
                fact_alignment = 0.9  # Good alignment
            else:
                fact_alignment = 0.6  # Weak alignment
        
        # Energy alignment
        statement_length = len(statement)
        energy_appropriate = True
        
        if current_energy == "high" and statement_length < 100:
            energy_appropriate = False  # Too short for high energy
        elif current_energy == "calm" and statement_length > 500:
            energy_appropriate = False  # Too long for calm energy
        
        accuracy_score = fact_alignment if energy_appropriate else fact_alignment * 0.8
        
        return {
            "status": "verified",
            "accuracy_score": accuracy_score,
            "fact_alignment": fact_alignment,
            "energy_appropriate": energy_appropriate,
            "notes": "Present petal verification complete"
        }
    
    def _verify_future(self, statement: str, intended_direction: str) -> Dict[str, Any]:
        """
        PETAL 3: Verify against intended trajectory
        
        Questions:
        - Does this move us toward our goal?
        - Does this open up future discussion?
        - Does this create interesting tangents?
        """
        if not intended_direction:
            return {
                "status": "no_direction",
                "trajectory_score": 0.5,
                "notes": "No intended direction specified"
            }
        
        # Check alignment with intended direction
        statement_lower = statement.lower()
        direction_lower = intended_direction.lower()
        
        # Simple keyword overlap
        direction_words = [w for w in direction_lower.split() if len(w) > 3]
        statement_words = [w for w in statement_lower.split() if len(w) > 3]
        
        overlap = len(set(direction_words) & set(statement_words))
        max_possible = len(direction_words) if direction_words else 1
        
        alignment = overlap / max_possible if max_possible > 0 else 0.5
        
        # Check if statement asks questions (opens future)
        opens_future = "?" in statement
        
        # Check if statement suggests next steps
        suggests_next = any(indicator in statement_lower for indicator in 
                          ["next", "then", "could", "might", "let's", "what if"])
        
        trajectory_score = alignment * 0.5
        if opens_future:
            trajectory_score += 0.25
        if suggests_next:
            trajectory_score += 0.25
        
        return {
            "status": "verified",
            "trajectory_score": min(trajectory_score, 1.0),
            "direction_alignment": alignment,
            "opens_future": opens_future,
            "suggests_next": suggests_next,
            "notes": "Future petal verification complete"
        }
    
    def _calculate_balance(self, petals: Dict) -> float:
        """
        Calculate overall balance score
        
        Perfect balance = all three petals equally strong
        Imbalance = one or more petals much weaker
        """
        past_score = petals["past"].get("continuity_score", 0.5)
        present_score = petals["present"].get("accuracy_score", 0.5)
        future_score = petals["future"].get("trajectory_score", 0.5)
        
        # Average score
        avg = (past_score + present_score + future_score) / 3
        
        # Variance (how unbalanced?)
        variance = sum((score - avg) ** 2 for score in [past_score, present_score, future_score]) / 3
        
        # Balance score: high average, low variance = good balance
        balance = avg * (1 - min(variance, 0.3))
        
        return round(balance, 2)
    
    def create_balanced_statement(self,
                                 theme: str,
                                 past_context: List[Dict] = None,
                                 current_facts: Dict = None,
                                 intended_direction: str = None) -> Dict[str, Any]:
        """
        Helper to create a well-balanced statement from scratch
        
        Uses three-petal guidance to suggest statement structure
        """
        print(f"\n[🌸 THREE PETALS CREATING - Balanced statement for: {theme}]")
        
        guidance = {
            "theme": theme,
            "recommendations": {
                "past_petal": self._past_guidance(theme, past_context or []),
                "present_petal": self._present_guidance(theme, current_facts or {}),
                "future_petal": self._future_guidance(theme, intended_direction or "")
            }
        }
        
        return guidance
    
    def _past_guidance(self, theme: str, past_context: List[Dict]) -> str:
        """Suggest how to connect to past"""
        if not past_context:
            return "Start fresh - no history to connect to"
        
        return f"Reference previous discussion about {theme} to show continuity"
    
    def _present_guidance(self, theme: str, current_facts: Dict) -> str:
        """Suggest how to ground in present"""
        if not current_facts:
            return f"State current understanding of {theme}"
        
        return f"Incorporate research findings about {theme} for accuracy"
    
    def _future_guidance(self, theme: str, intended_direction: str) -> str:
        """Suggest how to open future"""
        if not intended_direction:
            return f"Ask question or suggest next exploration of {theme}"
        
        return f"Tie {theme} to {intended_direction} for trajectory"
    
    def check_conversation_balance(self, 
                                  recent_exchanges: List[Dict]) -> Dict[str, Any]:
        """
        Check if overall conversation maintains three-petal balance
        
        Useful for periodic conversation health checks
        """
        if not recent_exchanges:
            return {"status": "no_data", "balance": 0.5}
        
        # Count how many exchanges show each petal
        past_strong = 0
        present_strong = 0
        future_strong = 0
        
        for ex in recent_exchanges:
            msg = ex.get("message", "")
            
            # Past indicators
            if any(word in msg.lower() for word in ["before", "earlier", "previously", "we discussed"]):
                past_strong += 1
            
            # Present indicators  
            if any(word in msg.lower() for word in ["now", "currently", "research shows", "facts"]):
                present_strong += 1
            
            # Future indicators
            if "?" in msg or any(word in msg.lower() for word in ["next", "could", "might", "let's"]):
                future_strong += 1
        
        total = len(recent_exchanges)
        
        return {
            "status": "analyzed",
            "total_exchanges": total,
            "petal_strength": {
                "past": past_strong / total if total > 0 else 0,
                "present": present_strong / total if total > 0 else 0,
                "future": future_strong / total if total > 0 else 0
            },
            "recommendation": self._balance_recommendation(
                past_strong, present_strong, future_strong, total
            )
        }
    
    def _balance_recommendation(self, past: int, present: int, future: int, total: int) -> str:
        """Recommend how to rebalance conversation"""
        if total == 0:
            return "No data"
        
        past_pct = past / total
        present_pct = present / total
        future_pct = future / total
        
        weakest = min(past_pct, present_pct, future_pct)
        
        if weakest == past_pct:
            return "Strengthen past petal: Reference earlier discussion more"
        elif weakest == present_pct:
            return "Strengthen present petal: Ground in current facts/research"
        else:
            return "Strengthen future petal: Ask more questions, suggest next steps"
