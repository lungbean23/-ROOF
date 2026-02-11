"""
Topic Tracker - Story Intern

Monitors topic saturation and suggests fresh angles.

Analyzes:
- Keyword frequency
- Topic repetition
- Saturation levels
- Adjacent unexplored topics
"""

from collections import Counter
from typing import List, Dict, Any
import re


class TopicTracker:
    """
    Fast analysis of topic saturation
    
    Used by Director to detect when conversation is beating a dead horse
    """
    
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'can', 'that', 'this', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
            'who', 'when', 'where', 'why', 'how', 'so', 'if', 'yeah', 'well', 'like'
        }
    
    def analyze(self, recent_exchanges: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze topic saturation from recent exchanges
        
        Args:
            recent_exchanges: List of recent conversation exchanges
        
        Returns:
            Report with saturation metrics and suggestions
        """
        if not recent_exchanges:
            return {
                "saturation": 0.0,
                "dominant_topics": [],
                "suggestions": [],
                "status": "no_data"
            }
        
        # Extract all words
        all_words = []
        for ex in recent_exchanges:
            message = ex.get('message', '')
            words = self._extract_keywords(message)
            all_words.extend(words)
        
        if not all_words:
            return {
                "saturation": 0.0,
                "dominant_topics": [],
                "suggestions": [],
                "status": "no_keywords"
            }
        
        # Count keyword frequency
        word_counts = Counter(all_words)
        total_keywords = len(all_words)
        
        # Find dominant topics (top keywords)
        dominant = word_counts.most_common(10)
        
        # Calculate saturation (how concentrated are top topics?)
        if total_keywords > 0:
            top_5_count = sum(count for word, count in dominant[:5])
            saturation = top_5_count / total_keywords
        else:
            saturation = 0.0
        
        # Format dominant topics
        dominant_topics = [
            {
                "keyword": word,
                "count": count,
                "percentage": count / total_keywords if total_keywords > 0 else 0
            }
            for word, count in dominant[:5]
        ]
        
        # Generate suggestions based on saturation
        suggestions = self._generate_suggestions(saturation, dominant_topics)
        
        return {
            "saturation": round(saturation, 2),
            "dominant_topics": dominant_topics,
            "suggestions": suggestions,
            "total_keywords": total_keywords,
            "unique_keywords": len(word_counts),
            "status": "analyzed"
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Lowercase and extract words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out stop words and short words
        keywords = [
            w for w in words 
            if w not in self.stop_words and len(w) > 3
        ]
        
        return keywords
    
    def _generate_suggestions(self, saturation: float, dominant_topics: List[Dict]) -> List[str]:
        """Generate suggestions based on saturation level"""
        suggestions = []
        
        if saturation > 0.8:
            # Very high saturation - urgent pivot needed
            top_topic = dominant_topics[0]['keyword'] if dominant_topics else "current topic"
            suggestions.append(f"URGENT: Topic '{top_topic}' saturated at {saturation:.0%}")
            suggestions.append(f"Pivot to adjacent topics or fresh angles")
            suggestions.append(f"Avoid repeating '{top_topic}' in next 3 exchanges")
        
        elif saturation > 0.6:
            # Moderate saturation - gentle redirect
            top_topics = ', '.join([t['keyword'] for t in dominant_topics[:3]])
            suggestions.append(f"Topics '{top_topics}' becoming repetitive")
            suggestions.append(f"Consider branching to related but unexplored angles")
        
        elif saturation > 0.4:
            # Healthy focus
            suggestions.append("Good topic focus with diversity")
            suggestions.append("Continue current trajectory")
        
        else:
            # Too scattered
            suggestions.append("Conversation lacks focus - too scattered")
            suggestions.append("Consider deepening one thread before moving on")
        
        return suggestions
    
    def detect_loops(self, recent_exchanges: List[Dict[str, Any]], window: int = 3) -> List[str]:
        """
        Detect repetitive conversation loops
        
        Args:
            recent_exchanges: Recent exchanges
            window: How many exchanges back to check
        
        Returns:
            List of detected loops
        """
        loops = []
        
        if len(recent_exchanges) < window * 2:
            return loops
        
        # Compare recent window with previous window
        recent_window = recent_exchanges[-window:]
        previous_window = recent_exchanges[-window*2:-window]
        
        # Extract keywords from each
        recent_keywords = set()
        for ex in recent_window:
            recent_keywords.update(self._extract_keywords(ex.get('message', '')))
        
        previous_keywords = set()
        for ex in previous_window:
            previous_keywords.update(self._extract_keywords(ex.get('message', '')))
        
        # Check overlap
        overlap = recent_keywords & previous_keywords
        overlap_ratio = len(overlap) / len(recent_keywords) if recent_keywords else 0
        
        if overlap_ratio > 0.7:
            loops.append(f"High keyword overlap ({overlap_ratio:.0%}) - likely repetitive loop")
            loops.append(f"Repeated keywords: {', '.join(list(overlap)[:5])}")
        
        return loops
