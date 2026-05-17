from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

from dotenv import load_dotenv

import aiosqlite
import requests
import asyncio
import threading
import os

# =========================
# ENV VARIABLES
# =========================

load_dotenv()

# =========================
# BACKGROUND ASYNC LOOP
# =========================

_ASYNC_LOOP = asyncio.new_event_loop()

_ASYNC_THREAD = threading.Thread(
    target=_ASYNC_LOOP.run_forever,
    daemon=True
)

_ASYNC_THREAD.start()


def _submit_async(coro):
    return asyncio.run_coroutine_threadsafe(
        coro,
        _ASYNC_LOOP
    )


def run_async(coro):
    return _submit_async(coro).result()


def submit_async_task(coro):
    """
    Used by Streamlit frontend
    for async streaming.
    """
    return _submit_async(coro)

# =========================
# LLM
# =========================

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.3,
    default_headers={
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "My Chatbot"
    }
)

# =========================
# TOOLS
# =========================

search_tool = DuckDuckGoSearchRun(
    region="us-en"
)


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price.

    Example:
    AAPL
    TSLA
    """

    url = (
        "https://www.alphavantage.co/query?"
        f"function=GLOBAL_QUOTE&symbol={symbol}"
        "&apikey=C9PE94QUEW9VWGFM"
    )

    response = requests.get(url)

    return response.json()


tools = [
    search_tool,
    get_stock_price
]

llm_with_tools = llm.bind_tools(tools)

# =========================
# STATE
# =========================


class ChatState(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

# =========================
# CHAT NODE
# =========================


async def chat_node(state: ChatState):

    messages = state["messages"]

    response = await llm_with_tools.ainvoke(
        messages
    )

    return {
        "messages": [response]
    }

# =========================
# TOOL NODE
# =========================

tool_node = ToolNode(tools)

# =========================
# CHECKPOINTER
# =========================


async def _init_checkpointer():

    conn = await aiosqlite.connect(
        "chatbot.db"
    )

    return AsyncSqliteSaver(conn)


checkpointer = run_async(
    _init_checkpointer()
)

# =========================
# GRAPH
# =========================

graph = StateGraph(ChatState)

graph.add_node(
    "chat_node",
    chat_node
)

graph.add_node(
    "tools",
    tool_node
)

graph.add_edge(
    START,
    "chat_node"
)

graph.add_conditional_edges(
    "chat_node",
    tools_condition
)

graph.add_edge(
    "tools",
    "chat_node"
)

chatbot = graph.compile(
    checkpointer=checkpointer
)

# =========================
# THREAD HELPERS
# =========================


async def _alist_threads():

    all_threads = set()

    async for checkpoint in checkpointer.alist(None):

        all_threads.add(
            checkpoint.config["configurable"]["thread_id"]
        )

    return list(all_threads)


def retrieve_all_threads():

    return run_async(
        _alist_threads()
    )