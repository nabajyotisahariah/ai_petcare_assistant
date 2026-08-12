from crewai.tools import tool
from typing import List, Dict, Any
from app.services.services import ClinicService, AppointmentService, PetService, PrescriptionService, ProductService

clinic_svc = ClinicService()
appointment_svc = AppointmentService()
pet_svc = PetService()
prescription_svc = PrescriptionService()
product_svc = ProductService()

# --- Clinic Tools ---
@tool("find_nearby_clinics")
def find_nearby_clinics() -> str:
    """Finds and returns a list of nearby clinics."""
    clinics = clinic_svc.find_nearby_clinics()
    if not clinics:
        return "No nearby clinics found."
    return str([{"id": c["id"], "name": c["name"], "address": c["address"], "phone": c["phone"], "is_open_now": c["is_open_now"]} for c in clinics])

@tool("is_clinic_open")
def is_clinic_open(clinic_id: str) -> str:
    """Checks if a specific clinic is open right now."""
    clinic = clinic_svc.get_clinic(clinic_id)
    if not clinic:
        return f"Clinic {clinic_id} not found."
    return f"Clinic {clinic['name']} is {'open' if clinic['is_open_now'] else 'closed'} right now."

@tool("get_clinic_doctors")
def get_clinic_doctors(clinic_id: str) -> str:
    """Gets a list of doctors for a specific clinic."""
    doctors = clinic_svc.get_clinic_doctors(clinic_id)
    if not doctors:
        return f"No doctors found for clinic {clinic_id}."
    return str([{"id": d["id"], "name": d["name"], "specialties": d["specialties"]} for d in doctors])

# --- Appointment Tools ---
@tool("get_available_slots")
def get_available_slots(clinic_id: str = None) -> str:
    """Gets available appointment slots. Can be filtered by clinic_id."""
    slots = appointment_svc.get_available_slots(clinic_id)
    if not slots:
        return "No available slots found."
    return str(slots)

# --- Pet Tools ---
@tool("get_pet_profile")
def get_pet_profile(pet_id: str) -> str:
    """Retrieves the profile information for a pet."""
    if isinstance(pet_id, dict) and 'pet_id' in pet_id:
        pet_id = pet_id['pet_id']
    pet = pet_svc.get_pet(pet_id)
    if not pet:
        return f"Pet {pet_id} not found."
    return str(pet)

# --- Prescription Tools ---
@tool("get_latest_prescription")
def get_latest_prescription(pet_id: str) -> str:
    """Retrieves the latest prescription for a pet."""
    rx_list = prescription_svc.get_pet_prescriptions(pet_id)
    if not rx_list:
        return "No prescriptions found for this pet."
    return str(rx_list)

@tool("check_refill_eligibility")
def check_refill_eligibility(prescription_id: str) -> str:
    """Checks if a specific prescription is eligible for a refill."""
    status = prescription_svc.check_refill_eligibility(prescription_id)
    return str(status)

# --- Commerce Tools ---
@tool("search_products")
def search_products(query: str = None, category: str = None, max_price: float = None) -> str:
    """Searches for pet products based on query, category, and max price."""
    results = product_svc.search_products(query=query, category=category, max_price=max_price)
    if not results:
        return "No products found matching criteria."
    return str(results)
