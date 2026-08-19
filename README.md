# 🚀 LangGraph MCP Chatbot with Production Guardrails

An advanced AI chatbot system built using **LangGraph**, **LangChain**, **Streamlit**, and **OpenRouter LLMs** featuring persistent SQLite memory, multi-thread conversations, tool orchestration, context sanitization, and production-grade security guardrails.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/LangGraph-Agentic_Workflows-black?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/OpenRouter-LLM_API-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Guardrails-Active-success?style=for-the-badge" />
</p>

---

## 📌 Features

### ✅ Production-Grade Security Guardrails
* **Prompt Input Guardrail**: Intercepts prompt injection attacks, SQL commands (`DROP TABLE`), script injections, and system overrides *before* reaching the LLM API.
* **Tool Parameter Guardrail**: Middleware (`tool_guardrail_node`) that inspects tool arguments for malicious patterns prior to execution.
* **Pydantic Schema Validation**: Enforces strict argument validation (e.g., stock symbols must strictly match `^[A-Z]{1,5}$`).
* **Tool Loop Protection**: Caps tool execution turns to a maximum threshold (`MAX_TOOL_CALLS_PER_TURN = 3`) to prevent infinite recursion loops.

### ✅ Persistent Multi-Thread Conversations
* Unlimited conversation threads saved in SQLite (`chatbot.db`).
* Context memory sanitization (`sanitize_messages`) to prevent history blowups and state pollution.
* Restore previous conversations after application restart.

### ✅ LangGraph Agentic Workflow
* ReAct-style state loop (`START -> chat_node -> tools_condition -> (tools -> chat_node | END)`).
* Autonomous tool routing and tool selection.
* System security policy enforcement (`SYSTEM_SECURITY_PROMPT`).

### ✅ Real-Time Streaming & Tools
* Token-by-token streaming UI powered by Streamlit.
* Integrated tools: DuckDuckGo Web Search & AlphaVantage Stock Price API.

---

## 🏗️ System Architecture

```text
               ┌───────────────────────┐
               │     Streamlit UI      │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │       chat_node       │ ──► [Prompt Input Guardrail]
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │    tools_condition    │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │  tool_guardrail_node  │ ──► [Argument & Loop Guardrail]
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │   OpenRouter / Tools  │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │  SQLite Checkpointer  │
               └───────────┬───────────┘
```

---

## 📂 Project Structure

```bash
mcp-chatbot/
│
├── langgraph_mcp_backend.py    # LangGraph workflow, tools & guardrails middleware
├── streamlit_mcp_frontend.py   # Streamlit multi-thread streaming frontend
├── verify_guardrails.py        # Automated guardrail verification script
├── requirements.txt            # Project dependencies (UTF-8)
├── .env.example                # API key template
├── dockerfile                  # Docker container configuration
├── dockignore                  # Docker ignore configuration
├── .gitignore                  # Git ignore policy
├── README.md                   # Project documentation
└── test.py                     # Basic graph invocation test
```

---

## 🚀 Quick Setup & Execution

### 1. Clone & Navigate to Repository
```bash
git clone https://github.com/sAkhil2027/mcp-chatbot.git
cd mcp-chatbot
```

### 2. Create & Activate Virtual Environment
```bash
# On Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and insert your API keys:
```bash
cp .env.example .env
```
Edit `.env`:
```env
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key
ALPHA_VANTAGE_API_KEY=your_alphavantage_key_optional
```

### 5. Launch the Streamlit App
```bash
streamlit run streamlit_mcp_frontend.py
```
Open **`http://localhost:8501`** in your browser.

---

## 🧪 Verification & Automated Testing

Run the automated guardrail verification suite to validate prompt input interception, tool parameter filtering, and recursion loop limits:

```bash
python verify_guardrails.py
```
