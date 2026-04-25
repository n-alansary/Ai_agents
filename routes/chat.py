from fastapi import APIRouter
from schemas.chat import ChatRequest, ChatResponse
from controllers.chat import chat_controller

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    return await chat_controller(request)
