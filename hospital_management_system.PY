import re
from datetime import datetime

# Base Person class for common attributes
# Hospital Management System
# This program allows doctors to manage patient records, including adding, searching, and removing patients,
# as well as scheduling appointments and adding notes.
# Base Person class for common attributes

class Person:
    def __init__(self , user_id, name, age, gender, phone, email):
        self.user_id = user_id  # Make sure to store the id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.email = email

    def __str__(self):
        return (f"ID: {self.user_id}\n"
                f"Name: {self.name}\n"
                f"Age: {self.age}\n"
                f"Gender: {self.gender}\n"
                f"Phone: {self.phone}\n"
                f"Email: {self.email}")

    def display_details(self):
        return self.__str__()

# Doctor class inherits from Person to include specialty
class Doctor(Person):
    def __init__(self, doctor_id, name, specialty):
        super().__init__(doctor_id, name, None, None, None, None)
        self.specialty = specialty

    def __str__(self):
        return f"{super().__str__()}\nSpecialty: {self.specialty}"

    def display_details(self):
        return f"Doctor {self.name}, {self.specialty}:\n{super().__str__()}"

# Patient class inherits from Person and includes illness, notes, and appointment scheduling
class Patient(Person):
    def __init__(self, patient_id, name, age, gender, phone, email, illness, note=""):
        super().__init__(patient_id, name, age, gender, phone, email)
        self.illness = illness
        self.note = note
        self.next_appointments = []

    def add_note(self, note):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.note += f"\n[{timestamp}] {note}"

    def schedule_appointment(self, date):
        self.next_appointments.append(date)

    def __str__(self):
        appointments_str = "\n".join(self.next_appointments) if self.next_appointments else "None"
        return (f"{super().__str__()}\n"
                f"Illness: {self.illness}\n"
                f"Note: {self.note or 'None'}\n"
                f"Appointments: {appointments_str}")

    def display_details(self):
        return (f"Patient {self.name}\n"
                f" ({self.age} years old):\n"
                f"{super().__str__()}\n"
                f"Illness: {self.illness}")

# Decorator for input validation
def validate_input(pattern, message, input_func):
    while True:
        user_input = input_func()
        if re.match(pattern, user_input):
            return user_input
        else:
            print(message)


DEBUG_MODE = True  # Set False to disable logging

# Decorator for logging activity
def log_activity(func):
    def wrapper(*args, **kwargs):
        if DEBUG_MODE:
            print(f"LOG: Calling function {func.__name__}...")
        result = func(*args, **kwargs)
        if DEBUG_MODE:
            print(f"LOG: Function {func.__name__} executed successfully.")
        return result
    return wrapper


# HospitalManagementSystem class now includes advanced functionality
class HospitalManagementSystem:
    def __init__(self):
        self.patients = {}
        self.doctors_data = {
            "999": Doctor("999", "Saif", "Orthopedic"),
            "888": Doctor("888", "Ziad", "Dentistry"),
            "777": Doctor("777", "Nour", "Ophthalmology"),
            "666": Doctor("666", "Omar", "Surgeon"),
            "555": Doctor("555", "Rodi", "Internist"),
            "444": Doctor("444", "Marwan", "Psychiatrist"),
            "333": Doctor("333", "Farah", "Gynecologist"),
            "222": Doctor("222", "Omnia", "Emergency"),
            "111": Doctor("111", "Rafiq", "Emergency"),
            "000": Doctor("000", "Mazen", "Pediatrician"),
        }
        self.current_doctor = None

    @log_activity
    def menu(self):
        while True:
            print("\n1. Enter System\n2. Exit")
            choice = input("Choose an option: ")
            if choice == "1":
                self.enter_system()
            elif choice == "2":
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def enter_system(self):
        doctor_id = input("Enter your Doctor ID to access the system: ")
        if doctor_id in self.doctors_data:
            self.current_doctor = self.doctors_data[doctor_id]
            print(f"Welcome Dr. {self.current_doctor.name} - {self.current_doctor.specialty}")
            self.system_menu()
        else:
            print("Invalid Doctor ID. Access Denied.")

    def system_menu(self):
        while True:
            print("\n1. Add Patient\n2. Search Patient\n3. Remove Patient\n4. Logout")
            choice = input("Choose an option: ")
            if choice == "1":
                self.add_patient()
            elif choice == "2":
                self.search_patient()
            elif choice == "3":
                self.remove_patient()
            elif choice == "4":
                print(f"Logging out Dr. {self.current_doctor.name}.")
                self.current_doctor = None
                break
            else:
                print("Invalid choice. Please try again.")


    @log_activity
    def add_patient(self):
        patient_id = validate_input(r"^\d+$", "Invalid ID! Please enter numbers only.", lambda: input("Enter Patient ID: "))
        name = validate_input(r"^[A-Za-z]+$", "Invalid Name! Please enter letters only.", lambda: input("Enter Name: "))
        age = validate_input(r"^\d+$", "Invalid Age! Please enter a valid number.", lambda: input("Enter Age: "))
        gender = validate_input(r"^[MFmf]$", "Invalid Gender! Please enter M or F.", lambda: input("Enter Gender (M/F): "))
        email = validate_input(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "Invalid Email! Please enter a valid email address.", lambda: input("Enter Email: "))
        phone = validate_input(r"^\d{10}$", "Invalid Phone! Please enter a 10-digit number.", lambda: input("Enter Phone: "))

        illness = input("Enter Illness: ")
        note = input("Enter Note: ")

        next_appointment = input("Schedule Next Appointment? (Y/N): ").strip().lower()
        appointment_date = None
        if next_appointment == "y":
            appointment_date = input("Enter Appointment Date (YYYY-MM-DD): ")

        patient = Patient(patient_id, name, age, gender, phone, email, illness, note)
        if note:
            patient.add_note(note)

        if appointment_date:
            patient.schedule_appointment(appointment_date)

        self.patients[patient_id] = patient
        print(f"Patient {name} added successfully.")

    @log_activity
    def search_patient(self):
        patient_id = input("Enter Patient ID to Search: ")
        patient = self.patients.get(patient_id)
        if not patient:
            print("Patient not found.")
            return

        print("\nPatient Details:")
        print(patient)

        add_note = input("Add New Note? (Y/N): ").strip().lower()
        if add_note == "y":
            note = input("Enter Note: ")
            patient.add_note(note)

        add_appointment = input("Schedule Next Appointment? (Y/N): ").strip().lower()
        if add_appointment == "y":
            appointment_date = input("Enter Appointment Date (YYYY-MM-DD): ")
            patient.schedule_appointment(appointment_date)

    @log_activity
    def remove_patient(self):
        patient_id = input("Enter Patient ID to Remove: ")
        if patient_id in self.patients:
            del self.patients[patient_id]
            print(f"Patient with ID {patient_id} removed successfully.")
        else:
            print("Patient not found.")

# Run the system
hospital_system = HospitalManagementSystem()
hospital_system.menu()
