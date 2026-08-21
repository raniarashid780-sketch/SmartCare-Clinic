"""
Smart Clinic Appointment and Diagnosis System
BS Artificial Intelligence – 2nd Semester Final Project

OOP Concepts Demonstrated:
1. Classes & Objects    : Every class is a blueprint; objects are created from them
2. Inheritance         : Patient/Doctor/Receptionist inherit from Person
                        Surgery/Medication/Therapy inherit from Treatment
3. Polymorphism        : introduce() and apply() behave differently per subclass
4. Encapsulation       : __symptoms and __rules are private; accessed via getters only
5. Abstraction (ABC)   : Person and Treatment are abstract; cannot be instantiated directly
6. Operator Overloading: __lt__, __gt__, __str__ on Appointment enable sorting and printing
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from colorama import init, Fore, Style
from db import get_connection
from queries import add_patient, add_symptom, add_appointment, get_all_doctors, get_all_patients, get_patient_symptoms, get_all_appointments, insert_default_doctors

# initialise colorama – makes colors work on Windows too
init(autoreset=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER – colored print shortcuts
# Plain functions, not classes. Just make terminal output readable.
# ─────────────────────────────────────────────────────────────────────────────


def print_header(text: str) -> None:
    border = "=" * 55
    print(f"\n{Fore.GREEN}{border}")
    print(f"  {text}")
    print(f"{border}{Style.RESET_ALL}")


def print_section(text: str) -> None:
    print(f"\n{Fore.CYAN}  -- {text} --{Style.RESET_ALL}")


def print_success(text: str) -> None:
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")


def print_urgent(text: str) -> None:
    print(f"{Fore.RED}{text}{Style.RESET_ALL}")


def print_info(text: str) -> None:
    print(f"  {text}")


# ─────────────────────────────────────────────────────────────────────────────
# 1. ABSTRACTION + CLASSES & OBJECTS
#    Person is abstract – you CANNOT do Person(1, "Ali", 25) directly.
#    It forces every subclass to implement introduce().
# ─────────────────────────────────────────────────────────────────────────────


class Person(ABC):
    def __init__(self, person_id: int, name: str, age: int) -> None:
        self.person_id = person_id
        self.name = name
        self.age = age

    @abstractmethod
    def introduce(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.person_id}, name={self.name}, age={self.age})"


# ─────────────────────────────────────────────────────────────────────────────
# 2. INHERITANCE + POLYMORPHISM
#    All three inherit from Person.
#    Each implements introduce() differently – same method name, different output.
# ─────────────────────────────────────────────────────────────────────────────


class Patient(Person):
    def __init__(
        self, person_id: int, name: str, age: int, symptoms: list[str]
    ) -> None:
        super().__init__(person_id, name, age)
        self.__symptoms = symptoms  # ENCAPSULATION: private attribute

    def introduce(self) -> str:
        return f"Hi, I am patient {self.name}. I am here for treatment."

    def get_symptoms(self) -> list[str]:  # getter – only way to read private symptoms
        return self.__symptoms.copy()

    def __str__(self) -> str:
        return f"Patient(id={self.person_id}, name={self.name}, age={self.age}, symptoms={self.get_symptoms()})"


class Doctor(Person):
    def __init__(self, person_id: int, name: str, age: int, specialty: str) -> None:
        super().__init__(person_id, name, age)
        self.specialty = specialty

    def introduce(self) -> str:
        return f"Hello, I am Dr. {self.name}, specialist in {self.specialty}."

    def __str__(self) -> str:
        return f"Doctor(id={self.person_id}, name={self.name}, age={self.age}, specialty={self.specialty})"


class Receptionist(Person):
    def __init__(self, person_id: int, name: str, age: int, shift: str) -> None:
        super().__init__(person_id, name, age)
        self.shift = shift

    def introduce(self) -> str:
        return f"Welcome! I am {self.name}, receptionist on the {self.shift} shift."

    def __str__(self) -> str:
        return f"Receptionist(id={self.person_id}, name={self.name}, age={self.age}, shift={self.shift})"


# ─────────────────────────────────────────────────────────────────────────────
# 3. ABSTRACTION + INHERITANCE + POLYMORPHISM
#    Treatment is abstract – apply() must be defined in every subclass.
#    Surgery, Medication, Therapy each apply() differently – polymorphism.
# ─────────────────────────────────────────────────────────────────────────────


class Treatment(ABC):
    def __init__(self, patient: Patient) -> None:
        self.patient = patient

    @abstractmethod
    def apply(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__} for {self.patient.name}"


class Surgery(Treatment):
    def apply(self) -> str:
        return (
            f"Scheduling surgery for {self.patient.name}. Pre-op checklist initiated."
        )


class Medication(Treatment):
    def apply(self) -> str:
        return f"Prescribing medication to {self.patient.name}. Dosage and timing explained."


class Therapy(Treatment):
    def apply(self) -> str:
        return f"Starting therapy sessions for {self.patient.name}. Weekly schedule assigned."


# ─────────────────────────────────────────────────────────────────────────────
# 4. OPERATOR OVERLOADING
#    __lt__ and __gt__ allow Python to sort Appointment objects automatically.
#    __str__ controls what prints when you do print(appointment).
#    Priority: urgent first, then earlier time slot.
# ─────────────────────────────────────────────────────────────────────────────


class Appointment:
    def __init__(
        self,
        doctor: Doctor,
        patient: Patient,
        time_slot: datetime,
        urgent: bool = False,
    ) -> None:
        self.doctor = doctor
        self.patient = patient
        self.time_slot = time_slot
        self.urgent = urgent

    def __gt__(self, other: Appointment) -> bool:
        # self is "greater" (higher priority) if self is urgent and other is not
        if self.urgent != other.urgent:
            return self.urgent  # True > False, so urgent wins
        # if same urgency, earlier time slot = higher priority
        return self.time_slot < other.time_slot

    def __lt__(self, other: Appointment) -> bool:
        # opposite of __gt__
        if self.urgent != other.urgent:
            return other.urgent  # self is less if OTHER is the urgent one
        return self.time_slot > other.time_slot

    def __str__(self) -> str:
        label = "URGENT" if self.urgent else "Regular"
        return (
            f"Appointment({label}) - Patient: {self.patient.name}, "
            f"Doctor: Dr. {self.doctor.name}, "
            f"Time: {self.time_slot.strftime('%Y-%m-%d %H:%M')}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 5. ENCAPSULATION
#    DiagnosisEngine hides __rules and __urgent_symptoms as private attributes.
#    Nobody outside can access or change the rules directly.
#    The system decides urgency – not the patient.
# ─────────────────────────────────────────────────────────────────────────────


class DiagnosisEngine:
    def __init__(self) -> None:
        # YOUR IDEA: treatment → list of symptoms (inverted structure)
        # cleaner, scalable, no repetition
        self.__rules = {
            "Surgery": ["fracture", "broken bone"],
            "Medication": ["fever", "cough", "infection", "chest pain", "heart pain"],
            "Therapy": ["stress", "anxiety", "insomnia"],
        }
        # system decides urgency based on these – patient does NOT choose
        self.__urgent_symptoms = {"chest pain", "heart pain", "fracture", "broken bone"}

    def diagnose(self, symptoms: list[str]) -> str:
        cleaned = [s.strip().lower() for s in symptoms]
        # priority order: Surgery > Medication > Therapy
        # checks ALL symptoms, not just the first one
        priority = ["Surgery", "Medication", "Therapy"]
        for treatment in priority:
            for symptom in cleaned:
                if symptom in self.__rules[treatment]:
                    return treatment  # returns highest priority match
        return "General Checkup"

    def is_urgent(self, symptoms: list[str]) -> bool:
        return any(s.strip().lower() in self.__urgent_symptoms for s in symptoms)


# ─────────────────────────────────────────────────────────────────────────────
# 6. CLASSES & OBJECTS + ENCAPSULATION
#    Billing holds all cost data and prints a clean receipt.
#    __FEES and __URGENT_SURCHARGE are private class-level constants.
#    base_fee, surcharge, total are private – only readable via getters.
# ─────────────────────────────────────────────────────────────────────────────


class Billing:
    __FEES = {
        "Surgery": 15000.0,
        "Medication": 2500.0,
        "Therapy": 4000.0,
        "General Checkup": 1500.0,
    }
    __URGENT_SURCHARGE = 500.0

    def __init__(self, patient: Patient, service: str, urgent: bool = False) -> None:
        self.patient = patient
        self.service = service
        self.__base_fee = self.__FEES.get(service, 1500.0)
        self.__surcharge = self.__URGENT_SURCHARGE if urgent else 0.0
        self.__total = self.__base_fee + self.__surcharge

    def get_base_fee(self) -> float:
        return self.__base_fee

    def get_surcharge(self) -> float:
        return self.__surcharge

    def get_total(self) -> float:
        return self.__total

    def __str__(self) -> str:
        lines = [
            f"  Bill for        : {self.patient.name} (ID {self.patient.person_id})",
            f"  Service         : {self.service}",
            f"  Base fee        : PKR {self.__base_fee:,.0f}",
        ]
        if self.__surcharge > 0:
            lines.append(f"  Urgent surcharge: PKR {self.__surcharge:,.0f}")
        lines.append(f"  Total due       : PKR {self.__total:,.0f}")
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# 7. COMPOSITION
#    Clinic owns DiagnosisEngine inside it – that is composition.
#    Clinic manages all people, appointments, and the full patient flow.
# ─────────────────────────────────────────────────────────────────────────────


class Clinic:
    __SPECIALTY_MAP = {
        "Surgery": "Orthopedics",
        "Medication": "Internal Medicine",
        "Therapy": "Psychology",
        "General Checkup": "Internal Medicine",
    }
    __CARDIAC_SYMPTOMS = {"chest pain", "heart pain"}

    def __init__(self, name: str) -> None:
        self.name = name
        self.people: list[Person] = []
        self.appointments: list[Appointment] = []
        self.engine = DiagnosisEngine()  # composition: Clinic owns DiagnosisEngine

    def add_person(self, person: Person) -> None:
        self.people.append(person)

    def get_patients(self) -> list[Patient]:
        return [p for p in self.people if isinstance(p, Patient)]

    def get_doctors(self) -> list[Doctor]:
        return [p for p in self.people if isinstance(p, Doctor)]

    def assign_doctor(self, service: str, symptoms: list[str]) -> Doctor | None:
        doctors = self.get_doctors()
        # cardiac symptoms always go to Cardiology
        if any(s.strip().lower() in self.__CARDIAC_SYMPTOMS for s in symptoms):
            for d in doctors:
                if d.specialty == "Cardiology":
                    return d
        # otherwise use specialty map
        target = self.__SPECIALTY_MAP.get(service, "Internal Medicine")
        for d in doctors:
            if d.specialty == target:
                return d
        return doctors[0] if doctors else None  # fallback

    def schedule_appointment(self, appt: Appointment) -> None:
        self.appointments.append(appt)
        self.appointments.sort(reverse=True)  # uses __gt__ / __lt__

    def suggest_treatment(self, patient: Patient) -> Treatment | None:
        result = self.engine.diagnose(patient.get_symptoms())
        if result == "Surgery":
            return Surgery(patient)
        if result == "Medication":
            return Medication(patient)
        if result == "Therapy":
            return Therapy(patient)
        return None

    def show_staff(self) -> None:
        print_section("Clinic Staff")
        for person in self.people:
            if not isinstance(person, Patient):
                print_info(
                    person.introduce()
                )  # POLYMORPHISM: same call, different output

    def show_appointments(self) -> None:
        print_section("Current Appointment Queue")
        if not self.appointments:
            print_info("No appointments yet.")
            return
        for i, appt in enumerate(self.appointments, 1):
            line = f"{i}. {appt}"  # OPERATOR OVERLOADING: __str__
            if appt.urgent:
                print_urgent(line)
            else:
                print_info(line)

    def register_new_patient(self) -> None:
        print_section("New Patient Registration")

        name = input(f"{Fore.CYAN}  Your name      : {Style.RESET_ALL}").strip()
        while not name:
            name = input(
                f"{Fore.CYAN}  Name cannot be empty: {Style.RESET_ALL}"
            ).strip()

        while True:
            try:
                age = int(
                    input(f"{Fore.CYAN}  Your age       : {Style.RESET_ALL}").strip()
                )
                break
            except ValueError:
                print_info("  Please enter a valid number for age.")

        raw = input(
            f"{Fore.CYAN}  Symptoms (comma separated): {Style.RESET_ALL}"
        ).strip()
        symptoms = [s.strip() for s in raw.split(",") if s.strip()]
        if not symptoms:
            symptoms = ["unspecified"]

        # Save patient to database and get the database-generated ID
        conn = get_connection()
        if not conn:
            print_urgent("  Database connection failed!")
            return

        try:
            with conn:
                with conn.cursor() as cur:
                    # Insert patient into database
                    pid = add_patient(cur, name, age)

                    # Insert each symptom into database
                    for s in symptoms:
                        add_symptom(cur, pid, s)

                    # Create patient object with database ID
                    patient = Patient(pid, name, age, symptoms)

                    # diagnosis engine decides service and urgency – NOT the patient
                    service = self.engine.diagnose(symptoms)
                    urgent = self.engine.is_urgent(
                        symptoms
                    )  # ENCAPSULATION: private rules used here

                    doctor = self.assign_doctor(service, symptoms)
                    if doctor is None:
                        raise ValueError("No doctor available right now.")

                    time_slot = datetime.now().replace(second=0, microsecond=0)

                    # Build billing BEFORE inserting appointment, so fee reaches the DB
                    bill = Billing(patient, service, urgent=urgent)
                    fee = bill.get_total()

                    # Add appointment to database with calculated fee
                    appt_id = add_appointment(cur, pid, doctor.person_id, time_slot, urgent, service, fee)
                    appt = Appointment(doctor, patient, time_slot, urgent)
                    self.schedule_appointment(appt)  # auto-sorted via __gt__ / __lt__

                    # Only add to in-memory after DB transaction succeeds
                    self.add_person(patient)

                    print_success(f"\n  Patient registered. Auto-assigned ID: {pid}")
                    print_info(patient.introduce())  # POLYMORPHISM

                    treatment = self.suggest_treatment(patient)
                    if treatment:
                        print_info(f"  Treatment Type  : {treatment.__class__.__name__}")
                        print_info(f"  Action          : {treatment.apply()}")  # POLYMORPHISM
                    else:
                        print_info("  Action          : General Checkup recommended.")

                    print_section("Bill")
                    if urgent:
                        print_urgent(str(bill))
                    else:
                        print_success(str(bill))
        except ValueError as e:
            print_urgent(f"  {e}")
            return
        finally:
            conn.close()




# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# Linear flow: boot → show staff → show queue
#              → register patients → exit
# ─────────────────────────────────────────────────────────────────────────────


def run() -> None:
    clinic = Clinic("SmartCare Clinic")

    # Load staff (doctors) from database
    db_doctors = get_all_doctors()
    for doc_id, name, age, specialty in db_doctors:
        clinic.add_person(Doctor(doc_id, name, age, specialty))

    # If no doctors in DB, insert defaults
    if not clinic.get_doctors():
        insert_default_doctors()
        db_doctors = get_all_doctors()  # Reload after insert
        for doc_id, name, age, specialty in db_doctors:
            clinic.add_person(Doctor(doc_id, name, age, specialty))

    # Add receptionists (always fixed for this session)
    clinic.add_person(Receptionist(301, "Mina Ali", 28, "Morning"))

    # Restore patient history from database
    db_patients = get_all_patients()
    for pid, name, age in db_patients:
        symptoms = get_patient_symptoms(pid)
        if not symptoms:
            symptoms = ["unspecified"]
        clinic.add_person(Patient(pid, name, age, symptoms))

    # Restore appointment history from database
    db_appointments = get_all_appointments()
    for appt_id, patient_id, doctor_id, time_slot, urgent, diagnosis, fee in db_appointments:
        patient = next((p for p in clinic.get_patients() if p.person_id == patient_id), None)
        doctor = next((d for d in clinic.get_doctors() if d.person_id == doctor_id), None)
        if patient and doctor:
            clinic.schedule_appointment(Appointment(doctor, patient, time_slot, urgent))

    print_header(f"Welcome to {clinic.name}")
    clinic.show_staff()  # POLYMORPHISM: each person introduces differently
    clinic.show_appointments()  # OPERATOR OVERLOADING: sorted by urgency

    while True:
        print()
        again = (
            input(f"{Fore.CYAN}  Register a new patient? (yes / no): {Style.RESET_ALL}")
            .strip()
            .lower()
        )
        if again != "yes":
            break
        clinic.register_new_patient()
        clinic.show_appointments()  # show updated queue after each registration
    print_header("Thank you for visiting SmartCare Clinic. Goodbye!")


if __name__ == "__main__":
    run()
