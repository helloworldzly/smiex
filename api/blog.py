#-*-coding:utf-8-*-

from api import api
from flask import request, jsonify, make_response
from config.rescode import *

@api.route('/blog/admin/add', methods=['POST'])
def blog_admin_add():
    '''
        发表博客
    '''
    pass

@api.route('/blog/admin/edit', methods=['POST'])
def blog_admin_edit():
    '''
        编辑博客
    '''
    pass

@api.route('/blog/admin/delete', methods=['POST'])
def blog_admin_delete():
    '''
        删除博客
    '''
    pass

@api.route('/blog/info/<blogid>', methods=['GET'])
def blog_info(blogid):
    '''
        根据博客id查询博客内容
    '''
    pass

#TODO: 评论、转载、点赞