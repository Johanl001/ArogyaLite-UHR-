from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PatientCreate(BaseModel):
    name: str
    age: int = Field(ge=0, le=120)
    gender: str
    contact: str

class Patient(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    contact: str

class RecordCreate(BaseModel):
    patient_id: int
    note: str

class Record(BaseModel):
    id: int
    patient_id: int
    note: str
    created_at: Optional[str] = None
