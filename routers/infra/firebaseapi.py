import firebase_admin
from firebase_admin import auth

app = firebase_admin.initialize_app()


def is_valid_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
    except:
        return "FAIL"
    print(decoded_token)
    return decoded_token['uid']
