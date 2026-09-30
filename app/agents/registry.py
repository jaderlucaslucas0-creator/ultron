from app.agents.base import Agent
from app.agents.specialized import GENERAL_AGENT,RESEARCH_AGENT,CODING_AGENT,PLANNING_AGENT

AGENTS={a.name:a for a in [GENERAL_AGENT,RESEARCH_AGENT,CODING_AGENT,PLANNING_AGENT]}

def list_agents():
    return [{'name':a.name,'description':a.description} for a in AGENTS.values()]

def get_agent(name:str):
    return AGENTS.get(name)

def choose_agent(text:str):
    t=text.lower()
    if any(x in t for x in ['pesquise','pesquisar','notícia','noticias','web','internet']): return RESEARCH_AGENT
    if any(x in t for x in ['código','codigo','programar','python','javascript','github']): return CODING_AGENT
    if any(x in t for x in ['planeje','planejar','plano','organize','organizar']): return PLANNING_AGENT
    return GENERAL_AGENT
