from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from Enums.serverityLevelEnum import SeverityLevel
from config.db import Base
from sqlalchemy.orm import relationship


class Vaccine(Base):
    __tablename__ = 'vaccines'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    medical_history_id = Column(Integer, ForeignKey('medicalhistory.id'))
    vaccine_date = Column(String(255))
    vaccine_type = Column(String(255))
    location = Column(String(255))  
    dose = Column(String(255))

    medical_history = relationship("MedicalHistory", back_populates="vaccines")
