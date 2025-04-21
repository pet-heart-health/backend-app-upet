import random
import string
import datetime
from sqlalchemy.orm import Session
from models.otps import OTP
from config.db import get_db
from fastapi import Depends

class OTPServices:
    @staticmethod
    def generate_otp(clinic_id: int, db: Session):
        length=6
        otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        expiration_minutes = 10
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
        new_otp = OTP(otp=otp, expiration_time=expiration_time, clinicId=clinic_id)
        db.add(new_otp)
        db.commit()
        return otp


    @staticmethod
    def verify_otp(otp: str, db: Session):
        current_time = datetime.datetime.utcnow()
        otp_record = db.query(OTP).filter(
            OTP.otp == otp,
            OTP.expiration_time > current_time
        ).first()

        if otp_record:
            if otp_record.is_expired():
                db.delete(otp_record)
                db.commit()
                return None
            return otp_record
        return None
    
    @staticmethod
    def delete_otp_record(otp_record: OTP, db: Session):
        db.delete(otp_record)
        db.commit()