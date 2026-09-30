from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from app.core.security import require_api_key
from app.plugins.registry import list_plugins,execute_plugin

router=APIRouter(prefix='/api/plugins',dependencies=[Depends(require_api_key)])

class PluginRequest(BaseModel):
    plugin:str=Field(min_length=1,max_length=80)
    payload:dict={}

@router.get('')
def plugins(): return list_plugins()

@router.post('/execute')
def execute(p:PluginRequest):
    try: return {'plugin':p.plugin,'result':execute_plugin(p.plugin,p.payload)}
    except KeyError as e: raise HTTPException(404,str(e))
    except RuntimeError as e: raise HTTPException(409,str(e))
