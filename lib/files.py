#-*-coding:utf-8-*-

def create_dict(path, root):
    import os
    pathlist = os.listdir(path)
    for i, item in enumerate(pathlist):
        if os.path.isdir(os.path.join(path, item)):
            path = os.path.join(path, item)
            root[item] = {}
            create_dict(path, root[item])
            path = '/'.join(path.split('/')[:-1])
        else:
            root[item] = item

def get_download_catalog_json():
    '''
        生成文件目录json
    '''

    import os
    path = os.path.dirname(os.path.abspath(__file__))
    path = '/'.join(path.split('/')[:-1]) + '/static'
    root = {}
    create_dict(path, root)
    return root