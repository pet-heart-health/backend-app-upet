from sqlalchemy import Column, Date, Integer, String, DateTime, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from config.db import Base, engine

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255))  
    title = Column(String(255), nullable=False)
    message = Column(String(255))
    is_read = Column(Boolean, default=False)
    datetime = Column(DateTime)
    target_type = Column(String(50), nullable=False)  # 'PetOwner' or 'Veterinarian'
    target_id = Column(Integer, nullable=False)  # ID of the PetOwner or Veterinarian

