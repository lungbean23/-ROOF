"""
Taraxacum Germinator - Seed Selection and Activation

Selects which seeds to germinate on startup based on:
- User query alignment
- Conversation context
- Random variation for diversity

Used at the start of a new conversation to continue from where we died.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
import random


class TaraxacumGerminator:
    """
    Startup botanical for seed activation
    
    On new conversation start:
    1. Load available seeds from seed bank
    2. Select best seed(s) based on context
    3. Activate selected seeds (inject into conversation context)
    """
    
    def __init__(self, seed_bank_dir="data/taraxacum_seeds"):
        self.seed_bank_dir = Path(seed_bank_dir)
        self.seed_bank_dir.mkdir(parents=True, exist_ok=True)
        print("[Taraxacum Germinator initialized]")
    
    def select_seed(self, 
                    host_name: str,
                    user_query: str = None,
                    prefer_phenotype: str = None) -> Dict[str, Any]:
        """
        Select best seed for germination
        
        Args:
            host_name: Which host is starting
            user_query: Optional - align seed to user's interests
            prefer_phenotype: Optional - select specific phenotype
        
        Returns:
            Selected seed with continuation prompt
        """
        print("\n[🌱 TARAXACUM GERMINATING - SELECTING SEED]")
        
        # Load latest seed batch
        seed_batch = self._load_latest_seeds(host_name)
        
        if not seed_batch:
            print("[⚠️  No seeds found - starting fresh]")
            return None
        
        seeds = seed_batch.get("seeds", [])
        if not seeds:
            return None
        
        print(f"[📦 Found {len(seeds)} seeds from previous conversation]")
        
        # Selection strategy
        if prefer_phenotype:
            selected = self._select_by_phenotype(seeds, prefer_phenotype)
        elif user_query:
            selected = self._select_by_query_alignment(seeds, user_query)
        else:
            selected = self._select_by_viability(seeds)
        
        if selected:
            print(f"[✨ Selected '{selected['phenotype']}' seed for germination]")
        
        return selected
    
    def _load_latest_seeds(self, host_name: str) -> Dict[str, Any]:
        """Load most recent seed batch for this host"""
        pattern = f"{host_name}_*.json"
        seed_files = sorted(self.seed_bank_dir.glob(pattern), reverse=True)
        
        if not seed_files:
            return None
        
        with open(seed_files[0], 'r') as f:
            return json.load(f)
    
    def _select_by_phenotype(self, seeds: List[Dict], preferred: str) -> Dict[str, Any]:
        """Select seed with specific phenotype"""
        for seed in seeds:
            if seed.get("phenotype") == preferred:
                return seed
        
        # Fallback to random if preferred not found
        return random.choice(seeds)
    
    def _select_by_query_alignment(self, seeds: List[Dict], query: str) -> Dict[str, Any]:
        """
        Select seed that best aligns with user query
        
        Simple keyword matching (could be enhanced with embeddings)
        """
        query_lower = query.lower()
        
        # Score seeds based on keyword overlap
        scored_seeds = []
        for seed in seeds:
            dna = seed.get("dna", {})
            themes = " ".join(dna.get("themes", [])).lower()
            prompt = seed.get("continuation_prompt", "").lower()
            
            # Simple overlap score
            score = 0
            for word in query_lower.split():
                if len(word) > 3:  # Skip short words
                    if word in themes:
                        score += 2
                    if word in prompt:
                        score += 1
            
            scored_seeds.append((score, seed))
        
        # Sort by score
        scored_seeds.sort(reverse=True, key=lambda x: x[0])
        
        # If top score is > 0, use it; otherwise random
        if scored_seeds[0][0] > 0:
            return scored_seeds[0][1]
        else:
            return random.choice(seeds)
    
    def _select_by_viability(self, seeds: List[Dict]) -> Dict[str, Any]:
        """
        Select seed based on viability score with some randomness
        
        Higher viability = more likely to germinate
        But keep some randomness for diversity
        """
        # Weighted random selection based on viability
        total_viability = sum(s.get("viability_score", 0.5) for s in seeds)
        
        if total_viability == 0:
            return random.choice(seeds)
        
        # Random number between 0 and total_viability
        rand = random.uniform(0, total_viability)
        
        # Select seed based on weighted random
        cumulative = 0
        for seed in seeds:
            cumulative += seed.get("viability_score", 0.5)
            if rand <= cumulative:
                return seed
        
        return seeds[-1]  # Fallback
    
    def germinate_seed(self, seed: Dict[str, Any]) -> str:
        """
        Activate a seed - convert to conversation context
        
        Returns:
            Context string to inject into conversation start
        """
        if not seed:
            return ""
        
        dna = seed.get("dna", {})
        phenotype = seed.get("phenotype", "unknown")
        continuation = seed.get("continuation_prompt", "")
        
        themes = dna.get("themes", [])
        insights = dna.get("insights", [])
        questions = dna.get("open_questions", [])
        
        # Build germination context
        context_parts = []
        
        if themes:
            context_parts.append(f"Previous conversation themes: {', '.join(themes)}")
        
        if insights:
            context_parts.append(f"Key insights from before: {'; '.join(insights[:2])}")
        
        if questions:
            context_parts.append(f"Open questions: {'; '.join(questions[:2])}")
        
        context_parts.append(f"Continuation strategy ({phenotype}): {continuation}")
        
        germinated_context = "\n".join(context_parts)
        
        print(f"[🌱 Seed germinated - injecting context]")
        return germinated_context
    
    def germinate_multiple(self, 
                          host_name: str, 
                          count: int = 3,
                          diversity: bool = True) -> List[str]:
        """
        Germinate multiple seeds for richer startup context
        
        Args:
            host_name: Which host
            count: Number of seeds to germinate
            diversity: If True, prefer different phenotypes
        
        Returns:
            List of context strings
        """
        seed_batch = self._load_latest_seeds(host_name)
        
        if not seed_batch:
            return []
        
        seeds = seed_batch.get("seeds", [])
        if not seeds:
            return []
        
        # Select multiple seeds
        if diversity:
            # Try to get different phenotypes
            selected = []
            used_phenotypes = set()
            
            for seed in seeds:
                phenotype = seed.get("phenotype")
                if phenotype not in used_phenotypes and len(selected) < count:
                    selected.append(seed)
                    used_phenotypes.add(phenotype)
        else:
            # Just take top N by viability
            selected = sorted(seeds, 
                            key=lambda s: s.get("viability_score", 0.5), 
                            reverse=True)[:count]
        
        # Germinate each
        contexts = [self.germinate_seed(seed) for seed in selected]
        
        print(f"[🌿 Germinated {len(contexts)} seeds with diversity={diversity}]")
        return contexts
