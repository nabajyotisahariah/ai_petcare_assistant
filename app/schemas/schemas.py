from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Chat Request / Response ---
class ChatRequest(BaseModel):
    user_id: str = Field(..., description="The unique identifier for the user.")
    message: str = Field(..., description="The message or query from the user.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "USER-1001",
                "message": "Find a vet near me for Max and what are the available slots?"
            }
        }
    )

class ChatResponse(BaseModel):
    conversation_id: str = Field(..., description="The ID of the current conversation/session.")
    message: str = Field(..., description="The response message from the AI assistant.")
    intent: Optional[str] = Field(None, description="The detected intent of the user's message.")
    agents_used: List[str] = Field([], description="A list of specialized AI agents utilized to fulfill the request.")
    requires_confirmation: bool = Field(False, description="Whether the system needs user confirmation to proceed with a pending action.")
    pending_action: Optional[str] = Field(None, description="The type of action waiting for confirmation (e.g., 'BOOK_APPOINTMENT').")
    action_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters related to the pending action.")
    data: Optional[Dict[str, Any]] = Field(None, description="Structured data returned by the agent.")
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