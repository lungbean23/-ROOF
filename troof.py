#!/usr/bin/env python3
"""
┴ROOF Radio - Truth with a speech impediment
An infinite AI conversation where Goku and Homer seek truth together
"""

import sys
import json
import time
import signal
from pathlib import Path

from hosts import create_host
from interns import create_intern
from memory import Memory
from tts import get_tts_engine

class TroofRadio:
    def __init__(self, config_path="config.json"):
        # Load configuration
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Initialize components
        self.memory = Memory()
        self.tts = get_tts_engine()
        
        # Create interns
        self.taco = create_intern("taco", self.config)
        self.clunt = create_intern("clunt", self.config)
        
        # Create hosts
        self.goku = create_host("goku", self.config, "taco")
        self.homer = create_host("homer", self.config, "clunt")
        
        # Track state
        self.running = True
        self.exchange_count = 0
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
    
    def shutdown(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n[Shutting down ┴ROOF Radio...]")
        self.running = False
        
        # Save conversation
        filepath = self.memory.save_session()
        if filepath:
            print(f"[Conversation saved to: {filepath}]")
        
        print("[Thanks for listening!]")
        sys.exit(0)
    
    def broadcast(self, topic):
        """Start the infinite conversation on a topic"""
        
        print("\n" + "=" * 80)
        print("┴ROOF RADIO - Truth with a speech impediment")
        print("=" * 80)
        print(f"Topic: {topic}")
        print("Press Ctrl+C to stop the broadcast")
        print("=" * 80 + "\n")
        
        # Preload message to avoid jarring silence
        print("📻 Starting up the studio...")
        print("📻 Warming up the microphones...")
        print("📻 Goku and Homer are getting ready...\n")
        time.sleep(1)
        
        # Initialize memory
        self.memory.start_session(topic)
        
        # Goku starts the conversation
        current_speaker = self.goku
        current_intern = self.taco
        previous_message = None
        
        while self.running:
            try:
                self.exchange_count += 1
                
                # Intern does research
                research = current_intern.research(
                    topic, 
                    previous_context=self.memory.get_conversation_summary()
                )
                
                # Log the research activity
                self.memory.log_research(
                    intern_name=research["intern"],
                    topic=topic,
                    findings=research.get("findings", []),
                    source="web"
                )
                
                # Host speaks
                message = current_speaker.speak(
                    topic=topic,
                    research_brief=research,
                    other_host_message=previous_message,
                    conversation_summary=self.memory.get_conversation_summary()
                )
                
                # Output via TTS (currently just formatted print)
                self.tts.speak(message, current_speaker.name)
                
                # Save to memory
                self.memory.add_exchange(
                    current_speaker.name,
                    message,
                    research
                )
                
                # Prepare for next exchange
                previous_message = message
                
                # Alternate speakers
                if current_speaker == self.goku:
                    current_speaker = self.homer
                    current_intern = self.clunt
                else:
                    current_speaker = self.goku
                    current_intern = self.taco
                
                # Brief pause between exchanges
                time.sleep(self.config["settings"]["exchange_delay"])
                
            except Exception as e:
                print(f"\n[Error in broadcast: {e}]")
                print("[Attempting to continue...]")
                time.sleep(2)


def main():
    """CLI entry point"""
    
    # Check if topic provided
    if len(sys.argv) < 2:
        print("Usage: python troof.py \"Your topic here\"")
        print("\nExample:")
        print("  python troof.py \"Are LLMs actually reasoning?\"")
        sys.exit(1)
    
    topic = " ".join(sys.argv[1:])
    
    # Verify Ollama models are available
    try:
        import ollama
        response = ollama.list()
        
        # Extract model names from the ListResponse object
        model_names = []
        if hasattr(response, 'models'):
            # New Ollama library returns ListResponse with .models attribute
            for model in response.models:
                if hasattr(model, 'model'):
                    model_names.append(model.model)
        elif isinstance(response, dict):
            # Fallback for older versions that return dict
            for m in response.get('models', []):
                if isinstance(m, dict):
                    model_names.append(m.get('name', ''))
        
        required = ['deepseek-r1:14b', 'llama3.1:8b']
        missing = [m for m in required if m not in model_names]
        
        if missing:
            print(f"Error: Missing required Ollama models: {', '.join(missing)}")
            print("\nInstall them with:")
            for model in missing:
                print(f"  ollama pull {model}")
            sys.exit(1)
            
    except ImportError:
        print("Error: ollama Python package not found")
        print("Install with: pip install ollama")
        sys.exit(1)
    except Exception as e:
        print(f"Warning: Could not verify Ollama models: {e}")
        print("Attempting to continue anyway...")
        print("(Make sure deepseek-r1:14b and llama3.1:8b are installed)\n")
    
    # Start the broadcast
    radio = TroofRadio()
    radio.broadcast(topic)


if __name__ == "__main__":
    main()
