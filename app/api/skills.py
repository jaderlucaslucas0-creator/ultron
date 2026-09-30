from fastapi import APIRouter,Depends
from app.core.security import require_api_key
from app.skills.manager import SKILLS
router=APIRouter(prefix="/api/skills",dependencies=[Depends(require_api_key)])
@router.get("")
def skills(): return [{"name":s.name,"description":s.description,"enabled":True} for s in SKILLS]
