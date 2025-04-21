from datetime import datetime, timedelta, time, date
from typing import Optional
from pydantic import BaseModel, Field
from models.appointment import Appointment

class AppointmentSchemaCreate(BaseModel):
    date_day: date
    description: str
    start_time: time
    pet_id: int
    veterinarian_id: int
    
    def to_model(self) -> Appointment:

        start_datetime = datetime.combine(self.date_day, self.start_time)
        end_datetime = start_datetime + timedelta(minutes=30)
    
        return Appointment(
            date_day=self.date_day,
            description=self.description,
            start_time=self.start_time,
            end_time=end_datetime.time(),
            pet_id=self.pet_id,
            veterinarian_id=self.veterinarian_id
        )   

class AppointmentSchemaUpdate(BaseModel):
    diagnosis: str
    treatment: str
    

class AppointmentSchemaGet(BaseModel):
    id: int
    date_day: date
    diagnosis: Optional[str]
    treatment: Optional[str]
    description: str
    start_time: time
    end_time: time
    pet_id: int
    veterinarian_id: int
    status: str

    class Config:
        orm_mode = True
    
    @classmethod
    def from_orm(cls, appointment: Appointment):
        return cls(
            id=appointment.id,
            date_day=appointment.date_day,
            diagnosis=appointment.diagnosis,
            treatment=appointment.treatment,
            description=appointment.description,
            pet_id=appointment.pet_id,
            veterinarian_id=appointment.veterinarian_id,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            status=appointment.status
        )