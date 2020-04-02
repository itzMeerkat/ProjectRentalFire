from fastapi import APIRouter
from fastapi import Depends

from time import time

#import routers.infra.databaseapi as db
from modules.schema.data_schema import *

import modules.db.firebaseapi as db
from modules.db.firebaseapi import is_valid_token
router = APIRouter()

@router.get("/fb")
async def read_system_status(uid=Depends(is_valid_token)):
    return {"res": uid}


@router.post("/reservation/create")
async def create_reservation(reservation: ReserveUserRequest, uid=Depends(is_valid_token)):
    res = db.reserve_item(uid, reservation.item_name, reservation.amount, int(time()*1000))
    return res


@router.post("/reservation/cancel")
async def cancel_reservation(request: ReserveUserCancel, uid=Depends(is_valid_token)):
    request.status = 'canceled'
    r = db.update_db('activities', 'reservation_cancel', uid, request.aid, request)
    return {'r': str(r)}


@router.post("/reservation/checkout")
async def checkout_equip(request: ReserveFrontdeskCheckout, uid=Depends(is_valid_token)):
    request.status = 'checked out'
    r = db.update_db('activities','equip_checkout',uid, request.aid, request)
    return {'r': str(r)}


@router.post("/reservation/return")
async def return_equip(request: ReserveFrontdeskReturn, uid=Depends(is_valid_token)):
    request.status = 'closed'
    r = db.update_db('activities','equip_return',uid, request.aid, request)
    return {'r': str(r)}
