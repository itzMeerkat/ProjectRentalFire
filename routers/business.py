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
async def reservation_cancel(request: ReserveUserCancel, uid=Depends(AuthorizationFactory('activity', 'cancel'))):
    ctnt = {'reason': request.reason, 'status': 'canceled'}
    r = db.reservation_cancel(uid, request.aid, ctnt)
    return {'r': str(r)}


@router.post("/reservation/checkout")
async def reservation_checkout(request: ReserveFrontdeskCheckout, uid=Depends(AuthorizationFactory('activity', 'checkout'))):
    ctnt = {'item_ids':request.item_ids, 'status': 'checked out'}
    r = db.reservation_checkout(uid, request.aid, ctnt)
    return {'r': str(r)}


@router.post("/reservation/return")
async def reservation_return(request: ReserveFrontdeskReturn, uid=Depends(AuthorizationFactory('activity', 'return'))):
    ctnt = {'note': request.note, 'status': 'closed'}
    r = db.reservation_return(uid, request.aid, ctnt)
    return {'r': str(r)}
