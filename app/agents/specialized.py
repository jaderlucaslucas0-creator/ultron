from app.brain.providers import ollama
from app.services.research import research

async def general_agent(message: str) -> str:
    result = await ollama.generate(message)
    if result:
        return result
    return f"ULTRON online. Recebi: {message}\n\nA IA local ainda não está conectada. Configure Ollama para ativar respostas inteligentes sem OpenAI API Key."

async def research_agent(message: str) -> str:
    results = research.search(message)
    if not results:
        return "Não encontrei resultados para essa pesquisa."
    lines = ["Encontrei estes resultados:"]
    for item in results[:5]:
        lines.append(f"- {item['title']} — {item['url']}")
    return "\n".join(lines)
