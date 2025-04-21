from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from Enums.serverityLevelEnum import SeverityLevel
from config.db import Base
from sqlalchemy.orm import relationship

class Surgery(Base):
    __tablename__ = 'surgeries'

    id = Column(Integer, primary_key=True, index=True)
    medical_history_id = Column(Integer, ForeignKey('medicalhistory.id'))
    surgery_date = Column(String(255))
    description = Column(String(255))

    medical_history = relationship("MedicalHistory", back_populates="surgeries")
