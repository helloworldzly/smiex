#-*-coding:utf-8-*-

def add_activity(data):
    '''
        添加活动，返回活动id
        TODO: 改进活动id生成方式
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    activity_member = db.activity_member
    one = activity.find_one({'record':'latest_id'})
    if one == None:
        latest_id = 10000
        activity.insert({'record':'latest_id','latestid':10001})
    else:
        latest_id = one['latestid']
        activity.update({'record':'latest_id'},{'$set':{'latestid':latest_id+1}})

    now_id = latest_id + 1
    activity.insert({'activitydata':data,'activityid':str(now_id)})
    attendtype = data['attendtype']
    if attendtype == 0:
        activity_member.insert({
            'activityid':str(now_id),
            'member':[],
            'attendtype':attendtype,
            'teampeople':data['teampeople'],
            'teamnum':data['teamnum']}
        )
    else:
        activity_member.insert({
            'activityid':str(now_id),
            'member':[],
            'attendtype':attendtype,
            'peoplenum':data['peoplenum']}
        )
    return str(now_id)

def delete_activity(activityid, username):
    '''
        检查活动owner是否是username，是则删除活动，返回True或False
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    activity_member = db.activity_member
    one = activity.find_one({'activityid':activityid})

    if one == None:
        return False

    if one['activitydata']['owner'] != username:
        return False

    activity.remove({'activityid':activityid})
    activity_member.remove({'activityid':activityid})
    return True

def update_activity(activityid, data):
    '''
        更新活动信息
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    update_data = {}
    for item in data:
        update_data['activitydata.' + item] = data[item]
    activity.update({'activityid':activityid}, {'$set':update_data})

def get_activity_by_id(activityid):
    '''
        根据活动id查询activity表，获得活动信息
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    one = activity.find_one({'activityid':activityid})

    if one == None:
        return False, {}

    data = {}
    for item in one:
        if item != '_id':
            data[item] = one[item]
    print data
    return True, data

def get_activity_list():
    '''
        查询活动id列表，返回信息包括 活动时间、报名时间、海报
        #TODO 添加分页功能
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    res = activity.find({})

    ans = []
    for item in res:
        try:
            temp = {
                'title':item['activitydata']['title'],
                'starttime':item['activitydata']['starttime'],
                'endtime':item['activitydata']['endtime'],
                'bstarttime':item['activitydata']['bstarttime'],
                'bendtime':item['activitydata']['bendtime'],
                'seat':item['activitydata']['seat'],
                'activityid':item['activityid']
                }
            import time
            nowtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            if nowtime < item['activitydata']['bstarttime']:
                temp['state'] = '0'
            elif nowtime >= item['activitydata']['bstarttime'] and nowtime <= item['activitydata']['bendtime']:
                temp['state'] = '1'
            else:
                temp['state'] = '2'
            ans.append(temp)
        except:
            pass
    return ans

def get_activity_member_by_id(activityid, username):
    '''
        检查活动owner是否是username，是则返回报名人员
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    activity_member = db.activity_member

    one = activity.find_one({'activityid':activityid})

    if one == None:
        return False, 0, 0

    if one['activitydata']['owner'] != username:
        return False, 0, 0

    one = activity_member.find_one({'activityid':activityid})

    return True, one['attendtype'], one['member']

def check_activity_changeable(activityid, username):
    '''
        检查活动owner是否是username以及活动是否已经开始报名，返回True或False
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity

    one = activity.find_one({'activityid':activityid})

    if one == None:
        return False
    if one['activitydata']['owner'] != username:
        return False

    import time
    nowtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    bstarttime = one['activitydata']['bstarttime']

    if nowtime < bstarttime:
        return True
    return False

def check_attend_activity(activity_attend, activityid, username):
    '''
        检查某用户是否参加有参加活动
    '''
    if activity_attend == None:
        from model.mongodb import MongoDB
        db = MongoDB().db
        activity_attend = db.activity_attend

    one = activity_attend.find_one({'username':username})

    if one == None:
        return False
    activitylist = one['activitylist']
    if activityid in activitylist:
        return True
    return False

def update_attend_activity(activity_attend, activityid, username, op):
    '''
        更新用户参加活动
    '''
    if op == 1:
        one = activity_attend.find_one({'username':username})
        if one == None:
            activity_attend.insert({'username':username, 'activitylist':[activityid]})
        else:
            activity_attend.update({'username':username}, {'$push':{'activitylist':activityid}})
    elif op == 2:
        activity_attend.update({'username':username}, {'$pull':{'activitylist':activityid}})

def signup_person(activityid, username):
    '''
        检查活动id是否存在，是否在报名时间内，用户是否已经报名
        返回 0(成功) 1(活动不存在) 2(报名未开始) 3(报名已结束) 4(用户已报名) 5(活动类型不对) 6(名额已经满)
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    activity_attend = db.activity_attend
    activity_member = db.activity_member

    one = activity.find_one({'activityid':activityid})

    if one == None:
        return 1

    import time
    nowtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    bstarttime = one['activitydata']['bstarttime']
    bendtime = one['activitydata']['bendtime']

    if nowtime < bstarttime:
        return 2
    if nowtime > bendtime:
        return 3

    attendtype = one['activitydata']['attendtype']
    if attendtype == 0:
        return 5

    seat = one['activitydata']['seat']

    one = activity_member.find_one({'activityid':activityid})

    member = one['member']
    
    if check_attend_activity(activity_attend, activityid, username) == True:
        return 4

    peoplenum = one['peoplenum']
    if peoplenum == 0 or len(member) < peoplenum:
        if peoplenum != 0:
            #one = activity.find_one({'activityid':activityid})
            #seat = one['seat']
            activity.update({'activityid':activityid}, {'$set':{'activitydata.seat':seat-1}})
        activity_member.update({'activityid':activityid},{'$push':{"member":username}})
        update_attend_activity(activity_attend, activityid, username, 1)
        return 0
    return 6

def signdown_person(activityid, username):
    '''
        检查活动id是否存在，是否在报名时间内，用户是否已经报名
        返回 0(成功) 1(用户没报名) 2(未开始报名) 3(报名已结束) 4(活动不存在) 5(报名类型不对)
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    activity_attend = db.activity_attend
    activity_member = db.activity_member

    one = activity.find_one({'activityid':activityid})

    if one == None:
        return 4

    import time
    nowtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    bstarttime = one['activitydata']['bstarttime']
    bendtime = one['activitydata']['bendtime']

    if nowtime < bstarttime:
        return 2
    if nowtime > bendtime:
        return 3

    attendtype = one['activitydata']['attendtype']
    if attendtype == 0:
        return 5

    seat = one['activitydata']['seat']

    one = activity_member.find_one({'activityid':activityid})

    member = one['member']

    if check_attend_activity(activity_attend, activityid, username) == False:
        return 1

    peoplenum = one['peoplenum']
    activity_member.update({'activityid':activityid},{'$pull':{'member':username}})
    update_attend_activity(activity_attend, activityid, username, 2)
    if peoplenum != 0:
        activity.update({'activityid':activityid}, {'$set':{'activitydata.seat':seat+1}})
    return 0

def signup_team(activityid, username, usernum, userlist):
    '''
        检查活动id是否存在，是否在报名时间内，用户是否已经报名，是否超过报名人数
        返回 0(成功) 1(用户已报名) 2(未开始) 3(已结束) 4(活动不存在)
        5(活动类型错误) 6(报名队伍已满) 7(队伍人数超过限制)

        TODO: MESSAGE
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    activity_attend = db.activity_attend
    activity_member = db.activity_member

    one = activity_member.find_one({'activityid':activityid})

    if one == None:
        return 4

    import time
    nowtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    bstarttime = one['bstarttime']
    bendtime = one['bendtime']

    if nowtime < bstarttime:
        return 2
    if nowtime > bendtime:
        return 3

    attendtype = one['attendtype']
    if attendtype == 1:
        return 5

    for item in userlist:
        if check_attend_activity(activity_attend, activityid, item) == True:
            return 1

    teamnum = one['teamnum']
    teampeople = one['teampeople']
    member = one['member']
    if teampeople == -1 or usernum <= teampeople:
        if teamnum == -1 or len(member) < teamnum:
            if teampnum != -1:
                one = activity.find_one({'activityid':activityid})
                seat = one['seat']
                activity.update(one, {'$set':{'acitvity.seat':seat+1}})
            activity_member.update({'activityid':activityid},{'$push':{'member':{'leader':useranme, 'teameat':userlist}}})
            for item in userlist:
                update_attend_activity(activity_attend, activityid, username, 1)
        else:
            return 6
    else:
        return 7

def signdown_team(activityid, username):
    '''
        检查活动id是否存在，是否在报名时间内，用户是否已经报名，用户是否是队长
        返回 0(成功) 1(用户未报名) 2(未开始) 3(已结束) 4(活动不存在) 5(活动类型错误) 6(没权限)
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    activity_attend = db.activity_attend
    activity_member = db.activity_member

    one = activity_member.find_one({'activityid':activityid})

    if one == None:
        return 4

    import time
    nowtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    bstarttime = one['bstarttime']
    bendtime = one['bendtime']

    if nowtime < bstarttime:
        return 2
    if nowtime > bendtime:
        return 3

    attendtype = one['attendtype']
    if attendtype == 1:
        return 5

    if check_attend_activity(activity_attend, activityid, item) == False:
        return 1

    member = one['member']

    team = None
    for item in member:
        if item['leader'] == username:
            team = item
            break

    if team == None:
        return 6

    teamnum = one['teamnum']
    activity_member.update({'activityid':activityid}, {'$pull':{'member':team}})
    for item in team['teameat']:
        update_attend_activity(activity_attend, activityid, username, 2)
    if teamnum != -1:
        one = activity.find_one({'activityid':activityid})
        seat = one['seat']
        activity.update(one, {'$set':{'seat':seat-1}})
    return 0

def team_add_member(activityid, username, usernum, userlist):
    '''
        检查活动id是否存在，是否在报名时间内，用户是否已经报名，用户是否是队长
    '''
    from model.mongodb import MongoDB
    db = MongoDB().db
    activity = db.activity
    activity_attend = db.activity_attend
    activity_member = db.activity_member

    one = activity_member.find_one({'activityid':activityid})

    if one == None:
        return 4

    import time
    nowtime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    bstarttime = one['bstarttime']
    bendtime = one['bendtime']

    if nowtime < bstarttime:
        return 2
    if nowtime > bendtime:
        return 3

    attendtype = one['attendtype']
    if attendtype == 1:
        return 5

    for item in userlist:
        if check_attend_activity(activity_attend, activityid, item) == True:
            return 1
    # TODO