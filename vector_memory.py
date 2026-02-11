"""
Qdrant Vector Memory for ┴ROOF Radio with Botanical Integration
Modern vector database with Python 3.14 support + Taraxacum & Trillium
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from datetime import datetime
from pathlib import Path

# Import botanicals
from botanicals.taraxacum import TaraxacumSeedSpreader, TaraxacumGerminator
from botanicals.trillium import TrilliumRhizome, TrilliumThreePetals


class VectorConversationMemory:
    """
    Qdrant-based semantic conversation memory with botanical enhancements
    
    Three-layer memory architecture:
    1. Buffer (this class) - Immediate caching (seconds to minutes)
    2. Trillium - Deep persistent wisdom (days/weeks/months)
    3. Taraxacum - Survival seeds across context death
    """
    
    def __init__(self, host_name, persist_dir="data/conversation_vectors"):
        self.host_name = host_name
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        # CRITICAL: Each host needs its own Qdrant instance
        # Use host-specific subdirectory to prevent lock conflicts
        host_storage_path = self.persist_dir / f"qdrant_{host_name.lower()}"
        
        # Initialize Qdrant client (local mode, persistent)
        self.client = QdrantClient(path=str(host_storage_path))
        
        # Collection name
        self.collection_name = f"{host_name.lower()}_conversation"
        
        # Vector dimension for FastEmbed default model
        self.vector_size = 384  # all-MiniLM-L6-v2
        
        # Create collection if doesn't exist
        try:
            self.client.get_collection(self.collection_name)
            print(f"[Qdrant: Using existing collection '{self.collection_name}']")
        except:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
            print(f"[Qdrant: Created collection '{self.collection_name}']")
        
        self.exchange_count = 0
        
        # Initialize botanicals
        self.taraxacum_spreader = TaraxacumSeedSpreader()
        self.taraxacum_germinator = TaraxacumGerminator()
        self.trillium_rhizome = TrilliumRhizome()
        self.trillium_petals = TrilliumThreePetals()
        
        # Context monitoring for death detection
        self.context_tokens_estimate = 0
        self.context_max_tokens = 100000  # Conservative estimate
        
        print(f"[Vector Memory (Qdrant) + Botanicals initialized for {host_name}]")
        
        # Try to germinate seeds from previous conversation
        self._startup_from_seeds()
    
    def _startup_from_seeds(self):
        """Attempt to continue from previous conversation seeds"""
        seed = self.taraxacum_germinator.select_seed(self.host_name)
        if seed:
            context = self.taraxacum_germinator.germinate_seed(seed)
            print(f"\n[🌱 {self.host_name} continuing from previous conversation]")
            print(f"[Seed phenotype: {seed.get('phenotype')}]")
            # Store germination context for later retrieval
            self.germination_context = context
            return context
        return None
    
    def _generate_embedding(self, text):
        """
        Generate embedding using Qdrant's built-in FastEmbed
        
        Uses all-MiniLM-L6-v2 (384 dimensions, fast, accurate)
        """
        from fastembed import TextEmbedding
        
        # Initialize embedding model (cached after first call)
        if not hasattr(self, '_embedding_model'):
            self._embedding_model = TextEmbedding(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        
        # Generate embedding
        embeddings = list(self._embedding_model.embed([text]))
        return embeddings[0].tolist()
    
    def _generate_id(self, text, exchange_num):
        """Generate unique UUID for this exchange"""
        import uuid
        # Create deterministic UUID from namespace + exchange info
        namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # Standard DNS namespace
        unique_str = f"{self.host_name}_{exchange_num}_{text[:50]}"
        return str(uuid.uuid5(namespace, unique_str))
    
    def _estimate_context_usage(self):
        """Estimate current context window usage"""
        # Rough estimate: ~4 chars per token
        estimated_tokens = self.context_tokens_estimate
        usage_ratio = estimated_tokens / self.context_max_tokens
        return usage_ratio
    
    def _extract_themes(self, recent_exchanges):
        """Extract themes from recent exchanges for botanicals"""
        themes = []
        for ex in recent_exchanges[-3:]:  # Last 3 exchanges
            msg = ex.get('message', '')
            # Simple extraction - just use first few words as theme proxy
            words = msg.split()[:5]
            if len(words) >= 3:
                themes.append(' '.join(words))
        return list(set(themes))[:3]  # Unique, max 3
    
    def add_exchange(self, message, other_host_message=None, research_context=None):
        """
        Add exchange to Qdrant vector database + feed botanicals
        
        Stores:
        - Message as vector embedding (buffer)
        - Feeds Trillium rhizome (deep memory)
        - Monitors for context death (Taraxacum trigger)
        """
        self.exchange_count += 1
        
        # Update context estimate (rough)
        self.context_tokens_estimate += len(message) // 4
        if other_host_message:
            self.context_tokens_estimate += len(other_host_message) // 4
        
        # Generate embedding for the message
        message_vector = self._generate_embedding(message)
        
        # Create metadata
        payload = {
            "exchange_num": self.exchange_count,
            "timestamp": datetime.now().isoformat(),
            "host": self.host_name,
            "message": message,
            "message_length": len(message)
        }
        
        # Add research metadata if available
        if research_context and research_context.get("findings"):
            payload["has_research"] = True
            payload["research_query"] = research_context.get("query", "")
        
        # Store in Qdrant (buffer)
        point_id = self._generate_id(message, self.exchange_count)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=message_vector,
                    payload=payload
                )
            ]
        )
        
        # Also store what other host said (for context)
        if other_host_message:
            other_name = "Homer" if self.host_name == "Goku" else "Goku"
            other_vector = self._generate_embedding(other_host_message)
            
            other_payload = {
                "exchange_num": self.exchange_count,
                "timestamp": datetime.now().isoformat(),
                "host": other_name,
                "message": other_host_message,
                "message_length": len(other_host_message),
                "context_for": self.host_name
            }
            
            # Generate separate UUID for context
            import uuid
            namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
            context_str = f"{other_name}_context_{self.exchange_count}_{other_host_message[:50]}"
            other_id = str(uuid.uuid5(namespace, context_str))
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=other_id,
                        vector=other_vector,
                        payload=other_payload
                    )
                ]
            )
        
        print(f"[Qdrant: Stored exchange #{self.exchange_count}]")
        
        # BOTANICAL INTEGRATION
        
        # 1. Feed Trillium rhizome (every 3 exchanges during healthy conversation)
        context_usage = self._estimate_context_usage()
        if self.exchange_count % 3 == 0 and context_usage < 0.6:
            recent = self.get_recent_flow(3)
            themes = self._extract_themes(recent)
            if themes:
                self.trillium_rhizome.deepen_roots(themes)
        
        # 2. Check for context death (Taraxacum activation threshold)
        if context_usage > 0.8:
            self._prepare_for_death()
    
    def _prepare_for_death(self):
        """
        TARAXACUM: Scatter seeds before context death
        
        Called when context usage > 80%
        """
        print(f"\n[⚠️  {self.host_name} context pressure: {self._estimate_context_usage():.1%}]")
        
        # Get recent exchanges
        recent_exchanges = self.get_recent_flow(5)
        
        # Extract themes
        themes = self._extract_themes(recent_exchanges)
        
        # Build conversation state
        conversation_state = {
            "host_name": self.host_name,
            "recent_exchanges": recent_exchanges,
            "themes": themes,
            "unanswered_questions": []  # Could track these
        }
        
        # Scatter seeds
        report = self.taraxacum_spreader.prepare_for_death(conversation_state)
        print(f"[🌼 {self.host_name} scattered {report['seed_count']} seeds for next generation]")
    
    def get_deep_wisdom(self, current_topic):
        """
        TRILLIUM: Retrieve accumulated wisdom from rhizome
        
        Returns themes and insights from all past conversations
        """
        return self.trillium_rhizome.get_deep_context([current_topic])
    
    def verify_response_balance(self, response):
        """
        TRILLIUM: Use three petals to verify response quality
        
        Returns balance score and recommendations
        """
        recent = self.get_recent_flow(3)
        
        verification = self.trillium_petals.verify_statement(
            statement=response,
            past_context=recent,
            current_facts={},  # Could add research findings here
            intended_direction=""  # Could track conversation goals
        )
        
        return verification
    
    def get_relevant_context(self, current_topic, n_results=3):
        """
        Retrieve semantically relevant exchanges using vector similarity
        
        Args:
            current_topic: What we're discussing now
            n_results: Number of relevant exchanges to retrieve
        
        Returns:
            List of relevant exchanges sorted by similarity
        """
        if self.exchange_count == 0:
            return []
        
        # Generate query vector
        query_vector = self._generate_embedding(current_topic)
        
        # Search Qdrant for similar exchanges
        search_results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=min(n_results * 2, self.exchange_count),
            score_threshold=0.3
        ).points
        
        # Format results
        relevant = []
        for result in search_results[:n_results]:
            relevant.append({
                "exchange_num": result.payload.get("exchange_num", 0),
                "host": result.payload.get("host", "Unknown"),
                "message": result.payload.get("message", ""),
                "distance": 1.0 - result.score,
                "similarity": result.score
            })
        
        if relevant:
            avg_sim = sum(r['similarity'] for r in relevant) / len(relevant)
            print(f"[Qdrant: Retrieved {len(relevant)} relevant exchanges (avg similarity: {avg_sim:.0%})]")
        else:
            print("[Qdrant: No relevant exchanges found]")
        
        return relevant
    
    def get_recent_flow(self, n_exchanges=2):
        """Get most recent exchanges in chronological order"""
        if self.exchange_count == 0:
            return []
        
        # Scroll through all points
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=100,
            with_payload=True,
            with_vectors=False
        )
        
        # Filter to only main exchanges
        main_exchanges = [
            p for p in points 
            if p.payload.get("host") == self.host_name and "context_for" not in p.payload
        ]
        
        # Sort by exchange number
        main_exchanges.sort(key=lambda x: x.payload.get("exchange_num", 0), reverse=True)
        
        # Take most recent n_exchanges
        recent = main_exchanges[:n_exchanges]
        recent.reverse()  # Chronological order
        
        return [{
            "exchange_num": ex.payload.get("exchange_num", 0),
            "host": ex.payload.get("host", "Unknown"),
            "message": ex.payload.get("message", ""),
            "timestamp": ex.payload.get("timestamp", "")
        } for ex in recent]
    
    def should_avoid_statement(self, potential_statement, similarity_threshold=0.85):
        """Check if statement is too similar to recent exchanges"""
        if self.exchange_count == 0:
            return False
        
        # Generate embedding
        query_vector = self._generate_embedding(potential_statement)
        
        # Search for similar statements
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=3
        ).points
        
        # Check similarity
        for result in results:
            if result.score > similarity_threshold:
                print(f"[Qdrant: Statement too similar ({result.score:.2%}) - avoiding]")
                return True
        
        return False
    
    def get_conversation_summary(self):
        """Generate summary of recent conversation"""
        if self.exchange_count == 0:
            return "No conversation yet."
        
        recent = self.get_recent_flow(n_exchanges=5)
        
        summary_parts = []
        for ex in recent:
            summary_parts.append(
                f"Exchange #{ex['exchange_num']} ({ex['host']}): {ex['message'][:100]}..."
            )
        
        return "\n".join(summary_parts)
    
    def clear(self):
        """Clear all conversation memory (buffer only, botanicals persist)"""
        try:
            self.client.delete_collection(self.collection_name)
            print(f"[Qdrant: Deleted collection '{self.collection_name}']")
        except:
            pass
        
        # Recreate collection
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE
            )
        )
        
        self.exchange_count = 0
        self.context_tokens_estimate = 0
        print(f"[Qdrant: Collection cleared for {self.host_name}]")
        print("[Note: Trillium rhizome and Taraxacum seeds persist across resets]")
