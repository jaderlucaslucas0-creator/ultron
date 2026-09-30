import sqlite3
from pathlib import Path
from app.core.config import settings

class MemoryStore:
    def __init__(self):
        path = Path(settings.database_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT, role TEXT, content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        self.db.commit()

    def add(self, conversation_id, role, content):
        self.db.execute("INSERT INTO messages(conversation_id,role,content) VALUES(?,?,?)",(conversation_id,role,content))
        self.db.commit()

    def list(self, conversation_id):
        rows = self.db.execute("SELECT role,content,created_at FROM messages WHERE conversation_id=? ORDER BY id",(conversation_id,)).fetchall()
        return [{"role":r[0],"content":r[1],"created_at":r[2]} for r in rows]

memory = MemoryStore()
