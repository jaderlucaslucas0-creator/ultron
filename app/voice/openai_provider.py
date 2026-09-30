from openai import OpenAI
from app.core.config import settings
class OpenAIVoiceProvider:
 def __init__(self):
  if not settings.openai_api_key: raise RuntimeError("OPENAI_API_KEY não configurada.")
  kw={"api_key":settings.openai_api_key}
  if settings.openai_base_url: kw["base_url"]=settings.openai_base_url
  self.client=OpenAI(**kw)
 def transcribe(self,audio,filename):
  return self.client.audio.transcriptions.create(model=settings.stt_model,file=(filename,audio,"audio/webm")).text.strip()
 def synthesize(self,text,voice,speed):
  return self.client.audio.speech.create(model=settings.tts_model,voice=voice,input=text,speed=speed,response_format="mp3").content
