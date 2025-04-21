from fastapi import HTTPException, status
from models.user import User

from sqlalchemy.orm import Session
from auth.schemas.auth import UserType
from models.petOwner import PetOwner
from models.veterinarian import Veterinarian
class UserService:
    
    @staticmethod
    def get_user_by_id(user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe o no es un propietario de mascotas no registrado.")
        return user
    
    @staticmethod
    def change_image(role_id: int, role, image: str, db: Session):   
        if role == UserType.Owner:
            user_id = db.query(PetOwner).filter(PetOwner.id == role_id).first().userId
        else:
            user_id = db.query(Veterinarian).filter(Veterinarian.id == role_id).first().user_id
        user = UserService.get_user_by_id(user_id, db)
        user.image_url = image
        db.commit()
        db.refresh(user)
        return user
    
