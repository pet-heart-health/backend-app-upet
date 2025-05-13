import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, time, date
from fastapi import HTTPException

from models.appointment import Appointment
from schemas.appointment import AppointmentSchemaCreate, AppointmentSchemaUpdate
from services.appointment import AppointmentService
from Enums.statusAppointmentEnum import StatusAppointmentEnum

@patch('models.pet.Pet')
@patch('models.petOwner.PetOwner')
@patch('models.veterinarian.Veterinarian')
@patch('models.appointment.Appointment')
class TestAppointmentService(unittest.TestCase):
    """
    Pruebas unitarias para el servicio de Appointment (citas)
    """
    
    def setUp(self):
        """
        Configuración inicial para cada prueba
        """
        self.db = MagicMock()
        self.test_date = date(2025, 5, 10)
        self.test_time = time(14, 30)
        
        self.pet = MagicMock()
        self.pet.id = 1
        self.pet.name = "Firulais"
        self.pet.petOwnerId = 1
        
        self.pet_owner = MagicMock()
        self.pet_owner.id = 1
        self.pet_owner.name = "Juan Pérez"
        
        self.veterinarian = MagicMock()
        self.veterinarian.id = 1
        self.veterinarian.name = "Dr. García"
        
        self.appointment = MagicMock()
        self.appointment.id = 1
        self.appointment.date_day = self.test_date
        self.appointment.description = "Revisión anual"
        self.appointment.pet_id = 1
        self.appointment.veterinarian_id = 1
        self.appointment.start_time = self.test_time
        self.appointment.end_time = time(15, 0)
        self.appointment.status = StatusAppointmentEnum.upcoming
        self.appointment.diagnosis = None
        self.appointment.treatment = None

    def test_get_all_appointments(self, mock_appointment_cls, mock_vet_cls, mock_pet_owner_cls, mock_pet_cls):
        """
        Prueba la obtención de todas las citas
        """
        self.db.query.return_value.all.return_value = [self.appointment]
        
        result = AppointmentService.get_all_appointments(self.db)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.appointment.id)
        self.db.query.assert_called_once()
    
    def test_get_appointment_by_id_not_found(self, mock_appointment_cls, mock_vet_cls, mock_pet_owner_cls, mock_pet_cls):
        """
        Prueba la obtención de una cita por su ID cuando la cita no existe
        """
        self.db.query.return_value.filter.return_value.first.return_value = None
        
        with self.assertRaises(HTTPException) as context:
            AppointmentService.get_appointment_by_id(999, self.db)
        
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "La cita no existe.")

    def test_create_appointment_pet_not_found(self, mock_appointment_cls, mock_vet_cls, mock_pet_owner_cls, mock_pet_cls):
        """
        Prueba que falla la creación de cita cuando no existe la mascota
        """
        self.db.query.return_value.filter.return_value.first.return_value = None
        
        appointment_schema = MagicMock(spec=AppointmentSchemaCreate)
        appointment_schema.pet_id = 999
        appointment_schema.veterinarian_id = 1
        
        with self.assertRaises(HTTPException) as context:
            AppointmentService.create_appointment(appointment_schema, self.db)
        
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "La mascota no existe.")

    def test_post_appointment_update(self, mock_appointment_cls, mock_vet_cls, mock_pet_owner_cls, mock_pet_cls):
        """
        Prueba la actualización de una cita con diagnóstico y tratamiento
        """
        self.db.query.return_value.filter.return_value.first.return_value = self.appointment
        
        update_schema = MagicMock(spec=AppointmentSchemaUpdate)
        update_schema.diagnosis = "Infección leve"
        update_schema.treatment = "Antibióticos por 7 días"
        
        with patch.object(AppointmentService, 'get_appointment_by_id', return_value=self.appointment):
            result = AppointmentService.post_appointment(1, update_schema, self.db)
        
        self.assertEqual(self.appointment.diagnosis, "Infección leve")
        self.assertEqual(self.appointment.treatment, "Antibióticos por 7 días")
        self.assertEqual(self.appointment.status, StatusAppointmentEnum.completed)
        self.db.commit.assert_called_once()

    def test_get_appointments_by_pet_id(self, mock_appointment_cls, mock_vet_cls, mock_pet_owner_cls, mock_pet_cls):
        """
        Prueba la obtención de citas por ID de mascota
        """
        self.db.query.return_value.filter.return_value.first.return_value = self.pet
        self.db.query.return_value.filter.return_value.all.return_value = [self.appointment]
        
        result = AppointmentService.get_appointments_by_pet_id(1, self.db)
        
        self.assertEqual(result, [self.appointment])

    def test_get_appointments_by_veterinarian_id(self, mock_appointment_cls, mock_vet_cls, mock_pet_owner_cls, mock_pet_cls):
        """
        Prueba la obtención de citas por ID de veterinario
        """
        self.db.query.return_value.filter.return_value.first.return_value = self.veterinarian
        self.db.query.return_value.filter.return_value.all.return_value = [self.appointment]
        
        result = AppointmentService.get_appointments_by_veterinarian_id(1, self.db)
        
        self.assertEqual(result, [self.appointment])

if __name__ == '__main__':
    unittest.main()