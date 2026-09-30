from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "HERMES"
    database_url: str = ""
    local_ai_url: str = "http://127.0.0.1:11434"
    local_ai_model: str = "llama3.2"
    max_upload_mb: int = 10
    hermes_api_key: str = ""
    cors_origins: str = "*"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

settings = Settings()
