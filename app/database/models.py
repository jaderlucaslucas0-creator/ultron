from datetime import datetime, timezone
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

def now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(120))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Conversation(Base):
    __tablename__="conversations"
    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str]=mapped_column(String(200),default="Nova conversa")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Message(Base):
    __tablename__="messages"
    id: Mapped[int]=mapped_column(primary_key=True)
    conversation_id: Mapped[int]=mapped_column(ForeignKey("conversations.id"),index=True)
    role: Mapped[str]=mapped_column(String(30))
    content: Mapped[str]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Memory(Base):
    __tablename__="memories"
    id: Mapped[int]=mapped_column(primary_key=True)
    content: Mapped[str]=mapped_column(Text)
    category: Mapped[str]=mapped_column(String(50),default="general")
    authorized: Mapped[bool]=mapped_column(Boolean,default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)

class Task(Base):
    __tablename__="tasks"
    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str]=mapped_column(String(300))
    status: Mapped[str]=mapped_column(String(30),default="pending")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Skill(Base):
    __tablename__="skills"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(80),unique=True)
    description: Mapped[str]=mapped_column(Text)
    enabled: Mapped[bool]=mapped_column(Boolean,default=True)

class Log(Base):
    __tablename__="logs"
    id: Mapped[int]=mapped_column(primary_key=True)
    event: Mapped[str]=mapped_column(String(120))
    details: Mapped[str]=mapped_column(Text,default="")
    level: Mapped[str]=mapped_column(String(20),default="INFO")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Setting(Base):
    __tablename__="settings"
    id: Mapped[int]=mapped_column(primary_key=True)
    key: Mapped[str]=mapped_column(String(100),unique=True)
    value: Mapped[str]=mapped_column(Text,default="")

class Permission(Base):
    __tablename__="permissions"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(100),unique=True)
    level: Mapped[int]=mapped_column(default=1)

class Automation(Base):
    __tablename__="automations"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(200))
    schedule: Mapped[str]=mapped_column(String(100))
    enabled: Mapped[bool]=mapped_column(Boolean,default=True)
