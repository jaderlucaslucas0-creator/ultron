import base64
from openai import OpenAI
from app.core.config import settings

def analyze_image(data:bytes,content_type:str,prompt:str)->str:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada.")
    if not content_type.startswith("image/"):
        raise ValueError("Envie uma imagem.")
    if len(data)>10*1024*1024:
        raise ValueError("Imagem excede 10 MB.")
    kwargs={"api_key":settings.openai_api_key}
    if settings.openai_base_url: kwargs["base_url"]=settings.openai_base_url
    client=OpenAI(**kwargs)
    encoded=base64.b64encode(data).decode()
    response=client.chat.completions.create(
        model=settings.vision_model,
        messages=[{"role":"user","content":[
            {"type":"text","text":prompt},
            {"type":"image_url","image_url":{"url":f"data:{content_type};base64,{encoded}"}}
        ]}]
    )
    return response.choices[0].message.content or "Não consegui analisar a imagem."
