from pydantic import BaseModel
from typing import Optional, List

# Status: Open, Closed, Canceled, Failed

class ReserveUserRequest(BaseModel):
    item_name: str
    amount: int

class ReserveUserCancel(BaseModel):
    aid: str
    reason: str

class ReserveFrontdeskCheckout(BaseModel):
    aid: str
    item_ids: List[int]

class ReserveFrontdeskReturn(BaseModel):
    aid: str
    note: str

class UserProfile(BaseModel):
    email: str
    credit_score: int

class ChangeUserRole(BaseModel):
    user_email: str
    new_role: str

class IdToken(BaseModel):
    id_token: str