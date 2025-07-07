from fastapi import APIRouter, Depends, status
from config.db import get_db

from routes.user import endpoint 
from fastapi import HTTPException

from schemas.petOwner import PetOwnerSchemaGet, PetOwnerSchemaPost, PetOwnerUpdateInformation
from schemas.reminder import ReminderPostSchema, ReminderGetSchema
from services.reminderService import ReminderService



from sqlalchemy.orm import Session
from services.petOwnerService import PetOwnerService

from auth.schemas.auth import Token
reminders = APIRouter()
tag = "Reminders"
endpoint = "/reminders"

@reminders.post(endpoint, response_model=ReminderGetSchema, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_reminder(reminder: ReminderPostSchema, db: Session = Depends(get_db)):
    return ReminderGetSchema.from_orm(ReminderService.create_new_reminder(reminder, db))

@reminders.get(endpoint+ "/userId/{user_id}", response_model=list[ReminderGetSchema], status_code=status.HTTP_200_OK, tags=[tag])
def get_reminders(user_id: int, db: Session = Depends(get_db)):
    return ReminderService.get_reminders(user_id, db)

@reminders.get(endpoint, response_model=list[ReminderGetSchema], status_code=status.HTTP_200_OK, tags=[tag])
def get_all_reminders(db: Session = Depends(get_db)):
    return ReminderService.get_all_reminders(db)
