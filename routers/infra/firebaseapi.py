import firebase_admin
from firebase_admin import firestore
from firebase_admin import auth
from routers.infra.exceptions import make_401_exception

app = firebase_admin.initialize_app()
db = firestore.client()

def is_valid_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
    except:
        raise make_401_exception("Can't verify token", "Firebase")
    # print(decoded_token)
    return decoded_token['uid']


@firestore.transactional
def reserve_if_avaliable(transaction, equip_ref, amount):
    snapshot = equip_ref.get(transaction=transaction)
    new_amount = snapshot.get(u'amount') - amount

    if new_amount >= 0:
        transaction.update(equip_ref, {
            u'amount': new_amount
        })
        return True
    else:
        return False

def reserve_item(uid, category, amount, start_time):
    transaction = db.transaction()
    equipment_ref = db.collection(u'equipemtns').document(category)

    result = update_in_transaction(transaction, equipment_ref, amonut)
    if result:
        activity = {'uid':uid, 'equip_category': category, 'amount':amount, 'start_time': start_time}
        doc_ref = db.collection('activities').add(activity)
        print(doc_ref)
        aid = doc_ref[1]['id']
        print(aid)
        return aid
    else:
        return None


def reservation_cancel(aid):
    pass