import asyncio
from langchain_core.messages import HumanMessage
from langgraph_mcp_backend import chatbot

async def main():

    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    response = await chatbot.ainvoke(
        {
            "messages": [
                HumanMessage(content="What is AI?")
            ]
        },
        config=config
    )

    print(response["messages"][-1].content)

asyncio.run(main())