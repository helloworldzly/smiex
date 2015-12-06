#-*-coding:utf-8-*-

from api import api
from flask import request, jsonify, make_response
from config.rescode import *

@api.route('/activity/admin/add', methods=['POST'])
def activity_admin_add():
    '''
        添加活动
        参数： title description
        startyear startmonth startday starthour startminute
        endyear endmonth endday endhour endminute
        attendtype(0 or 1)
        (teampeoplenum teamnum if attendtype=1)
        (peoplenum if attendtype=0)
        filter(0 or 1 or 2)
        bstartyear bstartmonth bstartday bstarthour bstartminute
        bendyear bendmonth bendday bendhour bendminute
        fuzeren fuzerenphone
        poster(0 or 1)
        appendproblem(num)
        appendproblemlist
        返回值： SUCCESS activityid / INVALID_OPERATION / PERMISSION_DENIED / PARAMETER_ERROR
        验证参数表是否合法，不合法则返回 INVALID_OPERATION
        将相关信息写入数据库，将活动ID返回
    '''
    #cookies = request.cookies
    #if not 'session' in cookies:
    #    return jsonify(rescode=INVALID_OPERATION)

    #session = cookies['session']

    #from lib import get_username_by_session
    #username = get_username_by_session(session)
    #if username == None:
    #    return jsonify(rescode=INVALID_OPERATION)

    username = 'zengzhaoyang'

    from lib import check_authority
    if check_authority(username, 'addactivity') == False:
        return jsonify(rescode=PERMISSION_DENIED)

    form = request.form
    required = ['title', 'description', 
    'startyear', 'startmonth', 'startday', 'starthour', 'startminute',
    'endyear', 'endmonth', 'endday', 'endhour', 'endminute',
    'attendtype', 'filter',
    'bstartyear', 'bstartmonth', 'bstartday', 'bstarthour', 'bstartminute',
    'bendyear', 'bendmonth', 'bendday', 'bendhour', 'bendminute',
    'fuzeren', 'fuzerenphone', 'poster', 'appendproblem']

    datekey = ['startyear', 'startmonth', 'startday', 'starthour', 'startminute',
    'endyear', 'endmonth', 'endday', 'endhour', 'endminute',
    'bstartyear', 'bstartmonth', 'bstartday', 'bstarthour', 'bstartminute',
    'bendyear', 'bendmonth', 'bendday', 'bendhour', 'bendminute']

    data = {}
    for item in required:
        if not item in form:
            print item
            return jsonify(rescode=PARAMETER_ERROR)
        if not item in datekey:
            data[item] = form[item]

    from lib import check_time_valid

    if check_time_valid(form['startyear'], form['startmonth'], form['startday'], form['starthour'], form['startminute']) == False:
        return jsonify(rescode=PARAMETER_ERROR)
    if check_time_valid(form['endyear'], form['endmonth'], form['endday'], form['endhour'], form['endminute']) == False:
        return jsonify(rescode=PARAMETER_ERROR)
    if check_time_valid(form['bstartyear'], form['bstartmonth'], form['bstartday'], form['bstarthour'], form['bstartminute']) == False:
        return jsonify(rescode=PARAMETER_ERROR)
    if check_time_valid(form['bendyear'], form['bendmonth'], form['bendday'], form['bendhour'], form['bendminute']) == False:
        return jsonify(rescode=PARAMETER_ERROR)

    starttime = '%02d-%02d-%02d %02d:%02d'%(int(form['startyear']), int(form['startmonth']), int(form['startday']), int(form['starthour']), int(form['startminute']))
    endtime = '%02d-%02d-%02d %02d:%02d'%(int(form['endyear']), int(form['endmonth']), int(form['endday']), int(form['endhour']), int(form['endminute']))
    bstarttime = '%02d-%02d-%02d %02d:%02d'%(int(form['bstartyear']), int(form['bstartmonth']), int(form['bstartday']), int(form['bstarthour']), int(form['bstartminute']))
    bendtime = '%02d-%02d-%02d %02d:%02d'%(int(form['bendyear']), int(form['bendmonth']), int(form['bendday']), int(form['bendhour']), int(form['bendminute']))

    data['starttime'] = starttime
    data['endtime'] = endtime
    data['bstarttime'] = bstarttime
    data['bendtime'] = bendtime

    if data['attendtype'] == '1':
        if not 'teampeople' in form or not 'teamnum' in form:
            return jsonify(rescode=PARAMETER_ERROR)
        else:
            data['teampeople'] = int(form['teampeople'])
            data['teamnum'] = int(form['teamnum'])
            data['seat'] = int(form['teamnum'])
    else:
        if not 'peoplenum' in form:
            return jsonify(rescode=PARAMETER_ERROR)
        else:
            data['peoplenum'] = int(form['peoplenum'])
            data['seat'] = int(form['peoplenum'])

    if data['appendproblem'] != '0':
        if not 'appendproblemlist' in form:
            return jsonify(rescode=PARAMETER_ERROR)
        temp_problem_list = form['appendproblemlist']
        temp_problem_list = temp_problem_list.split('###')
        if len(temp_problem_list) != data['appendproblem']:
            return jsonify(rescode=PARAMETER_ERROR)
        data['appendproblemlist'] = temp_problem_list

    if data['poster'] == '1':
        files = request.files
        if not 'file' in files:
            return jsonify(rescode=PARAMETER_ERROR)
        file_data = files['file']

        from lib import save_activity_poster
        file_url = save_activity_poster(file_data)
        data['posterurl'] = file_url

    data['owner'] = username
    from lib import add_activity
    activity_id = add_activity(data)

    return jsonify(rescode=SUCCESS, activityid=activity_id)

@api.route('/activity/admin/edit', methods=['POST'])
def activity_admin_edit():
    '''
        编辑活动
        参数：activityid
        title description
        startyear startmonth startday starthour startminute
        endyear endmonth endday endhour endminute
        attendtype(0 or 1)
        (teampeoplenum teamnum if attendtype=1)
        (peoplenum if attendtype=0)
        filter(0 or 1 or 2)
        bstartyear bstartmonth bstartday bstarthour bstartminute
        bendyear bendmonth bendday bendhour bendminute
        fuzeren fuzerenphone
        poster(0 or 1)
        appendproblem(num)
        appendproblemlist
        中的一项或几项
        返回值： SUCCESS / PARAMETER_ERROR / INVALID_OPERATION / PERMISSION_DENIED 
    '''
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(rescode=INVALID_OPERATION)

    # session = cookies['session']

    # from lib import get_username_by_session
    # username = get_username_by_session(session)

    # if username == None:
        # return jsonify(rescode=INVALID_OPERATION)


    username = 'zengzhaoyang'

    form = request.form
    if not 'activityid' in form:
        return jsonify(rescode=PARAMETER_ERROR)
    activityid = form['activityid']

    from lib import check_activity_changeable
    if check_activity_changeable(activityid, username) == False:
        return jsonify(rescode=PERMISSION_DENIED)

    required = ['title', 'description', 
    'startyear', 'startmonth', 'startday', 'starthour', 'startminute',
    'endyear', 'endmonth', 'endday', 'endhour', 'endminute',
    'attendtype', 'filter',
    'bstartyear', 'bstartmonth', 'bstartday', 'bstarthour', 'bstartminute',
    'bendyear', 'bendmonth', 'bendday', 'bendhour', 'bendminute',
    'fuzeren', 'poster', 'fuzerenphone', 'appendproblem']

    datekey = ['startyear', 'startmonth', 'startday', 'starthour', 'startminute',
    'endyear', 'endmonth', 'endday', 'endhour', 'endminute',
    'bstartyear', 'bstartmonth', 'bstartday', 'bstarthour', 'bstartminute',
    'bendyear', 'bendmonth', 'bendday', 'bendhour', 'bendminute']

    srequired = ['startyear', 'startmonth', 'startday', 'starthour', 'startminute']
    erequired = ['endyear', 'endmonth', 'endday', 'endhour', 'endminute']
    bsrequired = ['bstartyear', 'bstartmonth', 'bstartday', 'bstarthour', 'bstartminute']
    berequired = ['bendyear', 'bendmonth', 'bendday', 'bendhour', 'bendminute']

    scnt = 0
    ecnt = 0
    bscnt = 0
    becnt = 0

    data = {}
    for item in required:
        if item in form:
            if not item in datekey:
                data[item] = form[item]
            if item in srequired:
                scnt += 1
            if item in erequired:
                ecnt += 1
            if item in bsrequired:
                bscnt += 1
            if item in berequired:
                becnt += 1

    if scnt != 0 and scnt != 5:
        return jsonify(rescode=PARAMETER_ERROR)
    if ecnt != 0 and ecnt != 5:
        return jsonify(rescode=PARAMETER_ERROR)
    if bscnt != 0 and bscnt != 5:
        return jsonify(rescode=PARAMETER_ERROR)
    if becnt != 0 and becnt != 5:
        return jsonify(rescode=PARAMETER_ERROR)

    from lib import check_time_valid

    if scnt == 5:
        if check_time_valid(form['startyear'], form['startmonth'], form['startday'], form['starthour'], form['startminute']) == False:
            return jsonify(rescode=PARAMETER_ERROR)
        else:
            starttime = '%02d-%02d-%02d %02d:%02d'%(int(form['startyear']), int(form['startmonth']), int(form['startday']), int(form['starthour']), int(form['startminute']))
            data['starttime'] = starttime
    if ecnt == 5:
        if check_time_valid(form['endyear'], form['endmonth'], form['endday'], form['endhour'], form['endminute']) == False:
            return jsonify(rescode=PARAMETER_ERROR)
        else:
            endtime = '%02d-%02d-%02d %02d:%02d'%(int(form['endyear']), int(form['endmonth']), int(form['endday']), int(form['endhour']), int(form['endminute']))
            data['endtime'] = endtime
    if bscnt == 5:
        if check_time_valid(form['bstartyear'], form['bstartmonth'], form['bstartday'], form['bstarthour'], form['bstartminute']) == False:
            return jsonify(rescode=PARAMETER_ERROR)
        else:
            bstarttime = '%02d-%02d-%02d %02d:%02d'%(int(form['bstartyear']), int(form['bstartmonth']), int(form['bstartday']), int(form['bstarthour']), int(form['bstartminute']))
            data['bstarttime'] = bstarttime
    if becnt == 5:
        if check_time_valid(form['bendyear'], form['bendmonth'], form['bendday'], form['bendhour'], form['bendminute']) == False:
            return jsonify(rescode=PARAMETER_ERROR)
        else:
            bendtime = '%02d-%02d-%02d %02d:%02d'%(int(form['bendyear']), int(form['bendmonth']), int(form['bendday']), int(form['bendhour']), int(form['bendminute']))
            data['bendtime'] = bendtime

    if 'attendtype' in form:
        if form['attendtype'] == '1':
            if not 'teampeople' in form or not 'teamnum' in form:
                return jsonify(rescode=PARAMETER_ERROR)
            data['teampeople'] = int(form['teampeople'])
            data['teamnum'] = int(form['teamnum'])
        else:
            if not 'peoplenum' in form:
                return jsonify(rescode=PARAMETER_ERROR)
            data['peoplenum'] = int(form['peoplenum'])

    if 'poster' in form:
        if form['poster'] == '1':
            files = request.files
            if not 'file' in files:
                return jsonify(rescode=PARAMETER_ERROR)
            file_data = files['file']

            from lib import save_activity_poster
            file_url = save_activity_poster(file_data)
            data['posterurl'] = file_url

    from lib import update_activity
    update_activity(activityid, data)

    return jsonify(rescode=SUCCESS)

@api.route('/activity/admin/delete', methods=['POST'])
def activity_admin_delete():
    '''
        删除活动
        参数： activityid
        返回值： SUCCESS / ACTIVITY_NOT_EXIST / INVALID_OPERATION / PERMISSION_DENIED
        查找activity表，删除活动id对应的活动
    '''
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(rescode=INVALID_OPERATION)

    # session = cookies['session']

    username = 'zengzhaoyang'

    form = request.form
    if not 'activityid' in form:
        return jsonify(rescode=INVALID_OPERATION)

    activityid = form['activityid']

    # from lib import get_username_by_session
    # username = get_username_by_session(session)
    # if username == None:
    #     return jsonify(rescode=INVALID_OPERATION)

    from lib import delete_activity
    res = delete_activity(activityid, username)

    if res == True:
        return jsonify(rescode=SUCCESS)
    else:
        return jsonify(rescode=ACTIVITY_NOT_EXIST)

@api.route('/activity/info/<activityid>', methods=['GET'])
def activity_info(activityid):
    '''
        查询活动信息
        参数： activityid
        返回值： SUCCESS activity / ACTIVITY_NOT_EXIST / INVALID_OPERATION
    '''
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(rescode=INVALID_OPERATION)
    username = 'zengzhaoyang'

    from lib import get_activity_by_id
    res, activity = get_activity_by_id(activityid)
    if res == False:
        return jsonify(rescode=ACTIVITY_NOT_EXIST)
    else:
        return jsonify(rescode=SUCCESS, activity=activity)

@api.route('/activity/list', methods=['GET'])
def activity_list():
    '''
        查询活动列表
        返回值： SUCCESS activitylist / INVALID_OPERATION
    '''
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(rescode=INVALID_OPERATION)
    username = 'zengzhaoyang'

    from lib import get_activity_list
    res = get_activity_list()
    return jsonify(rescode=SUCCESS, activitylist=res)

@api.route('/activity/member/<activityid>', methods=['GET'])
def activity_member(activityid):
    '''
        查询活动报名人员
        参数： activityid
        返回值： SUCCESS / INVALID_OPERATION / ACTIVITY_NOT_EXIST
    '''
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(rescode=INVALID_OPERATION)

    # session = cookies['session']
    # from lib import get_username_by_session
    # username = get_username_by_session(session)
    username = 'zengzhaoyang'

    if username == None:
        return jsonify(rescode=INVALID_OPERATION)

    from lib import get_activity_member_by_id
    res, attend_type, member = get_activity_member_by_id(activityid, username)

    if res == False:
        return jsonify(rescode=ACTIVITY_NOT_EXIST)
    else:
        return jsonify(rescode=SUCCESS, member=member)

@api.route('/activity/signup/person/<activityid>', methods=['POST'])
def activity_signup_person(activityid):
    '''
        报名活动（个人类型）
        参数： activityid
        返回值： SUCCESS / ACTIVITY_NOT_EXIST / SIGNUP_NOT_BEGIN / 
        SIGNUP_IS_END / USER_IS_SIGNUP / SIGNUP_TYPE_ERROR / MEMBER_FULL
        INVALID_OPERATION 
    '''
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(rescode=INVALID_OPERATION)

    # session = cookies['session']

    # from lib import get_username_by_session
    # username = get_username_by_session(session)
    username = 'zzy'

    if username == None:
        return jsonify(rescode=INVALID_OPERATION)

    from lib import signup_person
    res = signup_person(activityid, username)

    if res == 0:
        return jsonify(rescode=SUCCESS)
    elif res == 1:
        return jsonify(rescode=ACTIVITY_NOT_EXIST)
    elif res == 2:
        return jsonify(rescode=SIGNUP_NOT_BEGIN)
    elif res == 3:
        return jsonify(rescode=SIGNUP_IS_END)
    elif res == 4:
        return jsonify(rescode=USER_IS_SIGNUP)
    elif res == 5:
        return jsonify(rescode=SIGNUP_TYPE_ERROR)
    elif res == 6:
        return jsonify(rescode=MEMBER_FULL)

@api.route('/activity/signdown/person/<activityid>', methods=['POST'])
def activity_signdown_person(activityid):
    '''
        取消报名
        参数： activityid
        返回值： SUCCESS / INVALID_OPERATION / USER_NOT_SIGNUP / 
        SIGNDOWN_NOT_BEGIN / SIGNDOWN_IS_END / ACTIVITY_NOT_EXIST / 
        SIGNUP_TYPE_ERROR
    '''
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(rescode=INVALID_OPERATION)

    # session = cookies['session']

    # from lib import get_username_by_session
    # username = get_username_by_session(session)
    username = 'zzy'

    if username == None:
        return jsonify(rescode=INVALID_OPERATION)

    from lib import signdown_person
    res = signdown_person(activityid, username)

    if res == 0:
        return jsonify(rescode=SUCCESS)
    elif res == 1:
        return jsonify(rescode=USER_NOT_SIGNUP)
    elif res == 2:
        return jsonify(rescode=SIGNDOWN_NOT_BEGIN)
    elif res == 3:
        return jsonify(rescode=SIGNDOWN_IS_END)
    elif res == 4:
        return jsonify(rescode=ACTIVITY_NOT_EXIST)
    elif res == 5:
        return jsonify(rescode=SIGNUP_TYPE_ERROR)

@api.route('/activity/signup/team/<activityid>', methods=['POST'])
def activity_signup_team(activityid):
    '''
        报名活动（组队）
        取消报名
        参数： activityid usernum userlist
        返回值： SUCCESS / INVALID_OPERATION / USER_IS_SIGNUP / 
        SIGNUP_NOT_BEGIN / SIGNUP_IS_END / ACTIVITY_NOT_EXIST / 
        SIGNUP_TYPE_ERROR / MEMBER_FULL / MEMBER_NUM_EXIST / PARAMETER_ERROR
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']
    from lib import get_username_by_session
    username = get_username_by_session(session)

    if username == None:
        return jsonify(rescode=INVALID_OPERATION)

    form = request.form
    if not 'usernum' in form or not 'userlist' in form:
        return jsonify(rescode=PARAMETER_ERROR)

    usernum = form['usernum']
    userlist = form['userlist']

    if not username in userlist:
        return jsonify(rescode=INVALID_OPERATION)

    from lib import signup_team
    res = signup_team(activityid, username, usernum, userlist)

    if res == 0:
        return jsonify(rescode=SUCCESS)
    elif res == 1:
        return jsonify(rescode=USER_IS_SIGNUP)
    elif res == 2:
        return jsonify(rescode=SIGNUP_NOT_BEGIN)
    elif res == 3:
        return jsonify(rescode=SIGNUP_IS_END)
    elif res == 4:
        return jsonify(rescode=ACTIVITY_NOT_EXIST)
    elif res == 5:
        return jsonify(rescode=SIGNUP_TYPE_ERROR)
    elif res == 6:
        return jsonify(rescode=MEMBER_FULL)
    elif res == 7:
        return jsonify(rescode=MEMBER_NUM_EXIST)

@api.route('/activity/signdown/team/<activityid>', methods=['POST'])
def activity_signdown_team(activityid):
    '''
        活动整组取消报名
        参数： activityid
        返回值： SUCCESS / INVALID_OPERATION / USER_NOT_SIGNUP /
        SIGNDOWN_NOT_BEGIN / SIGNUP_IS_END / ACTIVITY_NOT_EXIST / 
        SIGNUP_TYPE_ERROR / PERMISSION_DEINED / PARAMETER_ERROR
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    from lib import get_username_by_session
    username = get_username_by_session(session)

    if username == None:
        return jsonify(rescode=INVALID_OPERATION)

    from lib import signdown_team
    res = signdown_team(activityid, username)

    if res == 0:
        return jsonify(rescode=SUCCESS)
    elif res == 1:
        return jsonify(rescode=USER_IS_SIGNUP)
    elif res == 2:
        return jsonify(rescode=SIGNDOWN_NOT_BEGIN)
    elif res == 3:
        return jsonify(rescode=SIGNDOWN_IS_END)
    elif res == 4:
        return jsonify(rescode=ACTIVITY_NOT_EXIST)
    elif res == 5:
        return jsonify(rescode=SIGNUP_TYPE_ERROR)
    elif res == 6:
        return jsonify(rescode=PERMISISION_DEINED)

@api.route('/activity/addperson/team/<activityid>', methods=['POST'])
def activity_addperson_team(activityid):
    '''
        活动组队添加人员
        取消报名
        参数： activityid usernum userlist
        返回值： SUCCESS / INVALID_OPERATION / USER_IS_SIGNUP / 
        SIGNUP_NOT_BEGIN / SIGNUP_IS_END / ACTIVITY_NOT_EXIST / 
        SIGNUP_TYPE_ERROR / MEMBER_NUM_EXIST / PARAMETER_ERROR /
        PERMISISION_DEINED
    '''
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(rescode=INVALID_OPERATION)

    session = cookies['session']

    form = request.form
    if not 'usernum' in form or not 'userlist' in form:
        return jsonify(rescode=INVALID_OPERATION)

    usernum = form['usernum']
    userlist = form['userlist']

    from lib import get_username_by_session
    username = get_username_by_session(session)

    if username == None:
        return jsonify(rescode=INVALID_OPERATION)

    from lib import team_add_member
    res = team_add_member(activityid, username, usernum, userlist)

    if res == 0:
        return jsonify(rescode=SUCCESS)
    elif res == 1:
        return jsonify(rescode=USER_IS_SIGNUP)
    elif res == 2:
        return jsonify(rescode=SIGNUP_NOT_BEGIN)
    elif res == 3:
        return jsonify(rescode=SIGNUP_IS_END)
    elif res == 4:
        return jsonify(rescode=ACTIVITY_NOT_EXIST)
    elif res == 5:
        return jsonify(rescode=SIGNUP_TYPE_ERROR)
    elif res == 6:
        return jsonify(rescode=MEMBER_NUM_EXIST)
    elif res == 7:
        return jsonify(rescode=PERMISSION_DENIED)

@api.route('/activity/deletepserson/team/<activityid>', methods=['POST'])
def activity_deleteperson_team(activityid):
    pass


@api.route('/activity/wechatsignup/<activityid>', methods=['GET'])
def activity_wechatsignup(activityid):
    pass