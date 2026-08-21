DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS symptoms;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;

CREATE TABLE doctors (
    id             SERIAL PRIMARY KEY,
    name           TEXT NOT NULL,
    age            INTEGER CHECK (age > 0 AND age < 120),
    specialization TEXT NOT NULL,
    phone          TEXT UNIQUE,
    experience_yrs INTEGER CHECK (experience_yrs >= 0)
);

CREATE TABLE patients (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age  INTEGER CHECK (age > 0 AND age < 150)
);

-- one row per symptom, real relational design instead of pipe-joined text
CREATE TABLE symptoms (
    id         SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    symptom    TEXT NOT NULL
);

CREATE TABLE appointments (
    id         SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id  INTEGER NOT NULL REFERENCES doctors(id),
    time_slot  TIMESTAMP NOT NULL,
    urgent     BOOLEAN NOT NULL DEFAULT FALSE,
    diagnosis  TEXT,
    fee        NUMERIC(10,2) CHECK (fee >= 0)
);