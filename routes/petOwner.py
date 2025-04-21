from fastapi import APIRouter, Depends, status
from config.db import get_db

from routes.user import endpoint 
from fastapi import HTTPException

from schemas.petOwner import PetOwnerSchemaGet, PetOwnerSchemaPost, PetOwnerUpdateInformation

from sqlalchemy.orm import Session
from services.petOwnerService import PetOwnerService

from auth.schemas.auth import Token
pet_owners = APIRouter()
tag = "Pet Owners"
endpoint = "/petowners"

@pet_owners.post(endpoint +"/{user_id}", response_model=Token, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_petowner(user_id: int, petowner: PetOwnerSchemaPost, db: Session = Depends(get_db)):
    return PetOwnerService.create_new_petowner(user_id, petowner, db)


@pet_owners.get(endpoint, response_model=list[PetOwnerSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_petowners(db: Session = Depends(get_db)):
    return PetOwnerService.get_petowners(db)

@pet_owners.get(endpoint + "/users/{user_id}", response_model=PetOwnerSchemaGet, tags=[tag])
def get_petowner_by_user_id(user_id: int, db: Session = Depends(get_db)):
    pet_owner = PetOwnerService.get_petowner_by_user_id(user_id, db)
    if not pet_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet Owner not found")
    return pet_owner

@pet_owners.get(endpoint + "/{petOwner_id}", response_model=PetOwnerSchemaGet, tags=[tag])
def get_by_id(petOwner_id: int, db: Session = Depends(get_db)):
    pet_owner = PetOwnerService.get_petOwner_by_id(petOwner_id, db)
    return pet_owner

@pet_owners.put(endpoint + "/{petOwner_id}", response_model=PetOwnerSchemaGet, tags=[tag])
def change_petOwner(petOwner_id: int, petOwner: PetOwnerUpdateInformation, db: Session = Depends(get_db)):
    return PetOwnerService.change_Datapetowner(petOwner_id, petOwner, db)
