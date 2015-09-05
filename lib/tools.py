#-*-coding:utf-8-*-

def generate_session():
    '''
        随机生成16位session
    '''
    import os
    from model.redisdb import RedisDB
    con = RedisDB().con
    code = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
    while True:
        if con.sismember('session',code) == False:
            con.sadd('session',code)
            break
        code = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
    return code

    

def generate_verify_code():
    '''
        随机生成6位验证码
    '''
    from random import randint
    code = ''
    for i in range(6):
        while True:
            num = randint(0,9)
            if i != 0 and code[i-1] == str(num):
                continue
            code += str(num)
            break
    return code

def send_email(email_data):
    '''
        暂时先用182.92.104.30
        等服务器弄好了，再自己搭建postfix服务器
    '''
    print email_data
    return 'haha'
    url = 'http://182.92.104.30/mail'
    res = requests.post(url, data=email_data)

def check_authority(username, authority_name):
    '''
        检查用户是否拥有相关权限，返回True或False
        角色权限表：
        student         1   attendactivity
        organization    2   addactivity
        teacher         3   addactivity
        root            4   all
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    user = db.user

    one = user.find_one({'username':username})
    if one == None:
        return False

    authority = one['authority']
    if authority == 4:
        return True
    if authority == 3 and authority_name == 'addactivity':
        return True
    if authority == 2 and authority_name == 'addactivity':
        return True
    if authority == 1 and authority_name == 'attendactivity':
        return True

    return False

def generate_qr_code():
    pass

def check_time_valid(year, month, day, hour, minute):
    '''
        检查时间是否合法，返回True或False
    '''
    from datetime import date
    try:
        date(year, month, day)
    except:
        return False
    if hour < 0 or hour > 23:
        return False
    if minute < 0 or minute > 59:
        return False
    return True