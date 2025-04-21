from datetime import time
from pydantic import BaseModel
from datetime import date
from models.veterinaryClinic import VeterinaryClinic


class VeterinaryClinicSchemaPost(BaseModel):
    name: str
    location: str
    phone_number: str
    description: str
    office_hours_start: time
    office_hours_end: time
    
    def to_model(self) -> VeterinaryClinic:
        return VeterinaryClinic(
            name=self.name,
            location=self.location,
            phone_number=self.phone_number,
            description=self.description,
            office_hours_start=self.office_hours_start,
            office_hours_end=self.office_hours_end
        )
    
class AvailabilitySchemaPost(BaseModel):
    date: date
    
class VeterinaryClinicSchemaGet(BaseModel):
    id: int
    name: str
    location: str
    services: str
    image_url: str
    description: str
    phone_number: str
    office_hours_start: time
    office_hours_end: time