from fastapi import APIRouter
from fastapi import Depends

from time import time

#import routers.infra.databaseapi as db
from modules.schema.data_schema import *

import modules.db.firebaseapi as db
from modules.db.firebaseapi import is_valid_token
router = APIRouter()

@router.get("/fb")
async def read_system_status(uid = Depends(is_valid_token)):
    return {"reservations": db.get_all_reservations()}


@router.post("/reservation/create")
async def create_reservation(reservation: ReserveUserRequest, uid = Depends(is_valid_token)):
    res = db.reserve_item(uid, reservation.item_name, reservation.amount, int(time()*1000))
    return res

@router.post("/reservation/cancel")
async def cancel_reservation(request: ReserveUserCancel):
    request.status = 'canceled'
    r = db.update_db('activities', request.aid, request)
    print(r)
    return r

@router.post("/reservation/checkout")
def checkout_equip(request: ReserveFrontdeskCheckout):
    request.status = 'checked out'
    r = db.update_db('activities', request.aid, request)
    print(r)
    return r

@router.post("/reservation/return")
def return_equip(request: ReserveFrontdeskReturn):
    request.status = 'closed'
    r = db.update_db('activities', request.aid, request)
    print(r)
    return r



"""
> Reserve
> Cancel reservation
"""
