from fastapi import APIRouter, Depends, status
from config.db import get_db

from routes.user import endpoint 
from fastapi import HTTPException

from schemas.petOwner import PetOwnerSchemaGet, PetOwnerSchemaPost, PetOwnerUpdateInformation
from schemas.favoriteClinics import FavoriteClinicsGet
from services.favoriteClinicService import FavoriteClinicService
from schemas.veterinaryClinic import VeterinaryClinicSchemaGet


from sqlalchemy.orm import Session
from services.petOwnerService import PetOwnerService

from auth.schemas.auth import Token
favorite_clinics = APIRouter()
tag = "Favorite Clinics"
endpoint = "/favoriteClinics"

@favorite_clinics.post(endpoint +"/userId/{user_id}/clinicId/{clinic_id}", response_model=bool, status_code=status.HTTP_201_CREATED, tags=[tag])
def toggle_favorite_clinic(user_id: int, clinic_id: int, db: Session = Depends(get_db)):
    return FavoriteClinicService.toggle_favorite_clinic(user_id, clinic_id, db)


@favorite_clinics.get(endpoint+ "/userId/{user_id}", response_model=list[VeterinaryClinicSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_favorite_clinics(user_id: int, db: Session = Depends(get_db)):
    return FavoriteClinicService.get_favorite_clinics(user_id, db)

