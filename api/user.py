#-*-coding:utf-8-*-

from api import api
from flask import request, jsonify, make_response
from config.rescode import *

@api.route('/register/step1', methods=['POST'])
def register_step1():
    '''
        用户注册STEP1
        参数: 用户名 密码
        返回值: SUCCESS / USERNAME_EXIST / INVALID_OPERATION

        对form参数进行检查，若不存在 'username' 或 'password' 则返回 INVALID_OPERATION
        对用户名进行判重，若用户名已存在，则返回 USER_NAME_EXIST
        对密码进行检查，若密码长度小于6位，则返回 INVALID_OPERATION
        将session username password插入temp_user数据库中
        返回SUCCESS
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']

    form = request.form
    if not 'username' in form or not 'password' in form:
        return jsonify(rescode=INVALID_OPERATION)

    username = form['username']
    password = form['password']

    from lib import check_username_exist
    if check_username_exist(session, username) == True:
        return jsonify(rescode=USERNAME_EXIST)

    if len(password) < 6:
        return jsonify(rescode=INVALID_OPERATION)

    import hashlib
    password = hashlib.md5(password).hexdigest()

    from lib import add_temp_user
    add_temp_user(session, username, password)

    return jsonify(rescode=SUCCESS)

@api.route('/register/step2', methods=['POST'])
def register_step2():
    '''
        用户注册STEP2
        参数: 邮箱
        返回值: SUCCESS / INVALID_OPERATION

        对form参数进行检查，若不存在 'email' 则返回 INVALID_OPERATION
        对邮箱进行判重，若用户名已存在，则返回 EMAIL_EXIST
        更新temp_user中session对应的记录，同时发送邮件验证码
        返回SUCCESS
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']

    form = request.form
    if not 'email' in form:
        return jsonify(rescode=INVALID_OPERATION)

    email = form['email']

    from lib import check_email_exist
    if check_email_exist(session, email) == True:
        return jsonify(rescode=EMAIL_EXIST)

    from lib import update_temp_user_email
    
    if update_temp_user_email(session, email) == False:
        return jsonify(rescode=INVALID_OPERATION)

    return jsonify(rescode=SUCCESS)

@api.route('/register/step2/verify', methods=['POST'])
def register_step2_verify():
    '''
        用户注册STEP2 确认验证码
        参数: 邮箱 验证码
        返回值: SUCCESS / INVALID_OPERATION / VERIFY_CODE_ERROR / THREE_TIME_ERROR

        对form参数进行检查，若不存在 'email' 和 'verifycode' 则返回 INVALID_OPERATION
        对邮箱和verifycode进行匹配，若不匹配则返回 VERIFY_CODE_ERROR，同时错误次数加一
        若错误次数达到三次，则返回 THREE_TIME_ERROR，删除当前临时验证码
        返回SUCCESS
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']

    form = request.form
    if not 'email' in form or not 'verifycode' in form:
        return jsonify(rescode=INVALID_OPERATION)

    email = form['email']
    verifycode = form['verifycode']

    from lib import check_verify_code
    res = check_verify_code(session, email, verifycode)

    if res == 4:
        return jsonify(rescode=INVALID_OPERATION)
    elif res == 2:
        return jsonify(rescode=THREE_TIME_ERROR)
    elif res == 1:
        return jsonify(rescode=VERIFY_CODE_ERROR)
    else:
        return jsonify(rescode=SUCCESS)

@api.route('/register/step2/resend', methods=['POST'])
def register_step2_resend():
    '''
        用户注册STEP2 重发邮件
        参数: 邮箱
        返回值: SUCCESS / INVALID_OPERATION

        对form参数进行检查，若不存在 'email' 则返回 INVALID_OPERATION
        对邮箱上次验证码创造时间进行判断，若与当前时间间隔少于一分钟，则返回 INVALID_OPERATION
        重新生成验证码，发送邮件
        返回SUCCESS
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']

    form = request.form
    if not 'email' in form:
        return jsonify(rescode=INVALID_OPERATION)

    email = form['email']

    from lib import resend_verify_code
    res = resend_verify_code(session, email)
    if res == False:
        return jsonify(rescode=INVALID_OPERATION)

    return jsonify(rescode=SUCCESS)

@api.route('/register/step3', methods=['POST'])
def register_step3():
    '''
        用户注册STEP3
        参数: 姓名 学号
        返回值: SUCCESS / NAME_STUDENTID_NOT_MATCH / INVALID_OPERATION / STUDENTID_OCCUPY

        对form参数进行检查，若不存在 'name' 和 'studentid' 则返回 INVALID_OPERATION
        对姓名和学号进行匹配检查，若学号已被使用，则返回 STUDENTID_OCCUPY
        若姓名和学号不匹配，则返回 NAME_STUDENTID_NOT_MATCH
        找到temp_user中session对应的记录值，将姓名、学号、用户名、密码和邮箱插入user表
        返回SUCCESS
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']

    form = request.form
    if not 'name' in form or not 'studentid' in form:
        return jsonify(rescode=INVALID_OPERATION)

    name = form['name']
    studentid = form['studentid']

    from lib import check_studentid_occupy

    if check_studentid_occupy(session, studentid) == True:
        return jsonify(rescode=STUDENTID_OCCUPY)

    from lib import check_name_studentid_match
    if check_name_studentid_match(name, studentid) == False:
        return jsonify(rescode=NAME_STUDENTID_NOT_MATCH)

    from lib import update_temp_user_name
    if update_temp_user_name(session, name, studentid) == False:
        return jsonify(rescode=INVALID_OPERATION)

    return jsonify(rescode=SUCCESS)

@api.route('/register/step4', methods=['GET'])
def register_setp4():
    '''
        用户注册STEP4 微信绑定
        参数: session
    '''
    return 'hello'

@api.route('/register/reset', methods=['GET'])
def register_reset():
    '''
        注册重置
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']

    from lib import register_db_reset
    register_db_reset(session)

    return jsonify(rescode=SUCCESS)

@api.route('/login', methods=['POST'])
def login():
    '''
        登录
        参数：用户名 密码 是否记住
        返回值： SUCCESS / USR_OR_PWD_ERROR / INVALID_OPERATION

        对form参数进行检查，若不存在 username password remember 则返回 INVALID_OPERATION
        检查username password是否匹配，若匹配，则将session与用户名作关联，返回SUCCESS
        若不匹配则返回 USR_OR_PWD_ERROR
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']

    form = request.form
    if not 'username' in form or not 'password' in form or not 'remember' in form:
        return jsonify(rescode=INVALID_OPERATION)

    username = form['username']
    password = form['password']
    remember = form['remember']

    import hashlib
    password = hashlib.md5(password).hexdigest()

    from lib import user_auth
    if user_auth(session, username, password, remember) == True:
        return jsonify(rescode=SUCCESS)
    else:
        return jsonify(rescode=USR_OR_PWD_ERROR)

@api.route('/logout', methods=['GET'])
def logout():
    '''
        注销
        删除cookie，返回SUCCESS
    '''
    cookies = request.cookies
    if 'session' in cookies:
        session = cookies['session']
        from lib import remove_session
        remove_session(session)
        resp = make_response(jsonify(rescode=SUCCESS))
        resp.delete_cookie('session')
        return resp
    else:
        return jsonify(rescode=SUCCESS)

@api.route('/getprofile', methods=['GET'])
def getprofile():
    '''
        获取用户资料
        从cookies获取session，根据session获取username
        根据username获得用户资料
        返回值：SUCCESS，data / INVALID_OPERATION / SESSION_TIMEOUT
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']
    from lib import get_username_by_session
    username = get_username_by_session(session)

    if username == None:
        return jsonify(rescode=SESSION_TIMEOUT)

    from lib import get_profile_by_username
    profile = get_profile_by_username()
    return jsonify(rescode=SUCCESS, profile=profile)

