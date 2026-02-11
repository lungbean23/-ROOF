"""
Writers Room - Conversation Direction System

The Writers Room steers ┴ROOF Radio conversations through:
- Director (DeepSeek) - Strategic conversation arc management
- Story Interns (Llama 3.1) - Fast parallel analysis

Components:
- director: Main conversation director/producer
- story_interns: Analysis interns (topic_tracker, question_generator, etc.)

Usage:
    from writers_room import Director
    
    # Initialize director (has its own vector memory)
    director = Director()
    
    # Get directive for next host
    directive = director.get_directive(
        host_name="Goku",
        recent_exchanges=[...],
        current_topic="AI ethics"
    )
    
    # Log what was said
    director.log_exchange(host_name="Goku", message="...")
"""

from .director import Director

__all__ = ['Director']
