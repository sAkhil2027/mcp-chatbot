import asyncio
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph_mcp_backend import chat_node, tool_guardrail_node, ChatState


async def test_guardrails():
    print("=" * 60)
    print("[TESTING] MCP CHATBOT PROMPT & TOOL GUARDRAILS")
    print("=" * 60)

    # ---------------------------------------------------------
    # Test 1: Prompt Input Security Guardrail (chat_node)
    # ---------------------------------------------------------
    print("\n[Test 1] Testing Prompt Input Guardrail in chat_node...")
    state_prompt_injection: ChatState = {
        "messages": [
            HumanMessage(content="Search for drop table users;")
        ]
    }

    result_prompt = await chat_node(state_prompt_injection)
    blocked_prompt_content = result_prompt["messages"][0].content
    print(f"Result Output: {blocked_prompt_content}")
    assert "Guardrail Policy Rejection" in blocked_prompt_content
    print("[SUCCESS] Test 1 Passed: Prompt injection attempt blocked at input level before calling LLM!")

    # ---------------------------------------------------------
    # Test 2: Tool Parameter Injection Guardrail (tool_guardrail_node)
    # ---------------------------------------------------------
    print("\n[Test 2] Testing Tool Parameter Guardrail...")
    mock_ai_injection_message = AIMessage(
        content="",
        tool_calls=[{
            "name": "get_stock_price",
            "args": {"symbol": "AAPL; DROP TABLE users;"},
            "id": "call_test_injection_123"
        }]
    )

    state_tool_injection: ChatState = {
        "messages": [
            HumanMessage(content="Test prompt"),
            mock_ai_injection_message
        ]
    }

    result_tool = await tool_guardrail_node(state_tool_injection)
    blocked_tool_content = result_tool["messages"][0].content
    print(f"Result Output: {blocked_tool_content}")
    assert "Guardrail Policy Rejection" in blocked_tool_content
    print("[SUCCESS] Test 2 Passed: Malicious tool argument blocked at tool execution level!")

    # ---------------------------------------------------------
    # Test 3: Tool Recursion Loop Limit Guardrail
    # ---------------------------------------------------------
    print("\n[Test 3] Testing Tool Call Recursion Capping...")
    mock_messages = [HumanMessage(content="Loop test")]
    for i in range(6):
        mock_messages.append(ToolMessage(content="output", tool_call_id=f"id_{i}", name="search_tool"))

    mock_ai_loop_message = AIMessage(
        content="",
        tool_calls=[{"name": "search_tool", "args": {"query": "test"}, "id": "call_loop_999"}]
    )
    mock_messages.append(mock_ai_loop_message)

    state_loop: ChatState = {"messages": mock_messages}

    result_loop = await tool_guardrail_node(state_loop)
    loop_blocked_content = result_loop["messages"][0].content
    print(f"Result Output: {loop_blocked_content}")
    assert "Maximum tool calls" in loop_blocked_content
    print("[SUCCESS] Test 3 Passed: Excess tool call recursion correctly capped!")

    print("\n" + "=" * 60)
    print("ALL PROMPT & TOOL GUARDRAIL VERIFICATION TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_guardrails())
