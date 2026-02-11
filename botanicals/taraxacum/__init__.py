"""
Taraxacum Botanical - Emergency Diversification

Like a dandelion spreading seeds before death, this botanical
scatters variant conversation seeds when context overflow approaches.

Components:
- seed_spreader: Extracts DNA and generates variant seeds on death
- germinator: Selects and activates seeds on startup

Usage:
    from botanicals.Taraxacum import seed_spreader, germinator
    
    # On approaching context death:
    spreader = seed_spreader.TaraxacumSeedSpreader()
    spreader.prepare_for_death(conversation_state)
    
    # On next startup:
    germ = germinator.TaraxacumGerminator()
    seed = germ.select_seed(host_name, user_query)
    context = germ.germinate_seed(seed)
"""

from .seed_spreader import TaraxacumSeedSpreader
from .germinator import TaraxacumGerminator

__all__ = ['TaraxacumSeedSpreader', 'TaraxacumGerminator']
