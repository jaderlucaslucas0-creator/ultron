import os, platform, subprocess, webbrowser
from urllib.parse import urlparse
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

TOKEN=os.getenv("ULTRON_AGENT_TOKEN","")
if not TOKEN or TOKEN in {"change-me","ultron"}:
    raise RuntimeError("Defina ULTRON_AGENT_TOKEN com um segredo forte antes de iniciar o Desktop Agent.")

app=FastAPI(title="ULTRON Desktop Agent")
class Command(BaseModel):
    action:str
    target:str=""

ALLOWED_APPS={"notepad":"notepad.exe","calculator":"calc.exe","paint":"mspaint.exe","explorer":"explorer.exe"}

def valid_url(value:str)->bool:
    try:
        parsed=urlparse(value)
        return parsed.scheme in {"http","https"} and bool(parsed.netloc)
    except Exception:
        return False

@app.get("/health")
def health(): return {"status":"online","platform":platform.system()}

@app.post("/command")
def command(cmd:Command,x_ultron_token:str|None=Header(default=None)):
    if x_ultron_token != TOKEN: raise HTTPException(status_code=401,detail="invalid token")
    action=cmd.action.lower().strip(); target=cmd.target.strip()
    if action=="open_url":
        if not valid_url(target): raise HTTPException(status_code=400,detail="URL inválida")
        webbrowser.open(target); return {"ok":True,"action":action,"target":target}
    if action=="open_app":
        key=target.lower()
        if key not in ALLOWED_APPS: return {"ok":False,"message":"Aplicativo não permitido"}
        subprocess.Popen(ALLOWED_APPS[key]); return {"ok":True,"action":action,"target":key}
    if action=="type_text":
        import pyautogui
        pyautogui.write(target,interval=.01); return {"ok":True,"action":action}
    if action=="hotkey":
        import pyautogui
        keys=[x.strip().lower() for x in target.split("+") if x.strip()]
        allowed={"ctrl","shift","alt","tab","enter","esc","space","win","a","c","v","x","z","s","f","n","t","l"}
        if not keys or any(key not in allowed for key in keys): return {"ok":False,"message":"Atalho não permitido"}
        pyautogui.hotkey(*keys); return {"ok":True,"action":action,"target":"+".join(keys)}
    return {"ok":False,"message":"command not allowed"}
