#-*-coding:utf-8-*-

def check_username_exist(session, username):
    '''
        检查用户名是否存在
        从temp_user和user表中查看记录是否存在
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    temp_user = db.temp_user

    one = temp_user.find_one({'username':username})
    if one != None:
        if one['session'] == session:
            return False
        return True

    user = db.user
    one = user.find_one({'username':username})
    if one != None:
        return True
    return False

def add_temp_user(session, username, password):
    '''
        添加临时用户
        将临时用户username和password与session绑定，添加时间戳
        插入temp_user表中
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    temp_user = db.temp_user

    import time
    temp_user.remove({'session':session})
    temp_user.insert({
        'username':username,
        'password':password,
        'session':session,
        'createtime':time.time()
        })

def check_email_exist(session, email):
    '''
        检查邮箱是否存在
        从temp_user和user表中查看记录是否存在
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    temp_user = db.temp_user

    one = temp_user.find_one({'email':email})
    if one != None:
        if one['session'] == session:
            return False
        return True

    user = db.user
    one = user.find_one({'email':email})
    if one != None:
        return True
    return False

def update_temp_user_email(session, email):
    '''
        根据session更新email
        生成随机验证码，向邮箱发送验证码
        从temp_user中查找session记录，将email code 以及errtry=0 pass=0添加至其中
    '''

    from model.mongodb import MongoDB
    db = MongoDB().db
    temp_user = db.temp_user

    one = temp_user.find_one({'session':session})
    if one == None:
        return False

    from lib import generate_verify_code
    code = generate_verify_code()

    email_data = {
        'fromuser':'X团队<gooooo@love-sysu.com>',
        'touser':email,
        'subject':'X网站注册邮件验证码',
        'message':'你好，您的邮件验证码是%s，20分钟内输入有效'%code
    }

    from lib import send_email
    send_email(email_data)

    import time
    temp_user.update({'session':session},{'$set':{'email':email,'code':code,'errtry':0,'pass':0,'createtime':time.time()}})
    return True

def check_studentid_occupy(session, studnetid):
    '''
        检查学号是否已被使用
        从temp_user和user表中查看记录是否存在
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    temp_user = db.temp_user

    one = temp_user.find_one({'studnetid':studnetid})
    if one != None:
        if one['session'] == session:
            return False
        return True

    user = db.user
    one = user.find_one({'studnetid':studnetid})
    if one != None:
        return True
    return False

def check_name_studentid_match(name, studentid):
    '''
        检查姓名和学号是否匹配
        从ident表中查看记录是否存在
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    ident = db.ident

    one = ident.find_one({'name':name,'studentid':studentid})
    if one == None:
        return False
    return True

def update_temp_user_name(session, name, studnetid):
    '''
        根据session更新查找temp_user里的记录
        将username password email name studentid插入user表
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    temp_user = db.temp_user
    user = db.user

    one = temp_user.find_one({'session':session})
    if one == None:
        return False

    if not 'username' in one or not'password' in one or not 'email' in one:
        return False

    username = one['username']
    password = one['password']
    email = one['email']

    import time
    user.remove({'username':username})
    user.insert({
        'username':username,
        'password':password,
        'email':email,
        'name':name,
        'studnetid':studnetid,
        'registertime':time.time(),
        'usertype':'student',
        'authority':1
        })

    return True

def check_verify_code(session, email, verifycode):
    '''
        根据session更新temp_user里的记录
        检查记录中验证码的值与verifycode是否匹配
        若匹配则返回 0，更新pass
        若不匹配，次数加一，返回 1
        若次数达到三次，返回 2
        错操作错误，返回4
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    temp_user = db.temp_user

    one = temp_user.find_one({'session':session,'email':email})
    if one == None:
        return 4

    if not 'code' in one:
        return 4

    if not 'pass' in one:
        return 4

    # if one['pass'] == 1:
    #     return 4

    real_verifycode = one['code']
    if real_verifycode == verifycode:
        temp_user.update({'session':session,'email':email},{'$set':{'pass':1}})
        return 0

    else:
        cnt = one['errtry']
        if cnt == 3:
            return 4
        cnt += 1
        temp_user.update({'session':session,'email':email},{'$set':{'errtry':cnt}})
        if cnt == 3:
            return 2
        else:
            return 1

def resend_verify_code(session, email):
    '''
        根据session查找temp_user里的记录
        检查记录中上次create时间与当前时间差是否超过一分钟
        重新发送验证码邮件
        更新创建时间和验证码
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    temp_user = db.temp_user

    one = temp_user.find_one({'session':session,'email':email})
    if one == None:
        return False

    if not 'pass' in one:
        return False

    if one['pass'] == 1:
        return False

    old_createtime = one['createtime']

    import time
    now_time = time.time()

    if now_time - old_createtime < 60:
        return False

    from lib import generate_verify_code
    code = generate_verify_code()

    email_data = {
        'fromuser':'X团队<gooooo@love-sysu.com>',
        'touser':email,
        'subject':'X网站注册邮件验证码',
        'message':'你好，您的邮件验证码是%s，20分钟内输入有效'%code
    }

    from lib import send_email
    send_email(email_data)

    temp_user.update({'session':session,'email':email},{'$set':{'code':code,'errtry':0,'pass':0,'createtime':now_time}})
    return True

def register_db_reset(session):
    '''
        删除temp_user表中session的记录
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    temp_user = db.temp_user

    temp_user.remove({'session':session})

def user_auth(session, username, password, remember):
    '''
        验证username和password是否匹配，若是则将sessoin与username关联
        若remember为1，则将session放入redis中的记住登录表中
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    user = db.user

    one = user.find_one({'username':username,'password':password})
    if one == None:
        return False

    from model.redisdb import RedisDB
    con = RedisDB().con
    key = 'session2username:'+session
    con.set(key, username)
    con.expire(key, 3600)

    return True

def get_username_by_session(session):
    '''
        根据session获得用户名
    '''
    from model.redisdb import RedisDB
    con = RedisDB().con
    key = 'session2username:'+session
    value = con.get(key)

    if value != None:
        con.expire(key, 3600)

    return value

def remove_session(session):
    '''
        删除session
    '''
    from model.redisdb import RedisDB
    con = RedisDB().con
    key = 'session2username:'+session
    con.delete(key)

def testtest():
    from lib import generate_verify_code
    code = generate_verify_code()
    print code

