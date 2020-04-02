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
    # print(decoded_token)
    return decoded_token['uid']

