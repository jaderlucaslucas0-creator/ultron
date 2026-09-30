from fastapi import APIRouter,Depends,File,Form,HTTPException,UploadFile
from app.core.security import require_api_key
from app.services.vision import analyze_image

router=APIRouter(prefix="/api/vision",dependencies=[Depends(require_api_key)])
@router.post("/analyze")
async def analyze(file:UploadFile=File(...),prompt:str=Form("Descreva e analise esta imagem em português brasileiro.")):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400,"Envie uma imagem.")
    data=await file.read()
    try:return {"filename":file.filename or "imagem","answer":analyze_image(data,file.content_type,prompt)}
    except ValueError as e: raise HTTPException(400,str(e))
    except Exception: raise HTTPException(502,"Não foi possível analisar a imagem.")
