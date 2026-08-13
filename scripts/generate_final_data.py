import json
import random
import os
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_US')

NUM_RECORDS = 500

out_dir = r"c:\Users\504508\PythonProject\PythonChatBot\ai_petcare_Assistant\data"
os.makedirs(out_dir, exist_ok=True)

users = [{"id": f"USER-{1001+i}", "name": fake.name(), "email": fake.email()} for i in range(NUM_RECORDS)]

species_breeds = {
    "Dog": ["Golden Retriever", "Labrador", "Poodle", "Bulldog"],
    "Cat": ["Siamese", "Persian", "Maine Coon", "Bengal"],
    "Bird": ["Parrot", "Canary"], "Rabbit": ["Holland Lop", "Mini Rex"]
}

pets = []
for i in range(NUM_RECORDS):
    sp = random.choice(list(species_breeds.keys()))
    pets.append({
        "id": f"PET-{1001+i}",
        "user_id": random.choice(users)["id"],
        "name": fake.first_name(),
        "species": sp,
        "breed": random.choice(species_breeds[sp]),
        "age": random.randint(1, 15)
    })

common_names = ["Pet Health Center", "City Vet Clinic", "Animal Hospital", "Loving Care Vet", "Happy Paws Clinic"]
state_city_zip = {
    "CA": [("Los Angeles", "90015"), ("San Francisco", "94103")],
    "TX": [("Houston", "77002"), ("Austin", "78701")],
    "NY": [("New York", "10001"), ("Buffalo", "14202")],
    "FL": [("Miami", "33132"), ("Orlando", "32801")],
    "IL": [("Chicago", "60601"), ("Springfield", "62701")],
    "PA": [("Philadelphia", "19102"), ("Pittsburgh", "15222")],
    "WA": [("Seattle", "98104")], "OH": [("Columbus", "43215")],
    "GA": [("Atlanta", "30303")], "NC": [("Charlotte", "28202")]
}
states_pool = list(state_city_zip.keys()) + ["CA", "CA", "TX", "TX", "NY", "NY"]

clinics = []
for i in range(NUM_RECORDS):
    st = random.choice(states_pool)
    ct, zp = random.choice(state_city_zip[st])
    nm = random.choice(common_names) if random.random() < 0.3 else fake.company() + " Veterinary"
    addr = f"{fake.street_address()}, {ct}, {st} {zp}"
    clinics.append({
        "id": f"CLINIC-{1001+i}",
        "name": nm,
        "address": addr,
        "phone": fake.phone_number(),
        "is_open_now": random.choice([True, False]),
        "hours": {"Monday": "8am-6pm", "Tuesday": "8am-6pm", "Wednesday": "8am-6pm", "Thursday": "8am-6pm", "Friday": "8am-6pm", "Saturday": "9am-1pm", "Sunday": "Closed"},
        "services": random.sample(["General Checkup", "Vaccinations", "Dental", "Surgery", "Grooming"], k=random.randint(2, 5))
    })

doctors = []
for i in range(NUM_RECORDS):
    doctors.append({
        "id": f"DOC-{1001+i}",
        "clinic_id": random.choice(clinics)["id"],
        "name": f"Dr. {fake.last_name()}",
        "specialties": random.sample(["General Practice", "Surgery", "Dentistry", "Dermatology", "Oncology"], k=random.randint(1, 3))
    })

appointment_slots = []
for i in range(NUM_RECORDS):
    doc = random.choice(doctors)
    dt = fake.date_time_between(start_date="-1y", end_date="+1y")
    appointment_slots.append({
        "id": f"SLOT-{100+i}",
        "clinic_id": doc["clinic_id"],
        "doctor_id": doc["id"],
        "datetime": dt.isoformat(),
        "is_available": random.choice([True, False])
    })

visits = []
for i in range(NUM_RECORDS):
    doc = random.choice(doctors)
    dt = fake.date_time_between(start_date="-2y", end_date="now")
    visits.append({
        "id": f"VISIT-{1001+i}",
        "pet_id": random.choice(pets)["id"],
        "clinic_id": doc["clinic_id"],
        "doctor_id": doc["id"],
        "date": dt.isoformat(),
        "notes": fake.sentence(),
        "weight_lbs": round(random.uniform(5.0, 80.0), 1)
    })

prescriptions = []
for i in range(NUM_RECORDS):
    visit = random.choice(visits)
    prescriptions.append({
        "id": f"RX-{1001+i}",
        "pet_id": visit["pet_id"],
        "doctor_id": visit["doctor_id"],
        "medication": random.choice(["Amoxicillin", "Rimadyl", "Heartgard", "Frontline"]),
        "dosage": f"{random.randint(1, 3)} tablet(s) daily",
        "instructions": "Give with food",
        "refills_remaining": random.randint(0, 3),
        "issue_date": visit["date"]
    })

products = []
for i in range(NUM_RECORDS):
    products.append({
        "id": f"PROD-{1001+i}",
        "name": fake.word().capitalize() + " " + random.choice(["Chow", "Treats", "Vitamins"]),
        "category": random.choice(["supplements", "dental treats", "food", "toys"]),
        "price": round(random.uniform(10.0, 100.0), 2),
        "inventory_count": random.randint(0, 200),
        "description": fake.text(max_nb_chars=100)
    })

files_to_save = {
    "users.json": users, "pets.json": pets, "clinics.json": clinics,
    "doctors.json": doctors, "appointment_slots.json": appointment_slots,
    "visits.json": visits, "prescriptions.json": prescriptions, "products.json": products
}

for filename, data in files_to_save.items():
    with open(os.path.join(out_dir, filename), 'w') as f:
        json.dump(data, f, indent=4)
        
print("Data generated successfully!")