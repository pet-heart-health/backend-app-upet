from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime
from config.db import Base
from Enums.userTypeEnum import UserType
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(155))
    email = Column(String(155), unique=True, index=True)
    password = Column(String(155))
    userType = Column(Enum(UserType, name='user_type'))
    registered = Column(Boolean, default=False)  
    image_url = Column(String(255), default="https://cdn.pixabay.m/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")
    reset_code = Column(String(255), nullable=True)
    reset_code_expiry = Column(DateTime, nullable=True)

    pet_owner = relationship("PetOwner", back_populates="user")
    veterinarian = relationship("Veterinarian", back_populates="user")



from models.petOwner import PetOwner  # Importa la clase PetOwner después de la definición de User
