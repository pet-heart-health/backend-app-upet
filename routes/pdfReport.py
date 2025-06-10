from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from config.db import get_db
from services.pdfService import PDFService
from io import BytesIO

pdf_router = APIRouter()

@pdf_router.get("/pets/{pet_id}/medical-report", tags=["PDF Reports"])
async def generate_pet_medical_report(
    pet_id: int, 
    db: Session = Depends(get_db)
):
    """
    Genera un reporte médico completo en PDF para una mascota específica
    
    - **pet_id**: ID de la mascota
    - Incluye: información básica, historial médico, vacunas, enfermedades, cirugías
    """
    try:
        pdf_buffer = PDFService.generate_medical_report(pet_id, db)
        
        return StreamingResponse(
            BytesIO(pdf_buffer.read()),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=reporte_medico_mascota_{pet_id}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno generando reporte: {str(e)}"
        )

@pdf_router.get("/pets/{pet_id}/medical-report/preview", tags=["PDF Reports"])
async def preview_pet_medical_report(
    pet_id: int, 
    db: Session = Depends(get_db)
):
    """
    Vista previa del reporte médico en el navegador
    """
    try:
        pdf_buffer = PDFService.generate_medical_report(pet_id, db)
        
        return StreamingResponse(
            BytesIO(pdf_buffer.read()),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=preview_reporte_mascota_{pet_id}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno generando vista previa: {str(e)}"
        )