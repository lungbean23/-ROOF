"""
Topic Evolution System for ┴ROOF Radio
Extracts interesting threads from conversation and evolves research organically
"""

import re
from collections import deque


class TopicEvolver:
    """
    Evolves conversation topics organically based on what hosts actually discuss
    
    Instead of researching "bushido" 20 times, it follows the natural flow:
    bushido → honor → giri → duty vs desire → modern applications
    """
    
    def __init__(self, max_history=10):
        self.conversation_flow = deque(maxlen=max_history)
        self.researched_topics = set()
        self.current_depth = 0
        
    def extract_interesting_concepts(self, host_message, previous_research=None):
        """
        Extract NEW interesting concepts from what the host actually said
        
        Args:
            host_message: What the host just said
            previous_research: Research findings that sparked this response
        
        Returns:
            List of interesting concepts to explore next
        """
        concepts = []
        
        # Extract quoted terms (things in "quotes" are usually specific concepts)
        quoted = re.findall(r'"([^"]+)"', host_message)
        concepts.extend(quoted)
        
        # Extract capitalized phrases (proper nouns, specific terms)
        # Match 2-4 word capitalized phrases
        capitalized = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b', host_message)
        concepts.extend(capitalized)
        
        # Extract parenthetical explanations - these often contain key terms
        # e.g., "duty (giri)" or "honor (bushido)"
        parentheticals = re.findall(r'\(([^)]+)\)', host_message)
        concepts.extend(parentheticals)
        
        # Extract concepts from research findings if provided
        if previous_research and previous_research.get('findings'):
            for finding in previous_research['findings']:
                # Skip the intern's question
                if finding.startswith('['):
                    continue
                    
                # Extract key phrases from titles (before the colon)
                if ':' in finding:
                    title = finding.split(':')[0]
                    # Get last 2-3 words of title (usually the key concept)
                    words = title.split()
                    if len(words) >= 2:
                        key_phrase = ' '.join(words[-2:])
                        concepts.append(key_phrase)
        
        # Deduplicate and filter
        unique_concepts = []
        seen = set()
        
        for concept in concepts:
            concept_lower = concept.lower().strip()
            
            # Skip if too short, too common, or already seen
            if len(concept_lower) < 4:
                continue
            if concept_lower in seen:
                continue
            if concept_lower in self.researched_topics:
                continue
                
            # Skip generic words
            generic_words = {'this', 'that', 'these', 'those', 'what', 'which', 
                           'when', 'where', 'with', 'from', 'about', 'also'}
            if concept_lower in generic_words:
                continue
            
            seen.add(concept_lower)
            unique_concepts.append(concept)
        
        return unique_concepts[:5]  # Top 5 most interesting
    
    def evolve_topic(self, original_topic, host_messages, research_history):
        """
        Evolve the conversation topic based on what's actually being discussed
        
        Args:
            original_topic: The initial topic
            host_messages: Recent messages from hosts
            research_history: Recent research findings
        
        Returns:
            New evolved topic to research
        """
        self.current_depth += 1
        
        # Early conversation: Stay close to original topic
        if self.current_depth <= 3:
            return original_topic
        
        # Mid conversation: Start extracting interesting concepts
        if self.current_depth <= 8:
            # Get last 2 host messages
            recent_messages = host_messages[-2:] if len(host_messages) >= 2 else host_messages
            
            all_concepts = []
            for msg in recent_messages:
                concepts = self.extract_interesting_concepts(msg)
                all_concepts.extend(concepts)
            
            # Pick the first unresearched concept
            for concept in all_concepts:
                if concept.lower() not in self.researched_topics:
                    self.researched_topics.add(concept.lower())
                    self.conversation_flow.append(concept)
                    print(f"[Topic Evolution: {original_topic} → {concept}]")
                    return concept
            
            # No new concepts found, return original
            return original_topic
        
        # Late conversation: Go deep on thread
        if self.current_depth > 8:
            # Look at the last evolved topic
            if self.conversation_flow:
                last_topic = self.conversation_flow[-1]
                
                # Extract sub-concepts from last topic
                concepts = self.extract_interesting_concepts(
                    f"Tell me more about {last_topic}",
                    research_history[-1] if research_history else None
                )
                
                for concept in concepts:
                    if concept.lower() not in self.researched_topics:
                        self.researched_topics.add(concept.lower())
                        self.conversation_flow.append(concept)
                        print(f"[Topic Evolution (deep): {last_topic} → {concept}]")
                        return concept
            
            # Reset depth occasionally to avoid getting too narrow
            if self.current_depth > 15:
                print(f"[Topic Evolution: Resetting to original topic]")
                self.current_depth = 0
                return original_topic
        
        return original_topic
    
    def get_conversation_thread(self):
        """Get the current conversation thread"""
        if not self.conversation_flow:
            return []
        return list(self.conversation_flow)
    
    def should_evolve(self, exchange_count):
        """
        Determine if we should evolve the topic
        
        Args:
            exchange_count: Number of exchanges so far
        
        Returns:
            Boolean
        """
        # Evolve every 2-3 exchanges after the initial setup
        if exchange_count < 4:
            return False
        
        # Evolve more frequently as conversation progresses
        if exchange_count < 10:
            return exchange_count % 3 == 0
        else:
            return exchange_count % 2 == 0
