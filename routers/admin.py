from fastapi import APIRouter, Depends
import modules.db.firebaseapi as db

from modules.schema.data_schema import ChangeUserRole
from modules.rbac.rbac import AuthorizationFactory
router = APIRouter()

@router.post('/newfrontdesk')
async def set_frontdesk(request: ChangeUserRole, uid=Depends(AuthorizationFactory('user_claims', 'modify'))):
    user_ref = db.auth.get_user_by_email(request.user_email)
    db.auth.set_custom_user_claims(user_ref.uid, {'role': request.new_role})
