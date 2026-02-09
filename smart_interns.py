"""
Smart Interns for ┴ROOF Radio
Uses modular research flows with full transparency
"""

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

from interns.base_intern import BaseIntern
from interns.research_flow import ResearchFlow
from interns.fact_check_flow import FactCheckFlow
from interns.digest import digest_web_results, format_findings_for_host


class SmartIntern(BaseIntern):
    def __init__(self, name, model, role, style):
        super().__init__(name, model, role, style)
        
        # Initialize flows
        self.research_flow = ResearchFlow(self)
        self.fact_check_flow = FactCheckFlow(self)
        
        # Track conversation progression
        self.conversation_stage = 0  # Increments with each research
        
        self.log("INTERN_INITIALIZED", f"{name} ready for research")
    
    def research(self, topic, previous_context=None):
        """
        Main research method - orchestrates the full research flow
        
        ENHANCED FLOW:
        1. Increment conversation stage
        2. Analyze context and identify knowledge gaps
        3. Generate clarifying question (Which? What? Where?)
        4. Execute targeted web search
        5. Digest and compress findings
        6. Return brief WITH clarifying question for host
        
        Returns research brief for host
        """
        print(f"[{self.name} researching...]", flush=True)
        
        self.conversation_stage += 1
        self.log("RESEARCH_SESSION_START", 
                f"Topic: {topic} | Stage: {self.conversation_stage}")
        
        # Step 1: Identify what to research with clarifying question
        research_query, clarifying_question = self.research_flow.identify_research_angle(
            topic, 
            previous_context or "",
            self.conversation_stage
        )
        
        self.log("CLARIFYING_QUESTION", 
                f"Asking: {clarifying_question} | Searching: {research_query}")
        
        # Step 2: Execute search
        raw_results = self.research_flow.execute_research(
            research_query, 
            self._web_search
        )
        
        # Step 3: Digest and compress
        digested = digest_web_results(raw_results, max_findings=3)
        self.log("DIGEST_COMPLETE", f"Compressed {len(raw_results)} results into {len(digested)} findings")
        
        # Step 4: Format for host
        formatted_findings = format_findings_for_host(digested, self.name, research_query)
        
        # Step 5: Inject clarifying question into findings
        if formatted_findings:
            # Add the question at the start
            formatted_findings.insert(0, f"[{self.name} wonders: {clarifying_question}]")
        
        # Step 6: Log final brief
        self.log("BRIEF_PREPARED", f"Prepared brief with {len(formatted_findings)} findings",
                {"findings": formatted_findings, "question": clarifying_question})
        
        # Build research brief
        research_brief = {
            "intern": self.name,
            "query": research_query,
            "clarifying_question": clarifying_question,
            "findings": formatted_findings,
            "raw_result_count": len(raw_results),
            "digest_count": len(digested),
            "conversation_stage": self.conversation_stage,
            "researched_topics": self.get_research_summary(),
            "disclaimer": "Web research broadens context but does not guarantee truth"
        }
        
        self.log("RESEARCH_SESSION_END", "Brief delivered to host")
        
        return research_brief
    
    def _web_search(self, query):
        """
        Perform actual web search
        Returns raw results for digestion
        """
        if DDGS is None:
            self.log("SEARCH_ERROR", "DDGS not available")
            return []
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                self.log("SEARCH_SUCCESS", f"Retrieved {len(results)} results for '{query}'")
                return results
        
        except Exception as e:
            self.log("SEARCH_FAILED", f"Error: {str(e)}")
            return []


def create_intern(name, config):
    """Factory function to create a smart intern"""
    intern_config = config["interns"][name]
    return SmartIntern(
        name=intern_config["name"],
        model=intern_config["model"],
        role=intern_config["role"],
        style=intern_config["style"]
    )
