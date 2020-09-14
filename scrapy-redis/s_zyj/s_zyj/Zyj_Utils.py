import time

import requests
import hashlib
import pymysql
from pymongo import MongoClient
from lxml import etree
import base64
import json
import urllib.parse


class Util:
    # get connect to mysql
    def MySQL(self):
        # Python 操作 MySQL
        conn_mysql = pymysql.connect(host="192.168.43.139", port=3306, user="root", passwd="root", db="sunline")
        return conn_mysql

    # get connect to Mongo
    def Mongo(self):
        # Python 操作 MongoDB
        conn_mongo = MongoClient("127.0.0.1", 27017)
        db = conn_mongo.QCC  # 连接 mydb 数据库，没有则自动创建
        return db.qcc_7  # 使用test_set集合，没有则自动创建
    # get md5 encode number

    def MD5(self, str):
        m2 = hashlib.md5()
        m2.update(str.encode('utf-8'))
        return m2.hexdigest()

    # insert into data to mysql
    def insert2mysql(self, mes, sql, exc=None):
        conn = self.MySQL()
        try:
            conn.cursor().execute(sql)
            if exc is not None:
                conn.cursor().execute(exc)
            conn.commit()
            print("[{}]|-- {} 插入成功".format(self.get_now_time(), str(mes)))
        except pymysql.err.IntegrityError:
            print("[{}]|-- {} 插入失败，数据重复！！".format(self.get_now_time(), str(mes)))
            conn.rollback()
        except pymysql.err.ProgrammingError as e:
            print(e)
            conn.rollback()

    def get_stamp(self):
        it = int(time.time())
        return it

    # get now time : yyyy-mm-dd HH:MM:SS
    def get_now_time(self):
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    # get request  and response
    def get_req(self, url, headers, verify=True, data=None):
        try:
            return requests.get(url=url, headers=headers)
        except Exception as e:
            print("request has Error,Mes:" + str(e))

    # get xpath object
    def get_xpath_obj(self, res):
        if isinstance(res, str):
            return etree.HTML(res)
        else:
            return etree.HTML(res.text)

    # get json obj
    def get_json_obj(self, str_obj):
        return json.loads(str_obj)

    # encode by base64
    def base64_encode(self, s):
        if isinstance(s, str):
            return base64.b64encode(bytes(s, encoding='utf-8'))
        else:
            if isinstance(s, float):
                return base64.b64encode(bytes(str(int(s)), encoding='utf-8'))
            elif isinstance(s, int):
                return base64.b64encode(bytes(str(s), encoding='utf-8'))
            else:
                print(type(s))

    def write2txt(self, filename, content):
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(content)
            print('文件写入成功！！')
            f.close()

    def readtxt(self, filename):
        with open(filename, 'r', encoding="utf-8") as f:
            return f.read()

    def url_encode(self, str):
        return urllib.parse.quote(str)

    def url_decode(self, str):
        return urllib.parse.unquote(str)



if __name__ == '__main__':
    u = Util()
    u.get_stamp()
    u.get_now_time()
