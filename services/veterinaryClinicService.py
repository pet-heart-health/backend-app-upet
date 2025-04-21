from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db

from models.veterinarian import Veterinarian
from schemas.veterinaryClinic import VeterinaryClinicSchemaGet, VeterinaryClinicSchemaPost
from models.veterinaryClinic import VeterinaryClinic
from models.availability import Availability
from services.otpService import OTPServices

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from datetime import date
from models.appointment import Appointment

class VeterinaryClinicService:

    @staticmethod
    def create_veterinary_clinic(clinic: VeterinaryClinicSchemaPost, db: Session):
        new_clinic = clinic.to_model() #transform the schema to a model
        start_time = new_clinic.office_hours_start
        end_time = new_clinic.office_hours_end
        
        if start_time < end_time:
            raise HTTPException(status_code=400, detail="La hora de inicio no puede ser mayor a la hora de fin")
        
        if start_time == end_time:
            raise HTTPException(status_code=400, detail="La hora de inicio no puede ser igual a la hora de fin")
            

        db.add(new_clinic)
        db.commit()
        return new_clinic

    @staticmethod
    def get_veterinary_clinics(db: Session) -> list[VeterinaryClinicSchemaGet]:
        return db.query(VeterinaryClinic).all()
    
    @staticmethod
    def generate_unique_password( clinic_id: int, db: Session):
        return OTPServices.generate_otp(db =db, clinic_id=clinic_id)
    
    @staticmethod
    def verify_veterinarian_register(clinic_name: str, otp_password: str, db: Session):
        # Verificar que el OTP sea válido y obtener el registro de OTP
        otp_record = OTPServices.verify_otp(otp_password, db)
        if not otp_record:
            raise HTTPException(status_code=400, detail="OTP no válido")
        
        # Obtener el clinicId del registro de OTP
        clinic_id = otp_record.clinicId
        OTPServices.delete_otp_record(otp_record, db)

        # Encontrar la clínica veterinaria por ID
        clinic = VeterinaryClinicService.get_veterinary_clinic_by_id(clinic_id, db=db)
        if not clinic:
            raise HTTPException(status_code=404, detail="Clínica veterinaria no encontrada")

        # Comparar el nombre de la clínica con el parámetro
        if clinic.name != clinic_name:
            raise HTTPException(status_code=400, detail="El nombre de la clínica no coincide")

        return clinic.id

    @staticmethod
    def get_veterinary_clinic_by_id(clinic_id: int, db: Session):
        clinic = db.query(VeterinaryClinic).filter(VeterinaryClinic.id == clinic_id).first()
        return clinic

