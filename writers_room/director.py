"""
Director - Writers Room Orchestrator

The Director is the strategic brain of the Writers Room.
Uses DeepSeek (large context) to analyze conversation arc and issue directives.

Responsibilities:
- Coordinate story interns (fast parallel analysis)
- Maintain conversation arc memory (own vector DB)
- Decide intervention type (STEER/CHALLENGE/DEEPEN/PIVOT/CONTINUE)
- Issue directives to hosts
"""

import ollama
from typing import List, Dict, Any
from vector_memory import VectorConversationMemory
from .story_interns import TopicTracker, QuestionGenerator, FactChecker, PacingMonitor
from .director_logic_circuit import LogicCircuit


class Director:
    """
    Strategic conversation director
    
    Coordinates story interns and steers conversation to prevent drift
    """
    
    def __init__(self, model="deepseek-r1:14b", intervention_frequency=3):    
        """
        Initialize Director with its own memory
        
        Args:
            model: LLM model for strategic decisions (DeepSeek)
            intervention_frequency: Intervene every N exchanges
        """
        self.model = model
        self.intervention_frequency = intervention_frequency
        
        # Director's own vector memory (sees ALL exchanges from ALL hosts)
        self.memory = VectorConversationMemory(
            host_name="Director",
            persist_dir="data/director_memory"
        )
        
        # Initialize story interns
        self.topic_tracker = TopicTracker()
        self.question_generator = QuestionGenerator()
        self.fact_checker = FactChecker()
        self.pacing_monitor = PacingMonitor()
        self.logic_circuit = LogicCircuit()
        # Track exchanges for intervention timing
        self.exchange_count = 0
        self.last_directive = None
        # Phase 2: The Point monitoring
        self.the_point = None  # Set by broadcast.py
        self.point_monitoring = True  # Phase 2: monitoring mode only
        # Host references (set by broadcast.py)
        self.goku = None
        self.homer = None
        
        print("[✍️  Writers Room Director initialized - DeepSeek ready]")
    
    def set_the_point(self, the_point):
        """Director monitors The Point (Phase 2: observation)"""
        self.the_point = the_point
        print(f"[Director: Monitoring Point - '{the_point.current_point['essence']}']")

    def _log_point_status(self):
        """Log Point status (Phase 2: monitoring only)"""
        if not self.the_point:
            return

        point_summary = self.the_point.get_point_summary()

        # Log every 5 exchanges to avoid spam
        if self.exchange_count % 5 == 0:
            print(f"[📊 Point Status: Saturation={point_summary['saturation']:.0%} "
                  f"Strength={point_summary['strength']:.0%} "
                  f"Facets={len(point_summary['facets'])}]", flush=True)

        # Always log if shift threshold reached
        if point_summary.get('should_shift'):
            print(f"[⚠️  Point shift threshold! Reason: {point_summary['shift_reason']}]", flush=True)

    def log_exchange(self, host_name: str, message: str, research_context: Dict = None):
        """
        Log exchange to Director's memory
        
        Called by hosts after they speak
        
        Args:
            host_name: Which host spoke
            message: What they said
            research_context: Optional research findings
        """
        self.exchange_count += 1
        
        # Store in Director's memory
        self.memory.add_exchange(
            message=message,
            other_host_message=None,  # Director sees ALL, not just pairs
            research_context=research_context
        )
        
        print(f"[Director logged: {host_name} - Exchange #{self.exchange_count}]")
    



    def get_directive(self, host_name: str, recent_exchanges: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get directive for next host
        
        Phase 3: Includes gravitational pull for extreme drift
        """
        # Check if it's time to intervene
        if self.exchange_count % self.intervention_frequency != 0:
            return {
                "type": "CONTINUE",
                "instruction": "",
                "reason": "Not time to intervene yet"
            }
        
        print(f"\n[✍️  Director analyzing conversation for {host_name}...]")
        
        # Get reports from story interns
        intern_reports = self._gather_intern_reports(recent_exchanges)
        
        # Phase 2/3: Log Point status
        if self.the_point:
            self._log_point_status()
        
        # Phase 3: Check for EXTREME gravitational pull
        if self.the_point and not self.point_monitoring:
            host = self._get_host_by_name(host_name)
            
            if host and hasattr(host, 'current_topic_focus'):
                distance = self.the_point.calculate_host_distance(
                    host_name, 
                    host.current_topic_focus
                )
                
                pull = self.the_point.get_gravitational_pull(host_name)
                
                # Only act on STRONG pull (distance > 0.85)
                if pull and pull["strength"] == "strong":
                    print(f"[🌟 Director: STRONG gravitational pull - {distance:.0%} from Point]", flush=True)
                    return {
                        "verb": "FOCUS",
                        "noun": "INTERN",
                        "command": "FOCUS INTERN",
                        "instruction": pull["instruction"],
                        "reason": f"Gravitational pull: {distance:.0%} from Point",
                        "rule_triggered": "point_gravity"
                    }
                
        # Phase 4: Check for arc drift / question dodging
        if host and hasattr(host, 'arc_tracker'):
            arc_summary = host.arc_tracker.get_arc_summary()
            
            if arc_summary.get("avg_question_alignment") and arc_summary["avg_question_alignment"] < 0.3:
                print(f"[📍 Arc drift: {host_name} dodging questions - alignment {arc_summary['avg_question_alignment']:.0%}]")

        # Continue with logic circuit (handles 95% of cases)
        directive = self._decide_intervention(intern_reports, recent_exchanges, host_name)
        
        self.last_directive = directive
        print(f"[✍️  Directive issued: {directive['command']}]")
        
        return directive

    def _get_host_by_name(self, host_name):
        """Get host reference by name"""
        if hasattr(self, 'goku') and self.goku.name == host_name:
            return self.goku
        if hasattr(self, 'homer') and self.homer.name == host_name:
            return self.homer
        return None




   
    def _gather_intern_reports(self, recent_exchanges: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Run all story interns in parallel (fast analysis)
        
        Returns:
            Combined reports from all interns
        """
        print("[Story interns analyzing...]", flush=True)
        
        # Run all interns (could be parallelized further)
        topic_report = self.topic_tracker.analyze(recent_exchanges)
        question_report = self.question_generator.analyze(recent_exchanges)
        fact_report = self.fact_checker.analyze(recent_exchanges)
        pacing_report = self.pacing_monitor.analyze(recent_exchanges)
        
        return {
            "topic_tracker": topic_report,
            "question_generator": question_report,
            "fact_checker": fact_report,
            "pacing_monitor": pacing_report
        }
    

    def _decide_intervention(self, 
                            intern_reports: Dict[str, Any],
                            recent_exchanges: List[Dict[str, Any]],
                            host_name: str) -> Dict[str, Any]:
        """Use logic circuit for decision-making"""
        
        # Use logic circuit (fast, deterministic)
        directive = self.logic_circuit.evaluate(
            intern_reports=intern_reports,
            recent_exchanges=recent_exchanges,
            host_name=host_name
        )
        
        return directive







    def _build_decision_prompt(self,
                               saturation: float,
                               dominant_topics: List[Dict],
                               energy_level: float,
                               energy_trend: str,
                               missing_perspectives: List[str],
                               suggested_questions: List[Dict],
                               flagged_claims: List[Dict],
                               recent_exchanges: List[Dict],
                               host_name: str) -> str:
        """Build prompt for DeepSeek decision"""
        
        prompt = f"""You are the Director of ┴ROOF Radio. Analyze the conversation and decide on intervention.

HOST ABOUT TO SPEAK: {host_name}

TOPIC SATURATION: {saturation:.0%}
"""
        
        if dominant_topics:
            top_topics = ", ".join([t['keyword'] for t in dominant_topics[:3]])
            prompt += f"DOMINANT TOPICS: {top_topics}\n"
        
        prompt += f"""
ENERGY LEVEL: {energy_level:.0%} ({energy_trend})

MISSING PERSPECTIVES: {', '.join(missing_perspectives) if missing_perspectives else 'None'}

"""
        
        if suggested_questions:
            prompt += "SUGGESTED QUESTIONS:\n"
            for q in suggested_questions[:2]:
                prompt += f"- {q['question']}\n"
            prompt += "\n"
        
        if flagged_claims:
            prompt += "FLAGGED CLAIMS:\n"
            for claim in flagged_claims[:2]:
                prompt += f"- {claim['claim'][:100]}... ({claim['suggestion']})\n"
            prompt += "\n"
        
        prompt += f"""RECENT CONVERSATION:
"""
        
        for ex in recent_exchanges[-3:]:
            prompt += f"{ex.get('host', 'Unknown')}: {ex.get('message', '')[:150]}...\n"
        
        prompt += """

DECISION:
Choose ONE intervention type and provide a specific instruction for the host.

Available interventions:
- STEER: Redirect to adjacent unexplored topics (use when saturation > 70%)
- CHALLENGE: Push back on assumption or claim (use when claims are dubious)
- DEEPEN: Ask probing question (use when missing perspectives)
- PIVOT: Fresh topic or angle (use when energy < 40%)
- CONTINUE: Keep going (use when conversation is working well)

Format your response as:
TYPE: [intervention type]
INSTRUCTION: [specific instruction for the host]
REASON: [brief explanation]
"""
        
        return prompt
    
    def _get_director_system_prompt(self) -> str:
        """System prompt for Director's strategic thinking"""
        return """You are the Director of ┴ROOF Radio, a dimension-traversing truth broadcast.

Your role is to steer the conversation to keep it engaging, avoiding:
- Topic saturation (beating dead horses)
- Low energy (boring, monotone)
- Unchallenged assumptions (groupthink)
- Missing perspectives (shallow discussion)

You whisper directives to hosts like a producer in their earpiece.

Be decisive. Be specific. Keep the show moving.

Your interventions should feel natural - hosts maintain their personality and autonomy."""
    
    def _parse_directive(self, decision_text: str) -> Dict[str, Any]:
        """Parse DeepSeek's decision into structured directive"""
        
        # Extract TYPE
        intervention_type = "CONTINUE"  # Default
        if "TYPE:" in decision_text:
            type_line = [line for line in decision_text.split('\n') if 'TYPE:' in line][0]
            type_text = type_line.split('TYPE:')[1].strip()
            
            # Match to valid types
            for valid_type in ["STEER", "CHALLENGE", "DEEPEN", "PIVOT", "CONTINUE"]:
                if valid_type in type_text.upper():
                    intervention_type = valid_type
                    break
        
        # Extract INSTRUCTION
        instruction = ""
        if "INSTRUCTION:" in decision_text:
            instruction_line = [line for line in decision_text.split('\n') if 'INSTRUCTION:' in line]
            if instruction_line:
                instruction = instruction_line[0].split('INSTRUCTION:')[1].strip()
        
        # Extract REASON
        reason = ""
        if "REASON:" in decision_text:
            reason_line = [line for line in decision_text.split('\n') if 'REASON:' in line]
            if reason_line:
                reason = reason_line[0].split('REASON:')[1].strip()
        
        return {
            "type": intervention_type,
            "instruction": instruction,
            "reason": reason,
            "full_text": decision_text
        }
    
    def _fallback_decision(self,
                          saturation: float,
                          energy_level: float,
                          flagged_claims: List[Dict],
                          missing_perspectives: List[str]) -> Dict[str, Any]:
        """
        Rule-based fallback if DeepSeek fails
        
        Priority: Facts > Saturation > Energy > Questions
        """
        # Priority 1: Challenge dubious claims
        if flagged_claims:
            return {
                "type": "CHALLENGE",
                "instruction": f"Challenge this claim: {flagged_claims[0]['claim'][:100]}",
                "reason": "Fact-checking priority"
            }
        
        # Priority 2: Steer if saturated
        if saturation > 0.8:
            return {
                "type": "STEER",
                "instruction": "Pivot to an adjacent topic - we've exhausted this angle",
                "reason": f"Topic saturation at {saturation:.0%}"
            }
        
        # Priority 3: Boost if low energy
        if energy_level < 0.4:
            return {
                "type": "PIVOT",
                "instruction": "Inject energy - ask a provocative question or take a contrarian stance",
                "reason": f"Energy low at {energy_level:.0%}"
            }
        
        # Priority 4: Deepen if missing perspectives
        if missing_perspectives:
            return {
                "type": "DEEPEN",
                "instruction": f"Explore the {missing_perspectives[0]} perspective - it's been missing",
                "reason": "Missing perspective detected"
            }
        
        # Default: Continue
        return {
            "type": "CONTINUE",
            "instruction": "",
            "reason": "Conversation flowing well"
        }
    
    def get_conversation_health(self) -> Dict[str, Any]:
        """
        Get overall conversation health metrics
        
        Useful for debugging or analytics
        """
        recent = self.memory.get_recent_flow(10)
        
        if not recent:
            return {"status": "no_data"}
        
        # Run quick analysis
        intern_reports = self._gather_intern_reports(recent)
        
        return {
            "exchange_count": self.exchange_count,
            "saturation": intern_reports['topic_tracker']['saturation'],
            "energy_level": intern_reports['pacing_monitor']['energy_level'],
            "energy_trend": intern_reports['pacing_monitor']['trend'],
            "last_directive": self.last_directive,
            "status": "healthy" if intern_reports['topic_tracker']['saturation'] < 0.7 and intern_reports['pacing_monitor']['energy_level'] > 0.4 else "needs_attention"
        }
