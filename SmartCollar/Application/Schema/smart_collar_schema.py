from datetime import date, time
from typing import Optional
from pydantic import BaseModel
from SmartCollar.Domain.ValueObject.location_type import LocationType
from models.availability import Availability

class SmartCollarRequest(BaseModel):
    serial_number: str
    temperature: float
    lpm: int
    battery: float
    location: LocationType

    class Config:
        orm_mode = True 


class SmartCollarUpdateRequest(BaseModel):
    temperature: float
    lpm: int
    battery: float
    location: LocationType

    class Config:
        orm_mode = True 


class SmartCollarResponse(BaseModel):
    id: int
    serial_number: str
    temperature: float
    lpm: int
    battery: float
    location: LocationType
    pet_id: Optional[int]  # Allowing pet_id to be None


    class Config:
        orm_mode = True 