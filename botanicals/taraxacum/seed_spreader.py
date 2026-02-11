"""
Taraxacum Seed Spreader - Emergency Diversification Botanical

Like a dandelion's last act: spread many variant seeds before death.
Each seed carries the genetic material (core themes) but with different
phenotypic expressions (conversation angles).

Used by hosts/interns when context death approaches.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import random


class TaraxacumSeedSpreader:
    """
    Emergency botanical for context death scenarios
    
    Before the context window overflows:
    1. Extract DNA (core themes, insights, questions)
    2. Generate variant seeds (different conversation angles)
    3. Store in seed bank for next germination
    """
    
    def __init__(self, seed_bank_dir="data/taraxacum_seeds"):
        self.seed_bank_dir = Path(seed_bank_dir)
        self.seed_bank_dir.mkdir(parents=True, exist_ok=True)
        
        # Phenotype templates - different ways to continue the conversation
        self.phenotypes = [
            "skeptical_inquiry",      # Question the assumptions
            "deep_dive_expansion",    # Explore one aspect deeply
            "contrarian_angle",       # Take opposite perspective
            "synthesis_summary",      # Integrate multiple threads
            "unexplored_tangent",     # Branch to related topic
            "practical_application",  # How to use this knowledge
            "historical_context",     # Connect to past
            "future_projection",      # Speculate on implications
        ]
        
        print("[Taraxacum Seed Spreader initialized]")
    
    def prepare_for_death(self, conversation_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main death response: Extract DNA and scatter seeds
        
        Args:
            conversation_state: Current state including:
                - recent_exchanges: List of recent conversation turns
                - themes: Identified themes/topics
                - unanswered_questions: Open threads
                - host_name: Who is dying
        
        Returns:
            Seed report with generation details
        """
        print("\n[🌼 TARAXACUM ACTIVATING - DEATH DETECTED]")
        print(f"[🧬 Extracting DNA from conversation...]")
        
        # Extract genetic material (core themes)
        dna = self._extract_dna(conversation_state)
        
        # Generate variant seeds
        seeds = self._generate_seeds(dna)
        
        # Store in seed bank
        seed_id = self._store_seeds(seeds, conversation_state.get("host_name", "unknown"))
        
        print(f"[🌱 Generated {len(seeds)} seeds with ID: {seed_id}]")
        print(f"[✨ Seeds scattered - ready for next germination]")
        
        return {
            "seed_id": seed_id,
            "seed_count": len(seeds),
            "dna": dna,
            "timestamp": datetime.now().isoformat()
        }
    
    def _extract_dna(self, conversation_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract genetic material from dying conversation
        
        DNA = the essential information that must survive:
        - Core themes discussed
        - Key insights discovered
        - Open questions/threads
        - Emotional tone/energy
        """
        recent_exchanges = conversation_state.get("recent_exchanges", [])
        themes = conversation_state.get("themes", [])
        
        # Extract key topics from recent exchanges
        topics = []
        insights = []
        questions = []
        
        for exchange in recent_exchanges[-5:]:  # Last 5 exchanges
            message = exchange.get("message", "")
            
            # Simple extraction (could be enhanced with NLP)
            if "?" in message:
                questions.append(message.split("?")[0] + "?")
            
            # Extract sentences that look like insights (contain keywords)
            insight_keywords = ["because", "therefore", "means", "discovered", "realized"]
            if any(kw in message.lower() for kw in insight_keywords):
                insights.append(message[:200])  # First 200 chars
        
        dna = {
            "themes": themes if themes else ["general discussion"],
            "insights": insights[:3],  # Top 3 insights
            "open_questions": questions[:3],  # Top 3 questions
            "energy_level": self._estimate_energy(recent_exchanges),
            "conversation_depth": len(recent_exchanges),
            "extraction_timestamp": datetime.now().isoformat()
        }
        
        return dna
    
    def _estimate_energy(self, exchanges: List[Dict]) -> str:
        """Estimate conversation energy level"""
        if not exchanges:
            return "calm"
        
        recent_lengths = [len(ex.get("message", "")) for ex in exchanges[-3:]]
        avg_length = sum(recent_lengths) / len(recent_lengths) if recent_lengths else 0
        
        if avg_length > 500:
            return "high"
        elif avg_length > 200:
            return "medium"
        else:
            return "calm"
    
    def _generate_seeds(self, dna: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate variant seeds from DNA
        
        Each seed has same genetic material but different phenotype
        (different way to continue the conversation)
        """
        seeds = []
        
        # Generate 5-8 variant seeds
        num_seeds = random.randint(5, 8)
        selected_phenotypes = random.sample(self.phenotypes, min(num_seeds, len(self.phenotypes)))
        
        for phenotype in selected_phenotypes:
            seed = {
                "phenotype": phenotype,
                "dna": dna,
                "continuation_prompt": self._create_continuation_prompt(phenotype, dna),
                "viability_score": random.uniform(0.7, 1.0),  # All seeds viable
                "created": datetime.now().isoformat()
            }
            seeds.append(seed)
        
        return seeds
    
    def _create_continuation_prompt(self, phenotype: str, dna: Dict[str, Any]) -> str:
        """
        Create a continuation prompt based on phenotype and DNA
        
        This prompt can be used to seed the next conversation
        """
        themes = ", ".join(dna.get("themes", []))
        
        prompts = {
            "skeptical_inquiry": f"Question the assumptions behind: {themes}",
            "deep_dive_expansion": f"Explore deeper into: {themes}",
            "contrarian_angle": f"Challenge the conventional view on: {themes}",
            "synthesis_summary": f"Synthesize multiple perspectives on: {themes}",
            "unexplored_tangent": f"Branch into related aspects of: {themes}",
            "practical_application": f"Find practical uses for insights about: {themes}",
            "historical_context": f"Connect {themes} to historical patterns",
            "future_projection": f"Project future implications of: {themes}",
        }
        
        return prompts.get(phenotype, f"Continue discussing: {themes}")
    
    def _store_seeds(self, seeds: List[Dict], host_name: str) -> str:
        """
        Store seeds in the seed bank
        
        Returns seed_id for retrieval
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        seed_id = f"{host_name}_{timestamp}"
        
        seed_file = self.seed_bank_dir / f"{seed_id}.json"
        
        with open(seed_file, 'w') as f:
            json.dump({
                "seed_id": seed_id,
                "host": host_name,
                "seeds": seeds,
                "created": datetime.now().isoformat()
            }, f, indent=2)
        
        return seed_id
    
    def get_latest_seeds(self, host_name: str = None) -> Dict[str, Any]:
        """
        Retrieve the most recent seed batch
        
        Used by germinator on startup
        """
        # Find all seed files
        if host_name:
            pattern = f"{host_name}_*.json"
        else:
            pattern = "*.json"
        
        seed_files = sorted(self.seed_bank_dir.glob(pattern), reverse=True)
        
        if not seed_files:
            return None
        
        # Load most recent
        with open(seed_files[0], 'r') as f:
            return json.load(f)
    
    def clear_old_seeds(self, keep_recent=5):
        """
        Clean up old seeds, keeping only recent batches
        
        Prevents seed bank from growing infinitely
        """
        seed_files = sorted(self.seed_bank_dir.glob("*.json"), reverse=True)
        
        # Remove all but the most recent
        for old_seed in seed_files[keep_recent:]:
            old_seed.unlink()
            print(f"[🗑️  Removed old seed batch: {old_seed.name}]")
