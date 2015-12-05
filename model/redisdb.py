#-*-coding:utf-8-*-

class RedisDB:
    def __init__(self):
        from redis import Redis
        self.con = Redis('192.168.239.131')