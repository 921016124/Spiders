# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql


class Lianjia1Pipeline(object):

    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    """
        提供数据持久化到MongoDB中的方式
    """
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline(object):
    """
        提供数据持久化到MongoDB中的方式
    """
    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        # 连接数据库
        self.conn = pymysql.connect(
            host=spider.settings.MYSQL_HOST,
            port=spider.settings.MYSQL_PORT,
            user=spider.settings.MYSQL_USER,
            password=spider.settings.MYSQL_PASSWD,
            db=spider.settings.MYSQL_DB,
            charset=spider.settings.CHARSET  # 编码格式
        )
        self.cur = self.conn.cursor()  # 游标

    def process_item(self, item, spider):
        if not hasattr(item, 'table_name'):  # 表设计为有table——name的item的存入mYsql数据库，无则直接返回item
            return item
        cols, values = zip(*item.items())  # 使用zip方法取cols和values列表
        sql = "INSERT INTO `{}` ({}) VALUES " \  
        "({}) ON DUPLICATE KEY UPDATE {}".format(  # on  为避免爬取到相同数据插入数据库后报错 使用更新方式插入
            item.table_name,
            ','.join(['`%s`' % k for k in cols]),
            ','.join(["%s"] * len(values)),
            ','.join(["{}=%s".format(k) for k in cols])
        )

        self.cur.execute(sql, values * 2)  # 执行sql语句 values作为第二个参数而不是直接在sql语句中这种写法可以防sql语句注入
        print(self.cur._last_executed)  # 打印 调试用
        self.conn.commit()  # 提交 存储到数据库
        return item

    def close_spider(self, spider):
        self.cur.close()  # 关闭游标
        self.conn.close()  # 关闭数据库


class OtherPipeline(object):
    """
        提供其他格式数据输出
        如：*.txt  *.xls  *.sql  *.xml  *.csv  *.json
    """
    pass
