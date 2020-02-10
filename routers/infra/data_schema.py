from pydantic import BaseModel
from typing import Optional, List

class ActionReserve(BaseModel):
    start_time: int
    category_id: int
    amount: int

class ActionReserveComplete(BaseModel):
    uid: int
    end_time: int
    status: int

class ActionRecord(ActionReserve, ActionReserveComplete):
    pass

class UserProfile(BaseModel):
    email: str
    credit_score: int

class ActivityHistory(BaseModel):
    history: List[ActionRecord]

class RequestResponse(BaseModel):
    def __init__(self, status):
        self.status = status
    status: int
