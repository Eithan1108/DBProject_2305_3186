import psycopg2
import random
from faker import Faker

fake = Faker()

categories = [
    "Imaging", "Monitoring", "Surgical", "Life Support", "Therapy", "Diagnostic", "Laboratory", "Sterilization"
]

device_names = [
    "MRI Scanner", "Ultrasound Machine", "ECG Monitor", "Ventilator", "Infusion Pump", "X-Ray Unit",
    "CT Scanner", "Defibrillator", "Sterilizer", "Blood Analyzer", "Surgical Light", "Patient Monitor",
    "Anesthesia Machine", "Oxygen Concentrator", "Dialysis Machine", "Surgical Table", "Infant Incubator",
    "Syringe Pump", "Cardiac Monitor", "Biopsy Device", "Nebulizer", "Glucose Meter", "Thermometer",
    "Stethoscope", "Laryngoscope", "Dermatoscope", "Pulse Oximeter", "Surgical Microscope", "EEG Machine",
    "EMG Device", "Endoscope", "Colposcope", "Autoclave", "Blood Pressure Monitor", "ECMO Machine",
    "Laser Therapy Unit", "Cryotherapy System", "Portable Suction Unit", "IV Stand", "Medical Refrigerator",
    "Pacemaker Tester", "Radiation Therapy Machine", "Dental Chair", "ENT Workstation", "CPAP Machine",
    "Eye Exam Chair", "Orthopedic Drill", "Bipap Ventilator", "Mobile C-Arm", "Bone Densitometer"
]


conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydatabase",
    user="eitan",
    password="ekfl2345"
)
cur = conn.cursor()

data = []
for i in range(1, 401):
    name = random.choice(device_names) + f" #{i}"
    emergency = random.choice([True, False])
    category = random.choice(categories)
    requires_building = name.startswith("MRI") or name.startswith("CT") or random.choice([False, False, True])
    volume = round(random.uniform(0.5, 50.0), 2)  # בין 0.5 ל־50 קוב
    data.append((i, name, emergency, category, requires_building, volume))

insert_query = """
INSERT INTO medical_equipment (medical_equipment_id, name, emergency_use, device_category, requires_building, volume)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cur.executemany(insert_query, data)

conn.commit()
cur.close()
conn.close()

print("✅ Inserted 400 medical equipment items successfully.")
