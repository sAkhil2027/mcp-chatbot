🚀 LangGraph MCP Chatbot using Streamlit + OpenRouter + SQLite

An advanced AI chatbot system built using LangGraph, LangChain, Streamlit, and OpenRouter LLMs with persistent memory, multi-thread conversations, tool calling, and real-time streaming responses.
This project demonstrates how to build a production-style conversational AI system with:
Stateful AI workflows
Multi-session conversations
Persistent SQLite memory
Real-time token streaming
Tool calling agents
Async architecture
LangGraph conditional workflows

📌 Features

✅ Persistent Multi-Thread Conversations

Create unlimited chat sessions
Restore previous conversations
Continue chats even after restarting the app
SQLite-based checkpoint persistence

✅ LangGraph AI Workflow

Built using LangGraph state machines with:
Chat Node
Tool Node
Conditional Routing
Stateful Execution

✅ Real-Time Streaming Responses
Token-by-token streaming
ChatGPT-like interaction experience
Smooth user experience using Streamlit streaming

✅ Intelligent Tool Calling
Integrated tools include:
🌐 DuckDuckGo Web Search
The AI automatically decides when tools are required.

✅ Async Architecture
Custom background async event loop implementation for:
non-blocking execution
streaming support
async database operations
scalable chatbot execution

✅ MCP Style Backend Architecture
Clean separation between:
Frontend UI
Backend graph execution
State management
Tool orchestration

🏗️ System Architecture
                ┌─────────────────────┐
                │    Streamlit UI     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ LangGraph Workflow  │
                └──────────┬──────────┘
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
 ┌─────────────────────┐        ┌─────────────────────┐
 │     Chat Node       │        │     Tool Node       │
 └─────────────────────┘        └─────────────────────┘
          │                                 │
          ▼                                 ▼
 ┌─────────────────────┐        ┌─────────────────────┐
 │  OpenRouter LLM     │        │ Search + Stock Tool │
 │   GPT-4o-mini       │        └─────────────────────┘
 └─────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ SQLite Checkpointer │
                └─────────────────────┘
                
⚙️ Tech Stack
Layer	Technology
Frontend	Streamlit
Workflow Engine	LangGraph
LLM Framework	LangChain
LLM Provider	OpenRouter
Model	GPT-4o-mini
Database	SQLite
Async DB	aiosqlite
Search Tool	DuckDuckGo
API Tool	AlphaVantage
Language	Python

📂 Project Structure
project/
│
├── langgraph_mcp_backend.py
├── streamlit_mcp_frontend.py
├── requirements.txt
├── dockerfile
├── dockignore
├── chatbot.db-shm
├── chatbot.db-wal
├── .gitignore
└── test.py

🔥 How It Works
Step 1 — User Sends Message
The user enters a message through the Streamlit chat interface.
Step 2 — Message Sent to LangGraph
The frontend streams the message into the LangGraph workflow.
chatbot.astream(
    {"messages": [HumanMessage(content=user_input)]},
    config=CONFIG,
    stream_mode="messages",
)
Step 3 — Chat Node Executes
The chatbot sends conversation history to the LLM.
response = await llm_with_tools.ainvoke(messages)
Step 4 — Conditional Tool Execution
LangGraph checks whether tools are needed.
If required:
execution routes to ToolNode
tool executes
result returns back to chatbot
Step 5 — Real-Time Streaming
Assistant responses are streamed token-by-token to Streamlit.
Step 6 — Persistent Memory Storage
All conversation states are stored using SQLite checkpointers.
AsyncSqliteSaver(conn)

🧠 LangGraph Workflow
START
   │
   ▼
chat_node
   │
   ├── Tool Needed? ──► ToolNode
   │                        │
   │                        ▼
   └────────────────── chat_node

The graph dynamically decides:
direct AI response
or tool execution


⚡ Backend Overview (langgraph_mcp_backend.py)
✅ Environment Variables
load_dotenv()
Loads API keys securely from .env.

✅ Background Async Event Loop
Since Streamlit is synchronous by default, a dedicated async loop is created.
_ASYNC_LOOP = asyncio.new_event_loop()
This enables:
async LangGraph execution
non-blocking streaming
async DB checkpointing

✅ LLM Configuration
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
)
Uses:
OpenRouter API
GPT-4o-mini model

✅ Tool Integration
🌐 DuckDuckGo Search
DuckDuckGoSearchRun()
Example:
AAPL
TSLA
MSFT

✅ State Management
class ChatState(TypedDict):
Stores:
conversation messages
state history

✅ SQLite Checkpointer
AsyncSqliteSaver(conn)
Provides:
persistent memory
thread restoration
conversation continuity

🎨 Frontend Overview (streamlit_mcp_frontend.py)
✅ Session State Management
Maintains:
thread IDs
message history
conversation switching

✅ Multi-Conversation Sidebar
Users can:
create new chats
switch between old chats
continue previous sessions



🚀 Installation
1. Clone Repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

3. Move into Project Folder
cd YOUR_REPOSITORY

4. Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Linux / Mac
python3 -m venv venv
source venv/bin/activate

5. Install Dependencies
pip install -r requirements.txt

🔑 Environment Variables
Create a .env file:
OPENROUTER_API_KEY=your_openrouter_api_key

Get your API key from:
https://openrouter.ai/

▶️ Run the Project
streamlit run streamlit_mcp_frontend.py

Open browser:
http://localhost:8501

🐳 Docker Setup
Build Docker Image
docker build -t langgraph-mcp-chatbot .
Run Container
docker run -p 8501:8501 --env-file .env langgraph-mcp-chatbot
💡 Example Queries
🌐 Web Search
Who is the CEO of OpenAI?
📈 Stock Price Query
What is the latest stock price of TSLA?
💬 General Conversation
Explain LangGraph in simple terms.


🎯 Key Concepts Demonstrated
LangGraph Stateful Workflows
Tool Calling AI Agents
Async Programming
Persistent Chat Memory
Multi-Conversation Systems
Real-Time Streaming
Production Chatbot Architecture
LLM Orchestration
Streamlit AI Interfaces


🔥 Why This Project Matters
This is not just a simple chatbot.
It demonstrates:
Production-level AI architecture
Stateful conversational systems
Real-world LangGraph workflows
Multi-tool orchestration
Persistent AI memory systems
Scalable async chatbot execution

👨‍💻 Author
Akhil Vikram Singh

AI/ML Engineer focused on:
Generative AI
LangGraph Agents
RAG Systems
AI Automation
⭐ If You Like This Project

Please consider giving this repository a ⭐ on GitHub.
