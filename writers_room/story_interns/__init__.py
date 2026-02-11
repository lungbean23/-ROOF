"""
Story Interns - Fast Analysis for Writers Room

Story interns provide rapid parallel analysis to the Director:
- Topic Tracker: Monitors topic saturation
- Question Generator: Identifies missing perspectives
- Fact Checker: Flags dubious claims
- Pacing Monitor: Detects energy drops

All interns use Llama 3.1 for fast, lightweight analysis.

Usage:
    from writers_room.story_interns import TopicTracker, QuestionGenerator
    
    tracker = TopicTracker()
    report = tracker.analyze(recent_exchanges)
    
    if report['saturation'] > 0.8:
        print("Topic saturated - need pivot!")
"""

from .topic_tracker import TopicTracker
from .question_generator import QuestionGenerator
from .fact_checker import FactChecker
from .pacing_monitor import PacingMonitor

__all__ = [
    'TopicTracker',
    'QuestionGenerator', 
    'FactChecker',
    'PacingMonitor'
]
