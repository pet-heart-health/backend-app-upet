from pydantic import BaseModel
from models.MedicalHistory.vaccine import Vaccine

class VaccineSchemaPost(BaseModel):
    name: str
    vaccineDate: str
    vaccineType: str
    dose: str
    location: str
    medicalHistoryId: int

    def to_model(self, medicalHistoryId: int) -> Vaccine:
        return Vaccine(
            name = self.name,
            vaccine_date=self.vaccineDate,
            vaccine_type=self.vaccineType,
            dose=self.dose,
            location=self.location,
            medical_history_id=medicalHistoryId
        )

class VaccineSchemaGet(BaseModel):
    id: int
    name : str
    vaccineDate: str
    vaccineType: str
    dose: str
    location: str
    medicalHistoryId: int

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, vaccine: Vaccine):
        return cls(
            id=vaccine.id,
            name = vaccine.name,
            vaccineDate=vaccine.vaccine_date,
            vaccineType=vaccine.vaccine_type,
            dose=vaccine.dose,
            location=vaccine.location,
            medicalHistoryId=vaccine.medical_history_id
        )
