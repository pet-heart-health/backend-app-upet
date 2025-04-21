from sqlalchemy import Column, Date, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base, engine

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255))  # Can be 'PetOwner' or 'Veterinarian'
    message = Column(String(255))
    datetime = Column(DateTime)
    notification_target_type = Column(String(50), nullable=False)  # 'PetOwner' or 'Veterinarian'
    notification_target_id = Column(Integer, nullable=False)  # ID of the PetOwner or Veterinarian

