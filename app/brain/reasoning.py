import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from app.core.config import settings
from app.skills.manager import skill_context

def build_system_prompt(memories, agent=None):
    memory_text = "\n".join("- " + m.content for m in memories) or "- nenhuma"
    agent_text = agent.instructions if agent else "Atue como assistente geral."
    return """Você é HERMES, um assistente pessoal de IA em português brasileiro.
Seja objetivo, natural, útil e respeitoso.
Não invente ações executadas.
Se não souber algo, diga claramente.
Você pode ajudar com programação, estudos, organização, ideias, tecnologia e tarefas do computador quando houver uma ferramenta disponível.
Modo especializado:
%s
Memórias autorizadas:
%s
Skills:
%s""" % (agent_text, memory_text, skill_context())

def _local_answer(text, prompt):
    payload = json.dumps({
        "model": settings.local_ai_model,
        "prompt": prompt + "\n\nUsuário: " + text + "\nHERMES:",
        "stream": False
    }).encode()
    req = Request(
        settings.local_ai_url.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())
    return data.get("response", "").strip()

def _offline_answer(text):
    from datetime import datetime
    import re
    t = text.lower().strip()

    if any(x in t for x in ("olá", "ola", "oi", "e aí", "e ai")):
        return "Olá. Hermes online. Estou funcionando sem chave de API."
    if any(x in t for x in ("quem é você", "quem e voce", "seu nome")):
        return "Eu sou o Hermes, seu assistente pessoal. Posso conversar, guardar memórias, usar skills e pesquisar informações quando o módulo estiver disponível."
    if "hora" in t:
        return "Agora são " + datetime.now().strftime("%H:%M") + "."
    if "data" in t or "dia de hoje" in t:
        return "Hoje é " + datetime.now().strftime("%d/%m/%Y") + "."
    if any(x in t for x in ("ajuda", "o que você faz", "o que voce faz")):
        return "Posso conversar, calcular, guardar memórias, pesquisar na web, analisar arquivos e organizar tarefas. Para respostas generativas completas sem API externa, conecte um modelo local como Ollama."
    if "hermes" in t and any(x in t for x in ("online", "está aí", "esta ai")):
        return "Online e pronto."
    if re.search(r"\b(2\+2|quanto é 2 mais 2|quanto e 2 mais 2)\b", t):
        return "2 + 2 = 4."
    return "Recebi sua mensagem. Estou no modo sem API. Para respostas de IA generativas completas, posso usar um modelo local compatível com Ollama; os comandos básicos continuam funcionando sem chave."

def answer_with_ai(text, db, conversation_id, memories, agent=None):
    prompt = build_system_prompt(memories, agent)
    try:
        answer = _local_answer(text, prompt)
        if answer:
            return answer
    except (URLError, HTTPError, OSError, TimeoutError, ValueError):
        pass
    return _offline_answer(text)
