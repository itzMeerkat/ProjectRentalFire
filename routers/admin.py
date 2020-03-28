from fastapi import APIRouter
import modules.db.firebaseapi as db

router = APIRouter()

@router.get('/logs')
async def get_logs():
    r = db.GetLog()
    # print(r[0])
    return {'data': r}
