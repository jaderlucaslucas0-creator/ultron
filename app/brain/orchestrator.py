from app.database.models import Conversation, Message
from app.database.repositories import recent_memories, add_log
from app.brain.router import route_request

def process_message(db,text,conversation_id=None):
    conversation=db.get(Conversation,conversation_id) if conversation_id else None
    if conversation is None:
        conversation=Conversation(title=text[:80] or "Nova conversa")
        db.add(conversation); db.commit(); db.refresh(conversation)
    db.add(Message(conversation_id=conversation.id,role="user",content=text)); db.commit()
    memories=recent_memories(db)
    handler=route_request(text)
    result=handler.handle(text,db,conversation.id,memories) if hasattr(handler,"handle") else handler(text,db,conversation.id,memories)
    db.add(Message(conversation_id=conversation.id,role="assistant",content=result))
    add_log(db,"chat.completed","conversation_id=%s" % conversation.id)
    return {"conversation_id":conversation.id,"answer":result}
