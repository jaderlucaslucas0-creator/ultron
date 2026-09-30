import sqlite3
from pathlib import Path
from threading import Lock
from app.core.config import settings

class MemoryStore:
    def __init__(self):
        path = Path(settings.database_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.lock = Lock()
        self.db.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        self.db.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, id)")
        self.db.commit()
    def add(self, conversation_id, role, content):
        with self.lock:
            self.db.execute("INSERT INTO messages(conversation_id, role, content) VALUES (?, ?, ?)", (conversation_id, role, content)); self.db.commit()
    def list(self, conversation_id, limit=50):
        rows=self.db.execute("SELECT role,content,created_at FROM messages WHERE conversation_id=? ORDER BY id DESC LIMIT ?",(conversation_id,limit)).fetchall(); rows.reverse()
        return [{"role":r[0],"content":r[1],"created_at":r[2]} for r in rows]
    def clear(self, conversation_id):
        with self.lock:
            self.db.execute("DELETE FROM messages WHERE conversation_id=?",(conversation_id,)); self.db.commit()
memory=MemoryStore()
