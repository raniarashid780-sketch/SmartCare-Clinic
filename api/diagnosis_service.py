from smart_clinic import DiagnosisEngine, Billing

def compute_urgency_and_fee(patient) -> tuple[bool, str, float]:
    # Build a plain list of symptom text from patient.symptoms
    symptom_list = [s.symptom for s in patient.symptoms]

    # Create an instance of DiagnosisEngine
    diagnosis_engine = DiagnosisEngine()

    # Call engine.is_urgent(...) and engine.diagnose(...) on the plain string list
    urgent = diagnosis_engine.is_urgent(symptom_list)
    diagnosis = diagnosis_engine.diagnose(symptom_list)

    # Build a Billing object and get the total fee
    billing = Billing(patient=patient, service=diagnosis, urgent=urgent)
    fee = billing.get_total()

    return urgent, diagnosis, fee