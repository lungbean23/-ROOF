"""
Broadcast orchestration for ┴ROOF Radio
Manages the infinite conversation loop with pipeline buffering and topic evolution
+ Writers Room conversation direction
"""

import time
import signal
import sys

from hosts import create_host
from smart_interns import create_intern
from memory import Memory
from tts import get_tts_engine
from pipeline_buffer import PipelineBuffer
from topic_evolver import TopicEvolver
from writers_room import Director  # NEW: Writers Room import
from writers_room.guide import ThePoint

class TroofRadio:
    def __init__(self, config):
        """
        Initialize radio station components
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Initialize components
        self.memory = Memory()
        self.tts = get_tts_engine()
        
        # Initialize pipeline buffer for smooth conversation flow
        self.pipeline = PipelineBuffer()
        
        # Initialize topic evolution for organic conversation
        self.topic_evolver = TopicEvolver(max_history=10)
        self.host_messages = []  # Track host messages for evolution
        
        # NEW: Initialize Writers Room Director
        print("[✍️  Initializing Writers Room Director...]")
        self.director = Director(
            model="deepseek-r1:14b",
            intervention_frequency=3  # Every 3 exchanges
        )
        # Create interns
        self.taco = create_intern("taco", self.config)
        self.clunt = create_intern("clunt", self.config)
        
        # Create hosts
        self.goku = create_host("goku", self.config, "taco")
        self.homer = create_host("homer", self.config, "clunt")
        
        # NEW: Wire director to both hosts
        self.goku.director = self.director
        self.homer.director = self.director
        print("[✍️  Writers Room connected to hosts]")
        
        self.director.goku = self.goku
        self.director.homer = self.homer
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
        
        # NEW: Print conversation health report from Director
        if hasattr(self, 'director'):
            health = self.director.get_conversation_health()
            print(f"[✍️  Conversation health: {health.get('status', 'unknown')}]")
            print(f"[✍️  Final saturation: {health.get('saturation', 0):.0%}]")
            print(f"[✍️  Final energy: {health.get('energy_level', 0):.0%}]")
        
        summary = self.the_point.get_point_summary()
        print(f"\n[📍 Point: '{summary['essence']}' - "
            f"Saturation {summary['saturation']:.0%}]")
        print("[Thanks for listening!]")
        sys.exit(0)
    
    def broadcast(self, topic):
        """
        Start the infinite conversation on a topic
        
        Args:
            topic: Topic to discuss
        """
        self.the_point = ThePoint(topic)
        print(f"[📍 The Point tracking: '{topic}']")
        self.director.set_the_point(self.the_point) 
        self.director.point_monitoring = False
        self._print_header(topic)
        self._print_startup_messages()
        
        # Initialize memory
        self.memory.start_session(topic)
        
        # Goku starts the conversation
        current_speaker = self.goku
        current_intern = self.taco
        previous_message = None
        original_topic = topic  # Save original topic for evolution
        
        # Main broadcast loop
        while self.running:
            try:
                self.exchange_count += 1
                
                # Try to get buffered response first (INSTANT if available)
                buffered = self.pipeline.get_buffered_response(timeout=0.1)
                
                if buffered:
                    # Use buffered response (near-zero latency!)
                    current_speaker = buffered["host"]
                    message = buffered["message"]
                    research = buffered["research"]
                    
                    print(f"[✓ Buffer HIT - instant response from {current_speaker.name}]", flush=True)
                else:
                    # Buffer miss - do research and generation live
                    research = self._conduct_research(current_intern, topic, original_topic)
                    message = self._host_speaks(current_speaker, topic, research, previous_message)
                
                # Track host message for topic evolution
                self.host_messages.append(message)
                if len(self.host_messages) > 10:
                    self.host_messages = self.host_messages[-10:]  # Keep last 10
                
                # Determine next speaker/intern
                next_speaker, next_intern = self._alternate_speakers(current_speaker)
                
                # Determine evolved topic for NEXT exchange
                next_topic = topic
                if self.topic_evolver.should_evolve(self.exchange_count + 1):
                    next_topic = self.topic_evolver.evolve_topic(
                        original_topic=original_topic,
                        host_messages=self.host_messages,
                        research_history=[]
                    )
                
                # START PIPELINE for next response BEFORE TTS starts
                # This happens in background while TTS plays
                self.pipeline.start_pipeline(
                    next_intern=next_intern,
                    next_host=next_speaker,
                    topic=next_topic,  # Use evolved topic!
                    current_message=message,
                    conversation_summary=self.memory.get_conversation_summary()
                )
                
                # Output phase (TTS plays while pipeline works in background)
                self.tts.speak(message, current_speaker.name)
                
                # Memory phase
                self._save_exchange(current_speaker.name, message, research)
                self.the_point.update_point_from_exchange(
                    host_name=current_speaker.name,
                    message=message,
                    research_context=research
                )
                # Prepare for next exchange
                previous_message = message
                current_speaker = next_speaker
                current_intern = next_intern
                topic = next_topic  # Update topic to evolved version
                
                # Brief pause between exchanges
                time.sleep(self.config["settings"]["exchange_delay"])
                
            except Exception as e:
                self._handle_error(e)
    
    def _print_header(self, topic):
        """Print broadcast header"""
        print("\n" + "=" * 80)
        print("┴ROOF RADIO - Truth with a speech impediment")
        print("=" * 80)
        print(f"Topic: {topic}")
        print("Press Ctrl+C to stop the broadcast")
        print("=" * 80 + "\n")
    
    def _print_startup_messages(self):
        """Print startup messages to avoid jarring silence"""
        print("📻 Starting up the studio...")
        print("📻 Warming up the microphones...")
        print("📻 Goku and Homer are getting ready...\n")
        time.sleep(1)
    
    def _conduct_research(self, intern, topic, original_topic):
        """
        Intern conducts research on potentially evolved topic
        
        Args:
            intern: The intern doing research
            topic: Current (possibly evolved) topic
            original_topic: Original topic for reference
        
        Returns:
            Research brief
        """
        # Determine if we should evolve the topic
        if self.topic_evolver.should_evolve(self.exchange_count):
            evolved_topic = self.topic_evolver.evolve_topic(
                original_topic=original_topic,
                host_messages=self.host_messages,
                research_history=[]  # Could pass research history here
            )
        else:
            evolved_topic = topic
        
        # Research the (possibly evolved) topic
        research = intern.research(
            evolved_topic, 
            previous_context=self.memory.get_conversation_summary()
        )
        
        # Log the research activity
        self.memory.log_research(
            intern_name=research["intern"],
            topic=evolved_topic,
            findings=research.get("findings", []),
            source="web"
        )
        
        return research
    
    def _host_speaks(self, host, topic, research, previous_message):
        """
        Host generates and returns response
        
        Returns:
            Host's message
        """
        return host.speak(
            topic=topic,
            research_brief=research,
            other_host_message=previous_message,
            conversation_summary=self.memory.get_conversation_summary()
        )
    
    def _save_exchange(self, host_name, message, research):
        """Save exchange to memory"""
        self.memory.add_exchange(host_name, message, research)
    
    def _alternate_speakers(self, current_speaker):
        """
        Alternate between speakers
        
        Returns:
            Tuple of (next_speaker, next_intern)
        """
        if current_speaker == self.goku:
            return self.homer, self.clunt
        else:
            return self.goku, self.taco
    
    def _handle_error(self, error):
        """Handle broadcast errors gracefully"""
        print(f"\n[Error in broadcast: {error}]")
        print("[Attempting to continue...]")
        time.sleep(2)
