from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Chat Request / Response ---
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    intent: Optional[str] = None
    agents_used: List[str] = []
    requires_confirmation: bool = False
    pending_action: Optional[str] = None
    action_parameters: Optional[Dict[str, Any]] = None

# --- Pet Schemas ---
class PetBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None

class Pet(PetBase):
    id: str
    user_id: str

class PetContext(PetBase):
    id: str
    recent_visits: List[Dict] = []
    latest_prescription: Optional[Dict] = None
    preferences: List[str] = []

# --- Clinic / Doctor Schemas ---
class Clinic(BaseModel):
    id: str
    name: str
    address: str
    phone: str
    is_open_now: bool = True
    hours: Dict[str, str] = {}
    services: List[str] = []

class Doctor(BaseModel):
    id: str
    clinic_id: str
    name: str
    specialties: List[str] = []

# --- Appointment Schemas ---
class AppointmentSlot(BaseModel):
    id: str
    clinic_id: str
    doctor_id: str
    datetime: datetime
    is_available: bool

class Appointment(BaseModel):
    id: str
    pet_id: str
    clinic_id: str
    doctor_id: str
    datetime: datetime
    status: str # e.g., "SCHEDULED", "CANCELLED"

class BookAppointmentRequest(BaseModel):
    pet_id: str
    clinic_id: str
    doctor_id: str
    slot_id: str

# --- Prescription / Product Schemas ---
class Prescription(BaseModel):
    id: str
    pet_id: str
    doctor_id: str
    medication: str
    dosage: str
    instructions: str
    refills_remaining: int
    issue_date: datetime

class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    inventory_count: int
    description: str

class RefillRequest(BaseModel):
    prescription_id: str
    pet_id: str