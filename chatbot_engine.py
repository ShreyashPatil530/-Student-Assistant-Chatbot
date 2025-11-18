"""
Chatbot Engine Module
Integrates memory management (mem0) and calendar access (Google Calendar)
to provide intelligent responses to user queries.

Citation:
- OpenAI API Documentation: https://platform.openai.com/docs
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI
from memory_manager import MemoryManager
from calendar_manager import CalendarManager

class ChatbotEngine:
    """
    Main chatbot engine that integrates memory and calendar functionalities.
    Processes user queries and generates intelligent responses.
    """
    
    def __init__(self, user_id: str, api_key: Optional[str] = None):
        """
        Initialize the chatbot engine.
        
        Args:
            user_id (str): Unique identifier for the user
            api_key (str, optional): OpenAI API key
        """
        self.user_id = user_id
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # Initialize memory and calendar managers
        self.memory_manager = MemoryManager(api_key=self.api_key)
        self.calendar_manager = CalendarManager()
        
        # Conversation history for context
        self.conversation_history = []
        
    def process_query(self, user_message: str) -> str:
        """
        Process user query and generate response.
        Determines if the query requires calendar access, memory operations, or both.
        
        Args:
            user_message (str): User's input message
            
        Returns:
            str: Chatbot's response
        """
        # Analyze query to determine intent
        intent = self._analyze_intent(user_message)
        
        response = ""
        
        # Handle calendar-related queries
        if intent['calendar']:
            calendar_info = self._handle_calendar_query(user_message, intent)
            response += calendar_info + "\n\n"
        
        # Handle memory-related operations
        if intent['memory_store']:
            memory_result = self._handle_memory_storage(user_message)
            response += memory_result + "\n\n"
        
        # Retrieve relevant memories for context
        relevant_memories = self.memory_manager.get_memories(
            user_id=self.user_id,
            query=user_message
        )
        memory_context = self.memory_manager.format_memories_for_context(relevant_memories)
        
        # Generate conversational response using GPT
        if not response or intent['conversational']:
            conversational_response = self._generate_response(
                user_message, 
                memory_context,
                response
            )
            response += conversational_response
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response.strip()
    
    def _analyze_intent(self, message: str) -> Dict[str, bool]:
        """
        Analyze user message to determine intent.
        
        Args:
            message (str): User's message
            
        Returns:
            dict: Dictionary with intent flags
        """
        message_lower = message.lower()
        
        # Calendar-related keywords
        calendar_keywords = [
            'meeting', 'schedule', 'calendar', 'event', 'appointment',
            'today', 'tomorrow', 'this week', 'next week', 'what do i have'
        ]
        
        # Memory storage keywords
        memory_keywords = [
            'remember', 'i prefer', 'my preference', 'note that',
            'keep in mind', 'don\'t forget'
        ]
        
        intent = {
            'calendar': any(keyword in message_lower for keyword in calendar_keywords),
            'memory_store': any(keyword in message_lower for keyword in memory_keywords),
            'conversational': True
        }
        
        return intent
    
    def _handle_calendar_query(self, message: str, intent: Dict) -> str:
        """
        Handle calendar-related queries.
        
        Args:
            message (str): User's message
            intent (dict): Parsed intent
            
        Returns:
            str: Calendar information response
        """
        message_lower = message.lower()
        
        # Authenticate if not already done
        if not self.calendar_manager.service:
            auth_success = self.calendar_manager.authenticate()
            if not auth_success:
                return "❌ Unable to access calendar. Please check authentication."
        
        # Determine time range based on query
        if 'today' in message_lower:
            events = self.calendar_manager.get_today_events()
            time_context = "today"
        elif 'week' in message_lower or 'this week' in message_lower:
            events = self.calendar_manager.get_week_events()
            time_context = "this week"
        else:
            # Default to next 7 days
            events = self.calendar_manager.get_week_events()
            time_context = "the next 7 days"
        
        # Format events
        formatted_events = self.calendar_manager.format_events_list(events)
        
        return f"Here are your events for {time_context}:\n\n{formatted_events}"
    
    def _handle_memory_storage(self, message: str) -> str:
        """
        Store information in memory based on user message.
        
        Args:
            message (str): User's message containing information to remember
            
        Returns:
            str: Confirmation message
        """
        result = self.memory_manager.add_memory(
            user_id=self.user_id,
            message=message,
            metadata={"timestamp": datetime.now().isoformat()}
        )
        
        if result['status'] == 'success':
            return "✓ I've noted that information and will remember it for future conversations."
        else:
            return "⚠ There was an issue saving that information."
    
    def _generate_response(self, user_message: str, memory_context: str, 
                          additional_context: str = "") -> str:
        """
        Generate conversational response using OpenAI GPT.
        
        Args:
            user_message (str): User's message
            memory_context (str): Formatted memory context
            additional_context (str): Any additional context (e.g., calendar info)
            
        Returns:
            str: Generated response
        """
        # Build system message with context
        system_message = f"""You are a helpful academic assistant chatbot for students.
You have access to the user's memories and calendar information.

{memory_context}

{additional_context}

Be friendly, concise, and helpful. Use the memory context to personalize your responses.
If you've already provided calendar or specific information, acknowledge it briefly."""

        # Build messages for API call
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        # Add recent conversation history (last 5 exchanges)
        if self.conversation_history:
            messages.extend(self.conversation_history[-10:])
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Call OpenAI API - using gpt-3.5-turbo (available on free tier)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I encountered an error generating a response: {str(e)}"
    
    def get_all_memories(self) -> List[Dict]:
        """
        Retrieve all memories for the current user.
        
        Returns:
            list: List of all user memories
        """
        return self.memory_manager.get_memories(user_id=self.user_id)
    
    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def reset_all_data(self):
        """Delete all memories and reset conversation history."""
        self.memory_manager.delete_all_memories(user_id=self.user_id)
        self.conversation_history = []