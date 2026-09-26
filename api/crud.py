from sqlalchemy.orm import Session
from sqlalchemy import select
from api.diagnosis_service import compute_urgency_and_fee
from api.models import Appointment, Doctor, Patient, Symptom
from api.schemas import DoctorCreate, PatientCreate, AppointmentCreate

class DoubleBookingError(Exception):
    def __init__(self, doctor_id: int, time_slot):
        self.doctor_id = doctor_id
        self.time_slot = time_slot
        super().__init__(f"Doctor {doctor_id} already booked at {time_slot}")

def create_patient(db: Session, patient_in: PatientCreate) -> Patient:
    patient = Patient(name=patient_in.name, age=patient_in.age)
    patient_in_symptoms = [Symptom(symptom=symptom) for symptom in patient_in.symptoms]
    patient.symptoms.extend(patient_in_symptoms)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patient(db: Session, patient_id: int) -> Patient | None:
    return db.get(Patient, patient_id)

def list_patients(db: Session) -> list[Patient]:
    return db.execute(select(Patient)).scalars().all()

def create_appointment(db: Session, appointment_in: AppointmentCreate) -> Appointment:
    patient = db.get(Patient, appointment_in.patient_id)  
    doctor = db.get(Doctor, appointment_in.doctor_id)

    if patient is None or doctor is None:
        raise ValueError("patient or doctor does not exist")  

    existing_appointment = db.execute(
        select(Appointment).where(
            Appointment.doctor_id == appointment_in.doctor_id,
            Appointment.time_slot == appointment_in.time_slot,
        )
    ).scalar_one_or_none()

    if existing_appointment:
        raise DoubleBookingError(appointment_in.doctor_id, appointment_in.time_slot)

    urgent, diagnosis, fee = compute_urgency_and_fee(patient)

    appointment = Appointment(
        patient=patient,
        doctor=doctor,
        time_slot=appointment_in.time_slot,
        urgent=urgent,
        diagnosis=diagnosis,
        fee=fee,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def create_doctor(db: Session, doctor_in: DoctorCreate) -> Doctor:
    doctor = Doctor(
        name=doctor_in.name,
        age=doctor_in.age,
        specialization=doctor_in.specialization,
        experience_yrs=doctor_in.experience_yrs,
        phone=doctor_in.phone
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

def get_doctor(db: Session, doctor_id: int) -> Doctor | None:
    return db.get(Doctor, doctor_id)


def list_doctors(db: Session) -> list[Doctor]:
    return db.execute(select(Doctor)).scalars().all()