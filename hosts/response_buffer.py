"""
Response Buffer System for ┴ROOF Radio
Pre-generates responses to eliminate awkward pauses
"""

import threading
import time
from queue import Queue


class ResponseBuffer:
    def __init__(self, host):
        self.host = host
        self.buffer_queue = Queue(maxsize=2)  # Buffer up to 2 responses ahead
        self.is_active = False
        self.buffer_thread = None
        
        # Track buffer health
        self.buffer_empty_count = 0
        self.total_requests = 0
        
    def start(self):
        """Start the buffer thread"""
        self.is_active = True
        self.buffer_thread = threading.Thread(target=self._buffer_worker, daemon=True)
        self.buffer_thread.start()
        self.host.log("BUFFER_START", "Response buffer activated")
    
    def stop(self):
        """Stop the buffer thread"""
        self.is_active = False
        if self.buffer_thread:
            self.buffer_thread.join(timeout=5)
        self.host.log("BUFFER_STOP", "Response buffer deactivated")
    
    def _buffer_worker(self):
        """Background thread that pre-generates responses"""
        while self.is_active:
            # If buffer has space, try to fill it
            if not self.buffer_queue.full():
                # This will be filled by prediction logic
                time.sleep(0.1)
            else:
                time.sleep(0.5)
    
    def get_response(self, timeout=None):
        """
        Get next response from buffer
        Falls back to direct generation if buffer is empty
        """
        self.total_requests += 1
        
        try:
            # Try to get from buffer first
            response = self.buffer_queue.get(timeout=timeout or 1.0)
            self.host.log("BUFFER_HIT", "Served response from buffer")
            return response
        except:
            # Buffer miss - log it
            self.buffer_empty_count += 1
            self.host.log("BUFFER_MISS", f"Buffer empty ({self.buffer_empty_count}/{self.total_requests} misses)")
            return None
    
    def queue_response(self, response):
        """Add a pre-generated response to buffer"""
        try:
            self.buffer_queue.put(response, block=False)
            self.host.log("BUFFER_ADD", "Queued pre-generated response")
            return True
        except:
            self.host.log("BUFFER_FULL", "Buffer full, discarding response")
            return False
    
    def get_buffer_health(self):
        """
        Get buffer performance metrics
        Returns hit rate percentage
        """
        if self.total_requests == 0:
            return 100.0
        
        hit_rate = ((self.total_requests - self.buffer_empty_count) / self.total_requests) * 100
        return hit_rate
    
    def should_prebuffer(self):
        """
        Determine if we should start pre-buffering
        Based on buffer level and conversation patterns
        """
        buffer_level = self.buffer_queue.qsize() / 2.0  # Normalize to 0-1
        
        # If buffer is less than 30% full, we should prebuffer
        if buffer_level < 0.3:
            self.host.log("PREBUFFER_TRIGGER", f"Buffer low ({buffer_level:.0%}), triggering prebuffer")
            return True
        
        return False
