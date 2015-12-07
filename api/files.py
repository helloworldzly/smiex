#-*-coding:utf-8-*-

from api import api
from flask import request, jsonify, make_response
from config.rescode import *

@api.route('/files/catalog/<regex(".*"):path>', methods=['GET'])
def files_catalog(path):
    '''
        获得下载目录json
        参数： path 文件绝对路径
        返回值： SUCCESS folderlist filelist/ INVALID_OPERATION
    '''

    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(rescode=INVALID_OPERATION)

    # session = cookies['session']

    username = 'zengzhaoyang'

    from lib import get_download_catalog_json

    print path
    catalog = get_download_catalog_json()
    temp = path.split('/')

    folderlist = []
    filelist = []
    try:
        if path != '':
            for item in temp:
                catalog = catalog[item]
        for item in catalog:
            if type(catalog[item]) == type(''):
                filelist.append(item)
            else:
                folderlist.append(item)
    except:
        pass
    return jsonify(rescode=SUCCESS, folderlist=folderlist, filelist=filelist)