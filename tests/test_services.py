import pytest
from app.services.services import PetService, ClinicService, AppointmentService, PrescriptionService, ProductService
from app.schemas.schemas import ChatRequest
from app.utils.state import ConversationState

def test_pet_service_loads_data():
    svc = PetService()
    pets = svc._load_data()
    assert len(pets) > 0
    assert pets[0]["id"] == "PET-1001"

def test_pet_service_get_pet():
    svc = PetService()
    pet = svc.get_pet("PET-1001")
    assert pet is not None
    assert pet["name"] == "PetName1"

def test_clinic_service_loads_data():
    svc = ClinicService()
    clinics = svc.get_all_clinics()
    assert len(clinics) > 0
    
def test_appointment_service_available_slots():
    svc = AppointmentService()
    slots = svc.get_available_slots("CLINIC-1001")
    assert len(slots) > 0
    assert slots[0]["clinic_id"] == "CLINIC-1001"

def test_prescription_service_refill():
    svc = PrescriptionService()
    status = svc.check_refill_eligibility("RX-1001")
    assert status["eligible"] == True

def test_product_service_search():
    svc = ProductService()
    products = svc.search_products(category="dental treats")
    assert len(products) > 0
    assert products[0]["id"] == "PROD-1002"

def test_conversation_state():
    state = ConversationState()
    # Force memory store for test
    state.use_redis = False
    
    session = "test_user_1"
    state.set_pending_action(session, "BOOK_APPOINTMENT", {"slot_id": "123"})
    
    current = state.get_state(session)
    assert current["requires_confirmation"] == True
    assert current["pending_action"] == "BOOK_APPOINTMENT"
    
    state.clear_pending_action(session)
    cleared = state.get_state(session)
    assert cleared["requires_confirmation"] == False
    assert "pending_action" not in cleared
