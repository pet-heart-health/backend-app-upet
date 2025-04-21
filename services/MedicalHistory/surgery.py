from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.MedicalHistory.surgery import Surgery
from schemas.MedicalHistory.surgery import SurgerySchemaGet, SurgerySchemaPost
from validators.schema_validator import SchemaValidator
from validators.medical_history_validator import MedicalHistoryValidator

class SurgeryService:

    @staticmethod
    def add_surgery(medical_history_id: int, surgery: SurgerySchemaPost, db: Session):
        MedicalHistoryValidator.get_medical_history_by_id(medical_history_id, db)
        SchemaValidator.validate_schema(surgery, db)

        new_surgery = surgery.to_model(medical_history_id)
        db.add(new_surgery)
        db.commit()
        db.refresh(new_surgery)
        return SurgerySchemaGet.from_orm(new_surgery)
    
    @staticmethod
    def get_all_surgeries_by_medical_history_id(medical_history_id: int, db: Session):
        surgeries = db.query(Surgery).filter(Surgery.medical_history_id == medical_history_id).all()
        if not surgeries:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No surgeries found for the given medical history ID")
        return [SurgerySchemaGet.from_orm(surgery) for surgery in surgeries]