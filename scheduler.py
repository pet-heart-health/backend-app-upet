from datetime import datetime, timedelta
from django.template import engines
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session
import uvicorn
from config.db import get_db
from models.availability import Availability
from models.notification import Notification
from models.petOwner import PetOwner
from schedulare.appointment_schedulare import AppointmentScheduler
from services.availability import AvailabilityService
from config.db import SessionLocal
from services.availability import AvailabilityService


def check_and_reset_availabilities(db: Session):
    AvailabilityService.check_and_reset_availabilities(db)
    db.close()

def sending_notifys (db: Session):
    appointment_schedulare = AppointmentScheduler(db)
    appointment_schedulare.check_appointments_and_notify(db)
    db.close()


db = next(get_db())  # Obtener una sesión de base de datos
check_and_reset_availabilities(db)