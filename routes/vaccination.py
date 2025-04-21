from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.MedicalHistory.vaccine  import Vaccine as Vaccination
from schemas.vaccination import VaccinationSchemaGet, VaccinationSchemaPost

vaccinations = APIRouter()
tag = "Vaccinations"
endpoint = "/vaccinations"

