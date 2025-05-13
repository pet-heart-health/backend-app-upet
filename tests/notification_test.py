import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytz

from models.notification import Notification
from models.petOwner import PetOwner
from models.veterinarian import Veterinarian
from services.notification import NotificationService
from sqlalchemy.orm.exc import NoResultFound

class TestNotificationService(unittest.TestCase):
    """
    Pruebas unitarias para el servicio de Notification (notificaciones)
    """
    
    def setUp(self):
        """
        Configuración inicial para cada prueba
        """
        self.db = MagicMock()
        self.target_type = "PetOwner"
        self.target_id = 5
        self.message = "Recordatorio de cita para mañana"
        self.test_datetime = datetime.now(pytz.UTC)
        
    def test_create_notification_returns_correct_data(self):
        """
        Prueba que al crear una notificación se devuelven los datos correctos
        """
        def mock_db_add(obj):
            obj.id = 1
            
        self.db.add.side_effect = mock_db_add
        
        notification_service = NotificationService(self.db)
        result = notification_service.create_notification(
            target_type=self.target_type,
            target_id=self.target_id,
            message=self.message
        )
        
        self.assertEqual(result.id, 1)
        self.assertEqual(result.notification_target_type, self.target_type)
        self.assertEqual(result.notification_target_id, self.target_id)
        self.assertEqual(result.message, self.message)
        self.assertIsNotNone(result.datetime)
        
        self.assertEqual(self.db.add.call_count, 1)
        self.assertEqual(self.db.commit.call_count, 1)
        self.assertEqual(self.db.refresh.call_count, 1)
    
    def test_get_notifications_by_pet_owner(self):
        """
        Prueba obtener notificaciones para un PetOwner específico
        """
        pet_owner_id = 5
        mock_pet_owner = MagicMock(spec=PetOwner)
        mock_pet_owner.id = pet_owner_id
        
        self.db.query().filter().first.return_value = mock_pet_owner
        
        mock_notifications = [
            Notification(
                id=1,
                notification_target_type="PetOwner",
                notification_target_id=pet_owner_id,
                message="Notificación 1",
                datetime=self.test_datetime
            ),
            Notification(
                id=2,
                notification_target_type="PetOwner",
                notification_target_id=pet_owner_id,
                message="Notificación 2",
                datetime=self.test_datetime
            )
        ]
        
        self.db.query().filter().all.return_value = mock_notifications
        
        notification_service = NotificationService(self.db)
        result = notification_service.get_notifications_by_pet_owner(pet_owner_id)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].message, "Notificación 1")
        self.assertEqual(result[1].id, 2)
        self.assertEqual(result[1].message, "Notificación 2")

if __name__ == '__main__':
    unittest.main()