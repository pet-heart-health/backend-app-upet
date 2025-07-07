from sqlalchemy import Column, Integer, String, ForeignKey
from config.db import Base
from sqlalchemy.orm import relationship

class FavoriteClinic(Base):
    __tablename__ = "favorite_clinics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    clinic_id = Column(Integer, ForeignKey("veterinaryclinics.id"))

    user = relationship("User", back_populates="favorite_clinics")
    clinic = relationship("VeterinaryClinic", back_populates="favorite_clinics")