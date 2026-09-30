from fastapi import APIRouter,Depends,File,HTTPException,UploadFile
from fastapi.responses import Response
from pydantic import BaseModel,Field
from app.core.security import require_api_key
from app.voice.service import transcribe,synthesize
router=APIRouter(prefix="/api/voice",dependencies=[Depends(require_api_key)])
class TTSRequest(BaseModel):
 text:str=Field(min_length=1,max_length=5000); voice:str=Field(default="alloy",max_length=50); speed:float=Field(default=1,ge=.25,le=4)
@router.post("/transcribe")
async def transcribe_audio(file:UploadFile=File(...)):
 if not file.content_type or not file.content_type.startswith("audio/"): raise HTTPException(400,"Envie um arquivo de áudio.")
 data=await file.read()
 if not data: raise HTTPException(400,"Arquivo vazio.")
 if len(data)>25*1024*1024: raise HTTPException(413,"Áudio excede 25 MB.")
 try:return {"text":transcribe(data,file.filename or "ultron.webm")}
 except Exception:raise HTTPException(502,"Não foi possível transcrever o áudio.")
@router.post("/speak")
def speak(p:TTSRequest):
 try:return Response(content=synthesize(p.text,p.voice,p.speed),media_type="audio/mpeg")
 except Exception:raise HTTPException(502,"Não foi possível gerar a voz.")
