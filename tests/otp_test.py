import unittest
from unittest.mock import MagicMock
from services.otpService import OTPServices
from models.otps import OTP
import datetime

class TestOTPServices(unittest.TestCase):

    def test_generate_otp(self):
        mock_db = MagicMock()
        otp = OTPServices.generate_otp(clinic_id=1, db=mock_db)

        self.assertIsInstance(otp, str)
        self.assertEqual(len(otp), 6)
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_delete_otp_record(self):
        mock_db = MagicMock()
        otp_record = MagicMock()

        OTPServices.delete_otp_record(otp_record, db=mock_db)
        mock_db.delete.assert_called_once_with(otp_record)
        mock_db.commit.assert_called_once()
        
if __name__ == '__main__':
    unittest.main()