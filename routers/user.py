from fastapi import APIRouter

from starlette.requests import Request

from datetime import timedelta

#from routers.infra.auth import *
# from routers.infra.middleware import log_action
from routers.infra.exceptions import make_401_exception

router = APIRouter()

@router.post("/signup")
async def user_signup(user: UserFull, request: Request):
    log_action(request.client.host, user.username, "Sign Up", None)

    user.hashed_password = get_password_hash(user.hashed_password)
    db.PutUser(vars(user))
    return 200
