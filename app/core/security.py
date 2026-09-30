from fastapi import Header, HTTPException
from app.core.config import settings

def require_api_key(authorization: str | None = Header(default=None)):
    # Hermes funciona sem API key por padrão.
    # Se HERMES_API_KEY for configurada no servidor, ela passa a proteger as APIs.
    if not settings.hermes_api_key:
        return
    if authorization != f"Bearer {settings.hermes_api_key}":
        raise HTTPException(status_code=401, detail="Autenticação necessária.")
