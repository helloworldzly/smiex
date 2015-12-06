#-*-coding:utf-8-*-

class MongoDB:
    def __init__(self):
        from pymongo import MongoClient
        self.con = MongoClient('localhost')
        self.db = self.con.smie