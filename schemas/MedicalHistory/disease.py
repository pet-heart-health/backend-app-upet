from pydantic import BaseModel, validator

from Enums.serverityLevelEnum import SeverityLevel
from models.MedicalHistory.disease import Disease

class DiseaseSchemaPost(BaseModel):
    name: str
    medicalHistoryId: int
    diagnosisDate: str
    severity: SeverityLevel
    
    @validator('name')
    def name_must_have_min_length(cls, v):
        if len(v) < 5:
            raise ValueError('El nombre de la enfermedad debe tener al menos 5 caracteres')
        return v
    
    def to_model(self, medicalHistoryId: int) -> Disease:
        return Disease(
            name=self.name,
            medical_history_id=medicalHistoryId,
            diagnosis_date=self.diagnosisDate,
            severity=self.severity
        )
        

class DiseaseSchemaGet(BaseModel):
    id: int
    name: str
    medicalHistoryId: int
    diagnosisDate: str
    severity: SeverityLevel
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, disease: Disease):
        return cls(
            id=disease.id,
            name=disease.name,
            medicalHistoryId=disease.medical_history_id,
            diagnosisDate=disease.diagnosis_date,
            severity=disease.severity
        )