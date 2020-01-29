from fastapi import APIRouter

import routers.infra.databaseapi as db
from routers.infra.data_schema import *
from routers.infra.auth import *

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Security(get_current_user, scopes=["me"])):
    return current_user


@router.get("/me/items")
async def read_own_items(
    current_user: User = Security(get_current_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/status")
async def read_system_status(user: User = Depends(get_current_user)):
    return {"status": "ok"}
