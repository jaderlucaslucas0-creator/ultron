from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.brain.orchestrator import orchestrator
from app.memory.store import memory
from app.services.research import research
app=FastAPI(title="ULTRON AI",version="0.1.0")
ROOT=Path(__file__).resolve().parent.parent
@app.get("/health")
def health(): return {"status":"online","name":"ULTRON","version":"0.1.0","memory":"online","research":"online"}
@app.get("/")
def home(): return FileResponse(ROOT/"frontend"/"index.html")
@app.post("/api/chat")
async def chat(payload:dict):
    cid=str(payload.get("conversation_id") or "default").strip(); msg=str(payload.get("message") or "").strip()
    if not msg: raise HTTPException(status_code=400,detail="Mensagem vazia")
    memory.add(cid,"user",msg); reply=await orchestrator.handle(msg); memory.add(cid,"assistant",reply)
    return {"reply":reply,"conversation_id":cid}
@app.get("/api/memory/{conversation_id}")
def get_memory(conversation_id): return {"conversation_id":conversation_id,"messages":memory.list(conversation_id)}
@app.delete("/api/memory/{conversation_id}")
def clear_memory(conversation_id): memory.clear(conversation_id); return {"conversation_id":conversation_id,"cleared":True}
@app.get("/api/research")
def web_research(q:str):
    results=research.search(q); return {"query":q,"count":len(results),"results":results}
