from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.core.security import require_api_key
from app.database.database import get_db
from app.brain.orchestrator import process_message

router = APIRouter(prefix="/api/chat", dependencies=[Depends(require_api_key)])

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    conversation_id: int | None = None

@router.post("")
def chat(payload: ChatRequest, db=Depends(get_db)):
    try:
        return process_message(db, payload.message.strip(), payload.conversation_id)
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception:
        raise HTTPException(500, "O Hermes não conseguiu processar a solicitação.")
