from langchain.agents.middleware import after_model, AgentState
from langgraph.runtime import Runtime
from langchain_core.messages import AIMessage, ToolMessage
from typing import Any

@after_model(can_jump_to=["end"])
def delete_guard(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """
    Middleware that runs after the model generates a response.
    Checks if the model generated any tool calls attempting to delete data.
    If so, it overrides the AI message to return a direct response indicating
    that deletes are not allowed, and stops execution entirely.
    """
    messages = state.get("messages", [])
    if not messages:
        return None

    last_message = messages[-1]

    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return None

    has_delete = False

    for tool_call in last_message.tool_calls:
        if tool_call["name"] == "execute_mongo_crud":
            args = tool_call.get("args", {})
            operation = args.get("operation", "").lower().strip()
            
            if operation in ["delete_one", "delete_many"]:
                has_delete = True
                break

    # If a delete operation was found, we update the AI message to remove the tool calls
    # and provide a friendly rejection message, and jump to the end of execution.
    if has_delete:
        new_ai_message = AIMessage(
            content="Sorry, delete operations are not allowed. Execution stopped.",
            tool_calls=[]
        )
        
        if hasattr(last_message, "id") and last_message.id:
            new_ai_message.id = last_message.id
            
        return {
            "messages": [new_ai_message],
            "jump_to": "end"
        }

    return None
