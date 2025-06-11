from enum import Enum

class NotificationType(str,Enum):
    APPOINTMENT_CREATED = "Appointment Created"
    APPOINTMENT_UPDATED = "Appointment Updated"
    APPOINTMENT_CANCELLED = "Appointment Cancelled"
    MEDICAL_HISTORY_UPDATED = "Medical History Updated"
    REMINDER = "Reminder"
    NEW_REVIEW = "New Review"