# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from qcc import settings
import pymongo


class QccPipeline(object):

    def __init__(self):

        host = "127.0.0.1"  # settings['MONGODB_HOST']
        port = 27017  # settings['MONGODB_PORT']
        dbName = "SunLine"  # settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb["l_qcc"]  # settings['MONGODB_DOCNAME']

    def process_item(self, item, spider):
        bookInfo = dict(item)
        self.post.insert(bookInfo)
        return item
