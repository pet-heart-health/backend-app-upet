from pydantic import BaseModel, Field
from Enums.subscriptionTypeEnum import SubscriptionType
from models.petOwner import PetOwner
from models.user import User

class PetOwnerSchemaPost(BaseModel):
    numberPhone: str
    location: str

class PetOwnerUpdateInformation(BaseModel):
    numberPhone: str
    location: str
    name : str
    image_url : str

class PetOwnerSchemaGet(BaseModel):
    id: int
    name: str
    numberPhone: str
    image_url: str
    location: str
    subscriptionType: SubscriptionType
    
    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, petOwner: PetOwner, user: User):
        return cls(
            id=petOwner.id,
            name=user.name,
            numberPhone=petOwner.numberPhone,
            location=petOwner.location,
            image_url=user.image_url,
            subscriptionType=petOwner.subscriptionType
        )
    
    @staticmethod
    def update_information(petOwner: PetOwner, newInformation: PetOwnerUpdateInformation):
        petOwner.location = newInformation.location
        petOwner.numberPhone = newInformation.numberPhone
        petOwner.user.name = newInformation.name
        petOwner.user.image_url = newInformation.image_url
        return petOwner