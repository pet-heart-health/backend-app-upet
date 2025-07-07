from datetime import time
from pydantic import BaseModel
from datetime import date
from schemas.veterinaryClinic import VeterinaryClinicSchemaGet


class FavoriteClinicsGet(BaseModel):
    userId: int
    clinics: list[VeterinaryClinicSchemaGet]

    