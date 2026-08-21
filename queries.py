from db import get_connection

def add_patient(name, age):
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age) VALUES (%s, %s) RETURNING id;",
        (name, age)
    )
    patient_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()
    return patient_id

def get_all_patients():
    conn = get_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients;")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return patients

def add_doctor(name, age, specialization, phone, experience_yrs):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO doctors (name, age, specialization, phone, experience_yrs) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
        (name, age, specialization, phone, experience_yrs)
    )
    doctor_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()
    return doctor_id

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


def add_symptom(patient_id, symptom):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO symptoms (patient_id, symptom) VALUES (%s, %s);",
        (patient_id, symptom)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True



def add_appointment(patient_id, doctor_id, time_slot, urgent, diagnosis, fee):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO appointments (patient_id, doctor_id, time_slot, urgent, diagnosis, fee) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
        (patient_id, doctor_id, time_slot, urgent, diagnosis, fee)
    )
    appointment_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return appointment_id


def get_all_appointments():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute(
        """SELECT p.name, d.name, a.diagnosis, a.urgent, a.time_slot, a.fee
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.time_slot  DESC;"""
        )
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return appointments