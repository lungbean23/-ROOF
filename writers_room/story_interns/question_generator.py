"""
Question Generator - Story Intern

Identifies missing perspectives and creates provocative questions.

Analyzes:
- Missing 5W1H (who, what, when, where, why, how)
- Unexplored angles
- Assumptions not questioned
- Contrarian positions
"""

from typing import List, Dict, Any


class QuestionGenerator:
    """
    Fast analysis of missing perspectives
    
    Used by Director to inject curiosity and depth
    """
    
    def __init__(self):
        # Question frameworks
        self.frameworks = {
            "who": ["Who benefits?", "Who is affected?", "Who decides?", "Who pays?"],
            "what": ["What are alternatives?", "What's the evidence?", "What could go wrong?"],
            "when": ["When did this start?", "When will we know?", "When is the deadline?"],
            "where": ["Where else is this happening?", "Where does this lead?"],
            "why": ["Why now?", "Why not?", "Why does this matter?", "Why assume that?"],
            "how": ["How does it work?", "How do we know?", "How could it fail?"]
        }
    
    def analyze(self, recent_exchanges: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify missing perspectives and generate questions
        
        Args:
            recent_exchanges: Recent conversation exchanges
        
        Returns:
            Report with missing angles and suggested questions
        """
        if not recent_exchanges:
            return {
                "missing_perspectives": [],
                "suggested_questions": [],
                "coverage": {},
                "status": "no_data"
            }
        
        # Combine all recent messages
        combined_text = " ".join([ex.get('message', '') for ex in recent_exchanges])
        combined_lower = combined_text.lower()
        
        # Check which perspectives have been addressed
        coverage = {}
        for perspective in ["who", "what", "when", "where", "why", "how"]:
            # Simple check: has the word appeared?
            coverage[perspective] = perspective in combined_lower
        
        # Find missing perspectives
        missing = [p for p, covered in coverage.items() if not covered]
        
        # Generate questions for missing perspectives
        suggested_questions = []
        for perspective in missing[:3]:  # Top 3 missing
            questions = self.frameworks.get(perspective, [])
            if questions:
                suggested_questions.append({
                    "perspective": perspective,
                    "question": questions[0]  # Pick first question from framework
                })
        
        # Check for unchallenged assertions
        assertions = self._find_assertions(combined_text)
        
        # Generate contrarian questions
        if assertions:
            suggested_questions.append({
                "perspective": "contrarian",
                "question": f"What if the opposite is true about: {assertions[0][:50]}?"
            })
        
        return {
            "missing_perspectives": missing,
            "suggested_questions": suggested_questions,
            "coverage": coverage,
            "unchallenged_assertions": assertions[:3],
            "status": "analyzed"
        }
    
    def _find_assertions(self, text: str) -> List[str]:
        """
        Find strong assertions that could be challenged
        
        Look for phrases like "always", "never", "everyone", "no one"
        """
        assertion_markers = [
            "always", "never", "everyone", "no one", "all", "none",
            "must", "can't", "impossible", "certain", "obviously"
        ]
        
        assertions = []
        sentences = text.split('.')
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(marker in sentence_lower for marker in assertion_markers):
                assertions.append(sentence.strip())
        
        return assertions
    
    def generate_provocation(self, dominant_topic: str) -> str:
        """
        Generate a provocative question about the dominant topic
        
        Args:
            dominant_topic: The most discussed topic
        
        Returns:
            Provocative question to inject energy
        """
        provocations = [
            f"But what if {dominant_topic} is solving the wrong problem?",
            f"Who profits when we focus on {dominant_topic}?",
            f"What are we NOT talking about when we obsess over {dominant_topic}?",
            f"Is {dominant_topic} a distraction from deeper issues?",
            f"What would happen if we abandoned {dominant_topic} entirely?"
        ]
        
        import random
        return random.choice(provocations)
