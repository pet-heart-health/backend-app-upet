from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.MedicalHistory.disease import Disease
from schemas.MedicalHistory.disease import DiseaseSchemaGet, DiseaseSchemaPost
from validators.schema_validator import SchemaValidator
from validators.medical_history_validator import MedicalHistoryValidator

class DiseaseService:

    @staticmethod
    def add_disease(medical_history_id: int, disease: DiseaseSchemaPost, db: Session):
        # Validar que el historial médico exista
        MedicalHistoryValidator.get_medical_history_by_id(medical_history_id, db)
        SchemaValidator.validate_schema(disease, db)

        new_disease = disease.to_model(medical_history_id)
        db.add(new_disease)
        db.commit()
        db.refresh(new_disease)
        return DiseaseSchemaGet.from_orm(new_disease)

    @staticmethod
    def get_all_diseases_by_medical_history_id(medical_history_id: int, db: Session):
        diseases = db.query(Disease).filter(Disease.medical_history_id == medical_history_id).all()
        if not diseases:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No diseases found for the given medical history ID")
        return [DiseaseSchemaGet.from_orm(disease) for disease in diseases]