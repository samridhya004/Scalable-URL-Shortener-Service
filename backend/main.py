from backend.database.db import Base, engine
from backend.models import url
from fastapi import FastAPI
from backend.routes import url
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PromptCloud URL Shortener")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS
    allow_headers=["*"],
)

app.include_router(url.router)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is running"
    }

from backend.database.engine import engine
from backend.database.base import Base
from backend.models.url import URL

Base.metadata.create_all(bind=engine)
