# 🚀 LangGraph MCP Chatbot using Streamlit + OpenRouter + SQLite

An advanced AI chatbot system built using **LangGraph**, **LangChain**, **Streamlit**, and **OpenRouter LLMs** with persistent memory, multi-thread conversations, tool calling, and real-time streaming responses.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/LangGraph-Agentic_Workflows-black?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/OpenRouter-LLM_API-purple?style=for-the-badge" />
</p>

---

# 📌 Features

## ✅ Persistent Multi-Thread Conversations

* Create unlimited chat sessions
* Restore previous conversations
* Continue chats after restarting the application
* SQLite-based persistent memory

---

## ✅ LangGraph AI Workflow

Built using LangGraph state machines with:

* Chat Node
* Tool Node
* Conditional Routing
* Stateful Execution

---

## ✅ Real-Time Streaming Responses

* Token-by-token streaming
* ChatGPT-like interaction experience
* Smooth user experience using Streamlit

---

## ✅ Intelligent Tool Calling

Integrated tools include:

* 🌐 DuckDuckGo Web Search

The AI automatically decides when tools are required.

---

## ✅ Async Architecture

Custom background async event loop implementation for:

* Non-blocking execution
* Streaming support
* Async database operations
* Scalable chatbot execution

---

## ✅ MCP Style Backend Architecture

Clean separation between:

* Frontend UI
* Backend graph execution
* State management
* Tool orchestration

---

# 🏗️ System Architecture

```text
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
```

---

# ⚙️ Tech Stack

| Layer           | Technology   |
| --------------- | ------------ |
| Frontend        | Streamlit    |
| Workflow Engine | LangGraph    |
| LLM Framework   | LangChain    |
| LLM Provider    | OpenRouter   |
| Model           | GPT-4o-mini  |
| Database        | SQLite       |
| Async DB        | aiosqlite    |
| Search Tool     | DuckDuckGo   |
| API Tool        | AlphaVantage |
| Language        | Python       |

---

# 📂 Project Structure

```bash
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
```

---

# 🔥 How It Works

## Step 1 — User Sends Message

The user enters a message through the Streamlit chat interface.

---

## Step 2 — Message Sent to LangGraph

The frontend streams the message into the LangGraph workflow.

```python
chatbot.astream(
    {"messages": [HumanMessage(content=user_input)]},
    config=CONFIG,
    stream_mode="messages",
)
```

---

## Step 3 — Chat Node Executes

The chatbot sends conversation history to the LLM.

```python
response = await llm_with_tools.ainvoke(messages)
```

---

## Step 4 — Conditional Tool Execution

LangGraph checks whether tools are needed.

If required:

* Execution routes to ToolNode
* Tool executes
* Result returns back to chatbot

---

## Step 5 — Real-Time Streaming

Assistant responses are streamed token-by-token to Streamlit.

---

## Step 6 — Persistent Memory Storage

All conversation states are stored using SQLite checkpointers.

```python
AsyncSqliteSaver(conn)
```

---

# 🧠 LangGraph Workflow

```text
START
   │
   ▼
chat_node
   │
   ├── Tool Needed? ──► ToolNode
   │                        │
   │                        ▼
   └────────────────── chat_node
```

The graph dynamically decides:

* Direct AI response
* Or tool execution

---

# ⚡ Backend Overview (`langgraph_mcp_backend.py`)

## ✅ Environment Variables

```python
load_dotenv()
```

Loads API keys securely from `.env`.

---

## ✅ Background Async Event Loop

Since Streamlit is synchronous by default, a dedicated async loop is created.

```python
_ASYNC_LOOP = asyncio.new_event_loop()
```

This enables:

* Async LangGraph execution
* Non-blocking streaming
* Async DB checkpointing

---

## ✅ LLM Configuration

```python
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
)
```

Uses:

* OpenRouter API
* GPT-4o-mini model

---

## ✅ Tool Integration

### 🌐 DuckDuckGo Search

```python
DuckDuckGoSearchRun()
```

Enables live internet searching.

---

### 📈 Stock Price Tool

```python
@tool
def get_stock_price(symbol: str)
```

Fetches live stock data using AlphaVantage API.

Example:

```text
AAPL
TSLA
MSFT
```

---

## ✅ State Management

```python
class ChatState(TypedDict)
```

Stores:

* Conversation messages
* State history

---

## ✅ SQLite Checkpointer

```python
AsyncSqliteSaver(conn)
```

Provides:

* Persistent memory
* Thread restoration
* Conversation continuity

---

# 🎨 Frontend Overview (`streamlit_mcp_frontend.py`)

## ✅ Session State Management

Maintains:

* Thread IDs
* Message history
* Conversation switching

---

## ✅ Multi-Conversation Sidebar

Users can:

* Create new chats
* Switch between old chats
* Continue previous sessions

---

## ✅ Streaming UI

```python
st.write_stream(ai_only_stream())
```

Streams assistant output in real-time.

---

## ✅ Tool Status Visualization

```python
st.status()
```

Displays:

* Tool execution status
* Completion indicators

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

---

## 2. Move into Project Folder

```bash
cd YOUR_REPOSITORY
```

---

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Get your API key from:

```text
https://openrouter.ai/
```

---

# ▶️ Run the Project

```bash
streamlit run streamlit_mcp_frontend.py
```

Open browser:

```text
http://localhost:8501
```

---

# 🐳 Docker Setup

## Build Docker Image

```bash
docker build -t langgraph-mcp-chatbot .
```

---

## Run Container

```bash
docker run -p 8501:8501 --env-file .env langgraph-mcp-chatbot
```

---

# 💡 Example Queries

## 🌐 Web Search

```text
Who is the CEO of OpenAI?
```

---

## 📈 Stock Price Query

```text
What is the latest stock price of TSLA?
```

---

## 💬 General Conversation

```text
Explain LangGraph in simple terms.
```

---

# 🎯 Key Concepts Demonstrated

* LangGraph Stateful Workflows
* Tool Calling AI Agents
* Async Programming
* Persistent Chat Memory
* Multi-Conversation Systems
* Real-Time Streaming
* Production Chatbot Architecture
* LLM Orchestration
* Streamlit AI Interfaces

---

# 🔥 Why This Project Matters

This is not just a simple chatbot.

It demonstrates:

* Production-level AI architecture
* Stateful conversational systems
* Real-world LangGraph workflows
* Multi-tool orchestration
* Persistent AI memory systems
* Scalable async chatbot execution

This project is highly relevant for:

* AI Engineering
* Generative AI
* LLM Engineering
* Conversational AI
* Agentic AI Systems
* Production NLP Systems

---

# 👨‍💻 Author

##Akhil Vikram Singh

AI/ML Engineer focused on:
* Generative AI
* LangGraph Agents
* RAG Systems
* Computer Vision
* AI Automation

---

# ⭐ If You Like This Project

Please consider giving this repository a ⭐ on GitHub.
