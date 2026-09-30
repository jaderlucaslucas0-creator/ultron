from fastapi import APIRouter,Depends,File,HTTPException,UploadFile
from fastapi.responses import Response
from app.core.security import require_api_key
from app.database.database import get_db
from app.database.models import UploadedFile

router=APIRouter(prefix="/api/files",dependencies=[Depends(require_api_key)])
MAX_BYTES=10*1024*1024

@router.post("")
async def upload(file:UploadFile=File(...),db=Depends(get_db)):
    data=await file.read()
    if not data: raise HTTPException(400,"Arquivo vazio.")
    if len(data)>MAX_BYTES: raise HTTPException(413,"Arquivo excede 10 MB.")
    item=UploadedFile(filename=file.filename or "arquivo",content_type=file.content_type or "application/octet-stream",size=len(data),data=data)
    db.add(item); db.commit(); db.refresh(item)
    return {"id":item.id,"filename":item.filename,"content_type":item.content_type,"size":item.size}

@router.get("")
def list_files(db=Depends(get_db)):
    return [{"id":x.id,"filename":x.filename,"content_type":x.content_type,"size":x.size,"created_at":x.created_at.isoformat()} for x in db.query(UploadedFile).order_by(UploadedFile.id.desc()).all()]

@router.get("/{file_id}")
def download(file_id:int,db=Depends(get_db)):
    item=db.get(UploadedFile,file_id)
    if not item: raise HTTPException(404,"Arquivo não encontrado.")
    return Response(content=item.data,media_type=item.content_type,headers={"Content-Disposition":f'attachment; filename="{item.filename}"'})
