from sqlalchemy import Boolean, Column, Integer, String, Enum, Time
from config.db import Base, engine
from sqlalchemy.orm import relationship

class VeterinaryClinic(Base):
    __tablename__ = 'veterinaryclinics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    location = Column(String(255))  
    services = Column(String(255), default="as")
    office_hours_start = Column(Time, nullable=False)
    office_hours_end = Column(Time, nullable=False)
    phone_number = Column(String(255))
    description = Column(String(255))
    image_url = Column(String(255),default="https://previews.123rf.com/images/sonulkaster/sonulkaster1707/sonulkaster170700464/82258505-hospital-de-medicina-veterinaria-clínica-o-tienda-de-animales-para-animales-.jpg")

    veterinarians = relationship('Veterinarian', back_populates='clinic')

