# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class QccPipeline(object):

    def __init__(self):
        self.host = 'localhost'
        self.port = 27017
        self.dbName = 'QCC'
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        tdb = self.client[self.dbName]
        self.post = tdb['qiye']

    def process_item(self, item, spider):
        QiYe = dict(item)
        self.post.insert(QiYe)
        return item
