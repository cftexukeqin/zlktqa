from functools import wraps
from flask import session,redirect,url_for
# 登陆限制的装饰器
def login_required(func):
    @wraps(func)
    def warpper(*args,**kwargs):
        if session.get('user_id'):
            return  func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return warpper