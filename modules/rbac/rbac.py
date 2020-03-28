import casbin
e = casbin.Enforcer("./rbac_model.conf", "./rbac_policy.csv")

sub = "alice"  # the user that wants to access a resource.
obj = "data1"  # the resource that is going to be accessed.
act = "write"  # the operation that the user performs on the resource.

if e.enforce(sub, obj, act):
    print("Gut")
else:
    print("Nein")

def checkPermission(sub, obj, act):
    return e.enforce(sub, obj, act)