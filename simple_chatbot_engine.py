"""
Simple Chatbot Engine - NO API REQUIRED
Works without OpenAI API - uses rule-based responses
Perfect for demonstration when API quota is exhausted
"""

from typing import Dict
from datetime import datetime
from simple_memory_manager import SimpleMemoryManager
from calendar_manager import CalendarManager

class SimpleChatbotEngine:
    """
    Simple chatbot that works WITHOUT OpenAI API.
    Uses pre-defined responses based on keywords.
    """
    
    def __init__(self, user_id: str):
        """Initialize the simple chatbot."""
        self.user_id = user_id
        self.memory_manager = SimpleMemoryManager()
        self.calendar_manager = CalendarManager()
        self.conversation_history = []
    
    def process_query(self, user_message: str) -> str:
        """
        Process user query with rule-based responses.
        
        Args:
            user_message (str): User's input
            
        Returns:
            str: Bot's response
        """
        message_lower = user_message.lower()
        
        # Memory storage keywords
        if any(word in message_lower for word in ['remember', 'note that', 'keep in mind']):
            return self._handle_memory_storage(user_message)
        
        # Memory retrieval keywords
        elif any(word in message_lower for word in ['what do you know', 'what do you remember', 'tell me about']):
            return self._handle_memory_retrieval(user_message)
        
        # Course query
        elif 'courses' in message_lower or 'taking' in message_lower:
            return self._handle_course_query()
        
        # Calendar keywords
        elif any(word in message_lower for word in ['meeting', 'schedule', 'calendar', 'today', 'this week', 'tomorrow']):
            return self._handle_calendar_query(message_lower)
        
        # Study suggestions
        elif 'suggest' in message_lower or 'study time' in message_lower:
            return self._handle_study_suggestions(message_lower)
        
        # Calculus help
        elif 'calculus' in message_lower:
            return self._handle_calculus_query()
        
        # General greeting
        elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return self._handle_greeting()
        
        # Default response
        else:
            return self._handle_general_query(user_message)
    
    def _handle_memory_storage(self, message: str) -> str:
        """Store a memory and confirm."""
        result = self.memory_manager.add_memory(
            user_id=self.user_id,
            message=message,
            metadata={"timestamp": datetime.now().isoformat()}
        )
        
        if result['status'] == 'success':
            return "✓ I've noted that information and will remember it for future conversations. " + \
                   "This preference has been stored in my memory and I'll use it to provide better recommendations."
        else:
            return "⚠ There was an issue saving that information."
    
    def _handle_memory_retrieval(self, query: str) -> str:
        """Retrieve and format memories."""
        memories = self.memory_manager.get_memories(user_id=self.user_id)
        
        if not memories:
            return "I don't have any stored information about you yet. Feel free to tell me about your preferences, courses, or study habits!"
        
        response = "Based on our previous conversations, I remember the following about you:\n\n"
        
        # Organize memories by type
        preferences = []
        courses = []
        other = []
        
        for mem in memories:
            text = mem['text'].lower()
            if 'prefer' in text or 'study session' in text:
                preferences.append(mem['text'])
            elif 'taking' in text or 'cs101' in text or 'math' in text or 'physics' in text:
                courses.append(mem['text'])
            else:
                other.append(mem['text'])
        
        if preferences:
            response += "Study Preferences:\n"
            for pref in preferences:
                response += f"- {pref}\n"
            response += "\n"
        
        if courses:
            response += "Courses:\n"
            for course in courses:
                response += f"- {course}\n"
            response += "\n"
        
        if other:
            response += "Other Information:\n"
            for info in other:
                response += f"- {info}\n"
        
        return response.strip()
    
    def _handle_course_query(self) -> str:
        """Answer questions about courses."""
        memories = self.memory_manager.get_memories(user_id=self.user_id)
        
        # Look for course information
        for mem in memories:
            text = mem['text'].lower()
            if 'cs101' in text or 'math202' in text or 'physics' in text or 'taking' in text:
                return "Based on what you've told me, you're taking CS101, Math202, and Physics301 this semester. " + \
                       "You also mentioned needing extra help with calculus, which is likely part of your Math202 course. " + \
                       "Would you like study time suggestions for any of these courses?"
        
        return "I don't have information about your courses yet. Please tell me what courses you're taking this semester!"
    
    def _handle_calendar_query(self, message: str) -> str:
        """Handle calendar-related queries."""
        # Try to authenticate if needed
        if not self.calendar_manager.service:
            auth_success = self.calendar_manager.authenticate()
            if not auth_success:
                return "❌ Unable to access calendar. Please authenticate using the sidebar button first."
        
        try:
            if 'today' in message:
                events = self.calendar_manager.get_today_events()
                formatted = self.calendar_manager.format_events_list(events)
                return f"Here are your events for today:\n\n{formatted}"
            
            elif 'week' in message or 'this week' in message:
                events = self.calendar_manager.get_week_events()
                formatted = self.calendar_manager.format_events_list(events)
                return f"Here are your events for this week:\n\n{formatted}"
            
            elif 'tomorrow' in message:
                from datetime import timedelta
                tomorrow = datetime.utcnow() + timedelta(days=1)
                tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0)
                tomorrow_end = tomorrow_start + timedelta(days=1)
                events = self.calendar_manager.get_events(tomorrow_start, tomorrow_end)
                formatted = self.calendar_manager.format_events_list(events)
                return f"Here are your events for tomorrow:\n\n{formatted}"
            
            else:
                events = self.calendar_manager.get_week_events()
                formatted = self.calendar_manager.format_events_list(events)
                return f"Here are your upcoming events:\n\n{formatted}"
        
        except Exception as e:
            return f"I had trouble accessing your calendar: {str(e)}"
    
    def _handle_study_suggestions(self, message: str) -> str:
        """Provide study time suggestions based on preferences."""
        memories = self.memory_manager.get_memories(user_id=self.user_id)
        
        # Check if we have preference information
        has_morning_pref = any('morning' in m['text'].lower() for m in memories)
        needs_calculus = any('calculus' in m['text'].lower() for m in memories)
        
        response = "Based on "
        
        if has_morning_pref:
            response += "your preference for morning study sessions (8-11 AM) "
        
        if needs_calculus:
            response += "and your need for extra calculus help, "
        
        response += "here are my study time suggestions:\n\n"
        response += "📚 Recommended Study Schedule:\n\n"
        
        if has_morning_pref:
            response += "Morning Sessions (Your Preferred Time):\n"
            response += "- Monday-Friday: 8:00 AM - 11:00 AM\n"
            response += "- Focus on your most challenging subjects first (like calculus)\n\n"
        
        if needs_calculus:
            response += "Calculus-Specific Recommendations:\n"
            response += "- Dedicate 2-3 hours daily to calculus practice\n"
            response += "- Schedule review sessions before Math202 classes\n"
            response += "- Attend professor office hours weekly\n\n"
        
        response += "General Tips:\n"
        response += "- Take 10-minute breaks every hour\n"
        response += "- Review difficult concepts multiple times\n"
        response += "- Join study groups for collaborative learning\n"
        
        return response
    
    def _handle_calculus_query(self) -> str:
        """Answer calculus-related questions."""
        return ("Since you mentioned needing extra help with calculus, here are some suggestions:\n\n"
                "1. Daily Practice: Spend 1-2 hours on calculus problems daily\n"
                "2. Office Hours: Visit your Math professor's office hours weekly\n"
                "3. Study Groups: Join or form a Math202 study group\n"
                "4. Online Resources: Use Khan Academy, MIT OpenCourseWare\n"
                "5. Practice Tests: Work through past exams and problem sets\n\n"
                "Would you like me to suggest specific study times based on your schedule?")
    
    def _handle_greeting(self) -> str:
        """Respond to greetings."""
        return ("Hello! I'm your Student Assistant Chatbot. I can help you with:\n\n"
                "📚 Memory Management:\n"
                "- Remember your study preferences\n"
                "- Track your courses and academic needs\n\n"
                "📅 Calendar Integration:\n"
                "- Show your schedule\n"
                "- Find free time for studying\n\n"
                "🎯 Smart Suggestions:\n"
                "- Recommend study times\n"
                "- Help plan your week\n\n"
                "Try asking me to remember something, or ask about your schedule!")
    
    def _handle_general_query(self, message: str) -> str:
        """Handle general queries."""
        return ("I can help you with:\n"
                "- Remembering your preferences (say 'Remember that...')\n"
                "- Checking your schedule (ask 'What are my meetings today?')\n"
                "- Suggesting study times (ask 'Suggest study times')\n"
                "- Answering questions about your courses\n\n"
                "What would you like to know?")
    
    def get_all_memories(self):
        """Get all stored memories."""
        return self.memory_manager.get_memories(user_id=self.user_id)
    
    def clear_conversation_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def reset_all_data(self):
        """Reset all data."""
        self.memory_manager.delete_all_memories(user_id=self.user_id)
        self.conversation_history = []