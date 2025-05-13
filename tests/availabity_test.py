import unittest
from unittest.mock import MagicMock, patch
from datetime import date, time, datetime, timedelta

from models.availability import Availability
from models.veterinarian import Veterinarian
from models.veterinaryClinic import VeterinaryClinic
from schemas.availability import AvailabilitySchema
from services.availability import AvailabilityService

class TestAvailabilityService(unittest.TestCase):
    """
    Pruebas unitarias para el servicio de Availability (disponibilidad)
    """
    
    def setUp(self):
        """
        Configuración inicial para cada prueba
        """
        self.db = MagicMock()
        self.test_date = date(2025, 5, 10)
        self.test_start_time = time(9, 0)
        self.test_end_time = time(17, 0)
        
        self.veterinarian = MagicMock(spec=Veterinarian)
        self.veterinarian.id = 1
        self.veterinarian.name = "Dr. García"
        
        self.clinic = MagicMock(spec=VeterinaryClinic)
        self.clinic.office_hours_start = time(9, 0)
        self.clinic.office_hours_end = time(18, 0)
        self.veterinarian.clinic = self.clinic
        
        self.availability = MagicMock(spec=Availability)
        self.availability.id = 1
        self.availability.date = self.test_date
        self.availability.start_time = self.test_start_time
        self.availability.end_time = self.test_end_time
        self.availability.veterinarian_id = 1
        self.availability.is_available = True
        
    def test_delete_weekly_availabilities(self):
        """
        Prueba la eliminación de todas las disponibilidades semanales
        """
        AvailabilityService.delete_weekly_availabilities(self.db)
        
        self.assertEqual(self.db.query.call_count, 1)
        self.assertEqual(self.db.query.call_args[0][0], Availability)
        self.assertEqual(self.db.query().delete.call_count, 1)
        self.assertEqual(self.db.commit.call_count, 1)
        
    @patch('services.availability.datetime')
    def test_create_weekly_by_new_veterinarian(self, mock_datetime):
        """
        Prueba la creación de disponibilidades semanales para un nuevo veterinario
        """
        mock_now = datetime(2025, 5, 7, 10, 0)  # Un miércoles importante para calcular días hasta sábado
        mock_datetime.now.return_value = mock_now
        
        with patch.object(AvailabilityService, 'create_weekly_availabilities_for_veterinarian') as mock_create:
            AvailabilityService.create_weekly_by_new_veterinarian(self.veterinarian, self.db)
            
            self.assertEqual(mock_create.call_count, 1)
            args = mock_create.call_args[0]
            
            self.assertEqual(args[0], self.veterinarian)
            self.assertEqual(args[1], self.db)
            self.assertEqual(args[2], date(2025, 5, 7))
            self.assertEqual(args[3], 3)  # De miércoles (día 2) a sábado (día 5) hay 5-2=3 días

if __name__ == '__main__':
    unittest.main()