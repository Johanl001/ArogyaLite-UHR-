from fastapi import APIRouter, HTTPException
from backend.database.sqlite_manager import SQLiteManager
from backend.utils.security import hash_password, verify_password
from backend.utils.jwt_utils import create_access_token
from backend.database.models import UserCreate, UserLogin
import os

router = APIRouter(prefix="/auth", tags=["auth"])
DB_PATH = os.getenv("DB_PATH", "./data/health.db")
db = SQLiteManager(DB_PATH)

@router.post("/register")
def register(user: UserCreate):
    if db.get_user(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    uid = db.add_user(user.email, hash_password(user.password))
    return {"id": uid, "email": user.email}

@router.post("/login")
def login(user: UserLogin):
    u = db.get_user(user.email)
    if not u or not verify_password(user.password, u["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
