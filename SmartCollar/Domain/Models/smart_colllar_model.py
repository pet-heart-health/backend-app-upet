import json
from wsgiref import validate
from pydantic import parse_obj_as
from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.db import Base



class SmartCollar(Base):
    __tablename__ = 'smartcollars'
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(255), unique=True, nullable=False)
    temperature = Column(Float, nullable=True)
    lpm = Column(Integer, nullable=True)
    battery = Column(Float, nullable=False, default=100.0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=True, default=None)
    
    pet = relationship("Pet", back_populates="smartcollars")
