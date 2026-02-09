"""
┴ROOF Radio Interns Package
Research assistants with full transparency and smart workflows
"""

from .base_intern import BaseIntern
from .research_flow import ResearchFlow
from .fact_check_flow import FactCheckFlow
from .digest import digest_web_results, format_findings_for_host

__all__ = [
    'BaseIntern',
    'ResearchFlow', 
    'FactCheckFlow',
    'digest_web_results',
    'format_findings_for_host'
]
