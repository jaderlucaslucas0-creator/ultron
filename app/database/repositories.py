from sqlalchemy.orm import Session
from app.database.models import Memory, Log

def add_memory(db: Session, content: str, category: str="general"):
    item=Memory(content=content,category=category,authorized=True)
    db.add(item); db.commit(); db.refresh(item)
    return item

def recent_memories(db: Session, limit:int=10):
    return db.query(Memory).filter(Memory.authorized==True).order_by(Memory.updated_at.desc()).limit(limit).all()

def add_log(db: Session,event:str,details:str="",level:str="INFO"):
    item=Log(event=event,details=details[:4000],level=level)
    db.add(item); db.commit()
    return item
