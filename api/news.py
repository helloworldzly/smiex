#-*-coding:utf-8-*-

from api import api
from flask import request, jsonify, make_response
from config.rescode import *

@api.route('/news/add', methods=['POST'])
def news_add():
    '''
        发布新闻
    '''
    pass

@api.route('/news/edit', methods=['POST'])
def news_edit():
    '''
        编辑新闻
    '''
    pass

@api.route('/news/delete', methods=['POST'])
def news_delete():
    '''
        删除新闻
    '''
    pass

@api.route('/news/info/<newsid>', methods=['GET'])
def news_info(newsid):
    '''
        根据新闻id获取新闻
    '''
    pass