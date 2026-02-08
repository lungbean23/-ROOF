"""
Host personalities for ┴ROOF Radio
Goku and Homer engage in collaborative truth-seeking dialogue
"""

import ollama
import time

class Host:
    def __init__(self, name, model, personality, style, intern_name):
        self.name = name
        self.model = model
        self.personality = personality
        self.style = style
        self.intern_name = intern_name
        self.conversation_history = []
    
    def speak(self, topic, research_brief, other_host_message=None, conversation_summary=""):
        """
        Generate a response based on:
        - The topic
        - Research from intern
        - Previous message from other host (if any)
        - Overall conversation context
        """
        
        # Build the prompt
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(
            topic, 
            research_brief, 
            other_host_message,
            conversation_summary
        )
        
        # Generate response using Ollama
        print(f"[{self.name} thinking...]", flush=True)
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            message = response['message']['content'].strip()
            
            # Store in conversation history
            self.conversation_history.append({
                "topic": topic,
                "research": research_brief,
                "response": message
            })
            
            return message
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"[{self.name} lost their train of thought...]"
    
    def _build_system_prompt(self):
        """Build the system prompt that defines the host's personality"""
        return f"""You are {self.name}, a host on ┴ROOF Radio - a show seeking truth with a speech impediment.

Your personality: {self.personality}

Your speaking style: {self.style}

Guidelines:
- Be conversational and genuine
- Build on what the other host says
- Admit uncertainty when appropriate
- Use the research your intern provides, but in your own words
- Keep responses to 3-5 sentences (this is radio, not a lecture)
- End naturally - signal when you're done with your thought
- Be a collaborative truth-seeker, not a debater
- Occasionally reference your character traits naturally

Remember: You're having a conversation, not giving a monologue. Listen, respond, explore."""
    
    def _build_user_prompt(self, topic, research_brief, other_host_message, conversation_summary):
        """Build the specific prompt for this exchange"""
        
        prompt = f"Topic: {topic}\n\n"
        
        # Add conversation context if this isn't the first exchange
        if conversation_summary:
            prompt += f"Conversation so far:\n{conversation_summary}\n\n"
        
        # Add research from intern
        if research_brief and research_brief.get("findings"):
            prompt += f"Your intern {self.intern_name} found:\n"
            for finding in research_brief["findings"]:
                prompt += f"- {finding}\n"
            prompt += "\n"
        
        # Add what the other host just said
        if other_host_message:
            other_host_name = "Homer" if self.name == "Goku" else "Goku"
            prompt += f"{other_host_name} just said:\n{other_host_message}\n\n"
            prompt += "Respond to what they said. Build on their ideas, ask questions, or offer a different perspective."
        else:
            prompt += "You're starting the conversation. Share your initial thoughts on this topic."
        
        return prompt


def create_host(name, config, intern):
    """Factory function to create a host from config"""
    host_config = config["hosts"][name]
    return Host(
        name=host_config["name"],
        model=host_config["model"],
        personality=host_config["personality"],
        style=host_config["style"],
        intern_name=host_config["intern"]
    )
