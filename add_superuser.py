import modules.db.firebaseapi as db

u = db.auth.get_user_by_email('pkazhang@ucdavis.edu')
db.auth.set_custom_user_claims(u.uid, {'role': 'superuser'})
