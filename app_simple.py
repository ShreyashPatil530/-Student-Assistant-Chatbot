"""
Streamlit Frontend for Student Chatbot - SIMPLE VERSION
NO API QUOTA NEEDED - Works without OpenAI API calls
Perfect for demonstration when quota is exhausted
"""

import streamlit as st
import os
from dotenv import load_dotenv
from simple_chatbot_engine import SimpleChatbotEngine
import traceback

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Student Assistant Chatbot",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = "default_student"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def initialize_chatbot():
    """Initialize the simple chatbot engine."""
    try:
        if st.session_state.chatbot is None:
            with st.spinner("Initializing chatbot..."):
                st.session_state.chatbot = SimpleChatbotEngine(
                    user_id=st.session_state.user_id
                )
                st.success("✓ Chatbot initialized successfully! (Simple Mode - No API calls)")
        return True
    except Exception as e:
        st.error(f"❌ Error initializing chatbot: {str(e)}")
        st.error(traceback.format_exc())
        return False

def display_chat_message(role, content):
    """Display a chat message with appropriate styling."""
    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(content)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(content)

# Main UI
st.title("🎓 Student Assistant Chatbot (Simple Mode)")
st.markdown("### Your AI-powered academic companion - No API quota needed!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # User ID input
    user_id_input = st.text_input(
        "Student ID",
        value=st.session_state.user_id,
        help="Enter your unique student ID"
    )
    
    if user_id_input != st.session_state.user_id:
        st.session_state.user_id = user_id_input
        st.session_state.chatbot = None
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Initialize button
    if st.button("🚀 Initialize Chatbot", type="primary"):
        initialize_chatbot()
    
    st.divider()
    
    # Mode info
    st.info("ℹ️ Running in SIMPLE MODE\nNo OpenAI API calls required!\nPerfect for testing and demonstration.")
    
    st.divider()
    
    # Calendar authentication
    st.header("📅 Calendar Access")
    google_client_id = os.getenv('GOOGLE_CLIENT_ID')
    google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if google_client_id and google_client_secret:
        st.write("Google Credentials: ✓ Configured")
    else:
        st.write("Google Credentials: ❌ Missing")
    
    if st.button("🔐 Authenticate Google Calendar"):
        if st.session_state.chatbot:
            try:
                with st.spinner("Authenticating with Google Calendar..."):
                    success = st.session_state.chatbot.calendar_manager.authenticate()
                    if success:
                        st.success("✓ Calendar authenticated!")
                        st.session_state.authenticated = True
                    else:
                        st.error("❌ Authentication failed")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠ Please initialize chatbot first")
    
    if st.session_state.authenticated:
        st.success("✓ Calendar Connected")
    
    st.divider()
    
    # Memory management
    st.header("🧠 Memory Management")
    if st.button("📜 View All Memories"):
        if st.session_state.chatbot:
            memories = st.session_state.chatbot.get_all_memories()
            if memories:
                st.write(f"Found {len(memories)} memories:")
                for i, mem in enumerate(memories, 1):
                    st.write(f"{i}. {mem.get('text', 'N/A')}")
            else:
                st.info("No memories stored yet")
        else:
            st.warning("⚠ Please initialize chatbot first")
    
    if st.button("🗑️ Clear All Memories", type="secondary"):
        if st.session_state.chatbot:
            st.session_state.chatbot.reset_all_data()
            st.success("✓ All memories cleared")
        else:
            st.warning("⚠ Please initialize chatbot first")
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        if st.session_state.chatbot:
            st.session_state.chatbot.clear_conversation_history()
        st.success("✓ Chat history cleared")
        st.rerun()
    
    st.divider()
    
    # Help section
    st.header("💡 Example Queries")
    st.markdown("""
    **Test These Questions:**
    1. "Remember that I prefer morning study sessions between 8 AM and 11 AM"
    2. "Note that I'm taking CS101, Math202, and Physics301"
    3. "Keep in mind that I need extra help with calculus"
    4. "What do you know about my preferences?"
    5. "What courses am I taking?"
    
    **Calendar (if authenticated):**
    - "What are my meetings today?"
    - "Show my schedule for this week"
    
    **Study Help:**
    - "Suggest study times based on my schedule"
    - "When should I study calculus?"
    """)

# Main chat interface
st.divider()

# Display chat messages
for message in st.session_state.messages:
    display_chat_message(message["role"], message["content"])

# Chat input
user_input = st.chat_input("Ask me anything about your schedule, studies, or just chat...")

if user_input:
    # Check if chatbot is initialized
    if not st.session_state.chatbot:
        st.warning("⚠ Please initialize the chatbot first using the sidebar button!")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        display_chat_message("user", user_input)
        
        # Get chatbot response
        try:
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.process_query(user_input)
            
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})
            display_chat_message("assistant", response)
            
        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            st.error(error_message)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"I apologize, but I encountered an error: {str(e)}"
            })

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>🎓 Student Assistant Chatbot v1.0 - Simple Mode</p>
    <p>Powered by Local Storage and Google Calendar API</p>
    <p>✨ No OpenAI API quota needed!</p>
</div>
""", unsafe_allow_html=True)