from fastapi import APIRouter

router = APIRouter()

@router.get('/logs')
async def get_logs():
    r = db.GetLog()
    # print(r[0])
    return {'data': r}
