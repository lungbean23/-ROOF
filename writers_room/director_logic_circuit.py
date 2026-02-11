"""
Logic Circuit - Director's Decision-Making Rules

Maps conversation patterns to grammar-based commands.

Grammar:
- VERBS: FOCUS, AVOID
- NOUNS: INTERN, QUESTION

Rules are evaluated in priority order (highest first).
First matching rule wins.
"""

from typing import List, Dict, Any, Callable


class LogicCircuit:
    """
    Rule-based decision system for Director
    
    Analyzes conversation patterns and returns grammar commands
    """
    
    def __init__(self):
        self.rules = self._build_rules()
    
    def evaluate(self, 
                 intern_reports: Dict[str, Any],
                 recent_exchanges: List[Dict[str, Any]],
                 host_name: str) -> Dict[str, Any]:
        """
        Evaluate all rules and return first match
        
        Args:
            intern_reports: Reports from story interns
            recent_exchanges: Recent conversation history
            host_name: Which host is about to speak
        
        Returns:
            Directive with verb, noun, command, instruction, reason
        """
        # Get context info
        intern_name = "Taco" if host_name == "Goku" else "Clunt"
        other_host = "Homer" if host_name == "Goku" else "Goku"
        
        # Add exchanges to reports for pattern detection
        context = {
            **intern_reports,
            'recent_exchanges': recent_exchanges,
            'host_name': host_name,
            'intern_name': intern_name,
            'other_host': other_host
        }
        
        # Sort rules by priority (highest first)
        sorted_rules = sorted(self.rules, key=lambda r: r['priority'], reverse=True)
        
        # Evaluate each rule
        for rule in sorted_rules:
            try:
                # Check if condition matches
                if rule['condition'](context):
                    # Build instruction from template
                    instruction = rule['instruction_template'].format(
                        intern_name=intern_name,
                        other_host=other_host,
                        host_name=host_name
                    )
                    
                    print(f"[Logic circuit: {rule['name']} → {rule['verb']} {rule['noun']}]")
                    
                    return {
                        "verb": rule['verb'],
                        "noun": rule['noun'],
                        "command": f"{rule['verb']} {rule['noun']}",
                        "instruction": instruction,
                        "reason": f"Pattern: {rule['pattern']}",
                        "rule_triggered": rule['name']
                    }
            except Exception as e:
                # Rule evaluation failed, skip to next
                print(f"[Logic circuit: Rule '{rule['name']}' failed: {e}]")
                continue
        
        # No rules matched - default
        return {
            "verb": "FOCUS",
            "noun": "INTERN",
            "command": "FOCUS INTERN",
            "instruction": f"Build on what {intern_name} discovered",
            "reason": "Default: ground conversation in research",
            "rule_triggered": "default"
        }
    
    def _build_rules(self) -> List[Dict[str, Any]]:
        """
        Build the complete rule set
        
        Each rule has:
        - name: Rule identifier
        - pattern: What it detects
        - condition: Function that returns True if pattern matches
        - verb: Command verb (FOCUS/AVOID)
        - noun: Command noun (INTERN/QUESTION)
        - instruction_template: What to tell host (can use {intern_name}, {other_host}, {host_name})
        - priority: Higher = checked first
        """
        return [
            # ============================================================
            # PRIORITY 1: QUESTION HANDLING (100-110)
            # ============================================================
            
            {
                "name": "question_dodging",
                "pattern": "unanswered_question",
                "condition": self._detect_question_dodging,
                "verb": "FOCUS",
                "noun": "QUESTION",
                "instruction_template": "Answer {other_host}'s question directly - stop deflecting",
                "priority": 110
            },
            
            {
                "name": "question_exists",
                "pattern": "question_present",
                "condition": self._detect_question_present,
                "verb": "FOCUS",
                "noun": "QUESTION",
                "instruction_template": "Prioritize answering {other_host}'s question",
                "priority": 100
            },
            
            # ============================================================
            # PRIORITY 2: INTERN RESEARCH HANDLING (80-95)
            # ============================================================
            
            {
                "name": "ignoring_intern",
                "pattern": "fresh_research_ignored",
                "condition": self._detect_intern_ignored,
                "verb": "FOCUS",
                "noun": "INTERN",
                "instruction_template": "Use what {intern_name} just found - it's the key insight here",
                "priority": 95
            },
            
            {
                "name": "beating_dead_horse",
                "pattern": "same_research_repeated",
                "condition": lambda ctx: ctx['topic_tracker']['saturation'] > 0.8,
                "verb": "AVOID",
                "noun": "INTERN",
                "instruction_template": "Stop rehashing {intern_name}'s data - we've covered it thoroughly",
                "priority": 85
            },
            
            {
                "name": "moderate_saturation",
                "pattern": "topic_getting_stale",
                "condition": lambda ctx: 0.65 < ctx['topic_tracker']['saturation'] <= 0.8,
                "verb": "FOCUS",
                "noun": "INTERN",
                "instruction_template": "Find a fresh angle in {intern_name}'s research - topic is getting stale",
                "priority": 80
            },
            
            # ============================================================
            # PRIORITY 3: ENERGY MANAGEMENT (60-75)
            # ============================================================
            
            {
                "name": "energy_critical",
                "pattern": "very_low_energy",
                "condition": lambda ctx: ctx['pacing_monitor']['energy_level'] < 0.3,
                "verb": "FOCUS",
                "noun": "INTERN",
                "instruction_template": "INJECT ENERGY - what did {intern_name} find that's surprising or controversial?",
                "priority": 75
            },
            
            {
                "name": "energy_low",
                "pattern": "low_energy",
                "condition": lambda ctx: ctx['pacing_monitor']['energy_level'] < 0.5,
                "verb": "FOCUS",
                "noun": "INTERN",
                "instruction_template": "Boost energy - highlight what's interesting in {intern_name}'s findings",
                "priority": 70
            },
            
            {
                "name": "energy_falling",
                "pattern": "declining_energy",
                "condition": lambda ctx: ctx['pacing_monitor']['trend'] == 'falling',
                "verb": "FOCUS",
                "noun": "INTERN",
                "instruction_template": "Energy dropping - use {intern_name}'s research to reignite interest",
                "priority": 65
            },
            
            # ============================================================
            # PRIORITY 4: CONVERSATION QUALITY (50-55)
            # ============================================================
            
            {
                "name": "monotony_detected",
                "pattern": "monotonous_pattern",
                "condition": lambda ctx: ctx['pacing_monitor'].get('monotony_detected', False),
                "verb": "FOCUS",
                "noun": "INTERN",
                "instruction_template": "Break the monotony - vary your delivery using {intern_name}'s data",
                "priority": 55
            },
            
            # ============================================================
            # PRIORITY 5: DEFAULT (50)
            # ============================================================
            
            {
                "name": "fresh_intern_data",
                "pattern": "new_research_available",
                "condition": lambda ctx: True,  # Always has intern data
                "verb": "FOCUS",
                "noun": "INTERN",
                "instruction_template": "Build on what {intern_name} discovered",
                "priority": 50
            }
        ]
    
    # ================================================================
    # PATTERN DETECTION METHODS
    # ================================================================
    
    def _detect_question_dodging(self, context: Dict) -> bool:
        """
        Detect if a question was asked but not answered
        
        Looks for:
        - Question in previous message
        - Deflection markers in response
        - Long response without direct answer
        """
        recent = context.get('recent_exchanges', [])
        
        if len(recent) < 2:
            return False
        
        # Get last two exchanges
        prev_exchange = recent[-2]
        last_exchange = recent[-1]
        
        prev_message = prev_exchange.get('message', '')
        last_message = last_exchange.get('message', '')
        
        # Was a question asked?
        if '?' not in prev_message:
            return False
        
        # Deflection markers
        deflection_markers = [
            'interesting',
            'fascinating',
            'profound',
            'reminds me',
            'speaking of',
            'actually',
            'but what about',
            'that said',
            'on the other hand'
        ]
        
        # Count deflections
        deflection_count = sum(1 for marker in deflection_markers if marker in last_message.lower())
        
        # If 2+ deflections and long response, likely dodging
        if deflection_count >= 2 and len(last_message) > 200:
            return True
        
        # Check if response starts with deflection
        first_words = ' '.join(last_message.lower().split()[:5])
        if any(marker in first_words for marker in deflection_markers):
            return True
        
        return False
    
    def _detect_question_present(self, context: Dict) -> bool:
        """Check if a question was asked in previous exchange"""
        recent = context.get('recent_exchanges', [])
        
        if len(recent) < 2:
            return False
        
        prev_exchange = recent[-2]
        return '?' in prev_exchange.get('message', '')
    
    def _detect_intern_ignored(self, context: Dict) -> bool:
        """
        Detect if intern findings were provided but not acknowledged
        
        Checks:
        - Research was provided
        - Host didn't mention intern
        - Host didn't cite sources
        """
        recent = context.get('recent_exchanges', [])
        
        if not recent:
            return False
        
        last_exchange = recent[-1]
        message = last_exchange.get('message', '')
        research = last_exchange.get('research', {})
        
        # Was research provided?
        has_findings = bool(research.get('findings'))
        
        if not has_findings:
            return False
        
        # Did host mention intern?
        intern_names = ['taco', 'clunt']
        mentioned_intern = any(name in message.lower() for name in intern_names)
        
        # Did host cite sources?
        citation_markers = [
            'found', 'according to', 'study', 'research', 
            'report', 'data shows', 'evidence', 'survey'
        ]
        cited_sources = any(marker in message.lower() for marker in citation_markers)
        
        # If research provided but not acknowledged
        if not mentioned_intern and not cited_sources:
            return True
        
        return False


def create_logic_circuit() -> LogicCircuit:
    """Factory function to create logic circuit"""
    return LogicCircuit()
