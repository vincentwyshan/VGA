#coding=utf8


import sqlite3

db = sqlite3.connect('user.db')

try:
    db.execute("""create table user (email, name) """)
except:
    pass

try:
    db.execute(""" create table sina (email, request_token, request_secret,
                  access_token, access_secret) """)
except:
    pass

try:
    db.execute(""" create table weather (email, recently_send date, city) """)
except:
    pass

import basis
log = basis.getlogger(__name__)

def add(email, name=None):
    '''
    >>> id = add('vincent.wyshan@gmail.com', 'Vincent')
    >>> cursor = db.cursor()
    >>> abandon = cursor.execute("select count(0) from user where email = 'vincent.wyshan@gmail.com'")
    >>> cursor.fetchone()[0]
    1
    '''
    if name == None:
        name = email.split('@')[0]
    cursor = db.cursor()
    cursor.execute("select rowid from user where email = ?", (email,))
    rowid = cursor.fetchone()
    if rowid:
        return rowid[0]
    cursor.execute("insert into user(email, name) values(?,?)", (email, name))
    return cursor.lastrowid


def delete(email):
    pass


def update(email, **kwarg):
    '''
    >>> update('vincent.wyshan@gmail.com', name='vincent.wen', request_token='')
    >>> cursor = db.cursor()
    >>> abandon = cursor.execute("select name, request_token from user where email = 'vincent.wyshan@gmail.com'")
    >>> row = cursor.fetchone()
    >>> row[0] == 'vincent.wen'
    True
    >>> row[1] == ''
    True
    '''
    sql = "update user set "
    paras = []
    values = []
    for k,v in kwarg.items():
        paras.append('%s=?' % k)
        values.append(v)
    sql += ','.join(paras)
    sql += ' where email=?'
    values.append(email)
    db.execute(sql, tuple(values))
    db.commit()

def _exists(app, email):
    cursor = db.cursor()
    cursor.execute("select count(0) from user where email = ?", (email,))
    if cursor.fetchone()[0] == 0:
        raise Exception("User is not exists")
    cursor.execute("select count(0) from %s where email = ?" % app.lower(), (email,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("insert into %s (email) values(?)" % app.lower(), (email,))
    return

def update_app(app, email, **kwarg):
    '''
    >>> update_app('sina', 'vincent.wyshan@gmail.com', request_token='test-token')
    >>> info = get_app('sina', 'vincent.wyshan@gmail.com')
    >>> print info.get('request_token')
    test-token
    '''
    log.debug('check...')
    _exists(app, email)
    sql = "update %s set " % app.lower()
    paras = []
    values = []
    for k,v in kwarg.items():
        paras.append('%s=?' % k)
        values.append(v)
    sql += ','.join(paras)
    sql += ' where email=?'
    log.debug(sql)
    values.append(email)
    log.debug(values)
    db.execute(sql, tuple(values))
    db.commit()

def get(email):
    '''
    >>> update('vincent.wyshan@gmail.com', name='vincent.wen')
    >>> get('vincent.wyshan@gmail.com')['name']
    u'vincent.wen'
    '''
    sql = "select * from user where email = ?"
    cursor = db.cursor()
    cursor.execute(sql, (email,))
    columns = [c[0] for c in cursor.description]
    result = dict()
    data = cursor.fetchone()
    for i in range(len(cursor.description)):
        result[cursor.description[i][0]] = data[i]
    return result

def get_app(app, email):
    _exists(app, email)
    sql = "select * from %s where email = ?" % app.lower()
    cursor = db.cursor()
    cursor.execute(sql, (email,))
    columns = [c[0] for c in cursor.description]
    result = dict()
    data = cursor.fetchone()
    for i in range(len(cursor.description)):
        result[cursor.description[i][0]] = data[i]
    return result

def delete_app(app, email):
    sql = "delete from %s where email = ?" % app.lower()
    db.execute(sql, (email,))
    db.commit()
    return True
