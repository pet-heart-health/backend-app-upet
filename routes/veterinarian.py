from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db


from schemas.veterinarian import VeterinarianSchemaPost, VeterinarianSchemaGet

from schemas.veterinarian import VeterinarianSchemaGet, VeterinarianSchemaPost, VeterinarianProfileSchemaGet, VeterinarianUpdateInformation

from sqlalchemy.orm import Session
from schemas.veterinaryClinic import AvailabilitySchemaPost
from services.veterinarianService import VeterinarianService
from auth.schemas.auth import Token
veterinarians = APIRouter()
tag = "Veterinarians"


endpoint =  "/veterinarians"

@veterinarians.post( endpoint + "/{user_id}", response_model=Token, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_veterinarian(user_id: int, veterinarian: VeterinarianSchemaPost, db: Session = Depends(get_db)):
    return VeterinarianService.create_new_veterinarian(user_id, veterinarian, db)

@veterinarians.get(endpoint, response_model=list[VeterinarianSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_veterinarians(db: Session = Depends(get_db)):
    return VeterinarianService.get_all_vets(db)

@veterinarians.get(endpoint + "/users/{user_id}", response_model=VeterinarianSchemaGet, tags=[tag])
def get_veterinarian_by_user_id(user_id: int, db: Session = Depends(get_db)):
    veterinarian = VeterinarianService.get_vet_by_user_id(user_id, db)
    if not veterinarian:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinarian not found")
    return veterinarian

@veterinarians.get(endpoint + "/{vet_id}", response_model=VeterinarianSchemaGet, tags=[tag])
def get_veterinarian_by_id(vet_id: int, db: Session = Depends(get_db)):
    veterinarian = VeterinarianService.get_vet_by_id(vet_id, db)
    return veterinarian

@veterinarians.get(endpoint + "/vets/{clinic_id}", response_model=list[VeterinarianSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_vets_by_clinic_id(clinic_id: int, db: Session = Depends(get_db)):
    return VeterinarianService.get_vets_by_clinic_id(clinic_id, db)

@veterinarians.get(endpoint + "/reviews/{vet_id}", response_model=VeterinarianProfileSchemaGet, status_code=status.HTTP_200_OK, tags=[tag])
def get_vet_by_id_details(vet_id: int, db: Session = Depends(get_db)):
    return VeterinarianService.get_vet_by_id_details(vet_id, db)

@veterinarians.post(endpoint + "/{vet_id}/available_times", status_code=status.HTTP_200_OK, tags=[tag])
def get_available_times(vet_id: int, day: AvailabilitySchemaPost, db: Session = Depends(get_db)):
    return VeterinarianService.get_available_times(vet_id, day.date, db)

@veterinarians.put(endpoint + "/{vet_id}", response_model=VeterinarianSchemaGet, status_code=status.HTTP_200_OK, tags=[tag])
def change_vet_information(vet_id: int, vet: VeterinarianUpdateInformation, db: Session = Depends(get_db)):
    return VeterinarianService.change_DataVet(vet_id, vet, db)
