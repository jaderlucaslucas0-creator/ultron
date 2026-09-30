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

def answer_with_ai(text,db,conversation_id,memories,agent=None):
    if not settings.openai_api_key:
        return "O ULTRON está online, mas OPENAI_API_KEY ainda não foi configurada."
    kwargs={"api_key":settings.openai_api_key}
    if settings.openai_base_url:
        kwargs["base_url"]=settings.openai_base_url
    client=OpenAI(**kwargs)
    response=client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role":"system","content":build_system_prompt(memories,agent)},{"role":"user","content":text}],
        temperature=0.4)
    return response.choices[0].message.content or "Não recebi uma resposta do modelo."
