from datetime import datetime
from fastapi import HTTPException
from models.reminder import Reminder
from services.notification import NotificationService
from sqlalchemy.orm import Session
from models.petOwner import PetOwner
from schemas.reminder import ReminderPostSchema, ReminderGetSchema
from sqlalchemy.orm import joinedload
from scheduler_instance import scheduler
import pytz
from apscheduler.triggers.date import DateTrigger

class ReminderService:

    @staticmethod
    def create_new_reminder(reminder: ReminderPostSchema, db: Session):
        new_reminder = reminder.to_model()

        # Asegurar que la hora del reminder tenga zona horaria de Lima
        lima_tz = pytz.timezone('America/Lima')
        current_datetime = datetime.now(lima_tz)
        
        if new_reminder.date_time.tzinfo is None:
            new_reminder.date_time = lima_tz.localize(new_reminder.date_time)
        else:
            # En caso ya tenga tzinfo pero no sea Lima, convertir
            new_reminder.date_time = new_reminder.date_time.astimezone(lima_tz)

        db.add(new_reminder)
        db.commit()
        db.refresh(new_reminder)

        
        # Convertir la hora del reminder a hora local del servidor

        
        # Programar el recordatorio usando la hora correcta de Lima
        scheduler.add_job(
            NotificationService.send_reminder_notification,
            args=[new_reminder.id],
            trigger=DateTrigger(run_date=new_reminder.date_time)
            )

        return new_reminder
    
    @staticmethod
    def get_reminders(user_id: int, db: Session) -> list[ReminderGetSchema]:
        reminders = (
            db.query(Reminder)
            .filter(Reminder.user_id == user_id)
            .options(joinedload(Reminder.user))
            .all()
        )
        return [ReminderGetSchema.from_orm(reminder) for reminder in reminders]
    
    @staticmethod
    def get_reminders_for_scheduling(db: Session) -> list[Reminder]:
        reminders = (
            db.query(Reminder)
            .filter(Reminder.date_time > datetime.now())
            .all()
        )
        return reminders
    
    @staticmethod
    def get_all_reminders(db: Session) -> list[ReminderGetSchema]:
        reminders = db.query(Reminder).all()
        return [ReminderGetSchema.from_orm(reminder) for reminder in reminders]