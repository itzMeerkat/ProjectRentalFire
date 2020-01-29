import routers.infra.databaseapi as db
import time

def log_action(ip, username, action, val):
    db.PutLog({
        'time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'ip':ip,
        'username': username,
        'action': action,
        'value': val
        })
    return