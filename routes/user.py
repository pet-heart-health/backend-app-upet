from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db

from models.user import User
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from services.userService import UserService
from schemas.user import UserChangeImage, UserSchemaGet
users = APIRouter()
tag = "Users"

key = Fernet.generate_key()
func = Fernet(key)

endpoint = "/users"


@users.get(f"{endpoint}", response_model=list[UserSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@users.get(f"{endpoint}/{{user_id}}", response_model=UserSchemaGet, tags=[tag])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@users.put(f"{endpoint}/{{role_id}}", response_model=UserSchemaGet, tags=[tag])
def change_image(role_id: int, imageChange: UserChangeImage, db: Session = Depends(get_db)):
    user = UserService.change_image(role_id, imageChange.role,  imageChange.image_url, db)
    return user