# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import sys
sys.path.append("E:\Spider\Projects\SunLine\App_spider\scrapy\Yjt\Yjt")
import settings
import pymysql
from items import JrjgcfItem
from Utils_1 import Util
from scrapy.pipelines.files import FilesPipeline


class YjtPipeline(object):
    def __init__(self):
        self.dbparams = {
            'host': settings.MYSQL_HOST,
            'port': settings.MYSQL_PORT,
            'user': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWD,
            'database': settings.MYSQL_DB,
            'charset': settings.MYSQL_CHARSET
        }
        self.u = Util()

    def process_item(self, item, spider):
        conn = pymysql.connect(**self.dbparams)
        print("数据库连接成功~~~")
        if isinstance(item, JrjgcfItem):
            jrjgcf_data = (self.u.MD5(item["about_people"] + item["symbol_num"]), item["pub_date"], item["about_people"], item["handle_people"], item["punish_type"],
                           item["irregularities"], item["punish_content"], item["symbol_num"], item["file_url"],
                           item["file_name"], self.u.get_now_time())
            self.insert2mysql(self.jrjgcf_sql(jrjgcf_data), item["about_people"], conn)
        return item

    def insert2mysql(self, sql, mes, conn, exc=None):
        try:
            conn.cursor().execute(sql)
            if exc is not None:
                conn.cursor().execute(exc)
            conn.commit()
            print("[{}]|-- {} 插入成功".format(self.u.get_now_time(), str(mes)))
        except pymysql.err.IntegrityError:
            print("[{}]|-- {} 插入失败，数据重复！！".format(self.u.get_now_time(), str(mes)))
            conn.rollback()
        except pymysql.err.ProgrammingError as e:
            print(e)
            conn.rollback()
        except Exception as e:
            print(e)

    def jrjgcf_sql(self, data):
        sql = """insert into 
        yjt_jrjgcf(id, pub_date, about_people,handle_people, punish_type, irregularities, 
        punish_content, symbol_num, file_url, file_name, crawl_time) 
        values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % data
        return sql


class Jrjgcf_file(FilesPipeline):
    def get_media_requests(self, item, info):
        for file_url in item["file_url"]:
            print(file_url)
            yield scrapy.Request(file_url)

