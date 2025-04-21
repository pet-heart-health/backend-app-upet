from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.petOwner import PetOwner
from models.notification import Notification
from schemas.notification import NotificationSchemaGet, NotificationSchemaPost
from services.notification import NotificationService

notifications = APIRouter()
tag = "Notifications"

endpoint = "/notifications"

@notifications.get("/notifications/pet-owner/{pet_owner_id}")
def get_notifications_by_pet_owner(pet_owner_id: int, db: Session = Depends(get_db)):
    """
    Obtener todas las notificaciones para un PetOwner específico.
    """
    notification_service = NotificationService(db)
    notifications = notification_service.get_notifications_by_pet_owner(pet_owner_id)
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for the given PetOwner.")
    return notifications

@notifications.get("/notifications/veterinarian/{veterinarian_id}")
def get_notifications_by_veterinarian(veterinarian_id: int, db: Session = Depends(get_db)):
    """
    Obtener todas las notificaciones para un Veterinarian específico.
    """
    notification_service = NotificationService(db)
    notifications = notification_service.get_notifications_by_veterinarian(veterinarian_id)
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for the given Veterinarian.")
    return notifications

@notifications.get("/notifications")
def get_all_notifications(db: Session = Depends(get_db)):
    """
    Obtener todas las notificaciones en la base de datos.
    """
    notification_service = NotificationService(db)
    notifications = notification_service.get_all_notifications()
    return notifications