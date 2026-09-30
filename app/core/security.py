from fastapi import Header, HTTPException
from app.core.config import settings

def require_api_key(authorization: str | None = Header(default=None)):
    if not settings.ultron_api_key:
        return
    if authorization != f"Bearer {settings.ultron_api_key}":
        raise HTTPException(status_code=401, detail="Autenticação necessária.")
