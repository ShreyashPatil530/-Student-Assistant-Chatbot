# 🎓 Student Assistant Chatbot

A comprehensive AI-powered chatbot for students that integrates memory management using Mem0 and Google Calendar access for schedule retrieval. Built with Python, Streamlit, and OpenAI GPT-4.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents
- [Features](#features)
- [Demo Screenshots](#demo-screenshots)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Citations](#citations)
- [Assignment Requirements](#assignment-requirements)

## ✨ Features

### ✅ Task 1: Memory Management with Mem0
- Persistent memory storage using Mem0 library (LOCAL storage)
- Store student preferences, study habits, and personal details
- Retrieve and query memories across sessions
- Update and delete memory functionality
- Context-aware conversations using stored memories

### ✅ Task 2: Google Calendar Integration
- OAuth2 authentication with Google Calendar API
- Fetch meetings and events from user's calendar
- Query schedules by time range (today, this week, custom)
- Secure token management and data privacy
- Formatted event display with details

### ✅ Task 3: Streamlit Frontend
- Interactive chat interface
- User-friendly design with sidebar controls
- Real-time chat responses
- Memory and calendar management controls
- API status indicators
- Example queries and help section

### 🌟 Bonus Features
- Natural language processing for complex queries
- Intelligent intent detection (calendar vs memory vs conversation)
- Context-aware responses using GPT-4
- Study time suggestions based on preferences and schedule
- Conversation history management

## 📸 Demo Screenshots

### Main Interface
```
[Add screenshot of main chat interface here]
```

### Memory Management
```
[Add screenshot of stored memories here]
```

### Calendar Integration
```
[Add screenshot of calendar events here]
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Google Calendar API credentials
- OpenAI API key

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd student-assistant-chatbot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

**Note:** NO Mem0 API key required! This project uses LOCAL storage only.

## 🎯 Quick Start

```bash
# Run the Streamlit app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### First-Time Setup

1. **Enter Student ID**: Input your unique student ID in the sidebar
2. **Initialize Chatbot**: Click the "🚀 Initialize Chatbot" button
3. **Authenticate Calendar**: Click "🔐 Authenticate Google Calendar"
4. **Start Chatting**: Begin interacting with the chatbot!

## 💬 Usage Examples

### Memory Operations
```
User: "Remember that I prefer morning study sessions"
Bot: ✓ I've noted that information...

User: "What do you remember about me?"
Bot: You prefer morning study sessions...
```

### Calendar Queries
```
User: "What are my meetings today?"
Bot: Here are your events for today:
     1. 📅 Team Meeting
        Date: Monday, November 18, 2025
        Time: 2:00 PM - 3:00 PM
```

### Advanced Queries
```
User: "Suggest study times based on my schedule and preferences"
Bot: Looking at your calendar and knowing you prefer morning sessions:
     - Tomorrow 8:00 AM - 10:00 AM (no conflicts)
     - Wednesday 9:00 AM - 11:00 AM
```

## 📁 Project Structure

```
student-assistant-chatbot/
├── app.py                    # Streamlit frontend
├── chatbot_engine.py         # Main chatbot logic
├── memory_manager.py         # Mem0 integration
├── calendar_manager.py       # Google Calendar API
├── test_chatbot.py           # Testing script
├── requirements.txt          # Dependencies
├── .env                      # Environment variables
├── .env.example             # Template
├── .gitignore               # Git ignore
├── README.md                 # This file
├── SETUP_GUIDE.md           # Detailed setup
├── Sample_Responses.txt     # Test results
│
├── qdrant_data/             # Local memory storage
└── token.pickle             # Google OAuth token
```

## 🧪 Testing

### Automated Testing
```bash
python test_chatbot.py
```

### Manual Testing in Streamlit
1. Initialize the chatbot
2. Try memory operations
3. Authenticate Google Calendar
4. Test calendar queries
5. Try advanced integrated queries

### Test Results
Test results are saved in:
- `Sample_Responses.txt` - Detailed test documentation
- `Sample_Responses.json` - JSON format results

## 📚 Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Core language |
| Streamlit | 1.29.0 | Web interface |
| Mem0 | 0.1.0 | Memory management |
| OpenAI | 1.54.3 | GPT-4 API |
| Google Calendar API | v3 | Calendar access |
| Qdrant | 1.7.0 | Vector database |

## 📖 Citations

1. **Mem0 Library**
   - Documentation: https://docs.mem0.ai/
   - GitHub: https://github.com/mem0ai/mem0

2. **Google Calendar API**
   - Documentation: https://developers.google.com/calendar

3. **OpenAI API**
   - Documentation: https://platform.openai.com/docs

4. **Streamlit**
   - Documentation: https://docs.streamlit.io/

## 📝 Assignment Requirements

This project fulfills all assignment requirements:

### ✅ Task 1: Mem0 Memory Management
- [x] Install mem0 library
- [x] Configure LOCAL storage (no API key needed)
- [x] Implement add, update, query, delete operations
- [x] Test memory persistence across sessions

### ✅ Task 2: Google Calendar Integration  
- [x] OAuth2 authentication
- [x] Fetch calendar events
- [x] Query-based schedule retrieval
- [x] Secure token handling

### ✅ Task 3: Streamlit Frontend
- [x] Interactive chat interface
- [x] Memory and calendar integration
- [x] User controls and configuration
- [x] Test with sample queries

### 🌟 Bonus Features
- [x] Advanced NLP for complex queries
- [x] Context-aware responses
- [x] Intelligent suggestions
- [x] Complete documentation

## 🔧 Troubleshooting

### Common Issues

**Issue: Module not found errors**
```bash
pip install -r requirements.txt
```

**Issue: Google Calendar authentication fails**
```bash
# Delete token and re-authenticate
rm token.pickle
streamlit run app.py
```

**Issue: Mem0 configuration errors**
- Ensure OPENAI_API_KEY is set in .env
- Check that qdrant_data folder is writable

## 📞 Support

For questions or issues:
- Check SETUP_GUIDE.md for detailed instructions
- Review error messages carefully
- Ensure all environment variables are set

## 📄 License

This project is created for educational purposes as part of an academic assignment.

## 👨‍💻 Author

[Your Name]
- GitHub: [Your GitHub Profile]
- Email: [Your Email]

## 🙏 Acknowledgments

- Assignment provided by Build Fast with AI
- Mem0 library for memory management
- Google Calendar API for schedule integration
- OpenAI for GPT-4 capabilities
- Streamlit for the amazing framework

---

**Submission Date:** November 18, 2025  
**Submitted To:** prathmesh@buildfastwithai.com, shubham@buildfastwithai.com# 🎓 Student Assistant Chatbot

A comprehensive AI-powered chatbot for students that integrates memory management using Mem0 and Google Calendar access for schedule retrieval. Built with Python, Streamlit, and OpenAI GPT-4.

## 📋 Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Citations](#citations)

## ✨ Features

### Task 1: Memory Management with Mem0
- ✅ Persistent memory storage using Mem0 library
- ✅ Store student preferences, study habits, and personal details
- ✅ Retrieve and query memories across sessions
- ✅ Update and delete memory functionality
- ✅ Context-aware conversations using stored memories

### Task 2: Google Calendar Integration
- ✅ OAuth2 authentication with Google Calendar API
- ✅ Fetch meetings and events from user's calendar
- ✅ Query schedules by time range (today, this week, custom)
- ✅ Secure token management and data privacy
- ✅ Formatted event display with details

### Task 3: Streamlit Frontend
- ✅ Interactive chat interface
- ✅ User-friendly design with sidebar controls
- ✅ Real-time chat responses
- ✅ Memory and calendar management controls
- ✅ API status indicators
- ✅ Example queries and help section

### Bonus Features
- ✅ Natural language processing for complex queries
- ✅ Intelligent intent detection (calendar vs memory vs conversation)
- ✅ Context-aware responses using GPT-4
- ✅ Study time suggestions based on preferences and schedule

## 🛠 Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit**: Frontend framework for web interface
- **Mem0**: Memory management and storage
- **OpenAI GPT-4**: Natural language processing and response generation
- **Google Calendar API**: Calendar access and event retrieval
- **Google OAuth2**: Secure authentication
- **Qdrant**: Vector database for memory embeddings (local)
- **python-dotenv**: Environment variable management

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Google Calendar API credentials
- OpenAI API key

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd student-assistant-chatbot
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Google Calendar API Credentials
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

### Step 2: Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials and copy Client ID and Client Secret to `.env`

### Step 3: OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Generate an API key
3. Add the key to your `.env` file

## 🚀 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### First-Time Setup

1. **Enter Student ID**: Input your unique student ID in the sidebar
2. **Initialize Chatbot**: Click the "🚀 Initialize Chatbot" button
3. **Authenticate Calendar**: Click "🔐 Authenticate Google Calendar" to connect your calendar
4. **Start Chatting**: Begin interacting with the chatbot!

### Example Interactions

#### Calendar Queries
```
User: "What are my meetings today?"
Bot: [Displays today's calendar events with times and details]

User: "Show my schedule for this week"
Bot: [Displays all events for the next 7 days]
```

#### Memory Operations
```
User: "Remember that I prefer morning study sessions"
Bot: ✓ I've noted that information and will remember it for future conversations.

User: "Note that I'm taking CS101 and Math202 this semester"
Bot: ✓ I've noted that information...

User: "What courses am I taking?"
Bot: Based on what you've told me, you're taking CS101 and Math202 this semester.
```

#### Complex Queries (Bonus)
```
User: "Suggest study times based on my schedule and preferences"
Bot: Looking at your calendar and knowing you prefer morning sessions, I suggest:
     - Tomorrow 8:00 AM - 10:00 AM (no conflicts)
     - Wednesday 9:00 AM - 11:00 AM (before your 2 PM meeting)
```

## 📁 Project Structure

```
student-assistant-chatbot/
├── app.py                  # Streamlit frontend application
├── chatbot_engine.py       # Main chatbot logic and integration
├── memory_manager.py       # Mem0 memory management module
├── calendar_manager.py     # Google Calendar API integration
├── requirements
