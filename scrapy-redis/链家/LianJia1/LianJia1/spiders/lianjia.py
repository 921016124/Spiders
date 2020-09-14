# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from LianJia1.items import Lianjia1Item


class LianjiaSpider(RedisSpider):
    name = 'lianjia'
    allowed_domains = ['sz.lianjia.com']
    redis_key = "lj1:start_urls"

    def parse(self, response):
        loop_xpath = "//ul[@class=\"sellListContent\"]/li[contains(@class,\"LOGCLICKDATA\")]"
        items = response.xpath(loop_xpath)
        for item in items:
            s_item = Lianjia1Item()
            s_item['title'] = item.xpath("./div/div/a/text()").extract()[0]
            yield s_item
