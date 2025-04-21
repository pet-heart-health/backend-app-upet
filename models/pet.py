from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Enum, Date
from config.db import Base, engine
from Enums.speciesEnum import SpecieEnum
from Enums.genderEnum import GenderEnum
from sqlalchemy.orm import relationship
from models.petOwner import PetOwner
from SmartCollar.Domain.Models.smart_colllar_model import SmartCollar

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    petOwnerId = Column(Integer, ForeignKey('petowners.id'))
    breed = Column(String(255))
    species = Column(Enum(SpecieEnum, name='species_enum'), nullable=False)
    weight = Column(DECIMAL)
    birthdate = Column(Date)
    image_url = Column(String(255), default="https://image.freepik.com/vector-gratis/ilustracion-vector-dibujos-animados-lindo-animal-mascota_24640-53565.jpg")
    gender = Column(Enum(GenderEnum, name='gender'), nullable=False)

    pet_owner = relationship("PetOwner", back_populates="pets")
    appointments = relationship('Appointment', back_populates='pet')
    smartcollars = relationship("SmartCollar", back_populates="pet")
