from pydantic import BaseModel
from models.MedicalHistory.surgery import Surgery

class SurgerySchemaPost(BaseModel):
    surgeryDate: str
    description: str
    medicalHistoryId: int

    def to_model(self, medicalHistoryId: int) -> Surgery:
        return Surgery(
            surgery_date=self.surgeryDate,
            description=self.description,
            medical_history_id=medicalHistoryId
        )

class SurgerySchemaGet(BaseModel):
    id: int
    surgeryDate: str
    description: str
    medicalHistoryId: int

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, surgery: Surgery):
        return cls(
            id=surgery.id,
            surgeryDate=surgery.surgery_date,
            description=surgery.description,
            medicalHistoryId=surgery.medical_history_id
        )
