"""
Trillium Botanical - Deep Continuity

Like a trillium's persistent rhizome and three-petaled symmetry,
this botanical maintains deep memory and balanced perspective
across conversations.

Components:
- rhizome: Deep persistent memory (themes, insights, wisdom)
- three_petals: Triple verification (past, present, future)

Usage:
    from botanicals.Trillium import rhizome, three_petals
    
    # During healthy conversation:
    rhiz = rhizome.TrilliumRhizome()
    rhiz.deepen_roots(themes, insights)
    
    # For balanced perspective:
    petals = three_petals.TrilliumThreePetals()
    verification = petals.verify_statement(statement, past, present, future)
"""

from .rhizome import TrilliumRhizome
from .three_petals import TrilliumThreePetals

__all__ = ['TrilliumRhizome', 'TrilliumThreePetals']
