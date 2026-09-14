from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Patient name should be between 2 and 50 characters", json_schema_extra={"example": "John Doe"})
    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("name cannot be blank or whitespace-only")
        return v
    age: int = Field(..., gt=0, lt=120, description="Age should be between 1 and 120", json_schema_extra={"example": 30})
    symptoms: list[str] = Field(..., description="List of symptoms", json_schema_extra={"example": "Fever, Cough"})

class PatientOut(BaseModel):
    id: int
    name: str
    age: int
    symptoms: list[str]
    model_config = {
        "from_attributes": True
    }

class DoctorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Doctor's name should be between 2 and 50 characters", json_schema_extra={"example": "Dr. Smith"})
    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("name cannot be blank or whitespace-only")
        return v
    age: int = Field(..., gt=0, lt=120, description="Age should be between 1 and 120", json_schema_extra={"example": 45})
    specialization: str = Field(..., min_length=2, max_length=50, description="Doctor's specialization should be between 2 and 50 characters", json_schema_extra={"example": "Cardiology"})
    experience_years: int = Field(..., gt=0, description="Years of experience should be a positive integer", json_schema_extra={"example": 10})

class DoctorOut(BaseModel):
    id: int
    name: str
    age: int
    specialization: str
    experience_years: int
    model_config = {
        "from_attributes": True
    }

class AppointmentCreate(BaseModel):
    patient_id: int = Field(..., description="ID of the patient", json_schema_extra={"example": 1})
    doctor_id: int = Field(..., description="ID of the doctor", json_schema_extra={"example": 1})
    time_slot: datetime = Field(..., description="Appointment time slot", json_schema_extra={"example": "2023-09-15T10:00:00"})

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    time_slot: datetime
    urgent: bool
    diagnosis: str | None
    fee: float | None
    model_config = {"from_attributes": True}