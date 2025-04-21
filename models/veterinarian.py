from typing import List
from sqlalchemy import Boolean, Column, Integer, String, Enum
from config.db import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


from models.user import User  # Importa la clase User desde models.user
from models.veterinaryClinic import VeterinaryClinic  # Importa VeterinaryClinic después de User

class Veterinarian(Base):
    __tablename__ = 'veterinarians'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String(255), nullable=True)
    experience = Column(Integer, nullable=True)  # Permitir que la columna sea nula
    clinic_id = Column(Integer, ForeignKey('veterinaryclinics.id'))  # Nueva columna para la relación con VeterinaryClinic

    user = relationship("User", back_populates="veterinarian")
    clinic = relationship("VeterinaryClinic", back_populates="veterinarians")
    availabilities = relationship('Availability', back_populates='veterinarian')
    appointments = relationship('Appointment', back_populates='veterinarian')
    reviews = relationship("Review", back_populates="veterinarian")
