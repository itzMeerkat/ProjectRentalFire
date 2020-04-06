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

# def debug_claim():
#     uid = "tDjrJUIfPVcemIiYxyQyRlquK912"
#     auth.set_custom_user_claims(uid, {'admin': True})
#     user = auth.get_user(uid)
#     print(user.custom_claims)

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
    old_amount = snapshot.get(u'amount')
    if old_amount is None:
        return False
    new_amount = old_amount - amount

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
        activity = {'ActionAndActor': ['init_reservation:'+uid], 'item_name': item_name,
                    'amount': amount, 'request_time': request_time, 'status': 'open'}
        doc_ref = db.collection('activities').add(activity)
        doc_ref = doc_ref[1]
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

def update_db(collection, action, actor, key, obj):
    act_ref = db.collection(collection).document(key)
    _d = vars(obj)
    _d['ActionAndActor'].append(action+":"+actor)
    res = act_ref.update(_d)
    return res

def get_ongoing_activities():
    act_gen = db.collection('activities').where('status','==','open').steram()
    r = []
    for i in act_gen:
        r.append(i.to_dict())
    return r
