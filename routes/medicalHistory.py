from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from schemas.MedicalHistory.disease import DiseaseSchemaGet, DiseaseSchemaPost
from schemas.MedicalHistory.medical_result import MedicalResultSchemaGet, MedicalResultSchemaPost
from schemas.MedicalHistory.surgery import SurgerySchemaGet, SurgerySchemaPost
from schemas.MedicalHistory.vaccine import VaccineSchemaGet, VaccineSchemaPost
from schemas.medicalHistory import MedicalHistorySchemaPost, MedicalHistorySchemaGet
from services.medical_history import MedicalHistoryService

medical_histories = APIRouter()
tag = "Medical Histories"
endpoint = "/medicalhistories"

@medical_histories.post(endpoint, response_model=MedicalHistorySchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_medical_history(medical_history: MedicalHistorySchemaPost, db: Session = Depends(get_db)):
    return MedicalHistoryService.add_medical_history(medical_history, db)

@medical_histories.get(endpoint, response_model=list[MedicalHistorySchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_all_medical_histories(db: Session = Depends(get_db)):
    return MedicalHistoryService.get_all_medical_histories(db)

@medical_histories.get(endpoint + "/pet/{pet_id}", response_model=MedicalHistorySchemaGet, status_code=status.HTTP_200_OK, tags=[tag])
def get_medical_history_by_pet_id(pet_id: int, db: Session = Depends(get_db)):
    return MedicalHistoryService.get_medical_history_by_pet_id(pet_id, db)

@medical_histories.get(endpoint + "/{medical_history_id}", response_model=MedicalHistorySchemaGet, status_code=status.HTTP_200_OK, tags=[tag])
def get_medical_history(medical_history_id: int, db: Session = Depends(get_db)):
    return MedicalHistoryService.get_medical_history(medical_history_id, db)

@medical_histories.post(endpoint + "/{medical_history_id}/medicalresults", response_model=MedicalResultSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def add_medical_result_to_medical_history(medical_history_id: int, medical_result: MedicalResultSchemaPost, db: Session = Depends(get_db)):
    return MedicalHistoryService.add_medical_result(medical_history_id, medical_result, db)

@medical_histories.post(endpoint + "/{medical_history_id}/diseases", response_model=DiseaseSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def add_disease_to_medical_history(medical_history_id: int, disease: DiseaseSchemaPost, db: Session = Depends(get_db)):
    return MedicalHistoryService.add_disease(medical_history_id, disease, db)

@medical_histories.post(endpoint + "/{medical_history_id}/surgeries", response_model=SurgerySchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def add_surgery_to_medical_history(medical_history_id: int, surgery: SurgerySchemaPost, db: Session = Depends(get_db)):
    return MedicalHistoryService.add_surgery(medical_history_id, surgery, db)

@medical_histories.post(endpoint + "/{medical_history_id}/vaccines", response_model=VaccineSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def add_vaccine_to_medical_history(medical_history_id: int, vaccine: VaccineSchemaPost, db: Session = Depends(get_db)):
    return MedicalHistoryService.add_vaccine(medical_history_id, vaccine, db)

@medical_histories.get(endpoint + "/{medical_history_id}/medicalresults", response_model=list[MedicalResultSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_all_medical_results_by_medical_history_id(medical_history_id: int, db: Session = Depends(get_db)):
    return MedicalHistoryService.get_all_medical_results_by_id(medical_history_id, db)

@medical_histories.get(endpoint + "/{medical_history_id}/diseases", response_model=list[DiseaseSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_all_diseases_by_medical_history_id(medical_history_id: int, db: Session = Depends(get_db)):
    return MedicalHistoryService.get_all_diseases_by_id(medical_history_id, db)

@medical_histories.get(endpoint + "/{medical_history_id}/surgeries", response_model=list[SurgerySchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_all_surgeries_by_medical_history_id(medical_history_id: int, db: Session = Depends(get_db)):
    return MedicalHistoryService.get_all_surgeries_by_id(medical_history_id, db)

@medical_histories.get(endpoint + "/{medical_history_id}/vaccines", response_model=list[VaccineSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_all_vaccines_by_medical_history_id(medical_history_id: int, db: Session = Depends(get_db)):
    return MedicalHistoryService.get_all_vaccines_by_id(medical_history_id, db)

