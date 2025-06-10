from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from sqlalchemy.orm import Session
from datetime import datetime, date
from fastapi import HTTPException

from services.petService import PetServices
from services.medical_history import MedicalHistoryService
from services.petOwnerService import PetOwnerService

class PDFService:
    
    @staticmethod
    def _calculate_age(birthdate):
        if not birthdate:
            return "Sin especificar"
        
        today = datetime.now().date()
        years = today.year - birthdate.year
        months = today.month - birthdate.month
        
        if today < birthdate.replace(year=today.year):
            years -= 1
            months += 12
        
        if months < 0:
            months += 12
        
        if years == 0:
            return f"{months} meses"
        elif months == 0:
            return f"{years} años"
        else:
            return f"{years} años, {months} meses"
    
    @staticmethod
    def _format_date(date_value):
        """Formatea una fecha de manera segura"""
        if not date_value:
            return "Sin fecha"
        

        if isinstance(date_value, str):
            return date_value
        

        if hasattr(date_value, 'strftime'):
            return date_value.strftime('%d/%m/%Y')
        

        return str(date_value)
    
    @staticmethod
    def _format_enum_value(enum_value):
        if not enum_value:
            return "Sin especificar"
        
        enum_str = str(enum_value)
        
        if "." in enum_str:
            enum_str = enum_str.split(".")[-1]
        
        if isinstance(enum_value, tuple) and len(enum_value) > 0:
            enum_str = enum_value[0]
        
        species_mapping = {
            "Dog": "Perro", "Cat": "Gato", "Bird": "Ave", "Fish": "Pez",
            "Reptile": "Reptil", "Rodent": "Roedor", "Rabbit": "Conejo", "Other": "Otro"
        }
        
        gender_mapping = {
            "Male": "Macho", "Female": "Hembra", "Unknown": "Desconocido"
        }
        
        if enum_str in species_mapping:
            return species_mapping[enum_str]
        
        if enum_str in gender_mapping:
            return gender_mapping[enum_str]
        
        return enum_str.capitalize() if enum_str else "Sin especificar"
    
    @staticmethod
    def generate_medical_report(pet_id: int, db: Session):
        try:
            pet = PetServices.get_pet_by_id(pet_id, db)
            if not pet:
                raise HTTPException(status_code=404, detail="Mascota no encontrada")
            
            pet_owner_schema = None
            try:
                pet_owner_schema = PetOwnerService.get_petOwner_by_id(pet.petOwnerId, db)
            except Exception as e:
                print(f"Error obteniendo propietario: {e}")
            
            medical_history = None
            medical_results = []
            diseases = []
            surgeries = []
            vaccines = []

            try:
                medical_history = MedicalHistoryService.get_medical_history_by_pet_id(pet_id, db)
                print(f"Medical history encontrado: {medical_history.id if medical_history else 'None'}")
            except Exception as e:
                print(f"Error obteniendo historial médico base: {e}")

            if medical_history:
                try:
                    medical_results = MedicalHistoryService.get_all_medical_results_by_id(medical_history.id, db)
                    print(f"Medical results encontrados: {len(medical_results)}")
                except Exception as e:
                    print(f"Error obteniendo medical results: {e}")
                    medical_results = []
                
                try:
                    diseases = MedicalHistoryService.get_all_diseases_by_id(medical_history.id, db)
                    print(f"Diseases encontradas: {len(diseases)}")
                except Exception as e:
                    print(f"Error obteniendo diseases: {e}")
                    diseases = []
                
                try:
                    surgeries = MedicalHistoryService.get_all_surgeries_by_id(medical_history.id, db)
                    print(f"Surgeries encontradas: {len(surgeries)}")
                except Exception as e:
                    print(f"Error obteniendo surgeries: {e}")
                    surgeries = []
                
                try:
                    vaccines = MedicalHistoryService.get_all_vaccines_by_id(medical_history.id, db)
                    print(f"Vaccines encontradas: {len(vaccines)}")
                except Exception as e:
                    print(f"Error obteniendo vaccines: {e}")
                    vaccines = []

            print(f"=== RESUMEN FINAL ===")
            print(f"Medical history: {'Sí' if medical_history else 'No'}")
            print(f"Vaccines: {len(vaccines)}")
            print(f"Diseases: {len(diseases)}")
            print(f"Surgeries: {len(surgeries)}")
            print(f"Medical results: {len(medical_results)}")
            
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Encabezado del documento
            p.setFont("Helvetica-Bold", 20)
            p.drawString(50, height - 50, "REPORTE MÉDICO VETERINARIO")
            
            p.line(50, height - 80, width - 50, height - 80)
            
            # Información de la mascota
            y_position = height - 120
            p.setFont("Helvetica-Bold", 14)
            p.drawString(50, y_position, "INFORMACIÓN DE LA MASCOTA")
            
            y_position -= 30
            p.setFont("Helvetica", 12)
            
            pet_name = getattr(pet, 'name', 'Sin nombre')
            pet_species = PDFService._format_enum_value(pet.species)
            
            p.drawString(50, y_position, f"Nombre: {pet_name}")
            p.drawString(300, y_position, f"Especie: {pet_species}")
            
            y_position -= 20
            pet_breed = getattr(pet, 'breed', 'Sin especificar')
            pet_age = PDFService._calculate_age(getattr(pet, 'birthdate', None))
            
            p.drawString(50, y_position, f"Raza: {pet_breed}")
            p.drawString(300, y_position, f"Edad: {pet_age}")
            
            y_position -= 20
            pet_weight = getattr(pet, 'weight', None)
            pet_gender = PDFService._format_enum_value(pet.gender)
            
            weight_text = f"{pet_weight} kg" if pet_weight else "Sin especificar"
            p.drawString(50, y_position, f"Peso: {weight_text}")
            p.drawString(300, y_position, f"Sexo: {pet_gender}")
            
            y_position -= 20
            if hasattr(pet, 'birthdate') and pet.birthdate:
                birth_date_str = PDFService._format_date(pet.birthdate)
                p.drawString(50, y_position, f"Fecha de nacimiento: {birth_date_str}")
            
            # Información del propietario
            if pet_owner_schema:
                y_position -= 50
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "INFORMACIÓN DEL PROPIETARIO")
                
                y_position -= 30
                p.setFont("Helvetica", 12)
                
                owner_name = getattr(pet_owner_schema, 'name', 'Sin nombre')
                owner_email = getattr(pet_owner_schema, 'email', 'Sin email')
                owner_phone = getattr(pet_owner_schema, 'numberPhone', 'Sin teléfono')
                owner_location = getattr(pet_owner_schema, 'location', 'Sin ubicación')
                
                p.drawString(50, y_position, f"Nombre: {owner_name}")
                p.drawString(300, y_position, f"Email: {owner_email}")
                
                y_position -= 20
                p.drawString(50, y_position, f"Teléfono: {owner_phone}")
                p.drawString(300, y_position, f"Ubicación: {owner_location}")
            else:
                y_position -= 50
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "INFORMACIÓN DEL PROPIETARIO")
                
                y_position -= 30
                p.setFont("Helvetica", 12)
                p.drawString(50, y_position, "Información del propietario no disponible")
            
            # Historial médico básico
            if medical_history:
                y_position -= 50
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "HISTORIAL MÉDICO")
                
                y_position -= 30
                p.setFont("Helvetica", 12)
                
                if hasattr(medical_history, 'date') and medical_history.date:
                    history_date_str = PDFService._format_date(medical_history.date)
                    p.drawString(50, y_position, f"Fecha de creación: {history_date_str}")
                    y_position -= 20
                
                description = getattr(medical_history, 'description', 'Sin descripción')
                if len(description) > 80:
                    description = description[:80] + "..."
                p.drawString(50, y_position, f"Descripción: {description}")
            
            # Vacunas
            if vaccines:
                y_position -= 40
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "VACUNAS")
                y_position -= 20
                
                for vaccine in vaccines:
                    if y_position < 100:
                        p.showPage()
                        y_position = height - 50
                    
                    p.setFont("Helvetica", 10)
                    vaccine_name = getattr(vaccine, 'name', 'Vacuna sin nombre')
                    vaccine_date = getattr(vaccine, 'vaccine_date', None)
                    vaccine_date_str = PDFService._format_date(vaccine_date)
                    
                    p.drawString(50, y_position, f"• {vaccine_name} - {vaccine_date_str}")
                    y_position -= 15
            
            # Enfermedades
            if diseases:
                y_position -= 30
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "ENFERMEDADES")
                y_position -= 20
                
                for disease in diseases:
                    if y_position < 100:
                        p.showPage()
                        y_position = height - 50
                    
                    p.setFont("Helvetica", 10)
                    disease_name = getattr(disease, 'name', 'Enfermedad sin nombre')
                    diagnosis_date = getattr(disease, 'diagnosis_date', None)
                    diagnosis_date_str = PDFService._format_date(diagnosis_date)
                    
                    if diagnosis_date:
                        p.drawString(50, y_position, f"• {disease_name} - {diagnosis_date_str}")
                    else:
                        p.drawString(50, y_position, f"• {disease_name}")
                    y_position -= 15
            
            # Cirugías
            if surgeries:
                y_position -= 30
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "CIRUGÍAS")
                y_position -= 20
                
                for surgery in surgeries:
                    if y_position < 100:
                        p.showPage()
                        y_position = height - 50
                    
                    p.setFont("Helvetica", 10)
                    surgery_description = getattr(surgery, 'description', 'Cirugía sin descripción')
                    surgery_date = getattr(surgery, 'surgery_date', None)
                    surgery_date_str = PDFService._format_date(surgery_date)
                    
                    if surgery_date:
                        p.drawString(50, y_position, f"• {surgery_description} - {surgery_date_str}")
                    else:
                        p.drawString(50, y_position, f"• {surgery_description}")
                    y_position -= 15
            
            # Resultados médicos
            if medical_results:
                y_position -= 30
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "RESULTADOS MÉDICOS")
                y_position -= 20
                
                for result in medical_results:
                    if y_position < 100:
                        p.showPage()
                        y_position = height - 50
                    
                    p.setFont("Helvetica", 10)
                    result_type = getattr(result, 'result_type', 'Resultado médico')
                    result_date = getattr(result, 'result_date', None)
                    result_date_str = PDFService._format_date(result_date)
                    
                    if result_date:
                        p.drawString(50, y_position, f"• {result_type} - {result_date_str}")
                    else:
                        p.drawString(50, y_position, f"• {result_type}")
                    y_position -= 15
            
            # Si no hay información médica
            if not medical_history and not vaccines and not diseases and not surgeries and not medical_results:
                y_position -= 40
                p.setFont("Helvetica", 12)
                p.drawString(50, y_position, "No hay información médica registrada para esta mascota.")
            
            # Pie de página
            p.setFont("Helvetica", 8)
            p.drawString(50, 50, f"Reporte generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            p.drawString(width - 200, 50, "Sistema Veterinario UPET")
            
            p.save()
            buffer.seek(0)
            return buffer
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generando reporte PDF: {str(e)}")