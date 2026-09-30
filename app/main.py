from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.logger import configure_logging
from app.database.database import init_db
from app.api.chat import router as chat_router
from app.api.memory import router as memory_router
from app.api.skills import router as skills_router
from app.api.system import router as system_router
from app.api.voice import router as voice_router
from app.api.research import router as research_router
from app.api.vision import router as vision_router
from app.api.files import router as files_router
from app.api.automations import router as automations_router

configure_logging()

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app=FastAPI(title="ULTRON",version="3.0.0",lifespan=lifespan)
origins=["*"] if settings.cors_origins=="*" else [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
for router in (system_router,chat_router,memory_router,skills_router,voice_router,research_router,vision_router,files_router,automations_router):
    app.include_router(router)
app.mount("/",StaticFiles(directory="frontend",html=True),name="frontend")
