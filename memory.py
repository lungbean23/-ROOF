"""
Simple memory system for ┴ROOF Radio
Stores conversation history and allows hosts to reference past discussions
"""

import json
import os
from datetime import datetime
from pathlib import Path

class Memory:
    def __init__(self, logs_dir="logs"):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Create debug log directory
        self.debug_dir = self.logs_dir / "debug"
        self.debug_dir.mkdir(exist_ok=True)
        
        self.current_session = {
            "topic": "",
            "started_at": "",
            "exchanges": []
        }
        self.debug_log = []
    
    def start_session(self, topic):
        """Start a new conversation session"""
        self.current_session = {
            "topic": topic,
            "started_at": datetime.now().isoformat(),
            "exchanges": []
        }
        self.debug_log = []
        self._log_debug("SESSION_START", f"Starting new session: {topic}")
    
    def add_exchange(self, host_name, message, research_context=None):
        """Add a host's message to the current session"""
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "host": host_name,
            "message": message,
            "research": research_context
        }
        self.current_session["exchanges"].append(exchange)
        self._log_debug("EXCHANGE", f"{host_name}: {len(message)} chars, research: {bool(research_context)}")
    
    def _log_debug(self, event_type, message):
        """Log debug information about background processes"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "message": message
        }
        self.debug_log.append(log_entry)
        
        # Also print to a debug log file in real-time
        debug_file = self.debug_dir / f"debug_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(debug_file, 'a') as f:
            f.write(f"[{log_entry['timestamp']}] {event_type}: {message}\n")
    
    def log_research(self, intern_name, topic, findings, source="web"):
        """Log research activity with important note about broadening vs grounding"""
        self._log_debug("RESEARCH", 
            f"{intern_name} researched '{topic}' via {source} - found {len(findings)} items")
        self._log_debug("RESEARCH_NOTE",
            "Note: Web research BROADENS conversation context but does not necessarily GROUND it in truth")
        
        # Log actual findings
        for i, finding in enumerate(findings, 1):
            self._log_debug("RESEARCH_FINDING", f"{intern_name} #{i}: {finding[:100]}...")
    
    def save_session(self):
        """Save current session to disk"""
        if not self.current_session["exchanges"]:
            return None
        
        # Create filename from topic and timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_topic = "".join(c for c in self.current_session["topic"] if c.isalnum() or c in (' ', '-', '_'))
        safe_topic = safe_topic.replace(' ', '-').lower()[:50]
        filename = f"{timestamp}_{safe_topic}.json"
        
        # Save conversation
        filepath = self.logs_dir / filename
        with open(filepath, 'w') as f:
            json.dump(self.current_session, f, indent=2)
        
        # Save debug log separately
        debug_filename = f"{timestamp}_{safe_topic}_DEBUG.json"
        debug_filepath = self.debug_dir / debug_filename
        with open(debug_filepath, 'w') as f:
            json.dump({
                "session": self.current_session["topic"],
                "started_at": self.current_session["started_at"],
                "debug_log": self.debug_log
            }, f, indent=2)
        
        self._log_debug("SESSION_END", f"Saved to {filepath}")
        
        return filepath
    
    def get_recent_topics(self, limit=5):
        """Get recently discussed topics"""
        log_files = sorted(self.logs_dir.glob("*.json"), reverse=True)[:limit]
        topics = []
        
        for log_file in log_files:
            try:
                with open(log_file) as f:
                    data = json.load(f)
                    topics.append(data.get("topic", "Unknown"))
            except:
                continue
        
        return topics
    
    def get_conversation_summary(self):
        """Get a brief summary of the current conversation for context"""
        if len(self.current_session["exchanges"]) < 2:
            return ""
        
        summary = f"We've been discussing: {self.current_session['topic']}\n"
        summary += f"Exchange count: {len(self.current_session['exchanges'])}\n"
        
        # Get last 2 exchanges for immediate context
        recent = self.current_session["exchanges"][-2:]
        summary += "Recent points:\n"
        for ex in recent:
            summary += f"- {ex['host']}: {ex['message'][:100]}...\n"
        
        return summary
