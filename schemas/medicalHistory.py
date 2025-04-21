from datetime import date
from pydantic import BaseModel
from models.medicalHistory import MedicalHistory

class MedicalHistorySchemaPost(BaseModel):
    petId: int
    date: date
    description: str
    
    def to_model(self) -> MedicalHistory:
        return MedicalHistory(
            petId=self.petId,
            date=self.date,
            description=self.description
        )

class MedicalHistorySchemaGet(BaseModel):
    id: int
    petId: int
    date: date
    description: str

    class Config:
        orm_mode = True
    
    @classmethod
    def from_orm(cls, medical_history: MedicalHistory):
        return cls(
            id=medical_history.id,
            petId=medical_history.petId,
            date=medical_history.date,
            description=medical_history.description
        )
