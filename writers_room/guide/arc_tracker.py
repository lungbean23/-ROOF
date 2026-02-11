"""
Conversation Arc Tracker
Tracks individual host conversation arcs to detect drift and question dodging
"""

from typing import Dict, List, Optional
from collections import Counter
import re


class ConversationArcTracker:
    """
    Tracks conversation arc for a single host
    
    Detects:
    - Arc theme drift
    - Question dodging (via arc misalignment)
    - Energy level of engagement
    """
    
    def __init__(self, host_name: str):
        self.host_name = host_name
        
        # Current arc state
        self.current_arc = {
            "theme": None,
            "key_concepts": set(),
            "energy": 1.0,
            "exchanges_in_arc": 0
        }
        
        # Arc history
        self.arc_history = []
        
        # Question-response tracking
        self.pending_questions = []  # Questions asked by other host
        self.response_alignments = []  # How well responses addressed questions
    
    def update_from_exchange(self, 
                            message: str,
                            other_host_message: Optional[str] = None) -> Dict:
        """
        Update arc state from host's message
        
        Args:
            message: This host's message
            other_host_message: Previous message from other host (may contain question)
        
        Returns:
            Arc update report
        """
        # Extract key concepts from message
        concepts = self._extract_concepts(message)
        
        # Check if other host asked a question
        if other_host_message and self._contains_question(other_host_message):
            question_theme = self._extract_concepts(other_host_message)
            response_theme = concepts
            
            # Calculate alignment (how well response addresses question)
            alignment = self._calculate_alignment(question_theme, response_theme)
            
            self.response_alignments.append(alignment)
            
            # Detect question dodging (arc misalignment)
            if alignment < 0.3:
                arc_drift_detected = True
            else:
                arc_drift_detected = False
        else:
            arc_drift_detected = False
            alignment = None
        
        # Update or establish arc theme
        if not self.current_arc["theme"]:
            # First message - establish theme
            self.current_arc["theme"] = self._summarize_theme(concepts)
            self.current_arc["key_concepts"] = concepts
        else:
            # Check if still on same arc
            theme_overlap = len(concepts & self.current_arc["key_concepts"])
            if theme_overlap < 2:
                # Arc shift - save old arc and start new
                self.arc_history.append(self.current_arc.copy())
                self.current_arc = {
                    "theme": self._summarize_theme(concepts),
                    "key_concepts": concepts,
                    "energy": 1.0,
                    "exchanges_in_arc": 0
                }
            else:
                # Still on same arc - update concepts
                self.current_arc["key_concepts"].update(concepts)
        
        # Update energy (simple heuristic: message length and variety)
        self.current_arc["energy"] = min(1.0, len(message) / 500 + len(concepts) / 10)
        self.current_arc["exchanges_in_arc"] += 1
        
        return {
            "arc_theme": self.current_arc["theme"],
            "arc_energy": self.current_arc["energy"],
            "arc_drift_detected": arc_drift_detected,
            "question_alignment": alignment
        }
    
    def _extract_concepts(self, text: str) -> set:
        """Extract key concepts (simple bigrams + key nouns)"""
        # Lowercase and clean
        text = text.lower()
        
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                    'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
                    'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do',
                    'does', 'did', 'will', 'would', 'should', 'could', 'may',
                    'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        
        words = re.findall(r'\b\w+\b', text)
        words = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Get bigrams
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        
        # Return top concepts
        concepts = set(words[:10] + bigrams[:5])
        return concepts
    
    def _contains_question(self, text: str) -> bool:
        """Check if text contains a question"""
        return '?' in text or any(text.lower().startswith(q) for q in 
                                   ['what', 'why', 'how', 'when', 'where', 'who'])
    
    def _calculate_alignment(self, question_theme: set, response_theme: set) -> float:
        """
        Calculate how well response aligns with question
        
        Returns:
            Alignment score 0.0-1.0
        """
        if not question_theme or not response_theme:
            return 0.5
        
        overlap = len(question_theme & response_theme)
        return overlap / max(len(question_theme), len(response_theme))
    
    def _summarize_theme(self, concepts: set) -> str:
        """Summarize theme from concepts"""
        if not concepts:
            return "general"
        # Return most distinctive concept
        return list(concepts)[0] if concepts else "general"
    
    def get_arc_summary(self) -> Dict:
        """Get current arc summary"""
        return {
            "host": self.host_name,
            "theme": self.current_arc["theme"],
            "energy": self.current_arc["energy"],
            "exchanges_in_arc": self.current_arc["exchanges_in_arc"],
            "avg_question_alignment": sum(self.response_alignments) / len(self.response_alignments) if self.response_alignments else None
        }
