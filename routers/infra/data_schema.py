from pydantic import BaseModel
from typing import Optional, List

class ReserveActivity(BaseModel):
    uid: int
    item_name: int
    item_ids: List[int]
    amount: int
    reserve_begin_time: int
    checkin_time: int
    request_time: int
    return_time: int
    status: int
    note: str

class ReserveUserRequest(BaseModel):
    item_name: str
    amount: int
    reserve_begin_time: int

class ReserveUserCancel(BaseModel):
    reason: str

class ReserveFrontdeskVerify(BaseModel):
    success: int
    item_ids: List[int]
    checkin_time: int

class ReserveFrontdeskReturn(BaseModel):
    return_time: int
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
