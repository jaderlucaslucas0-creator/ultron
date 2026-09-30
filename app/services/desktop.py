import httpx
from app.core.config import settings
class DesktopService:
    async def command(self, action, target=""):
        if not settings.desktop_agent_url: return {"ok":False,"message":"Desktop Agent não configurado"}
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r=await c.post(settings.desktop_agent_url+"/command",json={"action":action,"target":target},headers={"X-Ultron-Token":settings.desktop_agent_token}); r.raise_for_status(); return r.json()
        except Exception as e: return {"ok":False,"message":str(e)}
desktop=DesktopService()
