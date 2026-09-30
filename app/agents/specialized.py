from app.agents.base import Agent

GENERAL_AGENT=Agent(
    "general","Assistente geral",
    "Responda tarefas gerais com clareza, contexto e objetividade."
)
RESEARCH_AGENT=Agent(
    "research","Pesquisa",
    "Diferencie conhecimento do modelo de dados obtidos na web. Quando pesquisa web estiver disponível, use-a e apresente fontes."
)
CODING_AGENT=Agent(
    "coding","Programação",
    "Atue como engenheiro de software. Analise requisitos, proponha implementação segura e não alegue que código foi executado sem execução real."
)
PLANNING_AGENT=Agent(
    "planning","Planejamento",
    "Transforme objetivos em etapas claras, verificáveis e priorizadas."
)
