import json
from urllib.request import Request,urlopen
from urllib.error import URLError,HTTPError
from openai import OpenAI
from app.core.config import settings
from app.skills.manager import skill_context

def build_system_prompt(memories,agent=None):
    memory_text="\n".join("- "+m.content for m in memories) or "- nenhuma"
    agent_text=(agent.instructions if agent else "Atue como assistente geral.")
    return """Você é ULTRON, um assistente pessoal de IA.
Seja objetivo, natural, educado e levemente futurista.
Nunca diga que executou uma ação se ela não foi realmente executada.
Se não souber, diga claramente.
Modo especializado:
%s
Memórias autorizadas:
%s
Skills:
%s""" % (agent_text,memory_text,skill_context())

def _local_answer(text,prompt):
    payload=json.dumps({
        "model":settings.local_ai_model,
        "prompt":prompt+"\n\nUsuário: "+text+"\nULTRON:",
        "stream":False
    }).encode()
    req=Request(settings.local_ai_url.rstrip("/")+"/api/generate",data=payload,headers={"Content-Type":"application/json"})
    with urlopen(req,timeout=8) as r:
        data=json.loads(r.read().decode())
    return data.get("response","").strip()

def _offline_answer(text):
    t=text.lower().strip()
    if any(x in t for x in ["olá","ola","oi","e aí","e ai"]):
        return "Olá. ULTRON online. Estou operando em modo local, sem chave de API."
    if "quem é você" in t or "quem e voce" in t:
        return "Sou o ULTRON, seu assistente pessoal. Atualmente estou em modo local, sem dependência de uma chave de API."
    if "hora" in t:
        from datetime import datetime
        return "Agora são "+datetime.now().strftime("%H:%M")+"."
    if "ajuda" in t:
        return "Posso conversar, organizar ideias, executar Skills disponíveis e usar os módulos configurados. Para respostas generativas completas, conecte um modelo local como Ollama."
    return "Recebi sua mensagem. O ULTRON está em modo offline porque nenhuma API de IA foi configurada. Para respostas generativas completas sem chave externa, conecte um modelo local compatível com Ollama."

def answer_with_ai(text,db,conversation_id,memories,agent=None):
    prompt=build_system_prompt(memories,agent)
    if settings.openai_api_key:
        kwargs={"api_key":settings.openai_api_key}
        if settings.openai_base_url:
            kwargs["base_url"]=settings.openai_base_url
        client=OpenAI(**kwargs)
        response=client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role":"system","content":prompt},{"role":"user","content":text}],
            temperature=0.4)
        return response.choices[0].message.content or "Não recebi uma resposta do modelo."
    try:
        answer=_local_answer(text,prompt)
        if answer:
            return answer
    except (URLError,HTTPError,OSError,TimeoutError):
        pass
    return _offline_answer(text)
