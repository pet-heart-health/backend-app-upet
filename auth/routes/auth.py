
from config.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from auth.schemas.auth import  Token, UserSchemaResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from schemas.user import UserSchemaPost, UserSchemaGet
from models.user import User
from  passlib.hash import bcrypt as func
from auth.services.auth import AuthServices
from ..config.auth import token_endpoint, tag, endpoint
from auth.schemas.auth import CreateUserRequest , UserChangePasswordRole, UserChangePassword, UserForgotPassword, UserVerifyCode
auth = APIRouter()


@auth.post(endpoint + '/sign-up', status_code=status.HTTP_201_CREATED,  response_model= Token, tags=[tag])
async def sign_up(create_user_request: UserSchemaPost, db: Session = Depends(get_db)):
    new_user = await AuthServices.sign_up(create_user_request = create_user_request, db=db)
    return new_user


@auth.post(token_endpoint, status_code=status.HTTP_200_OK, response_model=Token, tags=[tag])
async def sign_in(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    token = await AuthServices.sign_in(create_user_request = create_user_request , db=db)
    return token

#user_dependency = Annotated[dict, Depends(auth_services.get_current_user)]
#@auth.get(endpoint + '/current-user', status_code= status.HTTP_200_OK, tags=[tag])
#async def get_user(user: user_dependency, db: Session = Depends(get_db)):
    try:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return {"User": user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@auth.post(f"{endpoint}/forgot-password",  response_model=UserSchemaGet, tags=[tag])
def request_code(request: UserForgotPassword, db: Session = Depends(get_db)):
    user = AuthServices.request_code(request.email, db)
    return user

@auth.post(f"{endpoint}/verify_code",  response_model=UserSchemaGet, tags=[tag])
def verify_code(user_id: str,  request: UserVerifyCode, db: Session = Depends(get_db)):
    user = AuthServices.verify_code(user_id, request.code, db)
    return user

@auth.put(f"{endpoint}/change-password/{{user_id}}",  response_model=UserSchemaGet, tags=[tag])
def change_password(user_id: int,  request: UserChangePassword, db: Session = Depends(get_db)):
    user = AuthServices.change_password(user_id, request.password, db)
    return user

@auth.put(f"{endpoint}/change-password-by-role/{{role_id}}", response_model=UserSchemaGet, tags=[tag])
def change_password_by_role(role_id: int, passwordChange: UserChangePasswordRole, db: Session = Depends(get_db)):
    user = AuthServices.change_password_by_role(role_id, passwordChange.role,  passwordChange.password, db)
    return user
