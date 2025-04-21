from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.MedicalHistory.disease import Disease
from schemas.MedicalHistory.disease import DiseaseSchemaGet, DiseaseSchemaPost

diseases = APIRouter()
tag = "Diseases"
endpoint = "/diseases"



