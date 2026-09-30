import os, subprocess, webbrowser, platform
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
TOKEN=os.getenv('ULTRON_AGENT_TOKEN','change-me')
app=FastAPI(title='ULTRON Desktop Agent')
class Command(BaseModel): action:str; target:str=''
ALLOWED_APPS={'notepad':'notepad.exe','calculator':'calc.exe','paint':'mspaint.exe','explorer':'explorer.exe'}
@app.get('/health')
def health(): return {'status':'online','platform':platform.system()}
@app.post('/command')
def command(cmd:Command,x_ultron_token:str|None=Header(default=None)):
 if x_ultron_token!=TOKEN: raise HTTPException(401,'invalid token')
 a=cmd.action.lower().strip(); t=cmd.target.strip()
 if a=='open_url': webbrowser.open(t); return {'ok':True}
 if a=='open_app' and t.lower() in ALLOWED_APPS: subprocess.Popen(ALLOWED_APPS[t.lower()]); return {'ok':True}
 if a=='type_text':
  import pyautogui; pyautogui.write(t,interval=.01); return {'ok':True}
 if a=='hotkey':
  import pyautogui; pyautogui.hotkey(*[x.strip() for x in t.split('+')]); return {'ok':True}
 return {'ok':False,'message':'command not allowed'}
