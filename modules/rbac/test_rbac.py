import casbin
e = casbin.Enforcer("./rbac_model.conf", "./rbac_policy.csv")

tests = [
    ('frontdesk', 'activity', 'return', True),
    ('frontdesk', 'activity', 'checkout', True),
    ('frontdesk', 'activity', 'create', True),
    ('frontdesk', 'activity', 'cancel', True),

    ('admin', 'activity', 'return', True),
    ('admin', 'activity', 'checkout', True),
    ('admin', 'activity', 'create', True),
    ('admin', 'activity', 'cancel', True),

    ('user', 'activity', 'return', False),
    ('user', 'activity', 'checkout', False),
    ('user', 'activity', 'create', True),
    ('user', 'activity', 'cancel', True),

    ('user', 'user_claims', 'modify', False),
    ('admin', 'user_claims', 'modify', True),
    ('frontdesk', 'user_claims', 'modify', False),
]

for c in tests:
    correct_r = c[3]
    r = e.enforce(c[0],c[1],c[2])
    if correct_r != r:
        print('Error at case:', c,'Return:',r)

print('Test pass!')