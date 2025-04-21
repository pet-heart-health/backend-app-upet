from sqlalchemy import Column, Integer, String, ForeignKey
from config.db import Base
from sqlalchemy.orm import relationship

class MedicalHistory(Base):
    __tablename__ = 'medicalhistory'

    id = Column(Integer, primary_key=True, index=True)
    petId = Column(Integer, ForeignKey('pets.id'))
    date = Column(String(255))
    description = Column(String(255))

    # Relationships
    surgeries = relationship("Surgery", back_populates="medical_history")
    medical_results = relationship("MedicalResult", back_populates="medical_history")
    vaccines = relationship("Vaccine", back_populates="medical_history")
    diseases = relationship("Disease", back_populates="medical_history")
