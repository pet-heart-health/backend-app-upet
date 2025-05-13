import unittest
from unittest.mock import MagicMock, patch
from datetime import time, date
from fastapi import HTTPException

from models.veterinaryClinic import VeterinaryClinic
from models.veterinarian import Veterinarian
from schemas.veterinaryClinic import VeterinaryClinicSchemaPost, VeterinaryClinicSchemaGet
from services.veterinaryClinicService import VeterinaryClinicService
from services.otpService import OTPServices

class TestVeterinaryClinicService(unittest.TestCase):
    """
    Pruebas unitarias para el servicio de VeterinaryClinic (clínicas veterinarias)
    """
    
    def setUp(self):
        """
        Configuración inicial para cada prueba
        """
        self.db = MagicMock()
        
        # Datos para las pruebas
        self.clinic_id = 1
        self.name = "Clínica Veterinaria ABC"
        self.location = "Av. Principal 123"
        self.phone_number = "987654321"
        self.description = "Clínica especializada en animales domésticos"
        self.office_hours_start = time(9, 0)
        self.office_hours_end = time(18, 0)
        self.services = "Cirugía, Vacunación, Peluquería"
        self.image_url = "https://example.com/clinic.jpg"
        
        self.clinic = MagicMock(spec=VeterinaryClinic)
        self.clinic.id = self.clinic_id
        self.clinic.name = self.name
        self.clinic.location = self.location
        self.clinic.phone_number = self.phone_number
        self.clinic.description = self.description
        self.clinic.office_hours_start = self.office_hours_start
        self.clinic.office_hours_end = self.office_hours_end
        self.clinic.services = self.services
        self.clinic.image_url = self.image_url
    
    def test_create_veterinary_clinic_returns_correct_data(self):
        """
        Prueba que al crear una clínica veterinaria se devuelven los datos correctos
        """
        clinic_schema = VeterinaryClinicSchemaPost(
            name=self.name,
            location=self.location,
            phone_number=self.phone_number,
            description=self.description,
            office_hours_start=self.office_hours_start,
            office_hours_end=self.office_hours_end
        )
        
        with patch.object(VeterinaryClinicSchemaPost, 'to_model', return_value=self.clinic):
            result = VeterinaryClinicService.create_veterinary_clinic(clinic_schema, self.db)
            
            self.assertEqual(result.id, self.clinic_id)
            self.assertEqual(result.name, self.name)
            self.assertEqual(result.location, self.location)
            self.assertEqual(result.phone_number, self.phone_number)
            self.assertEqual(result.description, self.description)
            self.assertEqual(result.office_hours_start, self.office_hours_start)
            self.assertEqual(result.office_hours_end, self.office_hours_end)
            
            self.db.add.assert_called_once_with(self.clinic)
            self.db.commit.assert_called_once()
    
    def test_create_veterinary_clinic_invalid_hours(self):
        """
        Prueba que se lanza una excepción cuando las horas de oficina son inválidas
        """
        self.clinic.office_hours_start = time(18, 0)
        self.clinic.office_hours_end = time(9, 0)
        
        clinic_schema = MagicMock()
        clinic_schema.to_model.return_value = self.clinic
        
        with self.assertRaises(HTTPException) as context:
            VeterinaryClinicService.create_veterinary_clinic(clinic_schema, self.db)
        
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "La hora de inicio no puede ser mayor a la hora de fin")
    
    def test_get_veterinary_clinics_returns_all_clinics(self):
        """
        Prueba obtener todas las clínicas veterinarias
        """
        clinic2 = MagicMock(spec=VeterinaryClinic)
        clinic2.id = 2
        clinic2.name = "Clínica Veterinaria XYZ"
        
        clinics_list = [self.clinic, clinic2]
        
        self.db.query().all.return_value = clinics_list
        
        result = VeterinaryClinicService.get_veterinary_clinics(self.db)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, self.clinic_id)
        self.assertEqual(result[0].name, self.name)
        self.assertEqual(result[1].id, 2)
        self.assertEqual(result[1].name, "Clínica Veterinaria XYZ")
    
    def test_generate_unique_password_returns_otp(self):
        """
        Prueba que se genera una contraseña única (OTP) para una clínica
        """
        otp_value = "123456"
        with patch.object(OTPServices, 'generate_otp', return_value=otp_value):
            result = VeterinaryClinicService.generate_unique_password(self.clinic_id, self.db)
            
            self.assertEqual(result, otp_value)
    
    def test_verify_veterinarian_register_success(self):
        """
        Prueba la verificación exitosa del registro de un veterinario
        """
        otp_record = MagicMock()
        otp_record.clinicId = self.clinic_id
        
        with patch.object(OTPServices, 'verify_otp', return_value=otp_record):
            with patch.object(OTPServices, 'delete_otp_record'):
                with patch.object(VeterinaryClinicService, 'get_veterinary_clinic_by_id', return_value=self.clinic):
                    # Ejecutar el método a probar
                    result = VeterinaryClinicService.verify_veterinarian_register(self.name, "123456", self.db)
                    
                    # Verificar que se devuelve el ID de la clínica
                    self.assertEqual(result, self.clinic_id)
    
    def test_verify_veterinarian_register_invalid_name(self):
        """
        Prueba que se lanza una excepción cuando el nombre de la clínica es incorrecto
        """
        otp_record = MagicMock()
        otp_record.clinicId = self.clinic_id
        
        with patch.object(OTPServices, 'verify_otp', return_value=otp_record):
            with patch.object(OTPServices, 'delete_otp_record'):
                with patch.object(VeterinaryClinicService, 'get_veterinary_clinic_by_id', return_value=self.clinic):
                    # Verificar que se lanza la excepción con un nombre incorrecto
                    with self.assertRaises(HTTPException) as context:
                        VeterinaryClinicService.verify_veterinarian_register("Nombre Incorrecto", "123456", self.db)
                    
                    # Verificar el código y mensaje de error
                    self.assertEqual(context.exception.status_code, 400)
                    self.assertEqual(context.exception.detail, "El nombre de la clínica no coincide")
    
    def test_get_veterinary_clinic_by_id_returns_correct_clinic(self):
        """
        Prueba obtener una clínica veterinaria por ID
        """
        self.db.query().filter().first.return_value = self.clinic
        
        result = VeterinaryClinicService.get_veterinary_clinic_by_id(self.clinic_id, self.db)
        
        self.assertEqual(result.id, self.clinic_id)
        self.assertEqual(result.name, self.name)
        self.assertEqual(result.location, self.location)
        self.assertEqual(result.phone_number, self.phone_number)

if __name__ == '__main__':
    unittest.main()