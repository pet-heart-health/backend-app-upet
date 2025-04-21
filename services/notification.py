from typing import List
import pytz
from models.notification import Notification
from datetime import datetime
from sqlalchemy.orm import Session
from models.petOwner import PetOwner
from models.veterinarian import Veterinarian
from sqlalchemy.orm.exc import NoResultFound

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, target_type: str, target_id: int, message: str):
        """
        Crea una nueva notificación para el destinatario correspondiente.
        """
        new_notification = Notification(
            notification_target_type=target_type,
            notification_target_id=target_id,
            message=message,
            datetime=datetime.now(pytz.UTC)  # La notificación se marca en el momento actual
        )

        self.db.add(new_notification)
        self.db.commit()
        self.db.refresh(new_notification)
        return new_notification

    def _validate_pet_owner_exists(self, pet_owner_id: int):
        """
        Validate if the PetOwner exists.
        :param pet_owner_id: The ID of the PetOwner.
        """
        pet_owner = self.db.query(PetOwner).filter(PetOwner.id == pet_owner_id).first()
        if not pet_owner:
            raise NoResultFound(f"PetOwner with id {pet_owner_id} does not exist.")

    def _validate_veterinarian_exists(self, veterinarian_id: int):
        """
        Validate if the Veterinarian exists.
        :param veterinarian_id: The ID of the Veterinarian.
        """
        veterinarian = self.db.query(Veterinarian).filter(Veterinarian.id == veterinarian_id).first()
        if not veterinarian:
            raise NoResultFound(f"Veterinarian with id {veterinarian_id} does not exist.")
    def get_notifications_by_pet_owner(self, pet_owner_id: int):
            """
            Obtener todas las notificaciones para un PetOwner específico.
            :param pet_owner_id: El ID del PetOwner.
            :return: Lista de notificaciones.
            """
            self._validate_pet_owner_exists(pet_owner_id)
            notifications = self.db.query(Notification).filter(
                Notification.notification_target_type == "PetOwner",
                Notification.notification_target_id == pet_owner_id
            ).all()
            return notifications

    def get_notifications_by_veterinarian(self, veterinarian_id: int):
        """
        Obtener todas las notificaciones para un Veterinarian específico.
        :param veterinarian_id: El ID del Veterinarian.
        :return: Lista de notificaciones.
        """
        self._validate_veterinarian_exists(veterinarian_id)
        notifications = self.db.query(Notification).filter(
            Notification.notification_target_type == "Veterinarian",
            Notification.notification_target_id == veterinarian_id
        ).all()
        return notifications
    

    def get_all_notifications(self):
        """
        Obtener todas las notificaciones en la base de datos.
        :return: Lista de todas las notificaciones.
        """
        notifications = self.db.query(Notification).all()
        return notifications