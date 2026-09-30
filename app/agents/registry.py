from app.agents.specialized import general_agent, research_agent

def route(message: str):
    text = message.lower()
    research_words = ("pesquise", "pesquisar", "pesquisa", "procure", "buscar na internet", "notícias")
    if any(word in text for word in research_words):
        return research_agent
    return general_agent
