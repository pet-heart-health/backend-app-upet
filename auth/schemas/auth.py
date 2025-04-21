from pydantic import BaseModel
from enum import Enum

class CreateUserRequest (BaseModel):
    email: str
    password: str

class Token (BaseModel):
    access_token: str
    token_type: str


class UserType(str, Enum):
    Vet = "Vet"
    Owner = "Owner"

class UserSchemaPost(BaseModel):
    name: str
    email: str
    password: str
    userType: UserType

class UserSchemaResponse(BaseModel):
    id: int
    name: str
    email: str
    userType: UserType
    registered: bool

class UserChangePasswordRole(BaseModel):
    password: str
    role: UserType  

class UserChangePassword(BaseModel):
    password: str

class UserForgotPassword(BaseModel):
    email: str

class UserVerifyCode(BaseModel):
    code: str        
