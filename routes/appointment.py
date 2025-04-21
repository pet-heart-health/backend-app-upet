from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.appointment import Appointment
from models.veterinarian import Veterinarian
from models.pet import Pet
from schemas.appointment import AppointmentSchemaGet, AppointmentSchemaCreate, AppointmentSchemaUpdate
from datetime import datetime

from services.appointment import AppointmentService

appointments = APIRouter()
tag = "Appointments"

endpoint = "/appointments"

@appointments.get(endpoint, response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_appointments(db: Session = Depends(get_db)):
    return AppointmentService.get_all_appointments(db)


@appointments.get(endpoint + "/owner/{owner_id}", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_appointments_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    return AppointmentService.get_appointments_by_owner_id(owner_id, db)

@appointments.get(endpoint + "/{appointment_id}", response_model=AppointmentSchemaGet, status_code=status.HTTP_200_OK, tags=[tag])
def get_appointment_by_id(appointment_id: int, db: Session = Depends(get_db)):
    return AppointmentService.get_appointment_by_id(appointment_id, db)

@appointments.get(endpoint + "/pet/{pet_id}", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_appointments_by_pet_id(pet_id: int, db: Session = Depends(get_db)):
    return AppointmentService.get_appointments_by_pet_id(pet_id, db)

@appointments.get(endpoint + "/veterinarian/{veterinarian_id}", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_appointments_by_veterinarian_id(veterinarian_id: int, db: Session = Depends(get_db)):
    return AppointmentService.get_appointments_by_veterinarian_id(veterinarian_id, db)

@appointments.post(endpoint, response_model=AppointmentSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_appointment(appointment: AppointmentSchemaCreate, db: Session = Depends(get_db)):
    return AppointmentService.create_appointment(appointment, db)

@appointments.get(endpoint + "/owner/{owner_id}/upcoming", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_upcoming_appointments_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    return AppointmentService.get_upcoming_appointments_by_owner_id(owner_id, db)

@appointments.get(endpoint + "/owner/{owner_id}/past", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_past_appointments_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    return AppointmentService.get_completed_appointments_by_owner_id(owner_id, db)

@appointments.get(endpoint + "/veterinarian/{veterinarian_id}/upcoming", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_upcoming_appointments_by_veterinarian_id(veterinarian_id: int, db: Session = Depends(get_db)):
    return AppointmentService.get_upcoming_appointments_by_veterinarian_id(veterinarian_id, db)

@appointments.get(endpoint + "/veterinarian/{veterinarian_id}/past", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_past_appointments_by_veterinarian_id(veterinarian_id: int, db: Session = Depends(get_db)):
    return AppointmentService.get_completed_appointments_by_veterinarian_id(veterinarian_id, db)

@appointments.put(endpoint + "/{appointment_id}", response_model=AppointmentSchemaGet, status_code=status.HTTP_200_OK, tags=[tag])
def update_appointment(appointment_id: int, appointment: AppointmentSchemaUpdate, db: Session = Depends(get_db)):
    return AppointmentService.post_appointment(appointment_id, appointment, db)

    
