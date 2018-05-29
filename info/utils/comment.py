import functools
from flask import session,current_app,g
from info.models import User

def do_rank(index):
    if index==1:
       return 'first'
    elif index == 2:
       return 'second'
    elif index == 3:
       return 'third'
    else:
        return ''

def user_login_data(f):
    @functools.wraps(f)
    def wapper(*args,**kwargs):
        user_id = session.get("user_id")

        user = User.query.get(user_id)

        g.user = user
        return f(*args,**kwargs)
    return wapper