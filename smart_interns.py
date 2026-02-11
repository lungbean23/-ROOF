"""
Smart Interns for ┴ROOF Radio - Enhanced with Vector Memory
Scalable architecture: Each intern maintains persistent research history

Design Philosophy:
- Each intern is independent with own memory/personality
- Interns are listable/iterable for easy scaling
- State persists across sessions via vector DB
- Future: N interns with different angles all working in parallel
"""

from interns import BaseIntern, ResearchFlow, FactCheckFlow
from interns import digest_web_results, format_findings_for_host
from vector_memory import VectorConversationMemory
from ddgs import DDGS


class SmartIntern(BaseIntern):
    """
    Enhanced intern with persistent vector memory
    
    Each intern maintains their own research database for:
    - Building on previous findings
    - Avoiding duplicate searches
    - Cross-referencing information
    - Providing richer context over time
    """
    
    def __init__(self, name, model, role, style):
        super().__init__(name, model, role, style)
        
        # NEW: Persistent vector memory for this intern
        self.research_memory = VectorConversationMemory(
            host_name=f"Intern_{name}",
            persist_dir=f"data/{name.lower()}_research"
        )
        
        # Initialize flows
        self.research_flow = ResearchFlow(self)
        self.fact_check_flow = FactCheckFlow(self)
        
        # Track conversation progression
        self.conversation_stage = 0  # Increments with each research
        
        self.log("INTERN_INITIALIZED", f"{name} ready with vector memory at data/{name.lower()}_research")
    
    def research(self, topic, previous_context=None):
        """
        Main research method - orchestrates the full research flow
        
        ENHANCED FLOW:
        1. Check research memory for relevant past findings
        2. Increment conversation stage
        3. Analyze context and identify knowledge gaps
        4. Generate clarifying question (Which? What? Where?)
        5. Execute targeted web search
        6. Digest and compress findings
        7. Store findings in vector memory
        8. Return enriched brief WITH clarifying question for host
        
        Returns research brief for host
        """
        print(f"[{self.name} researching...]", flush=True)
        
        self.conversation_stage += 1
        self.log("RESEARCH_SESSION_START", 
                f"Topic: {topic} | Stage: {self.conversation_stage}")
        
        # STEP 1: Check if we have relevant past research
        past_research = self._recall_relevant_research(topic)
        
        # STEP 2: Identify what angle to research
        research_query, clarifying_question = self.research_flow.identify_research_angle(
            topic,
            previous_context or "",
            self.conversation_stage
        )
        
        self.log("CLARIFYING_QUESTION", 
                f"Asking: {clarifying_question} | Searching: {research_query}")
        
        # STEP 3: Execute web search
        results = self.research_flow.execute_research(
            research_query,
            self._web_search
        )
        
        if not results:
            self.log("RESEARCH_FAILED", "No results found")
            return self._empty_brief(topic, clarifying_question)
        
        # STEP 4: Digest results into findings
        digested = digest_web_results(results, max_findings=3)
        self.log("DIGEST_COMPLETE", f"Compressed {len(results)} results into {len(digested)} findings")
        
        # STEP 5: Format for host
        formatted_findings = format_findings_for_host(digested, self.name, topic)
        
        # STEP 6: Store findings in vector memory for future reference
        self._store_research_findings(topic, research_query, formatted_findings, results)
        
        # STEP 7: Build enriched brief
        brief = {
            "intern": self.name,
            "topic": topic,
            "findings": [
                f"[{self.name} wonders: {clarifying_question}]",  # Context for host
                *formatted_findings  # Actual findings
            ],
            "question": clarifying_question,
            "search_query": research_query,
            "past_research_available": bool(past_research)  # Signal if we have historical context
        }
        
        self.log("BRIEF_PREPARED", f"Prepared brief with {len(formatted_findings)} findings",
                {"findings": formatted_findings})
        self.log("RESEARCH_SESSION_END", "Brief delivered to host")
        
        return brief
    
    def _recall_relevant_research(self, topic):
        """
        Check vector memory for relevant past research
        
        Returns:
            List of relevant past findings or empty list
        """
        try:
            # Search our research memory for similar topics
            relevant = self.research_memory.get_relevant_context(topic, n_results=3)
            
            if relevant:
                self.log("MEMORY_RECALL", 
                        f"Found {len(relevant)} relevant past research entries",
                        {"topics": [r.get('message', '')[:50] for r in relevant]})
            
            return relevant
            
        except Exception as e:
            self.log("MEMORY_ERROR", f"Failed to recall research: {e}")
            return []
    
    def _store_research_findings(self, topic, query, findings, raw_results):
        """
        Store research findings in vector memory for future use
        
        This allows interns to:
        - Build on previous work
        - Avoid duplicate searches
        - Cross-reference information
        """
        try:
            # Create a summary of what we found
            research_summary = f"Research on '{query}': {' | '.join(findings[:2])}"
            
            # Store in vector DB with metadata
            self.research_memory.add_exchange(
                message=research_summary,
                other_host_message=None,
                research_context={
                    "topic": topic,
                    "query": query,
                    "findings": findings,
                    "result_count": len(raw_results),
                    "stage": self.conversation_stage
                }
            )
            
            self.log("MEMORY_STORED", f"Stored research findings for '{query}'")
            
        except Exception as e:
            self.log("MEMORY_STORE_ERROR", f"Failed to store findings: {e}")
    
    def _web_search(self, query):
        """Execute DuckDuckGo search"""
        try:
            with DDGS() as search:
                results = list(search.text(query, max_results=5))
                self.log("SEARCH_SUCCESS", f"Retrieved {len(results)} results for '{query}'")
                return results
        except Exception as e:
            self.log("SEARCH_ERROR", f"Search failed: {str(e)}")
            return []
    
    def _empty_brief(self, topic, question):
        """Return empty brief when research fails"""
        return {
            "intern": self.name,
            "topic": topic,
            "findings": [
                f"[{self.name} wonders: {question}]",
                f"No substantial information found for '{topic}'"
            ],
            "question": question,
            "search_query": topic
        }
    
    def get_research_stats(self):
        """
        Get statistics about this intern's research history
        
        Useful for debugging and analytics
        """
        try:
            # Get recent research from vector memory
            recent = self.research_memory.get_recent_flow(n_exchanges=10)
            
            return {
                "intern_name": self.name,
                "current_stage": self.conversation_stage,
                "topics_researched": len(self.researched_topics),
                "memory_entries": len(recent),
                "memory_location": f"data/{self.name.lower()}_research"
            }
        except Exception as e:
            return {
                "intern_name": self.name,
                "error": str(e)
            }


def create_intern(name, config):
    """
    Factory function to create an intern
    
    Designed for scalability - easy to create N interns:
    
    interns = [create_intern(name, config) for name in ["Taco", "Clunt", "Nova", "Zephyr"]]
    """
    intern_config = config["interns"][name]
    return SmartIntern(
        name=intern_config["name"],
        model=intern_config.get("model", "llama3.1:8b"),
        role=intern_config["role"],
        style=intern_config["style"]
    )


def create_intern_pool(config, intern_names=None):
    """
    Create a pool of interns for parallel research
    
    Args:
        config: Configuration dict
        intern_names: List of intern names to create, or None for all
    
    Returns:
        Dict of {intern_name: SmartIntern instance}
    
    Example:
        # Create just Taco and Clunt (current)
        pool = create_intern_pool(config, ["Taco", "Clunt"])
        
        # Create all available interns (future)
        pool = create_intern_pool(config)
        
        # Assign to hosts
        for host in hosts:
            host.intern = pool[host.assigned_intern_name]
    """
    if intern_names is None:
        # Create all interns defined in config
        intern_names = list(config["interns"].keys())
    
    pool = {}
    for name in intern_names:
        if name in config["interns"]:
            pool[name] = create_intern(name, config)
            print(f"[✓ Intern {name} added to pool with vector memory]")
        else:
            print(f"[✗ Intern {name} not found in config]")
    
    return pool
