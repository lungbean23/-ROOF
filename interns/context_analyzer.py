"""
Context Analyzer for ┴ROOF Radio Interns
Helps interns understand WHAT is actually being discussed
"""

import re
from typing import List, Dict, Set


class ContextAnalyzer:
    def __init__(self, intern):
        self.intern = intern
        
        # Question templates for different aspects
        self.clarifying_questions = {
            "which": ["Which specific {topic}?", "Which type of {topic}?", "Which brand/model of {topic}?"],
            "what": ["What exactly is {topic}?", "What does {topic} do?", "What are the features of {topic}?"],
            "where": ["Where is {topic} used?", "Where can you find {topic}?", "Where is {topic} located?"],
            "when": ["When was {topic} created?", "When is {topic} used?", "When did {topic} become popular?"],
            "why": ["Why use {topic}?", "Why is {topic} important?", "Why do people choose {topic}?"],
            "how": ["How does {topic} work?", "How is {topic} made?", "How do you use {topic}?"]
        }
    
    def extract_main_entities(self, topic: str, conversation_context: str = "") -> List[str]:
        """
        Extract the main entities/subjects being discussed
        
        Examples:
        - "bill recyclers" → ["bill recyclers", "bills", "recyclers", "cash handling"]
        - "Glory Global Solutions" → ["Glory Global Solutions", "cash technology", "ATMs"]
        """
        entities = []
        
        # Start with the main topic
        entities.append(topic)
        
        # Extract key nouns from conversation (simple version)
        # Look for capitalized words (potential proper nouns)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', conversation_context)
        entities.extend(proper_nouns[:3])  # Top 3
        
        # Extract compound nouns from topic
        words = topic.lower().split()
        if len(words) > 1:
            entities.append(words[0])  # First word
            entities.append(words[-1])  # Last word
        
        # Remove duplicates while preserving order
        seen = set()
        unique_entities = []
        for entity in entities:
            entity_lower = entity.lower()
            if entity_lower not in seen:
                seen.add(entity_lower)
                unique_entities.append(entity)
        
        self.intern.log("ENTITIES_EXTRACTED", f"Found entities: {unique_entities}")
        return unique_entities[:5]  # Top 5 entities
    
    def identify_knowledge_gaps(self, topic: str, conversation_context: str, 
                                researched_topics: Set[str]) -> List[Dict[str, str]]:
        """
        Identify what we DON'T know yet
        
        Returns list of knowledge gaps with suggested research queries
        """
        gaps = []
        
        # Extract entities
        entities = self.extract_main_entities(topic, conversation_context)
        main_entity = entities[0] if entities else topic
        
        # Check each question type
        for question_type, templates in self.clarifying_questions.items():
            for template in templates:
                query = template.format(topic=main_entity)
                search_query = f"{main_entity} {question_type}"
                
                # Skip if we've already researched this angle
                if search_query.lower() not in researched_topics:
                    gaps.append({
                        "question": query,
                        "search_query": search_query,
                        "question_type": question_type,
                        "entity": main_entity
                    })
        
        self.intern.log("GAPS_IDENTIFIED", f"Found {len(gaps)} knowledge gaps")
        return gaps
    
    def prioritize_research_angle(self, knowledge_gaps: List[Dict[str, str]], 
                                  conversation_stage: int) -> Dict[str, str]:
        """
        Choose the BEST research angle based on conversation stage
        
        Early conversation: Start with "what" and "which"
        Mid conversation: Focus on "how" and "why"  
        Late conversation: Explore "where" and "when"
        """
        
        if not knowledge_gaps:
            return None
        
        # Priority order based on conversation stage
        if conversation_stage <= 2:
            # Early: Define and specify
            priority = ["which", "what", "where"]
        elif conversation_stage <= 5:
            # Mid: Explain and analyze
            priority = ["how", "why", "what"]
        else:
            # Late: Context and history
            priority = ["when", "where", "why"]
        
        # Find first gap matching priority
        for question_type in priority:
            for gap in knowledge_gaps:
                if gap["question_type"] == question_type:
                    self.intern.log("ANGLE_PRIORITIZED", 
                                   f"Selected {question_type} question: {gap['question']}")
                    return gap
        
        # Fallback: return first available
        return knowledge_gaps[0]
    
    def generate_targeted_query(self, gap: Dict[str, str], 
                               intern_personality: str) -> str:
        """
        Generate a specific, targeted search query based on the knowledge gap
        
        Taco: Forward-looking, technical, recent
        Clunt: Critical, historical, alternative
        """
        entity = gap["entity"]
        question_type = gap["question_type"]
        
        # Base query
        base_query = gap["search_query"]
        
        # Customize based on intern personality
        if intern_personality == "Taco":
            # Taco adds: latest, technology, innovation keywords
            modifiers = {
                "which": f"best {entity} 2024 2025",
                "what": f"{entity} features specifications",
                "how": f"{entity} how it works technology",
                "why": f"{entity} benefits advantages",
                "where": f"{entity} market applications",
                "when": f"{entity} latest developments"
            }
        else:  # Clunt
            # Clunt adds: criticism, history, alternatives
            modifiers = {
                "which": f"{entity} comparison alternatives",
                "what": f"{entity} overview history",
                "how": f"{entity} problems issues",
                "why": f"{entity} criticism drawbacks",
                "where": f"{entity} usage limitations",
                "when": f"{entity} history evolution"
            }
        
        targeted_query = modifiers.get(question_type, base_query)
        
        self.intern.log("QUERY_GENERATED", f"Targeted query: {targeted_query}")
        return targeted_query
