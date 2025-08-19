import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.api.routes import router as api_router
from backend.api.auth import router as auth_router
from backend.database.sqlite_manager import SQLiteManager

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "./data/health.db")

app = FastAPI(title="ArogyaLite-UHR API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure DB exists on startup
sqlite_mgr = SQLiteManager(DB_PATH)
sqlite_mgr.init_db()

@app.get("/")
def root():
    return {"status": "ok", "service": "ArogyaLite-UHR"}

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
