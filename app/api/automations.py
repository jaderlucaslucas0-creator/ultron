from datetime import datetime, timezone
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from app.core.security import require_api_key
from app.database.database import get_db
from app.database.models import Automation

router=APIRouter(prefix="/api/automations",dependencies=[Depends(require_api_key)])
class AutomationRequest(BaseModel):
    name:str=Field(min_length=1,max_length=200)
    schedule:str=Field(min_length=1,max_length=100)
    enabled:bool=True

@router.post("")
def create(p:AutomationRequest,db=Depends(get_db)):
    x=Automation(name=p.name,schedule=p.schedule,enabled=p.enabled); db.add(x); db.commit(); db.refresh(x)
    return {"id":x.id,"name":x.name,"schedule":x.schedule,"enabled":x.enabled}

@router.get("")
def list_all(db=Depends(get_db)):
    return [{"id":x.id,"name":x.name,"schedule":x.schedule,"enabled":x.enabled} for x in db.query(Automation).order_by(Automation.id.desc()).all()]

@router.patch("/{automation_id}")
def toggle(automation_id:int,enabled:bool,db=Depends(get_db)):
    x=db.get(Automation,automation_id)
    if not x: raise HTTPException(404,"Automação não encontrada.")
    x.enabled=enabled; db.commit()
    return {"id":x.id,"enabled":x.enabled}

@router.delete("/{automation_id}")
def delete(automation_id:int,db=Depends(get_db)):
    x=db.get(Automation,automation_id)
    if not x: raise HTTPException(404,"Automação não encontrada.")
    db.delete(x); db.commit()
    return {"deleted":True,"id":automation_id}
