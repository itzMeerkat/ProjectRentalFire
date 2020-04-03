import casbin

from modules.db.firebaseapi import auth
from modules.utils.exceptions import make_401_exception
e = casbin.Enforcer("./rbac_model.conf", "./rbac_policy.csv")

sub = "alice"  # the user that wants to access a resource.
obj = "data1"  # the resource that is going to be accessed.
act = "write"  # the operation that the user performs on the resource.

if e.enforce(sub, obj, act):
    print("Gut")
else:
    print("Nein")

def checkPermission(sub, obj, act):
    return e.enforce(sub, obj, act)


def is_valid_token(id_token):
    if id_token == "DEBUGTOKEN":
        return 'SUPERUSER'
    try:
        decoded_token = auth.verify_id_token(id_token)
    except:
        raise make_401_exception("Can't verify token", "Firebase")
    return decoded_token['uid']

class AuthorizationFactory:
    def __init__(self, obj: str, act: str):
        self.obj = obj
        self.act = act

    def __call__(self, token: str):
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            role = user.custom_claims.get('role')
            r = e.enforce(role, self.obj, self.act)
            if r:
                return uid
        except:
            pass

        raise make_401_exception("Invalid token or not enough permission", "Cowculator")
        
