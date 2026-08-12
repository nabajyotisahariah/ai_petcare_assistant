import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# Fix seed for reproducibility
random.seed(42)

def generate_mock_data():
    base_dir = Path(__file__).resolve().parent.parent / "data"
    
    # --- Users (10) ---
    users = []
    for i in range(1, 11):
        users.append({
            "id": f"USER-{1000 + i}",
            "name": f"User {i}",
            "email": f"user{i}@example.com"
        })
        
    # --- Pets (20) ---
    species_breeds = {
        "Dog": ["Labrador", "Golden Retriever", "Bulldog", "Poodle", "Beagle", "German Shepherd"],
        "Cat": ["Siamese", "Persian", "Maine Coon", "Bengal", "Sphynx", "Ragdoll"]
    }
    pets = []
    for i in range(1, 21):
        species = random.choice(["Dog", "Cat"])
        breed = random.choice(species_breeds[species])
        user_id = random.choice(users)["id"]
        pets.append({
            "id": f"PET-{1000 + i}",
            "user_id": user_id,
            "name": f"PetName{i}",
            "species": species,
            "breed": breed,
            "age": random.randint(1, 15)
        })

    # --- Clinics (10) ---
    clinics = []
    for i in range(1, 11):
        clinics.append({
            "id": f"CLINIC-{1000 + i}",
            "name": f"PetCare Clinic {i}",
            "address": f"{random.randint(100, 999)} Main St, Cityville",
            "phone": f"555-01{i:02d}",
            "is_open_now": True,
            "hours": {
                "Monday": "8am - 6pm",
                "Tuesday": "8am - 6pm",
                "Wednesday": "8am - 6pm",
                "Thursday": "8am - 6pm",
                "Friday": "8am - 6pm",
                "Saturday": "9am - 1pm",
                "Sunday": "Closed"
            },
            "services": ["General Checkup", "Vaccinations", "Dental", "Surgery"]
        })

    # --- Doctors (20) ---
    doctors = []
    specialties_list = ["General Practice", "Surgery", "Dental", "Dermatology", "Cardiology"]
    for i in range(1, 21):
        clinic_id = clinics[(i - 1) % 10]["id"]
        doctors.append({
            "id": f"DOC-{1000 + i}",
            "clinic_id": clinic_id,
            "name": f"Dr. Vet {i}",
            "specialties": random.sample(specialties_list, k=random.randint(1, 2))
        })

    # --- Appointment Slots (100) ---
    slots = []
    now = datetime.now()
    slot_id_counter = 100
    for doc in doctors:
        # Generate 5 slots per doctor
        for d_offset in range(1, 6):
            slot_time = now + timedelta(days=d_offset, hours=random.randint(9, 16))
            # snap to hour
            slot_time = slot_time.replace(minute=0, second=0, microsecond=0)
            slots.append({
                "id": f"SLOT-{slot_id_counter}",
                "clinic_id": doc["clinic_id"],
                "doctor_id": doc["id"],
                "datetime": slot_time.isoformat(),
                "is_available": random.choice([True, True, False]) # Mostly available
            })
            slot_id_counter += 1

    # --- Prescriptions (30) ---
    medications = ["Apoquel 16mg", "Bravecto 16mg", "Heartgard Plus", "NexGard", "Carprofen", "Amoxicillin", "Metacam"]
    prescriptions = []
    for i in range(1, 31):
        pet = random.choice(pets)
        doc = random.choice(doctors)
        issue_date = now - timedelta(days=random.randint(10, 100))
        prescriptions.append({
            "id": f"RX-{1000 + i}",
            "pet_id": pet["id"],
            "doctor_id": doc["id"],
            "medication": random.choice(medications),
            "dosage": f"{random.randint(1, 2)} tablet(s) daily",
            "instructions": "Give with food",
            "refills_remaining": random.randint(0, 3),
            "issue_date": issue_date.isoformat()
        })

    # --- Products (100) ---
    categories = ["dental treats", "food", "toys", "supplements", "grooming"]
    products = []
    for i in range(1, 101):
        category = random.choice(categories)
        products.append({
            "id": f"PROD-{1000 + i}",
            "name": f"Premium Pet {category.title()} {i}",
            "category": category,
            "price": round(random.uniform(5.0, 80.0), 2),
            "inventory_count": random.randint(0, 100),
            "description": f"High quality {category} for your pet."
        })

    # --- Visits (50) ---
    visits = []
    for i in range(1, 51):
        pet = random.choice(pets)
        doc = random.choice(doctors)
        visit_date = now - timedelta(days=random.randint(1, 200))
        visits.append({
            "id": f"VISIT-{1000 + i}",
            "pet_id": pet["id"],
            "clinic_id": doc["clinic_id"],
            "doctor_id": doc["id"],
            "date": visit_date.isoformat(),
            "notes": "Routine checkup, everything looks good.",
            "weight_lbs": round(random.uniform(10, 80), 1)
        })

    # Write to files
    def write_json(filename, data):
        path = base_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    write_json("users.json", users)
    write_json("pets.json", pets)
    write_json("clinics.json", clinics)
    write_json("doctors.json", doctors)
    write_json("appointment_slots.json", slots)
    write_json("prescriptions.json", prescriptions)
    write_json("products.json", products)
    write_json("visits.json", visits)
    
    print(f"Successfully generated mock data in {base_dir}")
    print(f"- Users: {len(users)}")
    print(f"- Pets: {len(pets)}")
    print(f"- Clinics: {len(clinics)}")
    print(f"- Doctors: {len(doctors)}")
    print(f"- Appointment Slots: {len(slots)}")
    print(f"- Prescriptions: {len(prescriptions)}")
    print(f"- Products: {len(products)}")
    print(f"- Visits: {len(visits)}")

if __name__ == "__main__":
    generate_mock_data()
