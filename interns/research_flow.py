"""
Standard Research Flow for ┴ROOF Radio Interns
Intelligently selects research topics and avoids duplicates
"""

import re
from .context_analyzer import ContextAnalyzer


class ResearchFlow:
    def __init__(self, intern):
        self.intern = intern
        self.context_analyzer = ContextAnalyzer(intern)
    
    def identify_research_angle(self, main_topic, conversation_context, conversation_stage=1):
        """
        Identify what NEW angle to research based on conversation
        
        NEW STRATEGY:
        1. Analyze context to understand what's being discussed
        2. Identify knowledge gaps (What don't we know?)
        3. Generate clarifying questions (Which? What? Where?)
        4. Prioritize based on conversation stage
        5. Create targeted search query
        
        Returns:
            Tuple of (research_query, clarifying_question)
        """
        self.intern.log("ANGLE_IDENTIFICATION", f"Analyzing '{main_topic}' at stage {conversation_stage}")
        
        # Step 1: Identify knowledge gaps
        knowledge_gaps = self.context_analyzer.identify_knowledge_gaps(
            main_topic,
            conversation_context,
            self.intern.researched_topics
        )
        
        if not knowledge_gaps:
            # Fallback to simple approach
            self.intern.log("NO_GAPS", "No clear gaps found, using simple strategy")
            return self._simple_angle_selection(main_topic, conversation_context)
        
        # Step 2: Prioritize which gap to research
        selected_gap = self.context_analyzer.prioritize_research_angle(
            knowledge_gaps,
            conversation_stage
        )
        
        if not selected_gap:
            return self._simple_angle_selection(main_topic, conversation_context)
        
        # Step 3: Generate targeted query
        targeted_query = self.context_analyzer.generate_targeted_query(
            selected_gap,
            self.intern.name
        )
        
        clarifying_question = selected_gap["question"]
        
        self.intern.log("ANGLE_SELECTED", 
                       f"Question: {clarifying_question} | Query: {targeted_query}")
        
        return targeted_query, clarifying_question
    
    def _simple_angle_selection(self, main_topic, conversation_context):
        """
        Fallback to simple angle selection if context analysis doesn't work
        """
        # Start with base topic
        if not self.intern.has_researched(main_topic):
            self.intern.log("ANGLE_SELECTED", f"Base topic not yet researched: '{main_topic}'")
            return main_topic, f"What is {main_topic}?"
        
        # Generate related angles based on intern personality
        potential_angles = self._generate_angles(main_topic, conversation_context)
        
        # Find first unresearched angle
        for angle in potential_angles:
            if not self.intern.has_researched(angle):
                self.intern.log("ANGLE_SELECTED", f"New angle selected: '{angle}'")
                return angle, f"Tell me about {angle}"
        
        # If all angles researched, create a more specific one
        specific_angle = f"{main_topic} recent developments"
        self.intern.log("ANGLE_SELECTED", f"All angles exhausted, trying: '{specific_angle}'")
        return specific_angle, f"What are recent developments in {main_topic}?"
    
    def _generate_angles(self, main_topic, conversation_context):
        """
        Generate potential research angles based on intern role
        
        Taco focuses on: recent developments, technical details, innovations
        Clunt focuses on: controversies, alternatives, criticisms, history
        """
        angles = []
        
        if self.intern.name == "Taco":
            # Taco's angles: forward-looking, technical
            angles = [
                f"{main_topic} latest news",
                f"{main_topic} technology",
                f"{main_topic} innovations",
                f"{main_topic} future trends",
                f"{main_topic} market analysis"
            ]
        elif self.intern.name == "Clunt":
            # Clunt's angles: critical, historical, alternative
            angles = [
                f"{main_topic} criticism",
                f"{main_topic} alternatives",
                f"{main_topic} history",
                f"{main_topic} controversies",
                f"{main_topic} drawbacks"
            ]
        else:
            # Generic angles
            angles = [
                f"{main_topic} overview",
                f"{main_topic} analysis",
                f"{main_topic} information"
            ]
        
        # Log generated angles
        self.intern.log("ANGLES_GENERATED", f"Generated {len(angles)} potential angles", 
                       {"angles": angles})
        
        return angles
    
    def execute_research(self, research_query, search_function):
        """
        Execute web research with logging
        
        Args:
            research_query: What to search for
            search_function: Function that performs the actual search
        
        Returns:
            Raw search results
        """
        self.intern.log("RESEARCH_START", f"Executing search for: '{research_query}'")
        
        try:
            results = search_function(research_query)
            
            result_count = len(results) if results else 0
            self.intern.log("RESEARCH_COMPLETE", 
                          f"Found {result_count} results for '{research_query}'",
                          {"result_count": result_count})
            
            # Mark this topic as researched
            self.intern.mark_researched(research_query)
            
            return results
            
        except Exception as e:
            self.intern.log("RESEARCH_ERROR", f"Search failed: {str(e)}")
            return []
