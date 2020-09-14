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


class Util:

    def __init__(self):
        self.msg_from = '1256784086@qq.com'  # 发送方邮箱
        self.passwd = 'fwcqlgdjlpvkjida'  # 填入发送方邮箱的授权码
        self.msg_to = '921016124@qq.com'  # 收件人邮箱

    # get connect to mysql
    def MySQL(self):
        # Python 操作 MySQL
        conn_mysql = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="sunline")
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
        except pymysql.err.ProgrammingError:
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
    def get_req(self, url, headers, verify=True):
        while True:
            try:
                return requests.get(url=url, headers=headers)
            except Exception as e:
                print("request has Error,Mes:" + str(e))
                time.sleep(10)

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

    def sendErrorEmail(self, server, e, spidername):
        subject = "警告，你的程序已经停止!"  # 主题
        content = "服务器:{} \n爬虫 {} 已经停止\n请及时处理! \n异常信息:\n\n{}".format(server, spidername, e)
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = self.msg_from
        msg['To'] = self.msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(self.msg_from, self.passwd)
            s.sendmail(self.msg_from, self.msg_to, msg.as_string())
            print("异常邮件发送成功 !!!")
        except s.SMTPException as e:
            print("异常邮件发送失败 !!")
        finally:
            s.quit()

    def sendSuccessEmail(self, server, spidername):
        subject = "恭喜,程序已经执行完毕, 请查看数据!"  # 主题
        content = "服务器： {} 爬虫： {} 已经执行完毕! 请去数据库查看数据.".format(server, spidername)
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = self.msg_from
        msg['To'] = self.msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(self.msg_from, self.passwd)
            s.sendmail(self.msg_from, self.msg_to, msg.as_string())
            print("成功邮件发送成功 !!!")
        except s.SMTPException as e:
            print("成功邮件发送失败 !!")
        finally:
            s.quit()
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
