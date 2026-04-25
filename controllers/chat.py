from schemas.chat import ChatRequest, ChatResponse
from services.chat import process_chat_message

async def chat_controller(request: ChatRequest) -> ChatResponse:
    """
    Controller layer to handle the HTTP request structure and orchestrate the service call.
    """
    response_text = await process_chat_message(request.message, request.thread_id)
    
    return ChatResponse(
        response=response_text,
        thread_id=request.thread_id,
    )
