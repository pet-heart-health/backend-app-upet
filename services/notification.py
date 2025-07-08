from typing import List
import pytz
from config.db import SessionLocal
from models.notification import Notification
from datetime import datetime as dt
from sqlalchemy.orm import Session
from models.petOwner import PetOwner
from models.veterinarian import Veterinarian
from Enums.notificationTypeEnum import NotificationType
from Enums.notificationTargetTypeEnum import NotificationTargetType
from sqlalchemy.orm.exc import NoResultFound
from models.appointment import Appointment
from models.pet import Pet
from models.reminder import Reminder
from models.MedicalHistory.disease import Disease
from models.MedicalHistory.vaccine import Vaccine
from models.MedicalHistory.surgery import Surgery
from models.MedicalHistory.medical_result import MedicalResult

class NotificationService:
    @staticmethod
    def create_notification(db:Session, target_type: NotificationTargetType, target_id: int, message: str, title:str,notification_type: NotificationType, datetime: dt = None):
        """
        Crea una nueva notificación para el destinatario correspondiente.
        """
        new_notification = Notification(
             target_type=target_type,
            target_id=target_id,
            message=message,
            title=title,
            is_read=False,  # La notificación se marca como no leída por defecto
            type=notification_type,  # Tipo de notificación (por ejemplo, recordatorio, alerta, etc.)
            datetime=dt.now(pytz.UTC)  # La notificación se marca en el momento actual
        )

        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)
        return new_notification

    @staticmethod
    def create_notification_for_new_review_vet(db:Session, pet_owner: PetOwner, veterinarian: Veterinarian, review_message: str):

        # Notificación para el Veterinarian
        message_veterinarian = f"Has recibido una nueva reseña de {pet_owner.user.name}: {review_message}"
        title_veterinarian = "Nueva Reseña Recibida"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.NEW_REVIEW   
        )

    @staticmethod
    def create_notification_for_new_appointment(db:Session,appointment:Appointment,pet_owner: PetOwner, veterinarian: Veterinarian):
        """
        Crea notificaciones para el PetOwner y el Veterinarian cuando se crea una nueva cita.
        """
        # Notificación para el PetOwner
        message_owner = f"¡Tu cita con el veterinario {veterinarian.user.name} está programada para {appointment.date_day} a las {appointment.start_time}!"
        title_owner = "Nueva Cita Programada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.petOwner,
            target_id=pet_owner.id,
            message=message_owner,
            title=title_owner,
            notification_type=NotificationType.APPOINTMENT_CREATED
        )

        # Notificación para el Veterinarian
        message_veterinarian = f"Tienes una nueva cita programada con {pet_owner.user.name} para la mascota {appointment.pet.name} el {appointment.date_day} a las {appointment.start_time}."
        title_veterinarian = "Nueva Cita Asignada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.APPOINTMENT_CREATED
        )
        
    @staticmethod
    def create_notification_for_appointment_reminder(db:Session, appointment: Appointment, pet_owner: PetOwner, veterinarian: Veterinarian):
        """
        Crea notificaciones de recordatorio para el PetOwner y el Veterinarian 30 minutos antes de la cita.
        """
        # Notificación para el PetOwner
        message_owner = f"¡Tu cita con el veterinario {veterinarian.user.name} está a punto de comenzar! Faltan 30 minutos."
        title_owner = "Recordatorio de Cita"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.petOwner,
            target_id=pet_owner.id,
            message=message_owner,
            title=title_owner,
            notification_type=NotificationType.REMINDER
        )

        # Notificación para el Veterinarian
        message_veterinarian = f"¡Tu cita con la mascota {appointment.pet.name} está a punto de comenzar! Faltan 30 minutos."
        title_veterinarian = "Recordatorio de Cita"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.REMINDER
        )
    @staticmethod
    def create_notification_for_new_vaccine(db:Session, pet_owner: PetOwner, veterinarian: Veterinarian, pet: Pet, vaccine: Vaccine):
        """
        Crea notificaciones para el PetOwner y el Veterinarian cuando se registra una nueva vacuna en el historial médico de una mascota.
        """
        # Notificación para el PetOwner
        message_owner = f"Se ha registrado una nueva vacuna ({vaccine.name}) para la mascota {pet.name}"
        title_owner = "Nueva Vacuna Registrada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.petOwner,
            target_id=pet_owner.id,
            message=message_owner,
            title=title_owner,
            notification_type=NotificationType.VACCINE_ADDED
        )

        # Notificación para el Veterinarian
        message_veterinarian = f"Se ha registrado una nueva vacuna {vaccine.name} para la mascota {pet.name} del propietario {pet_owner.user.name}."
        title_veterinarian = "Nueva Vacuna Registrada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.VACCINE_ADDED
        )    
    
    @staticmethod
    def create_notification_for_new_disease(db:Session, pet_owner: PetOwner, veterinarian: Veterinarian, pet: Pet, disease: Disease):
        """
        Crea notificaciones para el PetOwner y el Veterinarian cuando se registra una nueva enfermedad en el historial médico de una mascota.
        """
        # Notificación para el PetOwner
        message_owner = f"Se ha registrado una nueva enfermedad ({disease.name}) para la mascota {pet.name}"
        title_owner = "Nueva Enfermedad Registrada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.petOwner,
            target_id=pet_owner.id,
            message=message_owner,
            title=title_owner,
            notification_type=NotificationType.DISEASE_ADDED
        )

        # Notificación para el Veterinarian
        message_veterinarian = f"Se ha registrado una nueva enfermedad ({disease.name}) para la mascota {pet.name} del propietario {pet_owner.user.name}."
        title_veterinarian = "Nueva Enfermedad Registrada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.DISEASE_ADDED
        )
    @staticmethod
    def create_notification_for_new_surgery(db:Session, pet_owner: PetOwner, veterinarian: Veterinarian, pet: Pet, surgery: Surgery):
        """
        Crea notificaciones para el PetOwner y el Veterinarian cuando se registra una nueva cirugía en el historial médico de una mascota.
        """
        # Notificación para el PetOwner
        message_owner = f"Se ha registrado una nueva cirugía ({surgery.name}) para la mascota {pet.name}"
        title_owner = "Nueva Cirugía Registrada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.petOwner,
            target_id=pet_owner.id,
            message=message_owner,
            title=title_owner,
            notification_type=NotificationType.SURGERY_ADDED
        )

        # Notificación para el Veterinarian
        message_veterinarian = f"Se ha registrado una nueva cirugía ({surgery.name}) para la mascota {pet.name} del propietario {pet_owner.user.name}."
        title_veterinarian = "Nueva Cirugía Registrada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.SURGERY_ADDED
        )
    @staticmethod
    def create_notification_for_new_medical_result(db:Session, pet_owner: PetOwner, veterinarian: Veterinarian, pet: Pet, medical_result: MedicalResult):
        """
        Crea notificaciones para el PetOwner y el Veterinarian cuando se registra un nuevo resultado médico en el historial médico de una mascota.
        """
        # Notificación para el PetOwner
        message_owner = f"Se ha registrado un nuevo resultado médico ({medical_result.name}) para la mascota {pet.name}"
        title_owner = "Nuevo Resultado Médico Registrado"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.petOwner,
            target_id=pet_owner.id,
            message=message_owner,
            title=title_owner,
            notification_type=NotificationType.MEDICAL_RESULT_ADDED
        )

        # Notificación para el Veterinarian
        message_veterinarian = f"Se ha registrado un nuevo resultado médico ({medical_result.name}) para la mascota {pet.name} del propietario {pet_owner.user.name}."
        title_veterinarian = "Nuevo Resultado Médico Registrado"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.MEDICAL_RESULT_ADDED
        )
        
    @staticmethod
    def create_notification_for_medical_history_update(db:Session, pet_owner: PetOwner, veterinarian: Veterinarian, pet:Pet):
        """
        Crea notificaciones para el PetOwner y el Veterinarian cuando se actualiza el historial médico de una mascota.
        """
        # Notificación para el PetOwner
        message_owner = f"El historial médico de tu mascota {pet.name} ha sido actualizado."
        title_owner = "Historial Médico Actualizado"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.petOwner,
            target_id=pet_owner.id,
            message=message_owner,
            title=title_owner,
            notification_type=NotificationType.MEDICAL_HISTORY_UPDATED
        )

        # Notificación para el Veterinarian
        message_veterinarian = f"El historial médico de la mascota {pet.name} del propietario {pet_owner.user.name} ha sido actualizado."
        title_veterinarian = "Historial Médico Actualizado"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.MEDICAL_HISTORY_UPDATED
        )
        
    @staticmethod
    def create_notification_for_appointment_completion(db:Session, appointment: Appointment, pet_owner: PetOwner, veterinarian: Veterinarian):
        """
        Crea notificaciones para el PetOwner y el Veterinarian cuando se completa una cita.
        """
        # Notificación para el PetOwner
        message_owner = f"Tu cita con el veterinario {veterinarian.user.name} para la mascota {appointment.pet.name} ha sido completada."
        title_owner = "Cita Completada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.petOwner,
            target_id=pet_owner.id,
            message=message_owner,
            title=title_owner,
            notification_type=NotificationType.APPOINTMENT_UPDATED
        )

        # Notificación para el Veterinarian
        message_veterinarian = f"La cita con la mascota {appointment.pet.name} del propietario {pet_owner.user.name} ha sido completada."
        title_veterinarian = "Cita Completada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.APPOINTMENT_UPDATED
        )
    
    @staticmethod
    def create_notification_for_appointment_cancellation(db:Session, appointment: Appointment, pet_owner: PetOwner, veterinarian: Veterinarian):
        """
        Crea notificaciones para el PetOwner y el Veterinarian cuando se cancela una cita.
        """
        # Notificación para el PetOwner
        message_owner = f"Tu cita con el veterinario {veterinarian.user.name} para la mascota {appointment.pet.name} ha sido cancelada."
        title_owner = "Cita Cancelada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.petOwner,
            target_id=pet_owner.id,
            message=message_owner,
            title=title_owner,
            notification_type=NotificationType.APPOINTMENT_CANCELLED
        )

        # Notificación para el Veterinarian
        message_veterinarian = f"La cita con la mascota {appointment.pet.name} del propietario {pet_owner.user.name} ha sido cancelada."
        title_veterinarian = "Cita Cancelada"
        NotificationService.create_notification(
            db=db,
            target_type=NotificationTargetType.veterinarian,
            target_id=veterinarian.id,
            message=message_veterinarian,
            title=title_veterinarian,
            notification_type=NotificationType.APPOINTMENT_CANCELLED
        )
    
    @staticmethod
    def _validate_pet_owner_exists(db: Session, pet_owner_id: int):
        """
        Validate if the PetOwner exists.
        :param pet_owner_id: The ID of the PetOwner.
        """
        pet_owner = db.query(PetOwner).filter(PetOwner.id == pet_owner_id).first()
        if not pet_owner:
            raise NoResultFound(f"PetOwner with id {pet_owner_id} does not exist.")

    @staticmethod
    def _validate_veterinarian_exists(db: Session, veterinarian_id: int):
        """
        Validate if the Veterinarian exists.
        :param veterinarian_id: The ID of the Veterinarian.
        """
        veterinarian = db.query(Veterinarian).filter(Veterinarian.id == veterinarian_id).first()
        if not veterinarian:
            raise NoResultFound(f"Veterinarian with id {veterinarian_id} does not exist.")
   
    @staticmethod
    def get_notifications_by_pet_owner(db: Session, pet_owner_id: int):
        """
        Obtener todas las notificaciones para un PetOwner específico.
        :param pet_owner_id: El ID del PetOwner.
        :return: Lista de notificaciones.
        """
        NotificationService._validate_pet_owner_exists(db, pet_owner_id)
        notifications = db.query(Notification).filter(
            Notification.target_type == "PetOwner",
            Notification.target_id == pet_owner_id
        ).all()
        return notifications

    @staticmethod
    def get_notifications_by_veterinarian(db: Session, veterinarian_id: int):
        """
        Obtener todas las notificaciones para un Veterinarian específico.
        :param veterinarian_id: El ID del Veterinarian.
        :return: Lista de notificaciones.
        """
        NotificationService._validate_veterinarian_exists(db, veterinarian_id)
        notifications = db.query(Notification).filter(
            Notification.target_type == "Veterinarian",
            Notification.target_id == veterinarian_id
        ).all()
        return notifications
    

    @staticmethod
    def get_all_notifications(db: Session):
        """
        Obtener todas las notificaciones en la base de datos.
        :return: Lista de todas las notificaciones.
        """
        notifications = db.query(Notification).all()
        return notifications
    
    
    @staticmethod
    def send_reminder_notification(reminder_id: int):
        """
        Enviar una notificación de recordatorio usando el ID.
        """
        print("Ejecutando send_reminder_notification con ID:", reminder_id)
        db = SessionLocal()
        try:
            reminder = db.query(Reminder).get(reminder_id)
            if not reminder:
                print(f"No se encontró reminder con id {reminder_id}")
                return

            pet_owner = db.query(PetOwner).filter(PetOwner.userId == reminder.userId).first()
            if not pet_owner:
                print(f"PetOwner con id {reminder.userId} no existe")
                return

            message = f"{reminder.description}"
            title = f"Recordatorio: {reminder.title}"

            NotificationService.create_notification(
                db=db,
                target_type=NotificationTargetType.petOwner,
                target_id=pet_owner.id,
                message=message,
                title=title,
                notification_type=NotificationType.REMINDER
            )
        except Exception as e:
            print(f"Error sending reminder notification: {e}")
        finally:
            db.close()
