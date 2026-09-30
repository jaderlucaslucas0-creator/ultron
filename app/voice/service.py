from app.voice.openai_provider import OpenAIVoiceProvider
def transcribe(audio,filename): return OpenAIVoiceProvider().transcribe(audio,filename)
def synthesize(text,voice,speed): return OpenAIVoiceProvider().synthesize(text,voice,speed)
