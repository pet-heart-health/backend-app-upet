from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.medicalHistory import MedicalHistory
from schemas.MedicalHistory.disease import DiseaseSchemaPost
from schemas.MedicalHistory.medical_result import MedicalResultSchemaPost
from schemas.MedicalHistory.surgery import SurgerySchemaPost
from schemas.MedicalHistory.vaccine import VaccineSchemaPost
from schemas.medicalHistory import MedicalHistorySchemaPost, MedicalHistorySchemaGet
from services.MedicalHistory.disease import DiseaseService
from services.MedicalHistory.medical_result import MedicalResultService
from services.MedicalHistory.surgery import SurgeryService
from services.MedicalHistory.vaccine import VaccineService
from validators.medical_history_validator import MedicalHistoryValidator

class MedicalHistoryService:

    @staticmethod
    def add_medical_history(medical_history: MedicalHistorySchemaPost, db: Session):
        new_medical_history = medical_history.to_model()
        db.add(new_medical_history)
        db.commit()
        db.refresh(new_medical_history)
        return MedicalHistorySchemaGet.from_orm(new_medical_history)
    
    @staticmethod
    def get_all_medical_histories(db: Session):
        medical_histories = db.query(MedicalHistory).all()
        return [MedicalHistorySchemaGet.from_orm(medical_history) for medical_history in medical_histories]
    
    @staticmethod
    def get_medical_history_by_pet_id(pet_id: int, db: Session):
        medical_history = db.query(MedicalHistory).filter(MedicalHistory.petId == pet_id).first()
        if not medical_history:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Historial médico no encontrado.")
        return medical_history

    @staticmethod
    def get_medical_history(medical_history_id: int, db: Session):
        medical_history = MedicalHistoryValidator.get_medical_history_by_id(medical_history_id, db)
        return MedicalHistorySchemaGet.from_orm(medical_history)

    @staticmethod
    def add_medical_result(medical_history_id: int, medical_result: MedicalResultSchemaPost, db: Session):
        MedicalHistoryValidator.get_medical_history_by_id(medical_history_id, db)
        return MedicalResultService.add_medical_result(medical_history_id, medical_result, db)

    @staticmethod
    def add_disease(medical_history_id: int, disease: DiseaseSchemaPost, db: Session):
        MedicalHistoryValidator.get_medical_history_by_id(medical_history_id, db)
        return DiseaseService.add_disease(medical_history_id, disease, db)

    @staticmethod
    def add_surgery(medical_history_id: int, surgery: SurgerySchemaPost, db: Session):
        MedicalHistoryValidator.get_medical_history_by_id(medical_history_id, db)
        return SurgeryService.add_surgery(medical_history_id, surgery, db)

    @staticmethod
    def add_vaccine(medical_history_id: int, vaccine: VaccineSchemaPost, db: Session):
        MedicalHistoryValidator.get_medical_history_by_id(medical_history_id, db)
        return VaccineService.add_vaccine(medical_history_id, vaccine, db)
    
    @staticmethod
    def get_all_medical_results_by_id(medical_history_id: int, db: Session):
        return MedicalResultService.get_all_medical_results_by_medical_history_id(medical_history_id, db)
    
    @staticmethod
    def get_all_diseases_by_id(medical_history_id: int, db: Session):
        return DiseaseService.get_all_diseases_by_medical_history_id(medical_history_id, db)
    
    @staticmethod
    def get_all_surgeries_by_id(medical_history_id: int, db: Session):
        return SurgeryService.get_all_surgeries_by_medical_history_id(medical_history_id, db)
    
    @staticmethod
    def get_all_vaccines_by_id(medical_history_id: int, db: Session):
        return VaccineService.get_all_vaccines_by_medical_history_id(medical_history_id, db)
