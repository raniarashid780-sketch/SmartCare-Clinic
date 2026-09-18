# 🏥 SmartCare Clinic

A clinic management system that started as a university OOP project and grew into a real, database-backed application — with both a terminal interface and a full REST API.

## The Problem

Small clinics often run on paper or spreadsheets — patient records get lost, doctors get double-booked, and there's no consistent way to flag urgent cases. SmartCare Clinic solves this with a structured, rule-based system: patients are logged with their symptoms, urgency is detected automatically, doctors are assigned by specialty, and bills are generated — all backed by a real PostgreSQL database that never loses data between sessions.

## Two Ways to Use It

| | |
|---|---|
| 🖥️ **Terminal App** | The original interactive CLI — register patients, book appointments, generate bills |
| 🌐 **REST API** | The same logic, exposed over HTTP with live interactive docs at `/docs` |

Both talk to the same database and share the same diagnosis/billing logic — nothing is duplicated between them.

## What It Actually Does

- 🩺 **Symptom-based diagnosis** — routes patients to Surgery, Medication, Therapy, or a General Checkup
- 🚨 **Automatic urgency detection** — chest pain, fractures, and similar symptoms get flagged and surcharged
- 👨‍⚕️ **Doctor assignment** by specialization
- 🚫 **No double-booking** — enforced at the database level, not just in code
- 💳 **Billing**, with urgent-case surcharges applied automatically
- 🗄️ **Real persistence** — PostgreSQL, with versioned schema migrations (Alembic), not drop-and-recreate

## Tech Stack

**Terminal app:** Python · PostgreSQL · psycopg2 · python-dotenv · colorama
**API:** FastAPI · SQLAlchemy 2.0 · Alembic · Pydantic · Uvicorn

## Database Schema
```
doctors → id, name, age, specialization, phone (unique), experience_yrs
patients → id, name, age
symptoms → id, patient_id → patients, symptom
appointments → id, patient_id, doctor_id, time_slot, urgent, diagnosis, fee
UNIQUE(doctor_id, time_slot) — no double-booking, ever
```

Foreign keys protect data integrity: a patient's appointment history can't be silently deleted, and a doctor can never be booked twice for the same slot — both guaranteed by the database itself.

## OOP Concepts Applied

Classes & objects · Inheritance · Polymorphism · Encapsulation · Abstraction · Operator overloading — see `smart_clinic.py` for the full implementation (`Patient`, `Doctor`, `Billing`, `Diagnosis`, and their relationships).

## Screenshot

![SmartCare-Clinic — showing a dry-run preview](assets/demo.png)

## Getting Started

```bash
git clone https://github.com/raniarashid780-sketch/SmartCare-Clinic.git
cd SmartCare-Clinic
pip install -r requirements.txt

# Set up the database
psql -U postgres -c "CREATE DATABASE smartcare;"
alembic upgrade head

# Configure credentials
cp .env.example .env
# edit .env with your DB_HOST / DB_PORT / DB_NAME / DB_USER / DB_PASSWORD
```

**Run the terminal app:**
```bash
python smart_clinic.py
```

**Run the API:**
```bash
python -m uvicorn api.main:app --reload
```
Then open `http://127.0.0.1:8000/docs`.

## Project Structure
```
SmartCare-Clinic/
├── smart_clinic.py # Terminal app
├── api/ # REST API (SQLAlchemy + FastAPI)
│ ├── models.py, schemas.py, crud.py
│ ├── diagnosis_service.py
│ └── main.py
├── alembic/ # Database migrations
└── schema.sql # Original schema (kept for history; Alembic is the source of truth now)
```
## About This Project

Built solo, in stages:

1. **The original OOP terminal app** — patients, doctors, diagnosis logic, billing — with CSV-based persistence.
2. **Migrated to PostgreSQL** — replaced CSV with a real relational database, schema designed by hand.
3. **Rebuilt the database layer with SQLAlchemy + Alembic** — real ORM models, versioned migrations instead of drop-and-recreate.
4. **Added a REST API with FastAPI** — the same diagnosis/billing logic, now exposed over HTTP with live interactive docs.

## License

See [LICENSE](LICENSE) for terms.

## Author

**Rania Rashid** — BS Artificial Intelligence, Ghazi University DG Khan
GitHub: [@raniarashid780-sketch](https://github.com/raniarashid780-sketch)