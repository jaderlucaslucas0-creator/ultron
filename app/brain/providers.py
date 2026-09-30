import httpx
from app.core.config import settings

class OllamaProvider:
    async def generate(self, prompt: str):
        try:
            async with httpx.AsyncClient(timeout=90) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/generate",
                    json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
                )
                response.raise_for_status()
                return response.json().get("response")
        except Exception:
            return None

ollama = OllamaProvider()
