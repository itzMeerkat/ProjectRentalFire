from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException

def make_401_exception(d, val):
    return HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=d,
        headers={"WWW-Authenticate": val},
    )