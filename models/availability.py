from sqlalchemy import Column, Integer, DateTime, String, Boolean, Date, Time
from config.db import Base, engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Availability(Base):
    __tablename__ = 'availabilities'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    veterinarian_id = Column(Integer, ForeignKey('veterinarians.id'))
    is_available = Column(Boolean, default=True)
   
   
    veterinarian = relationship('Veterinarian', back_populates='availabilities')

