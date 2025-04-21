from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel
from models.veterinarian import Veterinarian
from models.user import User
from models.veterinaryClinic import VeterinaryClinic
from schemas.review import ReviewSchemaGet
class VeterinarianSchemaPost(BaseModel):
    clinicName: str
    otp_password: str

class VeterinarianUpdateInformation(BaseModel):
    name: str
    description: Optional[str]
    image_url: Optional[str]
    experience: Optional[int]    
    
class VeterinarianSchemaGet(BaseModel):
    id: int
    name: str
    clinicId :int
    image_url: str
    description: Optional[str]
    experience: Optional[int]
    user_id: int
    
    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, veterinarian: Veterinarian, user: User):
        return cls(
            id=veterinarian.id,
            name=user.name,
            image_url= user.image_url,
            user_id=veterinarian.user_id,
            description=veterinarian.description,
            experience=veterinarian.experience,
            clinicId=veterinarian.clinic_id
        )
    
    @staticmethod
    def update_information(veterinarian: Veterinarian, newInformation: VeterinarianUpdateInformation):
        veterinarian.user.name = newInformation.name
        veterinarian.description = newInformation.description
        veterinarian.experience = newInformation.experience
        veterinarian.user.image_url=newInformation.image_url
        return veterinarian 
    
class VeterinarianProfileSchemaGet(BaseModel):
    id: int
    name: str
    image_url: str
    description: Optional[str]
    experience: Optional[int]
    clinicName : str
    workingHourStart: time
    workingHourEnd: time
    clinicAddress: str
    reviews: list[ReviewSchemaGet]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, veterinarian: Veterinarian, reviews: list[ReviewSchemaGet]):
        
        clinic: VeterinaryClinic = veterinarian.clinic
        user: User = veterinarian.user
        return cls(
            id=veterinarian.id,
            name=user.name,
            image_url= user.image_url,
            description = veterinarian.description, 
            experience = veterinarian.experience,
            clinicName=clinic.name,
            workingHourStart=clinic.office_hours_start,
            workingHourEnd=clinic.office_hours_end,
            clinicAddress=clinic.location,
            reviews=reviews
        )
    
   
    


   