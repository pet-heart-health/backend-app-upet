from sqlalchemy import Boolean, Column, Integer, String, Enum
from config.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(155))
    email = Column(String(155), unique=True, index=True)
    password = Column(String(155))
    userType = Column(Enum('Vet', 'Owner', name='user_type'))
    registered = Column(Boolean, default=False)  