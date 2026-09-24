from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.models import Appointment, Base, Doctor, Patient


def test_doctor_cannot_be_double_booked():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        doctor = Doctor(name="Dr. Test", specialization="General")
        patient = Patient(name="Test Patient")
        session.add_all([doctor, patient])
        session.commit()

        slot = datetime(2026, 10, 1, 10, 0)
        session.add(Appointment(patient_id=patient.id, doctor_id=doctor.id, time_slot=slot))
        session.commit()

        # Same doctor, same time: must be rejected
        session.add(Appointment(patient_id=patient.id, doctor_id=doctor.id, time_slot=slot))
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

        # Same doctor, different time: must work
        other_slot = datetime(2026, 10, 1, 11, 0)
        session.add(Appointment(patient_id=patient.id, doctor_id=doctor.id, time_slot=other_slot))
        session.commit()