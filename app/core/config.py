from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name:str="ULTRON"; database_url:str=""; openai_api_key:str=""; openai_base_url:str=""; openai_model:str="gpt-4o-mini"
    stt_model:str="gpt-4o-mini-transcribe"; tts_model:str="gpt-4o-mini-tts"; tts_voice:str="alloy"; tts_speed:float=1.0
    research_model:str="gpt-5.6-luna"; vision_model:str="gpt-5.6-luna"
    max_upload_mb:int=10; ultron_api_key:str=""; cors_origins:str="*"
    model_config=SettingsConfigDict(env_file=".env",case_sensitive=False,extra="ignore")
settings=Settings()
