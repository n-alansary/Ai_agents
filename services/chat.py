from services.agent_setup import agent, collection

async def process_chat_message(message: str, thread_id: str) -> str:
    """
    Service layer to interact with the LLM agent.
    """
    res = await agent.ainvoke(
        {"messages": [{"role": "user", "content": message}]},
        config={"configurable": {"collection": collection, "thread_id": thread_id}},
    )
    return res["messages"][-1].content
