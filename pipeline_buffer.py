"""
Advanced Pipeline Buffer for ┴ROOF Radio
Parallelizes research, generation, and TTS for near-zero latency
"""

import threading
import queue
import time
from datetime import datetime


class PipelineBuffer:
    """
    Advanced buffering system that parallelizes:
    1. Current host speaking (TTS playing)
    2. Next intern researching
    3. Next host generating response
    
    Result: Near-zero latency between exchanges
    """
    
    def __init__(self):
        # Buffer for completed responses
        self.response_queue = queue.Queue(maxsize=2)
        
        # Pipeline state
        self.pipeline_active = False
        self.pipeline_thread = None
        
        # Current pipeline task
        self.current_task = None
        self.task_lock = threading.Lock()
        
        # Metrics
        self.total_buffered = 0
        self.buffer_hits = 0
        self.buffer_misses = 0
        
        print("[Pipeline Buffer initialized]")
    
    def start_pipeline(self, next_intern, next_host, topic, current_message, conversation_summary):
        """
        Start pipeline for next response while current TTS plays
        
        This runs in the background during TTS playback
        
        Args:
            next_intern: Intern who will research
            next_host: Host who will respond
            topic: Current topic
            current_message: What current host just said
            conversation_summary: Context
        """
        
        def pipeline_worker():
            """Background worker that executes the full pipeline"""
            
            print(f"[Pipeline: Starting background generation for {next_host.name}]", flush=True)
            start_time = time.time()
            
            try:
                # Step 1: Intern research (happens immediately)
                print(f"[Pipeline: {next_intern.name} researching...]", flush=True)
                research = next_intern.research(topic, conversation_summary)
                research_time = time.time() - start_time
                print(f"[Pipeline: Research complete in {research_time:.1f}s]", flush=True)
                
                # Step 2: Host generation (happens while TTS still playing)
                print(f"[Pipeline: {next_host.name} generating...]", flush=True)
                response = next_host.speak(
                    topic=topic,
                    research_brief=research,
                    other_host_message=current_message,
                    conversation_summary=conversation_summary
                )
                generation_time = time.time() - start_time
                print(f"[Pipeline: Generation complete in {generation_time:.1f}s]", flush=True)
                
                # Step 3: Queue the complete package
                buffered_item = {
                    "host": next_host,
                    "message": response,
                    "research": research,
                    "generated_at": datetime.now().isoformat(),
                    "pipeline_time": generation_time
                }
                
                self.response_queue.put(buffered_item, block=False)
                self.total_buffered += 1
                
                total_time = time.time() - start_time
                print(f"[Pipeline: ✓ Response buffered in {total_time:.1f}s]", flush=True)
                
            except queue.Full:
                print(f"[Pipeline: Buffer full, discarding]", flush=True)
            except Exception as e:
                print(f"[Pipeline: Error - {e}]", flush=True)
        
        # Start pipeline in background thread
        self.pipeline_thread = threading.Thread(target=pipeline_worker, daemon=True)
        self.pipeline_thread.start()
    
    def get_buffered_response(self, timeout=0.5):
        """
        Try to get buffered response
        
        Returns:
            Buffered response dict or None if buffer empty
        """
        try:
            buffered = self.response_queue.get(timeout=timeout)
            self.buffer_hits += 1
            
            print(f"[Buffer HIT! Served pre-generated response (hit rate: {self.get_hit_rate():.0%})]", flush=True)
            return buffered
            
        except queue.Empty:
            self.buffer_misses += 1
            print(f"[Buffer MISS - generating live (hit rate: {self.get_hit_rate():.0%})]", flush=True)
            return None
    
    def get_hit_rate(self):
        """Calculate buffer hit rate"""
        total = self.buffer_hits + self.buffer_misses
        if total == 0:
            return 0.0
        return self.buffer_hits / total
    
    def get_stats(self):
        """Get buffer statistics"""
        return {
            "total_buffered": self.total_buffered,
            "buffer_hits": self.buffer_hits,
            "buffer_misses": self.buffer_misses,
            "hit_rate": self.get_hit_rate(),
            "queue_size": self.response_queue.qsize()
        }
