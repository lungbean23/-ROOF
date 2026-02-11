"""
Trillium Rhizome - Deep Continuity Botanical

Like a trillium's underground rhizome that persists year after year,
this botanical maintains deep thematic memory across conversation restarts.

The rhizome stores:
- Core wisdom accumulated over time
- Persistent themes that keep recurring
- Deep insights that transcend individual exchanges

Used by hosts/interns during healthy conversation flow to build lasting memory.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


class TrilliumRhizome:
    """
    Deep continuity botanical for persistent wisdom
    
    Unlike buffer (seconds) or Taraxacum (single death event),
    the rhizome builds slowly across many conversations:
    
    1. Identifies recurring themes
    2. Consolidates related insights
    3. Builds interconnected wisdom network
    4. Persists across conversation restarts
    """
    
    def __init__(self, rhizome_dir="data/trillium_rhizome"):
        self.rhizome_dir = Path(rhizome_dir)
        self.rhizome_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing rhizome or create new
        self.rhizome_file = self.rhizome_dir / "rhizome.json"
        self.rhizome = self._load_rhizome()
        
        print(f"[Trillium Rhizome initialized - {len(self.rhizome.get('nodes', {}))} wisdom nodes]")
    
    def _load_rhizome(self) -> Dict[str, Any]:
        """Load existing rhizome or create new"""
        if self.rhizome_file.exists():
            with open(self.rhizome_file, 'r') as f:
                rhizome = json.load(f)
                print(f"[🌿 Loaded existing rhizome from {self.rhizome_file}]")
                return rhizome
        else:
            print("[🌱 Creating new rhizome]")
            return {
                "nodes": {},  # Theme nodes
                "connections": {},  # Theme interconnections
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
    
    def _save_rhizome(self):
        """Persist rhizome to disk"""
        self.rhizome["last_updated"] = datetime.now().isoformat()
        
        with open(self.rhizome_file, 'w') as f:
            json.dump(self.rhizome, f, indent=2)
    
    def deepen_roots(self, themes: List[str], insights: List[str] = None):
        """
        Add depth to the rhizome during healthy conversation
        
        Args:
            themes: Current conversation themes
            insights: New insights to integrate
        
        This is called periodically during conversation, not on death.
        """
        print(f"\n[🌿 TRILLIUM DEEPENING - Adding to rhizome]")
        
        for theme in themes:
            theme_key = self._normalize_theme(theme)
            
            # Create or update theme node
            if theme_key not in self.rhizome["nodes"]:
                self.rhizome["nodes"][theme_key] = {
                    "theme": theme,
                    "first_seen": datetime.now().isoformat(),
                    "occurrences": 1,
                    "insights": [],
                    "energy": 1.0
                }
                print(f"[🌱 New theme node: {theme}]")
            else:
                self.rhizome["nodes"][theme_key]["occurrences"] += 1
                # Increase energy (capped at 10)
                current_energy = self.rhizome["nodes"][theme_key].get("energy", 1.0)
                self.rhizome["nodes"][theme_key]["energy"] = min(current_energy + 0.5, 10.0)
                print(f"[⚡ Theme '{theme}' energy: {self.rhizome['nodes'][theme_key]['energy']:.1f}]")
            
            # Add insights to this theme
            if insights:
                for insight in insights:
                    if insight not in self.rhizome["nodes"][theme_key]["insights"]:
                        self.rhizome["nodes"][theme_key]["insights"].append(insight)
                        print(f"[💡 Added insight to '{theme}']")
        
        # Update connections between themes (co-occurrence)
        self._update_connections(themes)
        
        # Persist
        self._save_rhizome()
        
        print(f"[✨ Rhizome deepened - now {len(self.rhizome['nodes'])} theme nodes]")
    
    def _normalize_theme(self, theme: str) -> str:
        """Normalize theme for consistent keys"""
        return theme.lower().strip().replace(" ", "_")
    
    def _update_connections(self, themes: List[str]):
        """
        Update co-occurrence connections between themes
        
        Themes discussed together are connected in the rhizome
        """
        if len(themes) < 2:
            return
        
        # Create connections between all pairs
        for i, theme1 in enumerate(themes):
            for theme2 in themes[i+1:]:
                key1 = self._normalize_theme(theme1)
                key2 = self._normalize_theme(theme2)
                
                # Create sorted connection key
                conn_key = tuple(sorted([key1, key2]))
                
                if conn_key not in self.rhizome["connections"]:
                    self.rhizome["connections"][str(conn_key)] = {
                        "themes": list(conn_key),
                        "strength": 1,
                        "created": datetime.now().isoformat()
                    }
                else:
                    self.rhizome["connections"][str(conn_key)]["strength"] += 1
    
    def get_deep_context(self, current_themes: List[str], max_depth: int = 3) -> Dict[str, Any]:
        """
        Retrieve deep context from rhizome based on current themes
        
        Returns interconnected wisdom relevant to current discussion
        """
        if not current_themes:
            return {"themes": [], "insights": [], "connections": []}
        
        print(f"\n[🌿 TRILLIUM RETRIEVING - Deep context for: {current_themes}]")
        
        relevant_nodes = []
        all_insights = []
        relevant_connections = []
        
        # Direct theme matches
        for theme in current_themes:
            theme_key = self._normalize_theme(theme)
            if theme_key in self.rhizome["nodes"]:
                node = self.rhizome["nodes"][theme_key]
                relevant_nodes.append({
                    "theme": node["theme"],
                    "occurrences": node["occurrences"],
                    "energy": node.get("energy", 1.0)
                })
                all_insights.extend(node.get("insights", []))
        
        # Find connected themes (one hop away)
        for theme in current_themes:
            theme_key = self._normalize_theme(theme)
            
            for conn_str, conn_data in self.rhizome["connections"].items():
                conn_themes = conn_data["themes"]
                
                if theme_key in conn_themes:
                    # Found a connection
                    other_theme = [t for t in conn_themes if t != theme_key][0]
                    
                    if other_theme in self.rhizome["nodes"]:
                        node = self.rhizome["nodes"][other_theme]
                        relevant_connections.append({
                            "theme": node["theme"],
                            "connection_strength": conn_data["strength"],
                            "energy": node.get("energy", 1.0)
                        })
                        all_insights.extend(node.get("insights", [])[:2])  # Add top 2 insights
        
        # Sort by energy
        relevant_nodes.sort(key=lambda x: x["energy"], reverse=True)
        relevant_connections.sort(key=lambda x: x["connection_strength"], reverse=True)
        
        context = {
            "direct_themes": relevant_nodes[:3],
            "connected_themes": relevant_connections[:3],
            "accumulated_insights": all_insights[:5],  # Top 5 insights
            "rhizome_depth": len(self.rhizome["nodes"])
        }
        
        print(f"[✨ Retrieved {len(relevant_nodes)} direct themes, {len(relevant_connections)} connections]")
        
        return context
    
    def get_strongest_themes(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the strongest (most energetic) themes in the rhizome
        
        These represent the core recurring interests
        """
        if not self.rhizome["nodes"]:
            return []
        
        # Sort by energy
        sorted_nodes = sorted(
            self.rhizome["nodes"].items(),
            key=lambda x: x[1].get("energy", 0),
            reverse=True
        )
        
        strongest = []
        for theme_key, node in sorted_nodes[:top_n]:
            strongest.append({
                "theme": node["theme"],
                "energy": node.get("energy", 1.0),
                "occurrences": node["occurrences"],
                "insight_count": len(node.get("insights", []))
            })
        
        return strongest
    
    def decay_energy(self, decay_rate: float = 0.9):
        """
        Natural decay of theme energy over time
        
        Themes not discussed recently lose energy.
        Call this periodically (e.g., once per conversation).
        """
        print("\n[🍂 TRILLIUM DECAY - Natural energy reduction]")
        
        for theme_key, node in self.rhizome["nodes"].items():
            old_energy = node.get("energy", 1.0)
            new_energy = old_energy * decay_rate
            
            # Minimum energy of 0.1 (themes never fully die)
            node["energy"] = max(new_energy, 0.1)
            
            if old_energy > 1.0 and new_energy < 1.0:
                print(f"[🍂 Theme '{node['theme']}' energy decayed below 1.0]")
        
        self._save_rhizome()
    
    def prune_weak_themes(self, min_energy: float = 0.2):
        """
        Remove very weak themes to prevent rhizome overgrowth
        
        Only call this occasionally (e.g., every 10 conversations)
        """
        print("\n[✂️  TRILLIUM PRUNING - Removing weak themes]")
        
        to_remove = []
        for theme_key, node in self.rhizome["nodes"].items():
            if node.get("energy", 1.0) < min_energy:
                to_remove.append(theme_key)
        
        for theme_key in to_remove:
            del self.rhizome["nodes"][theme_key]
            print(f"[✂️  Pruned weak theme: {self.rhizome['nodes'].get(theme_key, {}).get('theme', theme_key)}]")
        
        if to_remove:
            self._save_rhizome()
            print(f"[✨ Pruned {len(to_remove)} weak themes]")
    
    def get_rhizome_summary(self) -> str:
        """
        Generate a human-readable summary of the rhizome
        
        Useful for understanding what the bot has learned over time
        """
        if not self.rhizome["nodes"]:
            return "Rhizome is empty - no themes yet."
        
        strongest = self.get_strongest_themes(top_n=10)
        
        summary_parts = [
            f"Trillium Rhizome - {len(self.rhizome['nodes'])} total themes",
            f"Created: {self.rhizome.get('created', 'unknown')}",
            f"Last updated: {self.rhizome.get('last_updated', 'unknown')}",
            "",
            "Strongest themes:"
        ]
        
        for i, theme in enumerate(strongest, 1):
            summary_parts.append(
                f"{i}. {theme['theme']} "
                f"(energy: {theme['energy']:.1f}, "
                f"occurrences: {theme['occurrences']}, "
                f"insights: {theme['insight_count']})"
            )
        
        return "\n".join(summary_parts)
