# -*- coding: utf-8 -*-
import pymysql
import pymongo
import sys
# sys.path.append("")
from items import SrZyjItem, SrZyjJobItem, SrRzItem
import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SrZyjPipeline(object):
    def __init__(self):
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        dbname = settings.MONGODB_DBNAME
        sheetnames = settings.MONGODB_SHEETNAME
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post1 = mydb[sheetnames[0]]
        self.post2 = mydb[sheetnames[1]]
        self.post3 = mydb[sheetnames[2]]

    def process_item(self, item, spider):
        data = dict(item)
        if isinstance(item, SrZyjItem):
            self.post1.insert(data)
        elif isinstance(item, SrZyjJobItem):
            self.post2.insert(data)
        elif isinstance(item, SrRzItem):
            self.post3.insert(data)
        return item
