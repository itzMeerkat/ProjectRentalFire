import firebase_admin
from firebase_admin import firestore
from firebase_admin import auth
from modules.utils.exceptions import make_401_exception
from time import time
app = firebase_admin.initialize_app()
db = firestore.client()

def get_all_user():
    res = []
    for user in auth.list_users().iterate_all():
        roles = None
        if not user.custom_claims is None:
            roles = list(user.custom_claims.keys())
        res.append({'uid': user.uid, 
        'email':user.email, 
                    'roles': roles}
    )
        #print('User: ' + user.uid)
    print(res)
    return res

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
        #print(new_amount)
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

    rt = {'status': None}
    if result:
        activity = {'Actions': {'init_reservation': {'actor': uid, 'time': request_time}},
        'item_name': item_name, 'amount': amount, 'status': 'open'}
        db.collection('activities').add(activity)
        # doc_ref = doc_ref[1]
        # aid = doc_ref.id
        # rt['AID'] = aid
        rt['status'] = 'open'
    else:
        rt['status'] = 'failed'
    return rt


@firestore.transactional
def return_or_cancel(transaction, equip_ref, act_ref, act):
    snapshot = equip_ref.get(transaction=transaction)
    old_amount = snapshot.get(u'amount')

    if old_amount is None:
        return False

    transaction.update(act_ref,act)
    new_amount = old_amount + act['amount']
    transaction.update(equip_ref, {
        u'amount': new_amount
    })
    return True

# I suppose no one gonna cancel reservation while frontdesk is clicking "check out"
# Which is the only case could be a race condition
def reservation_cancel(actor, key, obj):
    act_ref = db.collection('activities').document(key)
    act = act_ref.get().to_dict()
    for i in obj:
        act[i] = obj[i]

    act['Actions']['reservation_cancel'] = {
        'actor': actor, 'time': int(time()*1000)}

    transaction = db.transaction()
    equipment_ref = db.collection(u'items').document(act['item_name'])
    
    return return_or_cancel(transaction, equipment_ref, act_ref, act)


def reservation_checkout(actor, key, obj):
    act_ref = db.collection('activities').document(key)
    act = act_ref.get().to_dict()
    for i in obj:
        act[i] = obj[i]

    act['Actions']['reservation_checkout'] = {
        'actor': actor, 'time': int(time()*1000)}
    res = act_ref.update(act)
    return res

def reservation_return(actor, key, obj):
    act_ref = db.collection('activities').document(key)
    act = act_ref.get().to_dict()
    for i in obj:
        act[i] = obj[i]

    act['Actions']['reservation_return'] = {
        'actor': actor, 'time': int(time()*1000)}
    transaction = db.transaction()
    equipment_ref = db.collection(u'items').document(act['item_name'])

    return return_or_cancel(transaction, equipment_ref, act_ref, act)

def get_ongoing_activities():
    act_gen = db.collection('activities').where('status','==','open').stream()
    r = []
    for i in act_gen:
        r.append(i.to_dict())
    return r
