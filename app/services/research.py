from openai import OpenAI
from app.core.config import settings

def research_web(query:str)->str:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada.")
    kwargs={"api_key":settings.openai_api_key}
    if settings.openai_base_url: kwargs["base_url"]=settings.openai_base_url
    client=OpenAI(**kwargs)
    response=client.responses.create(
        model=settings.research_model,
        tools=[{"type":"web_search_preview"}],
        input=(
            "Pesquise na web e responda em português brasileiro. "
            "Use fontes atuais e diferencie fatos de opiniões. "
            "Inclua as fontes relevantes quando disponíveis. Pergunta: "+query
        )
    )
    return getattr(response,"output_text","") or "A pesquisa não retornou texto."
