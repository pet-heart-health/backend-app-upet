import random
import string
import datetime
from sqlalchemy.orm import Session
from models.otps import OTP
from config.db import get_db
from fastapi import Depends
from fastapi import HTTPException, status
from models.petOwner import PetOwner
from models.pet import Pet
from schemas.medicalHistory import MedicalHistorySchemaPost
from schemas.pet import PetSchemaPost, PetSchemaResponse
from services.medical_history import MedicalHistoryService

class PetServices:
    @staticmethod
    def create_new_pet(petowner_id: int, pet: PetSchemaPost, db: Session ):
        pet_owner = db.query(PetOwner).filter(PetOwner.id == petowner_id).first()
        if not pet_owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El propietario de la mascota no existe.")

        if pet.weight <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El peso debe ser mayor a 0.")

 
        new_pet = Pet(petOwnerId=petowner_id, 
                      name=pet.name, 
                      birthdate=pet.birthdate, 
                      weight=pet.weight, 
                      species=pet.species,
                        breed=pet.breed, 
                        gender= pet.gender,
                        image_url= pet.image_url)
        db.add(new_pet)
        db.commit()
        db.refresh(new_pet)  # Para cargar el ID generado
        
    
        medicalHistory = MedicalHistorySchemaPost(
            petId=new_pet.id,  
            date=datetime.date.today(),
            description=f"Creación de historial médico de {new_pet.name}"
        )
        MedicalHistoryService.add_medical_history(medicalHistory,db=db)
        return new_pet

    
    @staticmethod
    def get_pet_by_user_id(pet_id: int, db: Session):
        pet = db.query(Pet).filter(Pet.id == pet_id).first()
        return pet

    @staticmethod
    def get_pets_by_petOwnerid(petOwner_id: int, db: Session):
        pets = db.query(Pet).filter(Pet.petOwnerId == petOwner_id).all()
        return pets
    
    @staticmethod
    def update_pet(pet_id: int, pet: PetSchemaPost, db: Session):
        pet_db = db.query(Pet).filter(Pet.id == pet_id).first()
        if not pet_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
  
        PetSchemaResponse.update_pet_from_schema(pet_db, pet)
        db.commit()
        return pet_db
    
    @staticmethod
    def get_pet_by_id(pet_id: int, db: Session):
        pet = db.query(Pet).filter(Pet.id == pet_id).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
        return pet
    
    @staticmethod
    def delete_pet(pet_id: int, db: Session):
        pet = db.query(Pet).filter(Pet.id == pet_id).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
        db.delete(pet)
        db.commit()
        return pet
       
       
