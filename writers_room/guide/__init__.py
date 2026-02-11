"""
Writers Room Guide System (Phase 1: Observation Mode)

The Guide system tracks strategic conversation elements:
- The Point: Gravitational center of conversation
- Arc Tracking: Host narrative threads (Phase 4+)
- Relationship Graph: Arc interactions (Phase 4+)

Current Phase: 1 (Observation Only)
- The Point observes and logs conversation essence
- No influence on directives or host behavior
- Pure data collection for tuning
"""

from .the_point import ThePoint

__all__ = ['ThePoint']

# Phase status
PHASE = 1
PHASE_NAME = "Observation Mode"
ACTIVE_COMPONENTS = ["ThePoint"]
