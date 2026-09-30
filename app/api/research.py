from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.core.security import require_api_key
from app.services.research import research_web

router = APIRouter(prefix="/api/research", dependencies=[Depends(require_api_key)])

class ResearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=5000)

@router.post("")
def research(p: ResearchRequest):
    try:
        return {"query": p.query, "answer": research_web(p.query)}
    except Exception as e:
        raise HTTPException(502, str(e))
