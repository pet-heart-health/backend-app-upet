from sqlalchemy import Column, Integer, DateTime, String
from config.db import Base, engine
import datetime

class OTP(Base):
    __tablename__ = 'otps'
    
    id = Column(Integer, primary_key=True, index=True)
    otp = Column(String(255), index=True)
    expiration_time = Column(DateTime)
    clinicId = Column(Integer)

    def is_expired(self):
        return self.expiration_time < datetime.datetime.utcnow()
    
