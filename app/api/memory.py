from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from app.core.security import require_api_key
from app.database.database import get_db
from app.database.models import Memory
from app.database.repositories import add_memory
router=APIRouter(prefix="/api/memory",dependencies=[Depends(require_api_key)])
class MemoryCreate(BaseModel):
    content:str=Field(min_length=1,max_length=5000)
    category:str=Field(default="general",max_length=50)
@router.get("")
def list_memory(db=Depends(get_db)):
    return [{"id":m.id,"content":m.content,"category":m.category} for m in db.query(Memory).order_by(Memory.updated_at.desc()).all()]
@router.post("")
def create_memory(payload:MemoryCreate,db=Depends(get_db)):
    m=add_memory(db,payload.content.strip(),payload.category)
    return {"id":m.id,"content":m.content,"category":m.category}
@router.delete("/{memory_id}")
def delete_memory(memory_id:int,db=Depends(get_db)):
    m=db.get(Memory,memory_id)
    if not m: raise HTTPException(404,"Memória não encontrada.")
    db.delete(m);db.commit();return {"deleted":True}
