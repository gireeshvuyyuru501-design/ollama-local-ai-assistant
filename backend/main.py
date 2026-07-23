from typing import List, Literal
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2:3b"

app = FastAPI(title="Ollama Local AI Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = DEFAULT_MODEL

@app.get("/")
def root():
    return {"message": "API is running", "docs": "/docs"}

@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            r.raise_for_status()
        return {"status": "healthy", "ollama": "connected"}
    except Exception as exc:
        return {"status": "degraded", "ollama": "not reachable", "detail": str(exc)}

@app.post("/chat")
async def chat(request: ChatRequest):
    payload = {
        "model": request.model,
        "messages": [m.model_dump() for m in request.messages],
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            r = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
            r.raise_for_status()
            data = r.json()
        return {"model": request.model, "content": data["message"]["content"]}
    except httpx.ConnectError as exc:
        raise HTTPException(status_code=503, detail="Start Ollama and pull the selected model.") from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Model response timed out.") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text) from exc
