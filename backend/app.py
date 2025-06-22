from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "agent"))

from agent.chat_agent import load_rag_agent
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

rag_agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_agent
    try:
        rag_agent = load_rag_agent("vectorstore/faiss_index")
        if not hasattr(rag_agent, "memory"):
            rag_agent.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        print("✅ RAG Agent uspešno učitan!")
    except Exception as e:
        print(f"❌ Greška pri učitavanju agenta: {e}")
    yield

app = FastAPI(title="TurBot API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    success: bool

class ChatHistoryMessage(BaseModel):
    id: int
    type: str  
    content: str
    timestamp: str | None = None  

class ChatHistory(BaseModel):
    messages: List[ChatHistoryMessage]

@app.get("/")
async def root():
    return {"message": "TurBot API je pokrenuta!", "status": "running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    if not rag_agent:
        raise HTTPException(status_code=500, detail="Agent nije inicijalizovan")
    try:
        response_text = rag_agent.chat(message.message, session_id=message.session_id)
        return ChatResponse(response=response_text, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška pri obradi: {str(e)}")

@app.get("/chat/history", response_model=ChatHistory)
async def get_chat_history(session_id: str = Query(...)):
    if not rag_agent:
        raise HTTPException(status_code=500, detail="Agent nije inicijalizovan")
    try:
        if session_id not in rag_agent.chat_histories:
            return ChatHistory(messages=[])
        
        history_msgs = rag_agent.chat_histories[session_id]
        
        history = []
        for i, msg in enumerate(history_msgs):
            history.append(ChatHistoryMessage(
                id=i,
                type="human" if isinstance(msg, HumanMessage) else "ai",
                content=msg.content,
                timestamp=None
            ))
        return ChatHistory(messages=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška pri dobijanju istorije: {str(e)}")

@app.delete("/chat/history")
async def clear_chat_history(session_id: str = Query(...)):
    if not rag_agent:
        raise HTTPException(status_code=500, detail="Agent nije inicijalizovan")
    try:
        if session_id in rag_agent.chat_histories:
            del rag_agent.chat_histories[session_id]
        return {"message": f"Istorija za sesiju {session_id} je obrisana", "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška pri brisanju istorije: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent_loaded": rag_agent is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
