from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent, collection

app = FastAPI(title="Squash Agent API")


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    thread_id: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    res = agent.invoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config={"configurable": {"collection": collection, "thread_id": request.thread_id}},
    )
    return ChatResponse(
        response=res["messages"][-1].content,
        thread_id=request.thread_id,
    )
