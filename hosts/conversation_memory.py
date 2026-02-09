"""
Conversation Memory for ┴ROOF Radio Hosts
Tracks what's been discussed to avoid repetitive exchanges
"""

from collections import deque
from datetime import datetime


class ConversationMemory:
    def __init__(self, host, max_memory=50):
        self.host = host
        self.max_memory = max_memory
        
        # Ring buffer of recent exchanges
        self.exchange_history = deque(maxlen=max_memory)
        
        # Topic tracking
        self.topic_mentions = {}  # topic -> count
        self.last_mention = {}     # topic -> exchange_number
        
        self.exchange_count = 0
    
    def add_exchange(self, message, research_context=None):
        """
        Record an exchange
        Extracts key concepts and tracks repetition
        """
        self.exchange_count += 1
        
        exchange = {
            "number": self.exchange_count,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "research": research_context,
            "key_concepts": self._extract_concepts(message)
        }
        
        self.exchange_history.append(exchange)
        
        # Update topic tracking
        for concept in exchange["key_concepts"]:
            self.topic_mentions[concept] = self.topic_mentions.get(concept, 0) + 1
            self.last_mention[concept] = self.exchange_count
        
        self.host.log("EXCHANGE_RECORDED", f"Exchange #{self.exchange_count} recorded")
    
    def _extract_concepts(self, message):
        """
        Extract key concepts from a message
        Simple word-based extraction for now
        """
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
                     'in', 'on', 'at', 'to', 'for', 'of', 'with', 'this', 'that',
                     'it', 'from', 'as', 'be', 'have', 'has', 'had', 'do', 'does',
                     'we', 'you', 'i', 'they', 'what', 'which', 'who', 'when', 'where'}
        
        words = message.lower().split()
        concepts = [w.strip('.,!?;:') for w in words if len(w) > 3 and w not in stopwords]
        
        return concepts[:10]  # Top 10 concepts
    
    def is_topic_stale(self, topic, staleness_threshold=20):
        """
        Check if a topic has been discussed too recently
        
        Args:
            topic: Topic to check
            staleness_threshold: Number of exchanges that must pass
        
        Returns:
            True if topic is stale (too recent), False if fresh
        """
        if topic.lower() not in self.last_mention:
            return False  # Never mentioned, so fresh
        
        last_mentioned = self.last_mention[topic.lower()]
        exchanges_since = self.exchange_count - last_mentioned
        
        if exchanges_since < staleness_threshold:
            self.host.log("TOPIC_STALE", 
                         f"'{topic}' mentioned {exchanges_since} exchanges ago (threshold: {staleness_threshold})")
            return True
        
        return False
    
    def get_overused_topics(self, threshold=5):
        """
        Get topics that have been mentioned too many times
        
        Returns:
            List of overused topics
        """
        overused = [topic for topic, count in self.topic_mentions.items() 
                   if count >= threshold]
        
        if overused:
            self.host.log("OVERUSED_TOPICS", f"Found {len(overused)} overused topics")
        
        return overused
    
    def get_recent_context(self, num_exchanges=3):
        """
        Get summary of recent conversation
        
        Returns:
            String summary of last N exchanges
        """
        if not self.exchange_history:
            return ""
        
        recent = list(self.exchange_history)[-num_exchanges:]
        
        context = f"Last {len(recent)} exchanges:\n"
        for ex in recent:
            context += f"- Exchange #{ex['number']}: {ex['message'][:100]}...\n"
        
        return context
    
    def should_avoid_topic(self, topic):
        """
        Determine if we should avoid discussing this topic right now
        
        Checks:
        - Is it too recent? (< 20 exchanges ago)
        - Is it overused? (> 5 mentions)
        """
        topic_lower = topic.lower()
        
        # Check staleness
        if self.is_topic_stale(topic):
            return True
        
        # Check overuse
        if topic_lower in self.topic_mentions and self.topic_mentions[topic_lower] > 5:
            self.host.log("TOPIC_OVERUSED", f"'{topic}' mentioned {self.topic_mentions[topic_lower]} times")
            return True
        
        return False
