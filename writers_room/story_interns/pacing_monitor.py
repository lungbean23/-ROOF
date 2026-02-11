"""
Pacing Monitor - Story Intern

Detects energy drops and engagement patterns.

Analyzes:
- Message length trends
- Energy level changes
- Monotony patterns
- Engagement signals
"""

from typing import List, Dict, Any
import statistics


class PacingMonitor:
    """
    Fast analysis of conversation energy and pacing
    
    Used by Director to detect when conversation needs a boost
    """
    
    def __init__(self):
        pass
    
    def analyze(self, recent_exchanges: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze pacing and energy from recent exchanges
        
        Args:
            recent_exchanges: Recent conversation exchanges
        
        Returns:
            Report with energy metrics and suggestions
        """
        if not recent_exchanges or len(recent_exchanges) < 3:
            return {
                "energy_level": 0.5,
                "trend": "stable",
                "suggestions": [],
                "status": "insufficient_data"
            }
        
        # Extract message lengths
        lengths = [len(ex.get('message', '')) for ex in recent_exchanges]
        
        # Calculate energy indicators
        avg_length = statistics.mean(lengths)
        recent_avg = statistics.mean(lengths[-3:])  # Last 3
        earlier_avg = statistics.mean(lengths[:3]) if len(lengths) >= 6 else avg_length
        
        # Energy level (based on message length and variation)
        # Longer messages = higher energy
        # High variation = higher energy
        if len(lengths) > 1:
            variation = statistics.stdev(lengths) if len(lengths) > 1 else 0
        else:
            variation = 0
        
        # Normalize energy (0-1 scale)
        # Base energy on length (assume 500 chars = high energy)
        base_energy = min(avg_length / 500, 1.0)
        
        # Boost for variation (engagement)
        variation_boost = min(variation / 200, 0.3)
        
        energy_level = min(base_energy + variation_boost, 1.0)
        
        # Detect trend
        if recent_avg > earlier_avg * 1.2:
            trend = "rising"
        elif recent_avg < earlier_avg * 0.8:
            trend = "falling"
        else:
            trend = "stable"
        
        # Detect monotony (all messages similar length)
        if variation < 50 and len(lengths) > 3:
            monotony = True
        else:
            monotony = False
        
        # Generate suggestions
        suggestions = self._generate_suggestions(energy_level, trend, monotony)
        
        # Check for questions (engagement signal)
        question_count = sum(1 for ex in recent_exchanges if '?' in ex.get('message', ''))
        question_ratio = question_count / len(recent_exchanges)
        
        return {
            "energy_level": round(energy_level, 2),
            "trend": trend,
            "avg_message_length": round(avg_length, 0),
            "monotony_detected": monotony,
            "question_ratio": round(question_ratio, 2),
            "suggestions": suggestions,
            "status": "analyzed"
        }
    
    def _generate_suggestions(self, energy: float, trend: str, monotony: bool) -> List[str]:
        """Generate suggestions based on energy metrics"""
        suggestions = []
        
        if energy < 0.3:
            suggestions.append("CRITICAL: Energy very low - inject controversy or humor")
            suggestions.append("Consider: provocative question, bold claim, or topic pivot")
        
        elif energy < 0.5:
            suggestions.append("Energy below optimal - consider energy boost")
            suggestions.append("Suggestions: challenge assumption, introduce conflict, ask 'why not?'")
        
        if trend == "falling":
            suggestions.append("Energy declining - conversation losing steam")
            suggestions.append("Action: pivot topic or inject fresh angle")
        
        if monotony:
            suggestions.append("Monotonous pattern detected - responses too similar in length")
            suggestions.append("Vary response style: short punchy vs longer exploration")
        
        if energy > 0.7 and trend == "rising":
            suggestions.append("High energy, rising trend - conversation is working!")
            suggestions.append("Continue current trajectory")
        
        if not suggestions:
            suggestions.append("Energy stable and healthy")
        
        return suggestions
    
    def detect_repetitive_patterns(self, recent_exchanges: List[Dict[str, Any]]) -> List[str]:
        """
        Detect repetitive phrasing patterns
        
        Args:
            recent_exchanges: Recent exchanges
        
        Returns:
            List of detected patterns
        """
        patterns = []
        
        if len(recent_exchanges) < 3:
            return patterns
        
        # Check for repetitive opening phrases
        openings = []
        for ex in recent_exchanges[-5:]:
            message = ex.get('message', '')
            # Get first 5 words
            words = message.split()[:5]
            if words:
                opening = ' '.join(words).lower()
                openings.append(opening)
        
        # Find duplicates
        from collections import Counter
        opening_counts = Counter(openings)
        
        for opening, count in opening_counts.items():
            if count >= 2:
                patterns.append(f"Repetitive opening: '{opening}' used {count} times")
        
        return patterns
