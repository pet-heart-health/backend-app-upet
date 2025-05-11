import unittest
from unittest.mock import MagicMock, patch
from datetime import date, time, datetime, timedelta
from fastapi import HTTPException

from models.veterinarian import Veterinarian
from models.user import User
from models.veterinaryClinic import VeterinaryClinic
from models.review import Review
from models.availability import Availability
from models.appointment import Appointment

from schemas.veterinarian import VeterinarianSchemaPost, VeterinarianSchemaGet, VeterinarianProfileSchemaGet, VeterinarianUpdateInformation
from services.veterinarianService import VeterinarianService
from services.veterinaryClinicService import VeterinaryClinicService
from services.availability import AvailabilityService
from auth.schemas.auth import UserType, Token

class TestVeterinarianService(unittest.TestCase):
    """
    Pruebas unitarias para el servicio de Veterinarian (veterinarios)
    """
    
    def setUp(self):
        """
        Configuración inicial para cada prueba
        """
        self.db = MagicMock()
        self.user_id = 5
        self.vet_id = 10
        self.clinic_id = 3
        self.clinic_name = "Clínica Veterinaria ABC"
        self.otp_password = "123456"
        
        # Mock del usuario
        self.user = MagicMock(spec=User)
        self.user.id = self.user_id
        self.user.name = "Dr. Smith"
        self.user.email = "smith@example.com"
        self.user.userType = UserType.Vet
        self.user.registered = False
        self.user.image_url = "https://example.com/smith.jpg"
        
        # Mock de la clínica
        self.clinic = MagicMock(spec=VeterinaryClinic)
        self.clinic.id = self.clinic_id
        self.clinic.name = self.clinic_name
        self.clinic.location = "Calle Principal 123"
        self.clinic.office_hours_start = time(9, 0)
        self.clinic.office_hours_end = time(18, 0)
        
        # Mock del veterinario
        self.veterinarian = MagicMock(spec=Veterinarian)
        self.veterinarian.id = self.vet_id
        self.veterinarian.user_id = self.user_id
        self.veterinarian.clinic_id = self.clinic_id
        self.veterinarian.description = "Especialista en animales pequeños"
        self.veterinarian.experience = 5
        self.veterinarian.user = self.user
        self.veterinarian.clinic = self.clinic
    
    def test_get_vet_by_id_returns_correct_data(self):
        """
        Prueba que obtener un veterinario por ID devuelve los datos correctos
        """
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_options = MagicMock()
        mock_first = MagicMock(return_value=self.veterinarian)
        
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.options.return_value = mock_options
        mock_options.first.return_value = self.veterinarian
        
        expected_response = {
            "id": self.vet_id,
            "name": self.user.name,
            "clinicId": self.clinic_id,
            "image_url": self.user.image_url,
            "description": self.veterinarian.description,
            "experience": self.veterinarian.experience,
            "user_id": self.user_id
        }
        
        with patch.object(VeterinarianSchemaGet, 'from_orm', return_value=expected_response):
            result = VeterinarianService.get_vet_by_id(self.vet_id, self.db)
            
            self.assertEqual(result["id"], self.vet_id)
            self.assertEqual(result["name"], self.user.name)
            self.assertEqual(result["clinicId"], self.clinic_id)
            self.assertEqual(result["image_url"], self.user.image_url)
            self.assertEqual(result["description"], self.veterinarian.description)
            self.assertEqual(result["experience"], self.veterinarian.experience)
            self.assertEqual(result["user_id"], self.user_id)
    
    def test_get_vet_by_id_not_found(self):
        """
        Prueba que se lanza una excepción cuando no se encuentra el veterinario
        """
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_options = MagicMock()
        mock_first = MagicMock(return_value=None)
        
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.options.return_value = mock_options
        mock_options.first.return_value = None
        
        with self.assertRaises(HTTPException) as context:
            VeterinarianService.get_vet_by_id(self.vet_id, self.db)
        
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Veterinarian not found")
    
    def test_create_new_veterinarian_returns_token(self):
        """
        Prueba que crear un nuevo veterinario devuelve un token válido
        """
        with patch('services.userService.UserService.get_user_by_id', return_value=self.user):
            with patch.object(VeterinaryClinicService, 'verify_veterinarian_register', return_value=self.clinic_id):
                with patch.object(AvailabilityService, 'create_weekly_by_new_veterinarian'):
                    mock_token = "mock_access_token_value"
                    with patch('auth.services.token.TokenServices.create_access_token', return_value=mock_token):
                        vet_schema = VeterinarianSchemaPost(
                            clinicName=self.clinic_name,
                            otp_password=self.otp_password
                        )
                        
                        result = VeterinarianService.create_new_veterinarian(self.user_id, vet_schema, self.db)
                        
                        self.assertEqual(result.access_token, mock_token)
                        self.assertEqual(result.token_type, "bearer")
                        
                        self.assertTrue(self.user.registered)
                        
                        self.db.add.assert_called_once()
                        self.db.commit.assert_called_once()
    
    def test_change_data_vet_updates_correctly(self):
        """
        Prueba que los datos del veterinario se actualizan correctamente
        """
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_first = MagicMock(return_value=self.veterinarian)
        
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = self.veterinarian
        
        new_name = "Dr. Johnson"
        new_description = "Cirujano veterinario especializado"
        new_experience = 8
        new_image = "https://example.com/new_image.jpg"
        
        update_data = VeterinarianUpdateInformation(
            name=new_name,
            description=new_description,
            experience=new_experience,
            image_url=new_image
        )
        
        with patch.object(VeterinarianSchemaGet, 'update_information', return_value=self.veterinarian):
            expected_response = {
                "id": self.vet_id,
                "name": new_name,
                "clinicId": self.clinic_id,
                "image_url": new_image,
                "description": new_description,
                "experience": new_experience,
                "user_id": self.user_id
            }
            
            with patch.object(VeterinarianSchemaGet, 'from_orm', return_value=expected_response):
                result = VeterinarianService.change_DataVet(self.vet_id, update_data, self.db)
                
                self.assertEqual(result["id"], self.vet_id)
                self.assertEqual(result["name"], new_name)
                self.assertEqual(result["description"], new_description)
                self.assertEqual(result["experience"], new_experience)
                self.assertEqual(result["image_url"], new_image)
                
                self.db.commit.assert_called_once()
                self.db.refresh.assert_called_once()

if __name__ == '__main__':
    unittest.main()