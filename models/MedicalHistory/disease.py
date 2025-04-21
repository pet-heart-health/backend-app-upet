from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from Enums.serverityLevelEnum import SeverityLevel
from config.db import Base
from sqlalchemy.orm import relationship

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key=True, index=True)
    medical_history_id = Column(Integer, ForeignKey('medicalhistory.id'))
    diagnosis_date = Column(String(255))
    name = Column(String(255))
    severity = Column(Enum(SeverityLevel))

    medical_history = relationship("MedicalHistory", back_populates="diseases")