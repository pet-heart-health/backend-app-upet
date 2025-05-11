import unittest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from models.user import User
from models.petOwner import PetOwner
from models.veterinarian import Veterinarian
from Enums.userTypeEnum import UserType
from services.userService import UserService

class TestUserService(unittest.TestCase):
    """
    Pruebas unitarias para el servicio de User (usuarios)
    """
    
    def setUp(self):
        """
        Configuración inicial para cada prueba
        """
        self.db = MagicMock()
        
        self.user_id = 1
        self.name = "Juan Pérez"
        self.email = "juan@example.com"
        self.user_type = UserType.Owner
        self.image_url = "https://example.com/image.jpg"
        self.registered = True
        
        self.user = MagicMock(spec=User)
        self.user.id = self.user_id
        self.user.name = self.name
        self.user.email = self.email
        self.user.userType = self.user_type
        self.user.image_url = self.image_url
        self.user.registered = self.registered
        
        self.owner_id = 5
        self.vet_id = 10
    
    def test_get_user_by_id_returns_correct_data(self):
        """
        Prueba que obtener un usuario por ID devuelve los datos correctos
        """
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_first = MagicMock(return_value=self.user)
        
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = self.user
        
        result = UserService.get_user_by_id(self.user_id, self.db)
        
        self.assertEqual(result.id, self.user_id)
        self.assertEqual(result.name, self.name)
        self.assertEqual(result.email, self.email)
        self.assertEqual(result.userType, self.user_type)
        self.assertEqual(result.image_url, self.image_url)
        self.assertEqual(result.registered, self.registered)
        
        self.db.query.assert_called()
        
    def test_get_user_by_id_not_found(self):
        """
        Prueba que se lanza una excepción cuando el usuario no existe
        """
        mock_query = MagicMock()
        mock_filter = MagicMock()
        
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        with self.assertRaises(HTTPException) as context:
            UserService.get_user_by_id(self.user_id, self.db)
        
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "El usuario no existe o no es un propietario de mascotas no registrado.")
    
    def test_change_image_for_pet_owner(self):
        """
        Prueba cambiar la imagen de un propietario de mascota
        """
        pet_owner = MagicMock()
        pet_owner.userId = self.user_id  # Versión camelCase
        pet_owner.user_id = self.user_id  # Versión snake_case
        
        mock_query_owner = MagicMock()
        mock_filter_owner = MagicMock()
        mock_first_owner = MagicMock(return_value=pet_owner)
        
        self.db.query.side_effect = [mock_query_owner, mock_query_owner]
        mock_query_owner.filter.return_value = mock_filter_owner
        mock_filter_owner.first.return_value = pet_owner
        
        mock_query_user = MagicMock()
        mock_filter_user = MagicMock()
        mock_first_user = MagicMock(return_value=self.user)
        
        self.db.query.side_effect = lambda model: mock_query_owner if model == PetOwner else mock_query_user
        
        new_image_url = "https://example.com/new_image.jpg"
        
        with patch.object(UserService, 'get_user_by_id', return_value=self.user):
            result = UserService.change_image(self.owner_id, UserType.Owner, new_image_url, self.db)
        
        self.assertEqual(self.user.image_url, new_image_url)
        
        self.db.commit.assert_called_once()
    
    def test_change_image_for_veterinarian(self):
        """
        Prueba cambiar la imagen de un veterinario
        """
        vet = MagicMock()
        vet.userId = self.user_id  # Versión camelCase
        vet.user_id = self.user_id  # Versión snake_case
        
        mock_query_vet = MagicMock()
        mock_filter_vet = MagicMock()
        mock_first_vet = MagicMock(return_value=vet)
        
        mock_query_user = MagicMock()
        mock_filter_user = MagicMock()
        mock_first_user = MagicMock(return_value=self.user)
        
        self.db.query.side_effect = lambda model: mock_query_vet if model == Veterinarian else mock_query_user
        mock_query_vet.filter.return_value = mock_filter_vet
        mock_filter_vet.first.return_value = vet
        mock_query_user.filter.return_value = mock_filter_user
        mock_filter_user.first.return_value = self.user
        
        new_image_url = "https://example.com/new_vet_image.jpg"
        
        with patch.object(UserService, 'get_user_by_id', return_value=self.user):
            result = UserService.change_image(self.vet_id, UserType.Vet, new_image_url, self.db)
        
        self.assertEqual(self.user.image_url, new_image_url)
        
        self.db.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()