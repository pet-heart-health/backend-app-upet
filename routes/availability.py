from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.availability import Availability
from schemas.availability import AvailabilitySchema
from services.availability import AvailabilityService

availabilities = APIRouter()
tag = "Availabilities"

endpoint = "/availabilities"

@availabilities.get(endpoint, response_model=list[AvailabilitySchema], status_code=status.HTTP_200_OK, tags=[tag])
def reset_availabilities(db: Session = Depends(get_db)):
    AvailabilityService.check_and_reset_availabilities(db)
    availabilities = db.query(Availability).all()
    availability_schemas = [AvailabilitySchema.from_orm(availability) for availability in availabilities]
    return availability_schemas
