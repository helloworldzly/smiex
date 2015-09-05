#-*-coding:utf-8-*-

class MongoDB:
    def __init__(self):
        import pymongo
        self.con = pymongo.Connection('localhost')
        self.db = self.con.smie