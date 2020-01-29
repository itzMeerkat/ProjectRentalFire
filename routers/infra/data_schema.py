from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    scopes: List[str] = []


class User(BaseModel):
    username: str
    email: str = None
    scopes: List[str] = []


class UserFull(User):
    hashed_password: str
