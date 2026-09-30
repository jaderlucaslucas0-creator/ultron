from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from app.brain.orchestrator import orchestrator
from app.memory.store import memory
from app.services.research import research

app = FastAPI(title="ULTRON AI", version="0.1.0")
ROOT = Path(__file__).resolve().parent.parent

@app.get("/health")
def health():
    return {"status":"online","name":"ULTRON","version":"0.1.0"}

@app.get("/")
def home():
    return FileResponse(ROOT / "frontend" / "index.html")

@app.post("/api/chat")
async def chat(payload: dict):
    conversation_id = str(payload.get("conversation_id") or "default")
    message = str(payload.get("message") or "").strip()
    if not message:
        return {"reply":"Diga o que você precisa."}
    memory.add(conversation_id, "user", message)
    reply = await orchestrator.handle(message)
    memory.add(conversation_id, "assistant", reply)
    return {"reply": reply, "conversation_id": conversation_id}

@app.get("/api/memory/{conversation_id}")
def get_memory(conversation_id: str):
    return {"messages": memory.list(conversation_id)}

@app.get("/api/research")
def web_research(q: str):
    return {"query": q, "results": research.search(q)}
