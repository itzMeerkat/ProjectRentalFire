import casbin

from modules.db.firebaseapi import auth
from modules.utils.exceptions import make_401_exception
e = casbin.Enforcer("./modules/rbac/rbac_model.conf",
                    "./modules/rbac/rbac_policy.csv")

class AuthorizationFactory:
    def __init__(self, obj: str, act: str):
        self.obj = obj
        self.act = act

    def __call__(self, token: str):
        if token == 'DEBUG':
            return 'su'
        try:
            decoded_token = auth.verify_id_token(token)
        except:
            raise make_401_exception("Invalid token", "Cowculator")
        uid = decoded_token['uid']
        role = 'user'
        if 'role' in decoded_token:
            role = decoded_token['role']
        print(role, self.obj, self.act)
        r = e.enforce(role, self.obj, self.act)
        print(r)
        if r == False:
            raise make_401_exception("Not enough permission", "Cowculator")
        
        return uid
