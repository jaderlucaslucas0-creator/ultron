from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from app.core.security import require_api_key
from app.agents.registry import list_agents,get_agent,choose_agent

router=APIRouter(prefix='/api/agents',dependencies=[Depends(require_api_key)])

class AgentRequest(BaseModel):
    agent:str=Field(min_length=1,max_length=80)
    text:str=Field(min_length=1,max_length=10000)

@router.get('')
def agents():
    return list_agents()

@router.post('/route')
def route_agent(text:str):
    a=choose_agent(text)
    return {'agent':a.name,'description':a.description}

@router.post('/run')
def run_agent(p:AgentRequest):
    a=get_agent(p.agent)
    if not a: raise HTTPException(404,'Agente não encontrado.')
    return {'agent':a.name,'answer':a.run(p.text)}
