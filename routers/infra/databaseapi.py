import pymongo

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo_client['RateAnything']

def GetUser(key):
    tar_user = db['Users'].find_one(key)
    # print(key, tar_user)
    return tar_user

def PutUser(val):
    # print(val)
    ins = db['Users'].insert_one(val)
    return ins.acknowledged

def PutLog(val):
    ins = db['Log'].insert_one(val)
    return ins.acknowledged

def GetLog(lim=10):
    qres = db['Log'].find({},{'_id':0})
    return list(qres)