import json
import random
from faker import Faker

fake = Faker('en_US')

# Real cities and zips for specific states to make them "proper" and correlated correctly.
# By limiting the number of states to 10, we ensure that many of the 500 clinics 
# will share the same state, fulfilling the requirement.
state_city_zip = {
    "CA": [("Los Angeles", "90015"), ("San Francisco", "94103"), ("San Diego", "92101"), ("Sacramento", "95814"), ("Fresno", "93721")],
    "TX": [("Houston", "77002"), ("Austin", "78701"), ("Dallas", "75201"), ("San Antonio", "78205"), ("Fort Worth", "76102")],
    "NY": [("New York", "10001"), ("Buffalo", "14202"), ("Rochester", "14604"), ("Albany", "12207"), ("Syracuse", "13202")],
    "FL": [("Miami", "33132"), ("Orlando", "32801"), ("Tampa", "33602"), ("Jacksonville", "32202"), ("Tallahassee", "32301")],
    "IL": [("Chicago", "60601"), ("Springfield", "62701"), ("Peoria", "61602"), ("Naperville", "60540"), ("Rockford", "61101")],
    "PA": [("Philadelphia", "19102"), ("Pittsburgh", "15222"), ("Allentown", "18101"), ("Erie", "16501"), ("Reading", "19601")],
    "WA": [("Seattle", "98104"), ("Spokane", "99201"), ("Tacoma", "98402"), ("Vancouver", "98660"), ("Bellevue", "98004")],
    "OH": [("Columbus", "43215"), ("Cleveland", "44114"), ("Cincinnati", "45202"), ("Toledo", "43604"), ("Akron", "44308")],
    "GA": [("Atlanta", "30303"), ("Augusta", "30901"), ("Savannah", "31401"), ("Athens", "30601"), ("Macon", "31201")],
    "NC": [("Charlotte", "28202"), ("Raleigh", "27601"), ("Greensboro", "27401"), ("Durham", "27701"), ("Winston-Salem", "27101")]
}

states_pool = list(state_city_zip.keys())
# Let's make CA, TX, and NY even more common to ensure a large grouping in the same states.
states_pool.extend(["CA", "CA", "TX", "TX", "NY", "NY"])

with open('clinics.json', 'r') as f:
    clinics = json.load(f)

for clinic in clinics:
    state = random.choice(states_pool)
    city, zipcode = random.choice(state_city_zip[state])
    
    # Generate a realistic street address (sometimes with a suite number)
    street = fake.street_address()
    if random.random() < 0.4:
        street += f" Suite {random.randint(100, 999)}"
        
    clinic["state"] = state
    clinic["address"] = f"{street}, {city}, {state} {zipcode}"

with open('clinics.json', 'w') as f:
    json.dump(clinics, f, indent=4)

print(f"Updated {len(clinics)} clinics successfully!")
