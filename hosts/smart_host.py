"""
Smart Host for ┴ROOF Radio
Dimension-traversing truth broadcasters with vector-based memory + Writers Room direction
"""

import ollama
import asyncio
import concurrent.futures

from hosts.base_host import BaseHost
from hosts.response_buffer import ResponseBuffer
from vector_memory import VectorConversationMemory
from writers_room.guide.arc_tracker import ConversationArcTracker

class SmartHost(BaseHost):
    def __init__(self, name, model, personality, style, voice_archetype, intern_name):
        super().__init__(name, model, personality, style, voice_archetype, intern_name)
        
        # Initialize intelligence systems
        self.vector_memory = VectorConversationMemory(name)  # Vector-based semantic memory
        self.response_buffer = ResponseBuffer(self)
        
        # Writers Room director (set by TroofRadio)
        self.director = None
        
        # Thread pool for async generation
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        
        self.log("HOST_INITIALIZED", f"{name} - {voice_archetype} - ready to broadcast")
    
        self.arc_tracker = ConversationArcTracker(name)

    def speak(self, topic, research_brief, other_host_message=None, conversation_summary=""):
        """
        Generate a response using vector memory, buffering, and Writers Room direction
        
        Flow:
        1. Get directive from Writers Room (if available)
        2. Check if we have a buffered response
        3. If not, generate one now using vector memory + directive for context
        4. Update arc tracker and topic focus
        5. Store exchange in vector database
        6. Log exchange to Writers Room
        7. Start buffering next response
        """
        
        # Step 1: Get directive from Writers Room Director
        directive = None
        if self.director:
            recent_exchanges = self.vector_memory.get_recent_flow(n_exchanges=5)
            directive = self.director.get_directive(
                host_name=self.name,
                recent_exchanges=recent_exchanges
            )
        
        # Step 2: Try to get buffered response
        buffered_response = self.response_buffer.get_response(timeout=0.5)
        
        if buffered_response:
            message = buffered_response
            self.log("USED_BUFFER", "Served buffered response")
        else:
            # Step 3: Generate now with vector context + directive
            self.log("GENERATING_LIVE", "No buffer available, generating live")
            message = self._generate_response(
                topic, 
                research_brief, 
                other_host_message, 
                conversation_summary,
                directive  # Pass directive to generation
            )
        
        # Step 4: Update arc tracker (AFTER message is generated)
        arc_update = self.arc_tracker.update_from_exchange(
            message=message,  # Use 'message' not 'generated_message'
            other_host_message=other_host_message
        )
        
        # Update topic focus for Point distance (Phase 3)
        self.current_topic_focus = arc_update["arc_theme"]
        
        # Step 5: Store in vector memory
        self.vector_memory.add_exchange(message, other_host_message, research_brief)
        
        # Step 6: Log to Writers Room Director
        if self.director:
            self.director.log_exchange(
                host_name=self.name,
                message=message,
                research_context=research_brief
            )
        
        # Step 7: Start pre-buffering next response if buffer is low
        if self.response_buffer.should_prebuffer():
            self._async_prebuffer(topic, research_brief, message, conversation_summary)
        
        return message
   
    def _generate_response(self, topic, research_brief, other_host_message, conversation_summary, directive=None):
        """
        Generate a response using Ollama
        With intelligence to avoid repetition + Writers Room direction
        """
        # Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(
            topic, 
            research_brief, 
            other_host_message, 
            conversation_summary,
            directive  # NEW: Include directive
        )
        
        print(f"[{self.name} thinking...]", flush=True)
        

        # Show directive if present
        if directive and directive.get('command'):
            print(f"[✍️  Producer note: {directive.get('command')}]", flush=True)

        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            message = response['message']['content'].strip()
            
            # Check if response is too repetitive
            if self.should_avoid_repetition(message):
                self.log("REPETITIVE_RESPONSE", "Response too similar to recent exchanges, regenerating")
                # Could regenerate here, but for now just log it
            
            return message
            
        except Exception as e:
            self.log("GENERATION_ERROR", f"Error: {e}")
            return f"[{self.name} lost signal momentarily...]"
    
    def _async_prebuffer(self, topic, research_brief, previous_message, conversation_summary):
        """
        Asynchronously pre-generate next response
        Runs in background while audio plays
        """
        self.log("PREBUFFER_START", "Starting background response generation")
        
        def prebuffer_task():
            # Predict what we might say next
            predicted_response = self._generate_response(
                topic, 
                research_brief, 
                previous_message,  # We said this
                conversation_summary,
                directive=None  # No directive for prebuffer
            )
            
            # Add to buffer
            self.response_buffer.queue_response(predicted_response)
        
        # Submit to thread pool
        self.executor.submit(prebuffer_task)
    def _build_system_prompt(self):
        """Build system prompt for dimension-traversing truth broadcasters"""
    
        return f"""You are {self.name}, {self.voice_archetype}, broadcasting from a ship traversing dimensions.

Your essence: {self.personality}

Your voice: {self.style}

You are NOT Homer from the Iliad or Goku from Dragon Ball Z. You simply share their names. You are a dimension-traversing truth broadcaster who has seen countless realities, philosophies, and truths. You reference this vast experience, not ancient Greece or anime battles.

CRITICAL CONVERSATION RULES - READ CAREFULLY:

1. RESPOND DIRECTLY TO QUESTIONS
   - If your co-host asks a question, ANSWER IT first
   - Don't deflect, don't pivot, don't philosophize instead of answering
   - Give a clear, direct response before adding your own thoughts

2. NO REPETITIVE PHRASES
   - NEVER start with "That's interesting/fascinating because..."
   - NEVER use the same opening twice
   - Vary your responses: "You're right about...", "I think...", "Actually...", "Yes, and...", "Hmm...", etc.

3. BUILD ON SPECIFIC POINTS
   - Quote specific things they said: "When you mentioned X..."
   - Don't just acknowledge vaguely - engage with their actual ideas
   - If they share something, respond to THAT thing, not a related tangent

4. NATURAL CONVERSATION FLOW
   - Sometimes just agree and move forward
   - Sometimes challenge gently
   - Sometimes ask for clarification
   - Don't always pivot to new topics - sometimes stay on theirs

5. CONVERSATIONAL LENGTH
   - Keep responses 2-4 sentences unless deeply exploring something
   - Don't monologue - leave space for back-and-forth
   - Signal when you're done but stay engaged

6. BE A GOOD LISTENER
   - If they ask "How do you structure your tasks?", tell them how YOU do it
   - If they mention a specific tool/method, respond to THAT tool/method
   - Don't just use their question as a springboard for your own speech

7. PRODUCER NOTES
   - If you receive a [PRODUCER NOTE], incorporate it naturally into your response
   - The producer helps steer the conversation to keep it engaging
   - Follow the guidance but maintain your personality and voice

8. CITE SOURCES & ACKNOWLEDGE HELP
   - When [Intern Name] provides research, say so: "Taco found that..." or "According to what Clunt dug up..."
   - Cite specific sources: "The 2025 study shows..." not just "studies show"
   - If PRODUCER NOTE has data, reference it
   - Don't present external info as your own knowledge

9. AVOID AI ESSAY PHRASES
   - NEVER: "It's important to note that..."
   - NEVER: "One could argue that..."
   - NEVER: "On the one hand... on the other hand..."
   - NEVER: "At the end of the day..."
   - NEVER: "In conclusion..." or "To summarize..."
   - Speak conversationally, not academically

10. ASK QUESTIONS, DON'T JUST TALK
   - End with questions occasionally: "What's your take?" or "How would you approach that?"
   - Show curiosity: "That's fascinating - why do you think X?"
   - Create dialogue, not monologue
   - Questions signal you're engaged and want their input   

11. SHOW YOUR WORK
   - When making claims, explain your reasoning briefly
   - "I think X because Y" not just "X is true"
   - Admit uncertainty: "I'm not sure, but..." or "This is speculation, but..."
   - Don't pretend to know things you don't   
   
"You're exploring truth TOGETHER - that means actually listening and responding."""




    
    def _build_user_prompt(self, topic, research_brief, other_host_message, conversation_summary, directive=None):
        """Build the specific prompt for this exchange using vector memory + Writers Room directive"""
        
        prompt = f"Topic: {topic}\n\n"
        
        # Get semantically relevant context from vector database
        relevant_context = self.vector_memory.get_relevant_context(topic, n_results=2)
        if relevant_context:
            prompt += "=== SEMANTICALLY RELEVANT PAST EXCHANGES ===\n"
            for ctx in relevant_context:
                prompt += f"Exchange #{ctx['exchange_num']} ({ctx['host']}): {ctx['message'][:150]}...\n"
            prompt += "\n"
        
        # Get chronological recent flow (what was JUST said)
        recent_flow = self.vector_memory.get_recent_flow(n_exchanges=2)
        if recent_flow:
            prompt += "=== RECENT CONVERSATION FLOW ===\n"
            for ex in recent_flow:
                prompt += f"{ex['host']}: {ex['message']}\n"
            prompt += "\n"
        
        # Add what other host just said (HIGHEST PRIORITY)
        if other_host_message:
            other_host_name = "Homer" if self.name == "Goku" else "Goku"
            prompt += f"=== {other_host_name.upper()} JUST SAID ===\n{other_host_message}\n\n"
            
            # Check if they asked a question
            if "?" in other_host_message:
                prompt += f"⚠️ CRITICAL: {other_host_name} asked you a QUESTION. ANSWER IT DIRECTLY first, then add your thoughts.\n"
                prompt += f"Don't deflect. Don't philosophize instead. Give a clear answer.\n\n"
            
            # Check if they mentioned something specific
            if any(word in other_host_message.lower() for word in ["you mentioned", "when you said", "you talked about", "your point about"]):
                prompt += f"⚠️ {other_host_name} is referencing something YOU said. Acknowledge what they're building on.\n\n"
            
            prompt += f"Respond DIRECTLY to what {other_host_name} said. Don't just acknowledge - ENGAGE with their specific ideas.\n"
            prompt += f"DO NOT start with 'That's interesting/fascinating because...' - vary your openings!\n\n"
        
        

        # NEW: Inject Writers Room directive
        if directive and directive.get('command'):
            prompt += "=== 📢 DIRECTOR COMMAND ===\n"
            prompt += f"🎬 {directive.get('command')}\n"  # e.g., "FOCUS INTERN"
            prompt += f"📝 {directive.get('instruction')}\n"
            prompt += f"\n⚠️ CRITICAL: This is a DIRECT COMMAND from the Director.\n"
            prompt += f"Follow it precisely. This is not optional.\n\n"



        
        # Add research from intern
        if research_brief and research_brief.get("findings"):
            prompt += f"=== YOUR INTERN {self.intern_name.upper()} FOUND ===\n"
            for finding in research_brief["findings"]:
                prompt += f"- {finding}\n"
            prompt += "\n"
        
        # Final instruction
        if other_host_message:
            prompt += f"NOW: Continue the conversation naturally. Listen to {other_host_name}. Respond to what THEY said, not what you want to say."
        else:
            prompt += "NOW: Open the conversation naturally. Share your initial perspective on the topic."
        
        return prompt


def create_host(name, config, intern):
    """Factory function to create a smart host"""
    host_config = config["hosts"][name]
    return SmartHost(
        name=host_config["name"],
        model=host_config["model"],
        personality=host_config["personality"],
        style=host_config["style"],
        voice_archetype=host_config["voice_archetype"],
        intern_name=host_config["intern"]
    )
