"""
Base Intern class for ┴ROOF Radio
All interns inherit from this and implement research flows
"""

import time
from pathlib import Path
from datetime import datetime
import json


class BaseIntern:
    def __init__(self, name, model, role, style, logs_dir="logs/interns"):
        self.name = name
        self.model = model
        self.role = role
        self.style = style
        
        # Setup logging
        self.logs_dir = Path(logs_dir)
        self.general_log_dir = self.logs_dir / "general"
        self.general_log_dir.mkdir(parents=True, exist_ok=True)
        
        # Track research history
        self.researched_topics = set()
        self.research_history = []
        
    def log(self, event_type, message, data=None):
        """Log intern activity with full transparency"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "intern": self.name,
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
    
    def has_researched(self, topic):
        """Check if this topic has already been researched"""
        return topic.lower() in self.researched_topics
    
    def mark_researched(self, topic):
        """Mark a topic as researched"""
        self.researched_topics.add(topic.lower())
        self.log("TOPIC_MARKED", f"Marked '{topic}' as researched")
    
    def get_research_summary(self):
        """Get summary of what's been researched so far"""
        return list(self.researched_topics)
