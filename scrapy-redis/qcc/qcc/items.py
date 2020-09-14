# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QccItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    loc = scrapy.Field()
    status = scrapy.Field()
    Fa_Ren = scrapy.Field()
    date = scrapy.Field()
    tele = scrapy.Field()
    Hang_ye = scrapy.Field()
    addr = scrapy.Field()
    softs = scrapy.Field()
    crawl_time = scrapy.Field()
    detail_url = scrapy.Field()

    pass
