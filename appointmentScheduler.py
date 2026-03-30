from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, ParamSpecArgs
import uuid


@dataclass
class TimeSlot:
    start_time: datetime
    end_time: datetime


@dataclass
class Doctor:
    doctor_id: str
    name: str
    specialization: str
    availability: List[TimeSlot]


@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    medical_history: List[str]


@dataclass
class Appointment:
    appointment_id: str
    doctor_id: str
    patient_id: str
    date_time: datetime  # start time
    duration: int
    status: str


# Function to implement

def get_patient(patients, patient_id) -> Optional[Patient]:
    for patient in patients:
        if patient.patient_id == patient_id:
            return patient
    return None


def get_doctors_with_specialization(doctors, specialization) -> List[Doctor]:
    filtered_doctors: List[Doctor] = []
    for doctor in doctors:
        if doctor.specialization == specialization:
            filtered_doctors.append(doctor)
    return filtered_doctors


def get_appointments_for_doctor(doctor, existing_appointments) -> List[Appointment]:
    appointments: List[Appointment] = []
    for appointment in existing_appointments:
        if appointment.doctor_id == doctor.doctor_id:
            appointments.append(appointment)
    return appointments


def is_doctor_available(
        doctor: Doctor,
        existing_appointments: List[Appointment],
        preferred_date_time: datetime,
        duration: int
) -> bool:
    # part-1: preferred date SHOULD be in availability of doctor
    flag = False
    for timeslot in doctor.availability:
        if (preferred_date_time >= timeslot.start_time
                and preferred_date_time + timedelta(minutes=duration) <= timeslot.end_time
        ):
            flag = True
            break
    if not flag:
        return False
    # part-2: there SHOULD NOT be an appointment conflicting with given time
    appointments: List[Appointment] = get_appointments_for_doctor(doctor, existing_appointments)
    for appointment in appointments:
        st_time = appointment.date_time
        en_time = st_time + timedelta(minutes=appointment.duration)
        if ((
                st_time <= preferred_date_time < en_time
        ) or (
                st_time < preferred_date_time + timedelta(minutes=duration) <= en_time
        )):
            return False
    return True


def schedule_appointment(
        doctors: List[Doctor],
        patients: List[Patient],
        existing_appointments: List[Appointment],
        patient_id: str,
        specialization: str,
        preferred_date_time: datetime,
        duration: int
) -> tuple[Optional[Appointment], Optional[str]]:
    """
    Returns: (Appointment, None) on success or (None, error_message) on failure
    """
    patient: Optional[Patient] = get_patient(patients, patient_id)
    if patient is None:
        return None, "Patient does not exist!"
    filtered_doctors: List[Doctor] = get_doctors_with_specialization(doctors, specialization)
    if len(filtered_doctors) == 0:
        return None, "This specialization is not provided"
    for doctor in filtered_doctors:
        if is_doctor_available(doctor, existing_appointments, preferred_date_time, duration):
            return Appointment(
                appointment_id="123",
                doctor_id=doctor.doctor_id,
                patient_id=patient_id,
                date_time=preferred_date_time,
                duration=duration,
                status="BOOKED"
            ), None
    return None, "No doctors available for given timeslot"


# Helper function
def parse_time(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M")


# ===== SAMPLE TEST DATA =====
def get_sample_data():
    """Returns sample doctors, patients, and existing appointments for testing"""

    # Sample Doctors
    doctors = [
        Doctor(
            doctor_id="D001",
            name="Dr. Smith",
            specialization="Cardiology",
            availability=[
                TimeSlot(parse_time("2025-07-25 09:00"), parse_time("2025-07-25 12:00")),
                TimeSlot(parse_time("2025-07-25 14:00"), parse_time("2025-07-25 17:00")),
            ]
        ),
        Doctor(
            doctor_id="D002",
            name="Dr. Johnson",
            specialization="Cardiology",
            availability=[
                TimeSlot(parse_time("2025-07-25 10:00"), parse_time("2025-07-25 16:00")),
            ]
        ),
        Doctor(
            doctor_id="D003",
            name="Dr. Williams",
            specialization="Pediatrics",
            availability=[
                TimeSlot(parse_time("2025-07-25 08:00"), parse_time("2025-07-25 12:00")),
                TimeSlot(parse_time("2025-07-25 13:00"), parse_time("2025-07-25 18:00")),
            ]
        ),
        Doctor(
            doctor_id="D004",
            name="Dr. Brown",
            specialization="Orthopedics",
            availability=[
                TimeSlot(parse_time("2025-07-25 09:30"), parse_time("2025-07-25 15:30")),
            ]
        ),
    ]

    # Sample Patients
    patients = [
        Patient(
            patient_id="P001",
            name="Alice Johnson",
            age=35,
            medical_history=["Hypertension", "Diabetes"]
        ),
        Patient(
            patient_id="P002",
            name="Bob Smith",
            age=45,
            medical_history=["Heart Disease"]
        ),
        Patient(
            patient_id="P003",
            name="Carol Davis",
            age=8,
            medical_history=["Asthma"]
        ),
        Patient(
            patient_id="P004",
            name="David Wilson",
            age=28,
            medical_history=["Sports Injury"]
        ),
    ]

    # Existing Appointments (to test conflict detection)
    existing_appointments = [
        Appointment(
            appointment_id="A001",
            doctor_id="D001",
            patient_id="P002",
            date_time=parse_time("2025-07-25 10:00"),
            duration=30,
            status="Scheduled"
        ),
        Appointment(
            appointment_id="A002",
            doctor_id="D002",
            patient_id="P001",
            date_time=parse_time("2025-07-25 11:00"),
            duration=45,
            status="Scheduled"
        ),
        Appointment(
            appointment_id="A003",
            doctor_id="D003",
            patient_id="P003",
            date_time=parse_time("2025-07-25 09:00"),
            duration=30,
            status="Scheduled"
        ),
    ]

    return doctors, patients, existing_appointments


def main():
    """Test the function with sample data"""
    doctors, patients, existing_appointments = get_sample_data()

    print("=== Medical Appointment System Test ===\n")

    # Test Case 1: Successful booking
    print("Test 1: Book Cardiology appointment for Alice")
    appointment, error = schedule_appointment(
        doctors, patients, existing_appointments,
        "P001", "Cardiology", parse_time("2025-07-25 15:00"), 30
    )
    print(f"Result: {appointment}")
    print(f"Error: {error}\n")

    # Test Case 2: Successful booking
    print("Test 2: Successful booking")
    appointment, error = schedule_appointment(
        doctors, patients, existing_appointments,
        "P004", "Cardiology", parse_time("2025-07-25 10:15"), 30
    )
    print(f"Result: {appointment}")
    print(f"Error: {error}\n")

    # Test Case 3: Conflict case
    print("Test 3: Try to book conflicting time slot")
    appointment, error = schedule_appointment(
        doctors, patients, existing_appointments,
        "P003", "Pediatrics", parse_time("2025-07-25 09:15"), 30
    )
    print(f"Result: {appointment}")
    print(f"Error: {error}\n")

    # Test Case 4: Invalid specialization
    print("Test 4: Book appointment for unavailable specialization")
    appointment, error = schedule_appointment(
        doctors, patients, existing_appointments,
        "P001", "Neurology", parse_time("2025-07-25 14:00"), 30
    )
    print(f"Result: {appointment}")
    print(f"Error: {error}\n")

    # Test Case 5: Invalid patient
    print("Test 5: Book appointment for non-existent patient")
    appointment, error = schedule_appointment(
        doctors, patients, existing_appointments,
        "P999", "Cardiology", parse_time("2025-07-25 14:00"), 30
    )
    print(f"Result: {appointment}")
    print(f"Error: {error}\n")


if __name__ == "__main__":
    main()
