import time
from fastapi import APIRouter,Depends
from app.core.security import require_api_key
from app.database.database import get_db
from app.database.models import Memory,Skill,Task,Automation
router=APIRouter()
START_TIME=time.time()
@router.get("/health")
def health(): return {"status":"online","service":"ULTRON"}
@router.get("/api/status",dependencies=[Depends(require_api_key)])
def status(db=Depends(get_db)):
    return {"status":"online","service":"ULTRON","uptime_seconds":int(time.time()-START_TIME),"memory_count":db.query(Memory).count(),"skills_count":db.query(Skill).count(),"tasks_count":db.query(Task).filter(Task.status!="done").count(),"automations_count":db.query(Automation).count()}
