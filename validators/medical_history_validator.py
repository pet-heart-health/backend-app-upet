from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.medicalHistory import MedicalHistory

class MedicalHistoryValidator:

    @staticmethod
    def get_medical_history_by_id(medical_history_id: int, db: Session) -> MedicalHistory:
        medical_history = db.query(MedicalHistory).filter(MedicalHistory.id == medical_history_id).first()
        if not medical_history:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El historial médico no existe.")
        return medical_history
