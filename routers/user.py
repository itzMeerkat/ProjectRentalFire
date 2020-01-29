from fastapi import APIRouter

from starlette.requests import Request

from datetime import timedelta

from routers.infra.auth import *
from routers.infra.middleware import log_action
from routers.infra.exceptions import make_401_exception

import routers.infra.databaseapi as db

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, form_data.scopes)
    if not user:
        raise make_401_exception("Incorrect username or password or requesting invalid permission", "Bearer")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup")
async def user_signup(user: UserFull, request: Request):
    log_action(request.client.host, user.username, "Sign Up", None)

    user.hashed_password = get_password_hash(user.hashed_password)
    db.PutUser(vars(user))
    return 200