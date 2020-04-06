from pydantic import BaseModel
from typing import Optional, List

# Status: Open, Closed, Canceled, Failed
class ReserveActivity(BaseModel):
    aid: str
    uid: int
    item_name: int
    item_ids: List[int]
    amount: int
    reserve_begin_time: int
    checkin_time: int
    request_time: int
    return_time: int
    status: str
    note: str

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
    status: int
    note: str


class UserProfile(BaseModel):
    email: str
    credit_score: int

class ActivityHistory(BaseModel):
    history: List[ReserveActivity]


# class RequestResponse(BaseModel):
#     def __init__(self, status):
#         self.status = status
#     status: int

class ChangeUserRole(BaseModel):
    user_email: str
    new_role: str

class IdToken(BaseModel):
    id_token: str