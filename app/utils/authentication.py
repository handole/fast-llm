from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from app import auth_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return pwd_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(seconds=auth_settings.jwt_expiry_time)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, auth_settings.jwt_secret, auth_settings.jwt_algoritm)
    return encode_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(seconds=auth_settings.jwt_expiry_time)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, auth_settings.jwt_refresh_secret, auth_settings.jwt_algoritm)
    return encode_jwt
