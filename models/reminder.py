from sqlalchemy import Column, Integer, String, Enum,DateTime
from config.db import Base
from Enums.subscriptionTypeEnum import SubscriptionType
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'))
    title = Column(String(100))
    description = Column(String(255))
    date_time = Column(DateTime)

    user = relationship("User", back_populates="reminders")