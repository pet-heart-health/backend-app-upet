from datetime import datetime
from pydantic import BaseModel

from models.petOwner import PetOwner
from models.user import User
from schemas.petOwner import PetOwnerSchemaGet
from models.reminder import Reminder

class ReminderPostSchema(BaseModel):
    title: str
    description: str
    date_time: datetime
    user_id: int

    class Config:
        orm_mode = True
        
    def to_model(self) -> Reminder:
        return Reminder(
            title=self.title,
            description=self.description,
            date_time=self.date_time,
            userId=self.user_id
        )
        
class ReminderGetSchema(BaseModel):
    id: int
    title: str
    description: str
    date_time: datetime
    user_id: int
    
    def from_orm(reminder: Reminder) -> "ReminderGetSchema":
        return ReminderGetSchema(
            id=reminder.id,
            title=reminder.title,
            description=reminder.description,
            date_time=reminder.date_time,
            user_id=reminder.userId
        )