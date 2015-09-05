#-*-coding:utf-8-*-

from api import api
from flask import request, jsonify, make_response
from config.rescode import *

@api.route('/message/boardcast', methods=['POST'])
def message_boardcast():
    '''
        消息广播
    '''
    pass

@api.route('/message/activity/boardcast/all', methods=['POST'])
def message_activity_boardcast_all():
    '''
        活动广播
    '''
    pass

@api.route('/message/activity/boardcast/leader', methods=['POST'])
def message_activity_boardcast_leader():
    '''
        活动队长广播
    '''
    pass

@api.route('/message/person', methods=['POST'])
def message_person():
    '''
        单独消息
    '''
    pass