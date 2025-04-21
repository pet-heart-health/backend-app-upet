from datetime import date, time
from pydantic import BaseModel
from models.availability import Availability

class AvailabilitySchema(BaseModel):
    date: date
    start_time: time
    end_time: time
    veterinarian_id: int
    is_available: bool = True
    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, availability_orm: Availability) -> 'AvailabilitySchema':
        return cls(
            date=availability_orm.date,
            start_time=availability_orm.start_time,
            end_time=availability_orm.end_time,
            veterinarian_id=availability_orm.veterinarian_id,
            is_available=availability_orm.is_available
        )