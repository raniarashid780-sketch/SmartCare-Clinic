# SmartCare Clinic — Appointment & Diagnosis System

A terminal-based clinic management system built in Python as a 2nd semester final project for BS Artificial Intelligence at Ghazi University.

## OOP Concepts Covered
- **Classes & Objects** — Every entity (Patient, Doctor, Billing) is a class
- **Inheritance** — Patient, Doctor, Receptionist all inherit from Person
- **Polymorphism** — introduce() and apply() behave differently per subclass
- **Encapsulation** — Private attributes __symptoms and __rules accessed via getters only
- **Abstraction** — Person and Treatment are abstract classes using ABC
- **Operator Overloading** — __lt__, __gt__, __str__ on Appointment for sorting and printing

## How to Run
1. Install dependencies:
   ```
   pip install colorama
   ```
2. Run the program:
   ```
   python Smart_Clinic_Appointment_&_Diagnosis_System_01.py
   ```

## Features
- Auto patient ID generation
- Symptom-based diagnosis engine
- Urgency detection (chest pain, fracture etc.)
- Doctor assignment by specialty
- Billing with urgent surcharge
- Colored terminal output

## Built By
Rania Rashid (GitHub: raniarashid780-sketch), Dua Batool, Raima Enayat — BS AI 2nd Semester, Ghazi University
