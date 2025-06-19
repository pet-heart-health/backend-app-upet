from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
import pytz
from models.appointment import Appointment
from models.pet import Pet
from models.petOwner import PetOwner
from models.veterinarian import Veterinarian
from Enums.notificationTargetTypeEnum import NotificationTargetType
from Enums.notificationTypeEnum import NotificationType
from services.notification import NotificationService
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

class AppointmentScheduler:

    def __init__(self, db: Session):
        try:
            self.db = db
            self.scheduler = BackgroundScheduler()
            self.scheduler.start()
            print("Scheduler iniciado correctamente.")
        except Exception as e:
            print(f"Error al iniciar el scheduler: {e}")

    def schedule_notifications(self):
        try:
            trigger = IntervalTrigger(minutes=30)  # Revisar cada minuto
            self.scheduler.add_job(self.check_appointments_and_notify, trigger)
            print("Job de revisión de citas programado para ejecutarse cada minuto.")
        except Exception as e:
            print(f"Error al programar las notificaciones: {e}")
        print(f"Scheduler jobs: {self.scheduler.get_jobs()}")



    def check_appointments_and_notify(self):
        """
        Revisa todas las citas próximas y envía notificaciones 30 minutos antes de la cita.
        """
        # Obtener la fecha y hora actuales en la zona horaria de Lima
        lima_tz = pytz.timezone('America/Lima')
        current_datetime = datetime.now(lima_tz)  # Hora actual en Lima
        print(f"Ejecutando job para revisar citas: {current_datetime}")

        # Sumar 30 minutos
        new_datetime = current_datetime + timedelta(minutes=30)
        print(f"Hora + 30 minutos: {new_datetime}")

        try:
            # Consultar todas las citas sin filtros
            appointments = self.db.query(Appointment).all()

            if appointments:
                print(f"Citas encontradas: {len(appointments)}")
                for appointment in appointments:
                    # Combinar date_day y start_time para obtener la fecha y hora completa de la cita
                    appointment_combined_datetime = datetime.combine(appointment.date_day, appointment.start_time)
                    
                    # Convertir appointment_combined_datetime en un datetime consciente de la zona horaria de Lima
                    appointment_combined_datetime = lima_tz.localize(appointment_combined_datetime)
                    
                    print(f"Evaluando cita: -> Cita: {appointment.date_day} {appointment.start_time}, Evaluando con: {appointment_combined_datetime} > {current_datetime} y <= {new_datetime}")

                    # Calcular la diferencia de tiempo entre la cita y la hora actual
                    time_diff = appointment_combined_datetime - current_datetime
                    print(f"Diferencia de tiempo: {time_diff}")

                    # Verificar si la diferencia está dentro del rango de 30 minutos
                    if timedelta(minutes=29, seconds=30) <= time_diff <= timedelta(minutes=30, seconds=30):
                        # Enviar la notificación si la diferencia está dentro del rango de 30 minutos
                        self.send_notification(appointment)
                    else:
                        print("La cita no está a 30 minutos de distancia, no se enviará notificación.")
            else:
                print("No se encontraron citas.")
        except Exception as e:
            print(f"Error al revisar las citas: {e}")



    def send_notification(self, appointment: Appointment):
        """
        Envía una notificación al dueño de la mascota y al veterinario.
        """
        try:
            
            
            pet = self.db.query(Pet).filter(Pet.id == appointment.pet_id).first()
            
            if not pet:
                print(f"Error: No se encontró la mascota para la cita de.")
                return
            

            pet_owner = self.db.query(PetOwner).filter(PetOwner.id == pet.petOwnerId).first()
            
            if not pet_owner:
                print(f"Error: No se encontró al dueño de la mascota para la cita.")
                return


            veterinarian = self.db.query(Veterinarian).filter(Veterinarian.id == appointment.veterinarian_id).first()
            if not pet_owner:
                print(f"Error: No se encontró al dueño de la mascota para la cita.")
                return

            NotificationService.create_notification_for_appointment_reminder(
                db=self.db,
                appointment=appointment,
                pet_owner=pet_owner,
                veterinarian=veterinarian,
            )
        
        except Exception as e:
            print(f"Error al enviar notificaciones: {e}")
