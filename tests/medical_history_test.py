import unittest
from unittest.mock import MagicMock, patch
from datetime import date
from fastapi import HTTPException

from models.medicalHistory import MedicalHistory
from schemas.medicalHistory import MedicalHistorySchemaPost, MedicalHistorySchemaGet
from services.medical_history import MedicalHistoryService

class TestMedicalHistoryService(unittest.TestCase):
    """
    Pruebas unitarias para el servicio de Medical History (historial médico)
    """
    
    def setUp(self):
        """
        Configuración inicial para cada prueba
        """
        self.db = MagicMock()
        self.pet_id = 10
        self.test_date = date(2025, 5, 10)
        self.description = "Revisión veterinaria de rutina"
        
    def test_add_medical_history_returns_correct_data(self):
        """
        Prueba que al crear un historial médico se devuelven los datos correctos
        """
        input_data = {
            "petId": self.pet_id,
            "date": self.test_date,
            "description": self.description
        }
        
        def mock_db_add(obj):
            obj.id = 1
            
        self.db.add.side_effect = mock_db_add
        
        with patch('schemas.medicalHistory.MedicalHistorySchemaPost') as mock_schema_class:
            medical_history = MedicalHistory(
                id=1,
                petId=self.pet_id,
                date=self.test_date,
                description=self.description
            )
            
            mock_schema = MagicMock()
            mock_schema.to_model.return_value = medical_history
            mock_schema_class.return_value = mock_schema
            mock_schema_class.parse_obj.return_value = mock_schema
            
            with patch('schemas.medicalHistory.MedicalHistorySchemaGet.from_orm') as mock_from_orm:
                mock_from_orm.return_value = {
                    "id": 1,
                    "petId": self.pet_id,
                    "date": self.test_date,
                    "description": self.description
                }
                
                result = MedicalHistoryService.add_medical_history(mock_schema, self.db)
                
                self.assertEqual(result["id"], 1)
                self.assertEqual(result["petId"], self.pet_id)
                self.assertEqual(result["date"], self.test_date)
                self.assertEqual(result["description"], self.description)
    
    def test_get_medical_history_returns_expected_values(self):
        """
        Prueba que al obtener un historial médico se devuelven los datos esperados
        """
        medical_history_id = 1
        
        medical_history = MedicalHistory(
            id=medical_history_id,
            petId=self.pet_id,
            date=self.test_date,
            description=self.description
        )
        
        with patch('validators.medical_history_validator.MedicalHistoryValidator.get_medical_history_by_id',
                  return_value=medical_history) as mock_validator:
            
            expected_response = {
                "id": medical_history_id,
                "petId": self.pet_id,
                "date": self.test_date,
                "description": self.description
            }
            
            with patch('schemas.medicalHistory.MedicalHistorySchemaGet.from_orm',
                      return_value=expected_response) as mock_from_orm:
                
                result = MedicalHistoryService.get_medical_history(medical_history_id, self.db)
                
                self.assertEqual(result["id"], medical_history_id)
                self.assertEqual(result["petId"], self.pet_id)
                self.assertEqual(result["date"], self.test_date)
                self.assertEqual(result["description"], self.description)
                
                mock_validator.assert_called_once_with(medical_history_id, self.db)

if __name__ == '__main__':
    unittest.main()