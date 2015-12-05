#-*-coding:utf-8-*-

class MongoDB:
    def __init__(self):
        from pymongo import MongoClient
        self.con = MongoClient('192.168.239.131')
        self.db = self.con.smie