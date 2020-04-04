from fastapi import APIRouter
from fastapi import Depends

from time import time

from modules.schema.data_schema import *

import modules.db.firebaseapi as db
from modules.rbac.rbac import AuthorizationFactory

router = APIRouter()

# @router.get("/fb")
# async def read_system_status(uid=Depends(AuthorizationFactory('debug','do'))):
#     user = db.auth.get_user(uid)
#     return {"u r": user.custom_claims}


@router.post("/reservation/create")
async def create_reservation(reservation: ReserveUserRequest,
                            uid=Depends(AuthorizationFactory('activity', 'create'))):
    res = db.reserve_item(uid, reservation.item_name, reservation.amount, int(time()*1000))
    return res


@router.post("/reservation/cancel")
async def cancel_reservation(request: ReserveUserCancel, uid=Depends(AuthorizationFactory('activity', 'cancel'))):
    request.status = 'canceled'
    r = db.update_db('activities', 'reservation_cancel', uid, request.aid, request)
    return {'r': str(r)}


@router.post("/reservation/checkout")
async def checkout_equip(request: ReserveFrontdeskCheckout, uid=Depends(AuthorizationFactory('activity','checkout'))):
    request.status = 'checked out'
    r = db.update_db('activities','equip_checkout',uid, request.aid, request)
    return {'r': str(r)}


@router.post("/reservation/return")
async def return_equip(request: ReserveFrontdeskReturn, uid=Depends(AuthorizationFactory('activity', 'return'))):
    request.status = 'closed'
    r = db.update_db('activities','equip_return',uid, request.aid, request)
    return {'r': str(r)}
