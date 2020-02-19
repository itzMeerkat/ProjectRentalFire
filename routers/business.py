from fastapi import APIRouter
from fastapi import Depends

#import routers.infra.databaseapi as db
from routers.infra.data_schema import *

from routers.infra.firebaseapi import is_valid_token, reserve_item, update_db
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
    res = reserve_item(uid, reservation.item_name, reservation.amount, utils.get_current_milli())
    return res

@router.post("/reservation/cancel")
async def cancel_reservation(request: ReserveUserCancel):
    request.status = 'canceled'
    r = update_db('activities', request.aid, request)
    print(r)
    return r

@router.post("/reservation/checkout")
def checkout_equip(request: ReserveFrontdeskCheckout):
    request.status = 'checked out'
    r = update_db('activities', request.aid, request)
    print(r)
    return r

@router.post("/reservation/return")
def return_equip(request: ReserveFrontdeskReturn):
    request.status = 'closed'
    r = update_db('activities', request.aid, request)
    print(r)
    return r



"""
> Reserve
> Cancel reservation
"""