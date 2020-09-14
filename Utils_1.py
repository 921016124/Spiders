import time
import random
import requests
import hashlib
import pymysql
from pymongo import MongoClient
from lxml import etree
import base64
import json
import urllib.parse
requests.packages.urllib3.disable_warnings()

class Util:
    # get connect to mysql
    def MySQL(self):
        # Python 操作 MySQL
        try:
            conn_mysql = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="wcs")
            # conn_mysql = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="sunline")
        except pymysql.err.OperationalError:
            time.sleep(5)
            # conn_mysql = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="sunline")
            conn_mysql = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="wcs")
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
            print("Exception: " + str(e))
            self.write2txt("Error.txt", sql)
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
    def get_req(self, url, headers, verify=False):
        try:
            return requests.get(url=url, headers=headers, verify=verify)
        except requests.exceptions.SSLError:
            time.sleep(10)
            return requests.get(url=url, headers=headers, verify=verify)
        except requests.exceptions.ConnectionError as e:
            print(e)
            time.sleep(10)
            return requests.get(url=url, headers=headers, verify=verify)
        except TimeoutError as e:
            print(e)

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
        with open(filename, 'a', encoding="utf-8") as f:
            f.write(content)
            print('文件写入成功！！')
            f.close()

    def write2file(self, file_path, file_name, file_type, req):
        """
            通过请求网页二进制文件，将文件保存到本地。
        :param file_path: 文件存储路径
        :param file_name: 文件名称
        :param file_type: 文件类型
        :param req: 网页返回的请求
        :return: None
        """
        with open(file_path + file_name + "." + file_type, "wb") as f:
            f.write(req.content)
        print(file_name + "文件保存完成！！")

    def readtxt(self, filename):
        with open(filename, 'r', encoding="utf-8") as f:
            return f.read()

    def url_encode(self, str):
        return urllib.parse.quote(str)

    def url_decode(self, str):
        return urllib.parse.unquote(str)

    def get_random_ua(self):
        ua = [
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
                "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
                "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"
            ]
        return random.choice(ua)


if __name__ == '__main__':
    u = Util()
    u.get_stamp()
    u.get_now_time()
