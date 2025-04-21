from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from Enums.serverityLevelEnum import SeverityLevel
from config.db import Base
from sqlalchemy.orm import relationship

class MedicalResult(Base):
    __tablename__ = 'medicalresults'

    id = Column(Integer, primary_key=True, index=True)
    medical_history_id = Column(Integer, ForeignKey('medicalhistory.id'))
    result_date = Column(String(255))
    result_type = Column(String(255))
    description = Column(String(255))

    medical_history = relationship("MedicalHistory", back_populates="medical_results")
