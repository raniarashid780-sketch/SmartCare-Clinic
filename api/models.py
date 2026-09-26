from datetime import datetime
from sqlalchemy import text, Text
from sqlalchemy import (
    Integer, String, ForeignKey, CheckConstraint, UniqueConstraint,
    Numeric, Boolean, DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Doctor(Base):
    __tablename__ = "doctors"
    __table_args__ = (
        CheckConstraint("age > 0 AND age < 120", name="doctors_age_check"),
        CheckConstraint("experience_yrs >= 0", name="doctors_experience_check")
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer)
    specialization: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str | None] = mapped_column(Text, unique=True)
    experience_yrs: Mapped[int | None] = mapped_column(Integer)

    appointments: Mapped[list["Appointment"]] = relationship(back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"
    __table_args__ = (
        CheckConstraint("age > 0 AND age < 150", name="patients_age_check"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer)

    symptoms: Mapped[list["Symptom"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="patient")


class Symptom(Base):
    __tablename__ = "symptoms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"), nullable=False
    )
    symptom: Mapped[str] = mapped_column(Text, nullable=False)

    patient: Mapped["Patient"] = relationship(back_populates="symptoms")


class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (
        CheckConstraint("fee >= 0", name="appointments_fee_check"),
        UniqueConstraint("doctor_id", "time_slot", name="uq_doctor_time_slot"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"), nullable=False
    )
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)
    time_slot: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    urgent: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    diagnosis: Mapped[str | None] = mapped_column(Text)
    fee: Mapped[float | None] = mapped_column(Numeric(10, 2))

    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")