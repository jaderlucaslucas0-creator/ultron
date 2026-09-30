from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
 ultron_name:str='ULTRON'
 ollama_base_url:str='http://127.0.0.1:11434'
 ollama_model:str='llama3.2'
 database_path:str='data/ultron.db'
 desktop_agent_url:str=''
 desktop_agent_token:str=''
 model_config=SettingsConfigDict(env_file='.env',extra='ignore')
settings=Settings()
