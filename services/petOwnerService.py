from fastapi import Depends, HTTPException, status
from config.db import get_db
from routes.user import endpoint as user_endpoint
from models.user import User
from models.petOwner import PetOwner
from schemas.petOwner import PetOwnerSchemaPost, SubscriptionType
from sqlalchemy.orm import Session
from auth.schemas.auth import UserType
from services.userService import UserService
from schemas.petOwner import PetOwnerSchemaGet, PetOwnerUpdateInformation
from auth.services.token import TokenServices
from auth.schemas.auth import Token
from datetime import timedelta
from sqlalchemy.orm import joinedload

class PetOwnerService:

    @staticmethod
    def create_new_petowner(user_id: int, petowner: PetOwnerSchemaPost, db: Session = Depends(get_db)):
        user = UserService.get_user_by_id(user_id, db)

        # Verificar que el userType sea Owner
        if user.userType != UserType.Owner:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es un propietario de mascotas.")

        if user.registered== True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya ha sido registrado")

        if len(petowner.numberPhone) != 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El número de teléfono debe tener 10 dígitos.")


        new_petowner = PetOwner(userId=user_id,
                                 numberPhone= petowner.numberPhone,
                                 location = petowner.location,
                                   subscriptionType=SubscriptionType.Basic)
        db.add(new_petowner)
        user.registered = True
        db.commit()
        
        token = TokenServices.create_access_token(user.email, new_petowner.id, user.userType, user.registered ,timedelta(hours=1))

        return Token(access_token=token, token_type="bearer")

    @staticmethod
    def get_petowners(db: Session = Depends(get_db)):
        petOwners = db.query(PetOwner).options(joinedload(PetOwner.user)).all()
        return [PetOwnerSchemaGet.from_orm(petOwner, petOwner.user) for petOwner in petOwners]

    
    @staticmethod
    def get_petowner_by_user_id(user_id: int, db: Session):
        petOwner = (
            db.query(PetOwner)
            .filter(PetOwner.userId == user_id)
            .options(joinedload(PetOwner.user))  # Carga la relación User junto con Veterinarian
            .first()
        )
        
        if not petOwner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PetOwner not found")

        user = petOwner.user
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return PetOwnerSchemaGet.from_orm(petOwner, user)
    
    @staticmethod
    def get_petOwner_by_id(petOwner_id: int, db: Session) -> PetOwnerSchemaGet:
        petOwner = (
            db.query(PetOwner)
            .filter(PetOwner.id == petOwner_id)
            .options(joinedload(PetOwner.user))  # Carga la relación User junto con Veterinarian
            .first()
        )
        
        if not petOwner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PetOwner not found")

        user = petOwner.user
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return PetOwnerSchemaGet.from_orm(petOwner, user)
    
    @staticmethod
    def change_Datapetowner(petowner_id: int, petowner: PetOwnerUpdateInformation, db: Session):
        petOwner_db = db.query(PetOwner).filter(PetOwner.id == petowner_id).first()
        if not petOwner_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PetOwner not found")
  
        PetOwnerSchemaGet.update_information(petOwner_db, petowner)
        db.commit()
        db.refresh(petOwner_db)
        return PetOwnerSchemaGet.from_orm(petOwner_db, petOwner_db.user)