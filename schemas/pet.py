from pydantic import BaseModel, Field
from enum import Enum
from datetime import date
from Enums.speciesEnum import SpecieEnum
from Enums.genderEnum import GenderEnum
from models.pet import Pet


class PetSchemaPost(BaseModel):
    name: str
    breed: str
    species: SpecieEnum
    weight: float = Field(..., gt=0)  # Validar que weight sea mayor a 0
    birthdate: date  
    image_url: str
    gender: GenderEnum

class PetSchemaResponse(BaseModel):
    id: int
    name: str
    petOwnerId: int
    breed: str
    species: SpecieEnum
    weight: float
    birthdate: date  
    image_url: str
    gender: GenderEnum
    
    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, pet: Pet):
        return cls(
            id = pet.id,
            name = pet.name,
            petOwnerId = pet.petOwnerId,
            breed = pet.breed,
            species = pet.species,
            weight = pet.weight,
            birthdate = pet.birthdate,
            image_url = pet.image_url,
            gender = pet.gender
        )
    
    @classmethod
    def update_pet_from_schema(cls, pet: Pet, pet_schema: PetSchemaPost):
        pet.name = pet_schema.name
        pet.breed = pet_schema.breed
        pet.species = pet_schema.species
        pet.weight = pet_schema.weight
        pet.birthdate = pet_schema.birthdate
        pet.image_url = pet_schema.image_url
        pet.gender = pet_schema.gender
        return pet