from fastapi import APIRouter
from fastapi import Depends

#import routers.infra.databaseapi as db
from routers.infra.data_schema import *

from routers.infra.firebaseapi import is_valid_token


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


def checkInventory(r):
    return True

@router.post("/reserve", response_model=RequestResponse)
async def reserve(reservation: ActionReserve, uid = Depends(is_valid_token)):
    if checkInventory(reservation):
        return RequestResponse(1)
    return RequestResponse(0)



"""
> Reserve
> Cancel reservation
"""