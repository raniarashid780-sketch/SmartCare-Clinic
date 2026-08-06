# SmartCare Clinic — Appointment & Diagnosis System

A terminal-based clinic management system built in Python as a 2nd semester final project for BS Artificial Intelligence at Ghazi University.

## Screenshot

![SmartCare-Clinic — showing a dry-run preview](assets/demo.png)

## Project Overview
This project simulates a simple clinic workflow where users can:
- register patients
- manage appointments
- view available doctors and staff
- perform basic diagnosis based on symptoms
- generate billing information

## Object-Oriented Concepts Covered
- **Classes & Objects** — entities such as Patient, Doctor, Receptionist, and Appointment are modeled as classes
- **Inheritance** — Patient, Doctor, and Receptionist inherit from Person
- **Polymorphism** — each subclass implements its own behavior for shared methods
- **Encapsulation** — private attributes are accessed through methods
- **Abstraction** — abstract base classes are used for core entities
- **Operator Overloading** — appointment objects support comparison and readable string output

## Features
- automatic patient ID generation
- symptom-based diagnosis suggestions
- urgent case detection
- doctor assignment by specialty
- billing and surcharge handling
- colored terminal output for better readability
- Data persistence with CSV file storage

## Requirements
Install the required dependency:

```bash
pip install -r requirements.txt
```

## How to Run
From the project folder, run:

```bash
python "smart_clinic.py"
```

## Files
- Smart_Clinic_Appointment_&_Diagnosis_System_01.py — main application
- patients.csv — stored patient records
- appointments.csv — stored appointment records
- requirements.txt — Python dependencies

## Built By
Rania Rashid, Dua Batool, and Raima Enayat

## Note
This project is designed for educational purposes and demonstrates core OOP concepts in a simple CLI application.
