from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from backend.database.models import PatientCreate, RecordCreate
from backend.ai.assistant import analyze_note
from backend.database.sqlite_manager import SQLiteManager
from backend.utils.jwt_utils import decode_token
import os

router = APIRouter()
DB_PATH = os.getenv("DB_PATH", "./data/health.db")
db = SQLiteManager(DB_PATH)

def auth_dependency(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]

@router.post("/patients", tags=["patients"])
def create_patient(data: PatientCreate, user=Depends(auth_dependency)):
    pid = db.add_patient(data.model_dump())
    return {"id": pid}

@router.get("/patients", tags=["patients"])
def get_patients(user=Depends(auth_dependency)):
    return db.list_patients()

@router.get("/patients/{patient_id}", tags=["patients"])
def get_patient_by_id(patient_id: int, user=Depends(auth_dependency)):
    p = db.get_patient(patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Not found")
    return p

@router.post("/records", tags=["records"])
def add_record(data: RecordCreate, user=Depends(auth_dependency)):
    rid = db.add_record(data.model_dump())
    return {"id": rid}

@router.get("/records/{patient_id}", tags=["records"])
def list_records(patient_id: int, user=Depends(auth_dependency)):
    return db.get_records(patient_id)

@router.post("/ai/analyze", tags=["ai"])
def ai_analyze(note: str, user=Depends(auth_dependency)):
    return analyze_note(note)
