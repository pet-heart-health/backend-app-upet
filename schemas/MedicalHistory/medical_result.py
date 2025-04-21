from pydantic import BaseModel
from models.MedicalHistory.medical_result import MedicalResult

class MedicalResultSchemaPost(BaseModel):
    resultDate: str
    resultType: str
    description: str
    medicalHistoryId: int

    def to_model(self, medicalHistoryId: int) -> MedicalResult:
        return MedicalResult(
            result_date=self.resultDate,
            result_type=self.resultType,
            description=self.description,
            medical_history_id=medicalHistoryId
        )

class MedicalResultSchemaGet(BaseModel):
    id: int
    resultDate: str
    resultType: str
    description: str
    medicalHistoryId: int

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, medical_result: MedicalResult):
        return cls(
            id=medical_result.id,
            resultDate=medical_result.result_date,
            resultType=medical_result.result_type,
            description=medical_result.description,
            medicalHistoryId=medical_result.medical_history_id
        )
