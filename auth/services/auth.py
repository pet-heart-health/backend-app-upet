from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import secrets
from models.petOwner import PetOwner
from models.veterinarian import Veterinarian
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user import User
from passlib.hash import bcrypt as bcrypt_context
from typing import Annotated
from ..config.auth import SECRET_KEY, ALGORITHM, token_url
from schemas.user import UserType
from auth.schemas.auth import CreateUserRequest, UserSchemaPost
from auth.schemas.auth import  Token, UserSchemaResponse
from sqlalchemy.orm import Session
from services.veterinarianService import VeterinarianService
from services.petOwnerService import PetOwnerService
from auth.services.token import TokenServices
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl=token_url)

class AuthServices:
    @staticmethod
    def authenticate_user(email: str, password: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.password):  
            return False
        
        return user


    async def get_current_user(self, token: Annotated[str,Depends(oauth2_bearer)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            if email is None or user_id is None:
                raise credentials_exception
            return {'email': email, 'user_id': user_id}
        except JWTError:
            raise credentials_exception
        
    @staticmethod
    async def sign_up(create_user_request: UserSchemaPost, db: Session):
        existing_user = db.query(User).filter(User.email == create_user_request.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email registered. Please use another email or sign in if you already have an account.")

        if create_user_request.userType not in ["Vet", "Owner"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UserType must be 'Vet' or 'Owner'.")

        new_user_data = {"name": create_user_request.name, 
                        "email": create_user_request.email, 
                        "userType": create_user_request.userType, 
                        "registered": False}
        new_user_data["password"] = bcrypt_context.encrypt(create_user_request.password.encode("utf-8"))

        new_user = User(**new_user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Refresh the user to get the updated data from the database

        token = TokenServices.create_access_token(new_user.email, new_user.id, new_user.userType, new_user.registered, timedelta(hours=1))

        return Token(access_token=token, token_type="bearer")
    
    @staticmethod
    async def sign_in(create_user_request: CreateUserRequest, db: Session):
        user = AuthServices.authenticate_user(create_user_request.email, create_user_request.password, db)
        role_id=0
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
            
        user_response = UserSchemaResponse(id=user.id, email=user.email, userType=user.userType, registered=user.registered, name=user.name)

        if user_response.registered == True:
            if user_response.userType == UserType.Vet:
                role_id = VeterinarianService.get_vet_by_user_id(user_response.id, db).id
            elif user_response.userType == UserType.Owner:
                role_id = PetOwnerService.get_petowner_by_user_id(user_response.id, db).id
        else:
            role_id = user_response.id

        token = TokenServices.create_access_token(user_response.email, role_id, user_response.userType, user_response.registered, timedelta(hours=1))

        return Token(access_token=token, token_type="bearer")
    
    @staticmethod
    def change_password(user_id: int, password: str, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        user.password = bcrypt_context.encrypt(password.encode("utf-8"))
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def change_password_by_role( role_id: int, role, password: str, db: Session):
        if role == UserType.Owner:
            user_id = db.query(PetOwner).filter(PetOwner.id == role_id).first().userId
        else:
            user_id = db.query(Veterinarian).filter(Veterinarian.id == role_id).first().user_id
        return AuthServices.change_password(user_id, password, db)    
         
    
    @staticmethod
    def request_code(email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist.")
        
        verification_code = ''.join(secrets.choice(string.digits) for _ in range(5))
        user.reset_code = verification_code
        user.reset_code_expiry = datetime.utcnow() + timedelta(minutes=5)
        db.commit()
        try:
            AuthServices.send_email_reset_password(email, verification_code)
        except Exception as e:
            print(f"Failed to send reset email: {e}")
        return user

    @staticmethod
    def send_email_reset_password(email, verification_code):
        message = f"To change your password, please enter the following code: {verification_code}"
        sender_email = "upet.recovery@gmail.com"
        sender_password = "wcpwiivynkcoizlf"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Password Reset - UPET"

        msg.attach(MIMEText(message, 'plain'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, email, text)
            server.quit()
            print(f"Email successfully sent to {email}")
        except Exception as e:
            print(f"Error sending email: {e}")
            raise 

    @staticmethod
    def verify_code(user_id: int, code: str, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist.")
        if user.reset_code == code and user.reset_code_expiry > datetime.utcnow():
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid code or expired.")    