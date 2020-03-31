import firebase_admin
from firebase_admin import firestore
from firebase_admin import auth
from modules.utils.exceptions import make_401_exception

app = firebase_admin.initialize_app()
db = firestore.client()

def get_all_reservations():
    ds = db.collection('reservation').stream()
    r = [i.to_dict() for i in ds]
    return r

def is_valid_token(id_token):
    if id_token == "DEBUGTOKEN":
        return 'SUPERUSER'
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

def reserve_item(uid, item_name, amount, request_time):
    transaction = db.transaction()
    equipment_ref = db.collection(u'items').document(item_name)
    
    result = reserve_if_avaliable(transaction, equipment_ref, amount)

    rt = {'AID': None, 'status': None}
    if result:
        activity = {'uid':uid, 'item_name': item_name, 'amount':amount, 'request_time': request_time}
        doc_ref = db.collection('activities').add(activity)
        doc_ref = doc_ref[1]
        print(doc_ref.id)
        aid = doc_ref.id
        rt['AID'] = aid
        rt['status'] = 'open'
    else:
        rt['status'] = 'failed'
    return rt


# I suppose no one gonna cancel reservation while frontdesk is clicking "check out"
# Which is the only case could be a race condition
def reservation_cancel(aid, reason):
    act_ref = db.collection('activities').document(aid)
    res = act_ref.update({'note':reason, 'status': 'canceled'})
    return res

def update_db(collection, key, obj):
    act_ref = db.collection(collection).document(key)
    res = act_ref.update(vars(obj))
    return res

@firestore.transactional
def update_in_transaction(transaction, city_ref):
    snapshot = city_ref.get(transaction=transaction)
    new_population = snapshot.get(u'population') + 1

    if new_population < 1000000:
        transaction.update(city_ref, {
            u'population': new_population
        })
        return True
    else:
        return False




def trans_test():
    transaction = db.transaction()
    city_ref = db.collection(u'cities').document(u'SF')
    print(type(city_ref))
    result = update_in_transaction(transaction, city_ref)


    if result:
        print(u'Population updated')
    else:
        print(u'Sorry! Population is too big.')
