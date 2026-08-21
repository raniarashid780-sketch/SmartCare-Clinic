from db import get_connection

def add_patient(cur, name, age):
    cur.execute(
        "INSERT INTO patients (name, age) VALUES (%s, %s) RETURNING id",
        (name, age)
    )
    return cur.fetchone()[0]

def add_symptom(cur, patient_id, symptom):
    cur.execute(
        "INSERT INTO symptoms (patient_id, symptom) VALUES (%s, %s)",
        (patient_id, symptom)
    )
    return True

def add_appointment(cur, patient_id, doctor_id, time_slot, urgent, diagnosis, fee):
    cur.execute(
        """INSERT INTO appointments (patient_id, doctor_id, time_slot, urgent, diagnosis, fee)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
        (patient_id, doctor_id, time_slot, urgent, diagnosis, fee)
    )
    return cur.fetchone()[0]



def get_all_patients():
    """Returns list of (id, name, age) tuples for all patients."""
    conn = get_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM patients;")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return patients


def get_patient_symptoms(patient_id):
    """Returns list of symptoms for a given patient."""
    conn = get_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT symptom FROM symptoms WHERE patient_id = %s;", (patient_id,))
    symptoms = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return symptoms


def get_all_doctors():
    conn = get_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, specialization FROM doctors;")
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return doctors


def insert_default_doctors():
    """Insert hardcoded default doctors into the database if none exist."""
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO doctors (id, name, age, specialization) VALUES (%s, %s, %s, %s)",
                           (201, "Ayesha Khan", 45, "Orthopedics"))
                cur.execute("INSERT INTO doctors (id, name, age, specialization) VALUES (%s, %s, %s, %s)",
                           (202, "Rohan Mehta", 39, "Internal Medicine"))
                cur.execute("INSERT INTO doctors (id, name, age, specialization) VALUES (%s, %s, %s, %s)",
                           (203, "Ali Khan", 50, "Cardiology"))
                cur.execute("INSERT INTO doctors (id, name, age, specialization) VALUES (%s, %s, %s, %s)",
                           (204, "Muhammad Hamza", 43, "Psychology"))
        return True
    except Exception as e:
        print(f"[DB WARNING] Could not insert default doctors: {e}")
        return False
    finally:
        conn.close()


def get_all_appointments():
    """Returns list of appointment records with all necessary IDs and data."""
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute(
        """SELECT a.id, a.patient_id, a.doctor_id, a.time_slot, a.urgent, a.diagnosis, a.fee
        FROM appointments a
        ORDER BY a.time_slot DESC;"""
    )
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return appointments