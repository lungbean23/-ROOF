"""
Fact Checker - Story Intern

Flags dubious claims and contradictions.

Analyzes:
- Unsupported claims
- Contradictions with research
- Dubious statistics
- Logical inconsistencies
"""

from typing import List, Dict, Any
import re


class FactChecker:
    """
    Fast analysis of factual claims
    
    Used by Director to identify claims needing verification or challenge
    """
    
    def __init__(self):
        # Markers of strong claims that need evidence
        self.claim_markers = [
            "proven", "fact", "studies show", "research shows", "data shows",
            "statistics", "percent", "%", "always", "never", "everyone", "no one",
            "impossible", "certain", "definitely", "obviously"
        ]
        
        # Hedging words (weaker claims, less concerning)
        self.hedges = [
            "might", "maybe", "perhaps", "possibly", "could", "seems",
            "appears", "suggests", "may", "likely", "probably"
        ]
    
    def analyze(self, recent_exchanges: List[Dict[str, Any]], research_context: List[Dict] = None) -> Dict[str, Any]:
        """
        Identify dubious claims and contradictions
        
        Args:
            recent_exchanges: Recent conversation exchanges
            research_context: Research findings from interns (if available)
        
        Returns:
            Report with flagged claims and suggestions
        """
        if not recent_exchanges:
            return {
                "flagged_claims": [],
                "contradictions": [],
                "unsupported_stats": [],
                "status": "no_data"
            }
        
        flagged_claims = []
        unsupported_stats = []
        
        # Analyze each exchange
        for ex in recent_exchanges[-5:]:  # Last 5
            message = ex.get('message', '')
            host = ex.get('host', 'Unknown')
            
            # Find strong claims
            claims = self._find_strong_claims(message)
            
            for claim in claims:
                flagged_claims.append({
                    "host": host,
                    "claim": claim,
                    "type": "unsupported_assertion",
                    "suggestion": "Request evidence or challenge assumption"
                })
            
            # Find statistics without attribution
            stats = self._find_unattributed_stats(message)
            
            for stat in stats:
                unsupported_stats.append({
                    "host": host,
                    "stat": stat,
                    "suggestion": "Ask for source"
                })
        
        # Check for internal contradictions
        contradictions = self._find_contradictions(recent_exchanges)
        
        return {
            "flagged_claims": flagged_claims[:3],  # Top 3
            "unsupported_stats": unsupported_stats[:2],  # Top 2
            "contradictions": contradictions,
            "total_flags": len(flagged_claims) + len(unsupported_stats) + len(contradictions),
            "status": "analyzed"
        }
    
    def _find_strong_claims(self, text: str) -> List[str]:
        """Find strong unhedged claims"""
        claims = []
        
        text_lower = text.lower()
        
        # Look for claim markers
        for marker in self.claim_markers:
            if marker in text_lower:
                # Extract sentence containing marker
                sentences = text.split('.')
                for sentence in sentences:
                    if marker in sentence.lower():
                        # Check if hedged
                        is_hedged = any(hedge in sentence.lower() for hedge in self.hedges)
                        if not is_hedged:
                            claims.append(sentence.strip())
        
        return claims[:3]  # Max 3
    
    def _find_unattributed_stats(self, text: str) -> List[str]:
        """Find statistics without clear attribution"""
        stats = []
        
        # Find percentages and numbers
        percent_pattern = r'\b\d+%|\b\d+\s*percent'
        number_pattern = r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand)'
        
        percentages = re.findall(percent_pattern, text, re.IGNORECASE)
        big_numbers = re.findall(number_pattern, text, re.IGNORECASE)
        
        all_stats = percentages + big_numbers
        
        # Check if attributed (contains "according to", "study", "research", etc.)
        attribution_markers = ["according to", "study", "research", "report", "source"]
        
        text_lower = text.lower()
        has_attribution = any(marker in text_lower for marker in attribution_markers)
        
        if all_stats and not has_attribution:
            for stat in all_stats[:2]:  # Max 2
                stats.append(stat)
        
        return stats
    
    def _find_contradictions(self, exchanges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Find contradictory statements in recent exchanges
        
        Simple contradiction detection: opposite phrases
        """
        contradictions = []
        
        if len(exchanges) < 2:
            return contradictions
        
        # Build list of statements
        statements = []
        for ex in exchanges:
            message = ex.get('message', '')
            host = ex.get('host', '')
            statements.append((host, message.lower()))
        
        # Look for contradictory pairs
        contradiction_pairs = [
            ("will", "won't"),
            ("is", "isn't"),
            ("can", "can't"),
            ("always", "never"),
            ("everyone", "no one"),
            ("should", "shouldn't")
        ]
        
        for i, (host1, stmt1) in enumerate(statements):
            for host2, stmt2 in statements[i+1:]:
                for pos, neg in contradiction_pairs:
                    if pos in stmt1 and neg in stmt2:
                        # Potential contradiction
                        contradictions.append({
                            "host1": host1,
                            "host2": host2,
                            "type": "potential_contradiction",
                            "suggestion": "Highlight and explore disagreement"
                        })
                        break
        
        return contradictions[:2]  # Max 2
