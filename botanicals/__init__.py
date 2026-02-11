"""
Botanicals - Complementary Memory Systems for ┴ROOF Radio

Two separate botanical tools used by hosts and interns:

TARAXACUM (Dandelion) - Emergency Diversification
    - Activates on approaching context death
    - Scatters variant seeds for next conversation
    - Strategy: Quantity, diversity, rapid dispersal

TRILLIUM - Deep Continuity
    - Activates during healthy conversation flow
    - Builds persistent wisdom across sessions
    - Strategy: Quality, persistence, balance

These COMPLEMENT the primary buffer (vector_memory_qdrant.py):
    - Buffer: Short-term cache (seconds to minutes, 67-75% hit rate)
    - Trillium: Long-term memory (themes across conversation)
    - Taraxacum: Genetic memory (survival across death)

Usage by hosts/interns:
    from botanicals.taraxacum import TaraxacumSeedSpreader, TaraxacumGerminator
    from botanicals.trillium import TrilliumRhizome, TrilliumThreePetals
    
    # Emergency response:
    if context_pressure > 0.8:
        spreader.prepare_for_death(state)
    
    # Continuity building:
    if conversation_depth > 3:
        rhizome.deepen_roots(themes)
"""

from . import taraxacum
from . import trillium

__all__ = ['taraxacum', 'trillium']
