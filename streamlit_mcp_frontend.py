import queue
import uuid
import os
import streamlit as st
from langgraph_mcp_backend import chatbot, retrieve_all_threads, submit_async_task, delete_thread, clear_all_threads
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

# =========================== Utilities ===========================
def generate_thread_id():
    return uuid.uuid4()


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get("messages", [])


def get_thread_title(thread_id):
    """
    Extracts a meaningful conversation title from the first user prompt,
    falling back to 'New Conversation' instead of raw UUID/numbers.
    """
    if "thread_titles" in st.session_state and thread_id in st.session_state["thread_titles"]:
        return st.session_state["thread_titles"][thread_id]

    try:
        messages = load_conversation(thread_id)
        for msg in messages:
            if isinstance(msg, HumanMessage) and msg.content:
                clean_text = str(msg.content).strip().split("\n")[0]
                title = clean_text[:28] + ("..." if len(clean_text) > 28 else "")
                if "thread_titles" not in st.session_state:
                    st.session_state["thread_titles"] = {}
                st.session_state["thread_titles"][thread_id] = title
                return title
    except Exception:
        pass

    return "New Conversation"


def set_thread_title(thread_id, title_text):
    """
    Sets a meaningful conversation title in session state.
    """
    clean_text = str(title_text).strip().split("\n")[0]
    title = clean_text[:28] + ("..." if len(clean_text) > 28 else "")
    if "thread_titles" not in st.session_state:
        st.session_state["thread_titles"] = {}
    st.session_state["thread_titles"][thread_id] = title


# ======================= Session Initialization ===================
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "thread_titles" not in st.session_state:
    st.session_state["thread_titles"] = {}

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread(st.session_state["thread_id"])

# Sidebar 
st.sidebar.title("🤖 LangGraph MCP Chatbot")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    reset_chat()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("💬 My Conversations")

for thread_id in list(st.session_state["chat_threads"])[::-1]:
    title = get_thread_title(thread_id)
    is_active = (thread_id == st.session_state["thread_id"])
    button_icon = "🟢" if is_active else "💬"
    button_label = f"{button_icon} {title}"

    col_btn, col_del = st.sidebar.columns([0.82, 0.18])
    with col_btn:
        if st.button(
            button_label,
            key=f"thread_{thread_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state["thread_id"] = thread_id
            messages = load_conversation(thread_id)

            temp_messages = []
            for msg in messages:
                role = "user" if isinstance(msg, HumanMessage) else "assistant"
                temp_messages.append({"role": role, "content": msg.content})
            st.session_state["message_history"] = temp_messages
            st.rerun()
    with col_del:
        if st.button("🗑️", key=f"del_{thread_id}", help=f"Delete '{title}'", use_container_width=True):
            delete_thread(thread_id)
            if thread_id in st.session_state["chat_threads"]:
                st.session_state["chat_threads"].remove(thread_id)
            if "thread_titles" in st.session_state and thread_id in st.session_state["thread_titles"]:
                del st.session_state["thread_titles"][thread_id]
            if st.session_state["thread_id"] == thread_id:
                reset_chat()
            st.rerun()

#  Main UI 

# history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type here...")

if user_input:
    # If first message in current thread, assign meaningful title
    curr_title = st.session_state["thread_titles"].get(st.session_state["thread_id"], "New Conversation")
    if curr_title == "New Conversation":
        set_thread_title(st.session_state["thread_id"], user_input)

    # User's message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }

    # Assistant streaming block
    with st.chat_message("assistant"):
        # Use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
            event_queue: queue.Queue = queue.Queue()

            async def run_stream():
                try:
                    async for message_chunk, metadata in chatbot.astream(
                        {"messages": [HumanMessage(content=user_input)]},
                        config=CONFIG,
                        stream_mode="messages",
                    ):
                        event_queue.put((message_chunk, metadata))
                except Exception as exc:
                    event_queue.put(("error", exc))
                finally:
                    event_queue.put(None)

            submit_async_task(run_stream())

            while True:
                item = event_queue.get()
                if item is None:
                    break
                message_chunk, metadata = item
                if message_chunk == "error":
                    raise metadata

                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                # Stream ONLY assistant tokens
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    # Save assistant message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
    st.rerun()