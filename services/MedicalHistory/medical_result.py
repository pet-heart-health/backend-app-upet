from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.MedicalHistory.medical_result import MedicalResult
from schemas.MedicalHistory.medical_result import MedicalResultSchemaGet, MedicalResultSchemaPost
from validators.schema_validator import SchemaValidator
from validators.medical_history_validator import MedicalHistoryValidator

class MedicalResultService:

    @staticmethod
    def add_medical_result(medical_history_id: int, medical_result: MedicalResultSchemaPost, db: Session):
        MedicalHistoryValidator.get_medical_history_by_id(medical_history_id, db)
        SchemaValidator.validate_schema(medical_result, db)

        new_medical_result = medical_result.to_model(medical_history_id)
        db.add(new_medical_result)
        db.commit()
        db.refresh(new_medical_result)
        return MedicalResultSchemaGet.from_orm(new_medical_result)
    
    @staticmethod
    def get_all_medical_results_by_medical_history_id(medical_history_id: int, db: Session):
        medical_results = db.query(MedicalResult).filter(MedicalResult.medical_history_id == medical_history_id).all()
        if not medical_results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No medical results found for the given medical history ID")
        return [MedicalResultSchemaGet.from_orm(result) for result in medical_results]