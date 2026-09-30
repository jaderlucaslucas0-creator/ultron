from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ultron_name: str = "ULTRON"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2"
    database_path: str = "data/ultron.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
