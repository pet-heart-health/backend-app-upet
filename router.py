from fastapi import APIRouter

from routes.user import users as user_router
from routes.veterinaryClinic import veterinary_clinics as veterinary_clinic_router
from routes.pet import pets as pet_router
from routes.appointment import appointments as appointment_router
from routes.notification import notifications as notification_router
from routes.medicalHistory import medical_histories as medical_history_router
from routes.petOwner import pet_owners as pet_owner_router
from routes.veterinarian import veterinarians as veterinarian_router
from routes.disease import diseases as disease_router
from routes.vaccination import vaccinations as vaccine_router
from routes.review import reviews as review_router
from routes.availability import availabilities as availability_router
from auth.routes.auth import auth as auth_router
from config.routes import prefix
from SmartCollar.Application.routes.smart_collar_route import smart_collar
routes = APIRouter()

# Include all the routes
routes.include_router(auth_router,  prefix= prefix)
routes.include_router(user_router, prefix= prefix)
routes.include_router(veterinary_clinic_router,  prefix= prefix)
routes.include_router(pet_router,  prefix= prefix)
routes.include_router(appointment_router,  prefix= prefix)
routes.include_router(notification_router,  prefix= prefix, tags=["Notifications"])
routes.include_router(medical_history_router,  prefix= prefix)
routes.include_router(pet_owner_router,  prefix= prefix)
routes.include_router(veterinarian_router, prefix= prefix)
routes.include_router(disease_router, prefix= prefix)
routes.include_router(vaccine_router,  prefix= prefix)
routes.include_router(review_router,  prefix= prefix)
routes.include_router(availability_router,  prefix= prefix)
routes.include_router(smart_collar,  prefix= prefix, tags=["SmartCollar"])