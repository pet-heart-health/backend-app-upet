import json
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session
from SmartCollar.Application.Schema.smart_collar_schema import SmartCollarRequest, SmartCollarResponse, SmartCollarUpdateRequest
from SmartCollar.Application.Services.smart_collar_service import SmartCollarService
from config.db import get_db


smart_collar = APIRouter()
tag = "SmartCollar"

endpoint = "/smart-collars"

@smart_collar.get(endpoint, response_model=list[SmartCollarResponse], status_code=status.HTTP_200_OK, tags=[tag])
def get_all_smart_collars(db: Session = Depends(get_db)):
    service = SmartCollarService(db)
    return service.get_all_smart_collars()

@smart_collar.post("/add_smart_collar", response_model=SmartCollarResponse)
def add_smart_collar(collar_data: SmartCollarRequest, db: Session = Depends(get_db)):
    service = SmartCollarService(db)
    return service.add_smart_collar(collar_data)

@smart_collar.delete("/delete_smart_collar/{collar_id}")
def delete_smart_collar(collar_id: int, db: Session = Depends(get_db)):
    service = SmartCollarService(db)
    success = service.delete_smart_collar(collar_id)
    if not success:
        raise HTTPException(status_code=404, detail="Collar not found")
    return {"message": "Smart collar deleted successfully"}

@smart_collar.put("/change_pet_association/{collar_id}/{new_pet_id}")
def change_pet_association(collar_id: int, new_pet_id: int, db: Session = Depends(get_db)):
    service = SmartCollarService(db)
    try:
        return service.change_pet_association(collar_id, new_pet_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@smart_collar.put("/smart-collars/{collar_id}", response_model=SmartCollarResponse)
def update_smart_collar(collar_id: int, collar_data: SmartCollarUpdateRequest, db: Session = Depends(get_db)):
    service = SmartCollarService(db)
    try:
        updated_collar = service.update_smart_collar(collar_id, collar_data)
        return updated_collar
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@smart_collar.get("/smart-collars/{collar_id}", response_model=SmartCollarResponse)
def get_smart_collar_by_id(collar_id: int, db: Session = Depends(get_db)):
    service = SmartCollarService(db)
    try:
        return service.get_by_id(collar_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@smart_collar.get("/smart-collars/pet/{pet_id}", response_model=list[SmartCollarResponse])
def get_smart_collars_by_pet_id(pet_id: int, db: Session = Depends(get_db)):
    service = SmartCollarService(db)
    try:
        return service.get_by_pet_id(pet_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@smart_collar.post("/smart-collars/{collar_id}")
def dessociate_pet(collar_id: int, db: Session = Depends(get_db)):
    service = SmartCollarService(db)
    try:
        return service.disassociate_smart_collar(collar_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
                   