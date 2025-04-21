from datetime import date, datetime, timedelta
from sqlite3 import ProgrammingError
from sqlalchemy import Inspector
from sqlalchemy.orm import Session
from models.availability import Availability
from models.appointment import Appointment  # Importa la clase Appointment
from models.veterinarian import Veterinarian
from models.veterinaryClinic import VeterinaryClinic
from schemas.availability import AvailabilitySchema
from config.db import get_db
from fastapi import Depends


class AvailabilityService:

    @staticmethod
    def check_and_reset_availabilities(db: Session):
        AvailabilityService.delete_weekly_availabilities(db)
        AvailabilityService.create_weekly_availabilities(db)
    
    @staticmethod
    def create_availability(availability: AvailabilitySchema, db: Session):
        availability_db = AvailabilitySchema.from_orm(availability)
        db.add(availability_db)
        db.commit()
        return availability_db
    
    @staticmethod
    def create_weekly_availabilities(db: Session):
        db.query(Availability).delete()  

        today = datetime.now().date()
        if today.weekday() == 6:  # Si hoy es domingo
            start_of_week = today + timedelta(days=1)  # Lunes de esta semana
        else:
            start_of_week = today

        # Obtener la resta de días hasta el sábado de la misma semana
        days_until_saturday = 5 - start_of_week.weekday()
        end_of_week = start_of_week + timedelta(days=days_until_saturday)  # Sábado de la misma semana

        veterinarians = db.query(Veterinarian).all()

        for vet in veterinarians:
            AvailabilityService.create_weekly_availabilities_for_veterinarian(vet, db, start_of_week, days_until_saturday)

        db.commit()

    @staticmethod
    def create_weekly_by_new_veterinarian(vet: Veterinarian, db: Session):
        today = datetime.now().date()
        if today.weekday() == 6:  # Si hoy es domingo
            start_of_week = today + timedelta(days=1)
        else:
            start_of_week = today
        
        days_until_saturday = 5 - start_of_week.weekday()
        
        AvailabilityService.create_weekly_availabilities_for_veterinarian(vet, db, start_of_week, days_until_saturday)

    @staticmethod
    def create_weekly_availabilities_for_veterinarian(vet: Veterinarian, db: Session, start_of_week: date, days_until_saturday: int):
        clinic: VeterinaryClinic = vet.clinic
        clinic_start_time = clinic.office_hours_start
        clinic_end_time = clinic.office_hours_end

        for i in range(days_until_saturday + 1):  # Horarios desde start_of_week hasta end_of_week
            date = start_of_week + timedelta(days=i)

            # Si es el día actual, redondea la hora de inicio a los próximos 30 minutos
            if date == datetime.now().date():
                now = datetime.now()
                minutes = (now.minute + 29) // 30 * 30  # Redondear a los próximos 30 minutos
                start_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=minutes)
                start_time = max(start_time.time(), clinic_start_time)  # Asegura que no inicie antes del horario de la clínica
            else:
                start_time = clinic_start_time

            # Verifica si ya existe una disponibilidad para esta fecha y hora
            existing_availability = db.query(Availability).filter_by(date=date, start_time=start_time, veterinarian_id=vet.id).first()
            
            if not existing_availability:  # Solo crea la disponibilidad si no existe
                availability = Availability(
                    date=date,
                    start_time=start_time,
                    end_time=clinic_end_time,
                    veterinarian_id=vet.id,
                    is_available=True
                )
                db.add(availability)

        db.commit()


    @staticmethod
    def delete_weekly_availabilities(db: Session):
        db.query(Availability).delete()  
        db.commit()