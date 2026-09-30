from app.agents.specialized import general_agent, research_agent
from app.agents.desktop import desktop_agent

def route(message: str):
    text = message.lower().strip()
    research_words = ("pesquise", "pesquisar", "pesquisa", "procure", "buscar na internet", "notícias")
    desktop_words = ("abra ", "abrir ", "feche ", "fechar ", "digite ", "pressione ", "atalho ", "computador", "desktop")
    if any(word in text for word in research_words):
        return research_agent
    if any(word in text for word in desktop_words):
        return desktop_agent
    return general_agent
