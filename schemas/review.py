from datetime import datetime
from pydantic import BaseModel

from models.review import Review
from models.petOwner import PetOwner
from models.user import User
from schemas.petOwner import PetOwnerSchemaGet
class ReviewSchemaPost(BaseModel):
    description : str
    stars : int
    veterinarian_id : int

    def to_model(self, pet_Owner_id) -> Review:
        return Review(
            description=self.description,
            stars=self.stars,
            veterinarian_id=self.veterinarian_id,
            petowner_id=pet_Owner_id
        )
    
class ReviewSchemaGet(BaseModel):
    id: int
    description : str
    stars : int
    review_time : datetime
    image_url : str
    pet_owner_name : str

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, review: Review,):
        petOwner: PetOwner = review.petowner
        user: User = petOwner.user

        return cls(
            id=review.id,
            description=review.description,
            stars=review.stars,
            review_time=review.review_time,
            image_url= user.image_url,
            pet_owner_name= user.name
        )
    