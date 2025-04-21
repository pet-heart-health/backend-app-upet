from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, Enum
from Enums.statusAppointmentEnum import StatusAppointmentEnum
from config.db import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    date_day = Column(Date, nullable=False, default=datetime.utcnow)
    description = Column(String(255))
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=False)
    veterinarian_id = Column(Integer, ForeignKey('veterinarians.id'), nullable=False)
    start_time = Column(Time)
    end_time = Column(Time)
    status = Column(Enum(StatusAppointmentEnum), default=StatusAppointmentEnum.upcoming)
    
    diagnosis = Column(String(255), nullable=True)
    treatment = Column(String(255),  nullable=True)
    
    pet = relationship('Pet', back_populates='appointments')
    veterinarian = relationship('Veterinarian', back_populates='appointments')
