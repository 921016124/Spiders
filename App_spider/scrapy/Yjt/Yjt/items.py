# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JrjgcfItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pub_date = scrapy.Field()  # 披露日期
    about_people = scrapy.Field()  # 当事人
    handle_people = scrapy.Field()  # 处理人
    punish_type = scrapy.Field()  # 处罚类型
    irregularities = scrapy.Field()  # 违法行为
    punish_content = scrapy.Field()  # 处罚内容
    symbol_num = scrapy.Field()  # 文号
    file_url = scrapy.Field()
    file_name = scrapy.Field()
    pass
