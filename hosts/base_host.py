"""
Base Host class for ┴ROOF Radio
All hosts inherit from this and implement intelligent conversation
"""

from pathlib import Path
from datetime import datetime
import json


class BaseHost:
    def __init__(self, name, model, personality, style, voice_archetype, intern_name, logs_dir="logs/hosts"):
        self.name = name
        self.model = model
        self.personality = personality
        self.style = style
        self.voice_archetype = voice_archetype
        self.intern_name = intern_name
        
        # Setup logging
        self.logs_dir = Path(logs_dir)
        self.general_log_dir = self.logs_dir / "general"
        self.general_log_dir.mkdir(parents=True, exist_ok=True)
        
        # Track conversation history (what we've already said)
        self.conversation_history = []
        self.topics_discussed = set()
        self.key_points_made = []
        
        # Buffering state
        self.next_response = None
        self.is_buffering = False
    
    def log(self, event_type, message, data=None):
        """Log host activity"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "host": self.name,
            "event": event_type,
            "message": message
        }
        
        if data:
            log_entry["data"] = data
        
        # Write to daily log file
        log_file = self.general_log_dir / f"{self.name.lower()}_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {event_type}: {message}\n")
            if data:
                f.write(f"  DATA: {json.dumps(data, indent=2)}\n")
        
        return log_entry
    
    def has_discussed(self, topic_key):
        """Check if we've already discussed this specific point"""
        return topic_key.lower() in self.topics_discussed
    
    def mark_discussed(self, topic_key):
        """Mark a topic as discussed"""
        self.topics_discussed.add(topic_key.lower())
        self.log("TOPIC_DISCUSSED", f"Marked '{topic_key}' as discussed")
    
    def add_key_point(self, point):
        """Track key points made in conversation"""
        self.key_points_made.append({
            "point": point,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 20 points to avoid bloat
        if len(self.key_points_made) > 20:
            self.key_points_made = self.key_points_made[-20:]
    
    def get_recent_points(self, limit=5):
        """Get recently made key points"""
        return [p["point"] for p in self.key_points_made[-limit:]]
    
    def should_avoid_repetition(self, potential_point):
        """Check if this point is too similar to recent points"""
        recent = self.get_recent_points()
        
        # Simple similarity check - could be enhanced
        for recent_point in recent:
            # If 50%+ of words overlap, it's repetitive
            words_potential = set(potential_point.lower().split())
            words_recent = set(recent_point.lower().split())
            
            if len(words_potential) == 0:
                continue
                
            overlap = len(words_potential & words_recent)
            similarity = overlap / len(words_potential)
            
            if similarity > 0.5:
                self.log("REPETITION_DETECTED", f"Point too similar to recent statement")
                return True
        
        return False
