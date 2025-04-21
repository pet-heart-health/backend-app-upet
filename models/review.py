from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from config.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    stars = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    review_time = Column(DateTime, default=datetime.utcnow)
    petowner_id = Column(Integer, ForeignKey('petowners.id'))
    veterinarian_id = Column(Integer, ForeignKey('veterinarians.id'))

    petowner = relationship('PetOwner', back_populates='reviews')
    veterinarian = relationship('Veterinarian', back_populates='reviews')
