from fastapi import Depends, Security, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jwt import PyJWTError
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes

from pydantic import ValidationError
from typing import List

from routers.infra.data_schema import *
import routers.infra.databaseapi as db
from routers.infra.exceptions import make_401_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token",
    scopes={
        "me": "Read information about the current user.",
        "items": "Read items."
    }
)

SECRET_KEY = "43bbbb5eb942d57de51decbc207b513f896203e665fbc691aaad3e2f9b03fa28"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    user_val = db.GetUser({'username': username})
    if not username is None:
        return UserFull(**user_val)

def verify_scopes(given, request):
    for i in request:
        if not i in given:
            return False
    return True


def authenticate_user(username: str, password: str, request_scopes: List[str]):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    if not verify_scopes(user.scopes, request_scopes):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = make_401_exception("Could not validate credentials", authenticate_value)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (PyJWTError, ValidationError):
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception


    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise make_401_exception("Not enough permissions", authenticate_value)
    return user

