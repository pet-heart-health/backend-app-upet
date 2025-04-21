from datetime import datetime, timedelta
from jose import  jwt
from ..config.auth import SECRET_KEY, ALGORITHM
from schemas.user import UserType


class TokenServices:
    @staticmethod
    def create_access_token(email: str,
                            user_id: int, 
                            user_role: UserType,
                            registered: bool, 
                            expires_delta: timedelta):
        to_encode = {"sub": email, "user_id": user_id, "user_role": user_role, "registered": registered}
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt