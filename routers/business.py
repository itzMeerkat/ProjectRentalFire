from fastapi import APIRouter
from fastapi import Depends

#import routers.infra.databaseapi as db
from routers.infra.data_schema import ReserveUserRequest

from routers.infra.firebaseapi import is_valid_token
import routers.infra.firebaseapi as fb
import routers.infra.utils as utils

router = APIRouter()

# @router.get("/me", response_model=User)
# async def read_users_me(current_user: User = Security(get_current_user, scopes=["me"])):
#     return current_user


# @router.get("/me/items")
# async def read_own_items(
#     current_user: User = Security(get_current_user, scopes=["items"])
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]


# @router.get("/status")
# async def read_system_status(user: User = Depends(get_current_user)):
#     return {"status": "ok"}


@router.get("/fb")
async def read_system_status(uid = Depends(is_valid_token)):
    return {"you are": uid}


@router.post("/reservation/create")
async def create_reservation(reservation: ReserveUserRequest, uid = Depends(is_valid_token)):
    aid = fb.reserve_item(uid, reservation.category, reservation.amount, utils.get_current_millisec())
    if not aid is None:
        return {"status": 200, "AID": aid}
    return {"status": 404}

@router.post("/reservation/verify")
async def verify_reservation(uid=Depends(is_valid_token)):



"""
> Reserve
> Cancel reservation
"""
