from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.petOwner import PetOwner

from schemas.pet import PetSchemaPost, PetSchemaResponse
from models.pet import Pet
from services.petService import PetServices
pets = APIRouter()
tag = "Pets"
endpoint = "/pets"


@pets.post( endpoint + "/{petowner_id}", response_model=PetSchemaResponse, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_pet(petowner_id: int, pet: PetSchemaPost, db: Session = Depends(get_db)):
    return PetServices.create_new_pet(petowner_id, pet, db)


@pets.get( endpoint, response_model=list[PetSchemaResponse], status_code=status.HTTP_200_OK, tags=[tag])
def get_pets(db: Session = Depends(get_db)):
    return PetServices.get_petowners(db)


@pets.get(  endpoint + "/{petowner_id}", response_model=list[PetSchemaResponse], status_code=status.HTTP_200_OK, tags=[tag])
def get_pets_by_owner(petowner_id: int, db: Session = Depends(get_db)):
    return PetServices.get_pets_by_petOwnerid(petowner_id, db)

@pets.put( endpoint + "/{pet_id}", response_model=PetSchemaResponse, status_code=status.HTTP_200_OK, tags=[tag])
def update_pet(pet_id: int, pet: PetSchemaPost, db: Session = Depends(get_db)):
    return PetServices.update_pet(pet_id, pet, db)

@pets.get(endpoint + "/pet/{pet_id}", response_model=PetSchemaResponse, status_code=status.HTTP_200_OK, tags=[tag])
def get_pet_by_id(pet_id: int, db: Session = Depends(get_db)):
    return PetServices.get_pet_by_id(pet_id, db)

@pets.delete( endpoint + "/{pet_id}", response_model=PetSchemaResponse, status_code=status.HTTP_200_OK, tags=[tag])
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    return PetServices.delete_pet(pet_id, db)


