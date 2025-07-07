from fastapi import Depends, HTTPException, status
from config.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from schemas.favoriteClinics import FavoriteClinicsGet
from schemas.veterinaryClinic import VeterinaryClinicSchemaGet
from models.favoriteClinic import FavoriteClinic as FavoriteClinicsModel


class FavoriteClinicService:
    @staticmethod
    def get_favorite_clinics(user_id, db:Session = Depends(get_db)) -> list[VeterinaryClinicSchemaGet]:
        favorite_clinics = db.query(FavoriteClinicsModel).filter(
            FavoriteClinicsModel.user_id == user_id
        ).options(joinedload(FavoriteClinicsModel.clinic)).all()

        if not favorite_clinics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No favorite clinics found for this user."
            )

        return [favorite_clinic.clinic for favorite_clinic in favorite_clinics]
    
    @staticmethod
    def toggle_favorite_clinic(user_id: int, clinic_id: int, db: Session = Depends(get_db)) -> bool:
        favorite_clinic = db.query(FavoriteClinicsModel).filter(
            FavoriteClinicsModel.user_id == user_id,
            FavoriteClinicsModel.clinic_id == clinic_id
        ).first()

        if favorite_clinic:
            db.delete(favorite_clinic)
        else:
            favorite_clinic = FavoriteClinicsModel(user_id=user_id, clinic_id=clinic_id)
            db.add(favorite_clinic)

        db.commit()
        return True