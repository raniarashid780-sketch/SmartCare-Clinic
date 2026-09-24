from fastapi import FastAPI, Depends, HTTPException
from api import crud
from api.models import Patient, Doctor
from sqlalchemy.orm import Session
from api.database import get_db
from api.crud import DoubleBookingError
from api.schemas import PatientCreate, DoctorCreate, DoctorOut, AppointmentCreate, PatientOut, AppointmentOut

app = FastAPI(title="SmartCare Clinic API")

@app.post("/patients/", response_model=PatientOut, status_code=201)
def create_patient(patient_in: PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient_in)

@app.get("/patients/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/patients/", response_model=list[PatientOut])
def list_patients(db: Session = Depends(get_db)):
    return crud.list_patients(db)


@app.post("/doctors/", response_model=DoctorOut, status_code=201)
def create_doctor(doctor_in: DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, doctor_in)

@app.get("/doctors/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.get("/doctors/", response_model=list[DoctorOut])
def list_doctors(db: Session = Depends(get_db)):
    return crud.list_doctors(db)


@app.post("/appointments/", response_model=AppointmentOut, status_code=201)
def create_appointment(appointment_in: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_appointment(db, appointment_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DoubleBookingError as e:
        raise HTTPException(status_code=409, detail=str(e))