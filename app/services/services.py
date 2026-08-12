import json
import logging
from pathlib import Path
from typing import List, Optional, Dict
from app.config import settings

logger = logging.getLogger(__name__)

class JSONServiceBase:
    def __init__(self, filename: str):
        self.filepath = Path(settings.data_dir) / filename
        
    def _load_data(self) -> List[Dict]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {self.filepath}: {e}")
            return []

    def _save_data(self, data: List[Dict]):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving {self.filepath}: {e}")

class PetService(JSONServiceBase):
    def __init__(self):
        super().__init__("pets.json")

    def get_pet(self, pet_id: str) -> Optional[Dict]:
        pets = self._load_data()
        return next((p for p in pets if p['id'] == pet_id), None)
    
    def get_pets_by_user(self, user_id: str) -> List[Dict]:
        pets = self._load_data()
        return [p for p in pets if p['user_id'] == user_id]

class ClinicService(JSONServiceBase):
    def __init__(self):
        super().__init__("clinics.json")
        self.doctors_file = Path(settings.data_dir) / "doctors.json"

    def get_all_clinics(self) -> List[Dict]:
        return self._load_data()

    def find_nearby_clinics(self) -> List[Dict]:
        # For mock, just return all as "nearby"
        return self.get_all_clinics()

    def get_clinic(self, clinic_id: str) -> Optional[Dict]:
        clinics = self._load_data()
        return next((c for c in clinics if c['id'] == clinic_id), None)
        
    def get_clinic_doctors(self, clinic_id: str) -> List[Dict]:
        try:
             with open(self.doctors_file, 'r', encoding='utf-8') as f:
                doctors = json.load(f)
                return [d for d in doctors if d['clinic_id'] == clinic_id]
        except Exception as e:
            logger.error(f"Error loading doctors: {e}")
            return []

class AppointmentService(JSONServiceBase):
    def __init__(self):
        super().__init__("appointment_slots.json")
        self.appointments_file = Path(settings.data_dir) / "appointments.json"

    def get_available_slots(self, clinic_id: str = None) -> List[Dict]:
        slots = self._load_data()
        available = [s for s in slots if s['is_available']]
        if clinic_id:
            available = [s for s in available if s['clinic_id'] == clinic_id]
        return available
    
    def book_appointment(self, pet_id: str, clinic_id: str, doctor_id: str, slot_id: str) -> Dict:
        slots = self._load_data()
        slot = next((s for s in slots if s['id'] == slot_id and s['is_available']), None)
        
        if not slot:
            raise ValueError("Slot is not available or does not exist.")
            
        # Update slot availability
        for s in slots:
            if s['id'] == slot_id:
                s['is_available'] = False
        self._save_data(slots)
        
        # Create appointment record
        appointments = []
        if self.appointments_file.exists():
            with open(self.appointments_file, 'r') as f:
                appointments = json.load(f)
                
        new_appointment = {
            "id": f"APP-{len(appointments) + 1001}",
            "pet_id": pet_id,
            "clinic_id": clinic_id,
            "doctor_id": doctor_id,
            "datetime": slot['datetime'],
            "status": "SCHEDULED"
        }
        appointments.append(new_appointment)
        
        with open(self.appointments_file, 'w') as f:
            json.dump(appointments, f, indent=4)
            
        return new_appointment

class PrescriptionService(JSONServiceBase):
    def __init__(self):
        super().__init__("prescriptions.json")

    def get_pet_prescriptions(self, pet_id: str) -> List[Dict]:
        rx = self._load_data()
        return [r for r in rx if r['pet_id'] == pet_id]
        
    def check_refill_eligibility(self, prescription_id: str) -> Dict:
        rx = self._load_data()
        script = next((r for r in rx if r['id'] == prescription_id), None)
        if not script:
            return {"eligible": False, "reason": "Prescription not found"}
        if script['refills_remaining'] > 0:
            return {"eligible": True, "refills_remaining": script['refills_remaining']}
        return {"eligible": False, "reason": "No refills remaining"}

class ProductService(JSONServiceBase):
    def __init__(self):
        super().__init__("products.json")

    def search_products(self, query: str = None, category: str = None, max_price: float = None) -> List[Dict]:
        products = self._load_data()
        results = products
        
        if category:
            results = [p for p in results if p['category'].lower() == category.lower()]
        if max_price:
            results = [p for p in results if p['price'] <= max_price]
        if query:
            q = query.lower()
            results = [p for p in results if q in p['name'].lower() or q in p['description'].lower()]
            
        return results

class VisitService(JSONServiceBase):
    def __init__(self):
        super().__init__("visits.json")

    def get_pet_visits(self, pet_id: str) -> List[Dict]:
        visits = self._load_data()
        return [v for v in visits if v['pet_id'] == pet_id]
