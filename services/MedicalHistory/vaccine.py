from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.MedicalHistory.vaccine import Vaccine
from schemas.MedicalHistory.vaccine import VaccineSchemaGet, VaccineSchemaPost
from validators.schema_validator import SchemaValidator
from validators.medical_history_validator import MedicalHistoryValidator

class VaccineService:

    @staticmethod
    def add_vaccine(medical_history_id: int, vaccine: VaccineSchemaPost, db: Session):
        MedicalHistoryValidator.get_medical_history_by_id(medical_history_id, db)
        SchemaValidator.validate_schema(vaccine, db)

        new_vaccine = vaccine.to_model(medical_history_id)
        db.add(new_vaccine)
        db.commit()
        db.refresh(new_vaccine)
        return VaccineSchemaGet.from_orm(new_vaccine)

    @staticmethod
    def get_all_vaccines_by_medical_history_id(medical_history_id: int, db: Session):
        vaccines = db.query(Vaccine).filter(Vaccine.medical_history_id == medical_history_id).all()
        if not vaccines:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No vaccines found for the given medical history ID")
        return [VaccineSchemaGet.from_orm(vaccine) for vaccine in vaccines]