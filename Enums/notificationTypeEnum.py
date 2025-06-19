from enum import Enum

class NotificationType(str,Enum):
    APPOINTMENT_CREATED = "Appointment Created"
    APPOINTMENT_UPDATED = "Appointment Updated"
    APPOINTMENT_CANCELLED = "Appointment Cancelled"
    MEDICAL_HISTORY_UPDATED = "Medical History Updated"
    VACCINE_ADDED = "Vaccine Added"
    DISEASE_ADDED = "Disease Added"
    SURGERY_ADDED = "Surgery Added"
    MEDICAL_RESULT_ADDED = "Medical Result Added"
    REMINDER = "Reminder"
    NEW_REVIEW = "New Review"