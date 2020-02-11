import firebase_admin
from firebase_admin import auth
from routers.infra.exceptions import make_401_exception

app = firebase_admin.initialize_app()


def is_valid_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
    except:
        raise make_401_exception("Can't verify token", "Firebase")
    print(decoded_token)
    return decoded_token['uid']
