"""
Research interns for ┴ROOF Radio
Taco and Clunt fetch live web context to keep hosts grounded
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from ddgs import DDGS

class Intern:
    def __init__(self, name, model, role, style):
        self.name = name
        self.model = model
        self.role = role
        self.style = style
    
    def research(self, topic, previous_context=None):
        """
        Conduct quick web research on a topic
        Returns a brief with key findings
        
        IMPORTANT: Web research BROADENS the conversation by introducing 
        new perspectives and information, but it does not necessarily 
        GROUND the conversation in verified truth. Sources may be biased,
        outdated, or incorrect.
        """
        print(f"[{self.name} researching...]", flush=True)
        
        # Actual web search
        findings = self._web_search(topic, previous_context)
        
        research_brief = {
            "intern": self.name,
            "findings": findings,
            "timestamp": time.time(),
            "disclaimer": "Web research broadens context but does not guarantee truth"
        }
        
        return research_brief
    
    def _web_search(self, topic, previous_context):
        """
        Perform actual web search and extract key points
        """
        findings = []
        
        try:
            # Use DuckDuckGo search
            with DDGS() as ddgs:
                # Search for the topic
                results = list(ddgs.text(topic, max_results=5))
                
                if results:
                    # Extract key information from top results
                    for i, result in enumerate(results[:3]):  # Top 3 results
                        title = result.get('title', '')
                        snippet = result.get('body', '')
                        
                        # Create a finding from this result
                        if title and snippet:
                            finding = f"{title}: {snippet[:150]}..."
                            findings.append(finding)
                
                # If we got results, personalize based on intern
                if findings:
                    if self.name == "Taco":
                        findings.insert(0, f"Latest info on '{topic}':")
                    else:  # Clunt
                        findings.insert(0, f"Different perspectives on '{topic}':")
                else:
                    findings = [f"Limited recent information found on '{topic}'"]
        
        except Exception as e:
            # Fallback to simulated research if web search fails
            print(f"[{self.name}: Web search failed, using basic context]")
            findings = [
                f"General context: {topic}",
                f"Common discussions around this topic",
                "Web search temporarily unavailable"
            ]
        
        return findings[:3]  # Limit to 3 findings max


def create_intern(name, config):
    """Factory function to create an intern from config"""
    intern_config = config["interns"][name]
    return Intern(
        name=intern_config["name"],
        model=intern_config["model"],
        role=intern_config["role"],
        style=intern_config["style"]
    )
