# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time


class QccSpider(CrawlSpider):
    name = 'qcc'
    allowed_domains = ['qichacha.com']
    start_urls = ['https://www.qichacha.com/g_AH']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.qichacha.com/firm_[a-zA-Z0-9]{32}.html'), callback="parse_item", follow=False),  # 处理详情页
        Rule(LinkExtractor(allow=r'https://www.qichacha.com/gongsi_area.shtml?prov=[A-Z]{2}&p=\d+'), callback="get_items", follow=True),  # 处理分页
        Rule(LinkExtractor(allow=r'https://www.qichacha.com/g_[A-Z]{2}.html'), callback="get_items", follow=True),  # 处理省份
    )

    def parse_item(self, response):
        # 详情页爬虫设计
        time.sleep(3)
        item = {}
        item["Company_Name"] = response.xpath("//div[@class=\"content\"]//h1/text()").extract()[0]
        Founding_Time = response.xpath("//section[@id=\"Cominfo\"]/table[2]/tr[2]/td[4]/text()")
        if Founding_Time:
            item["Founding_Time"] = Founding_Time.extract()[0].strip()
        else:
            item["Founding_Time"] = ""  # 在处理数据的时候，成立时间为空的舍弃该item
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        item["crawl_time"] = otherStyleTime
        yield item

    def get_items(self, response):
        items = response.xpath("//section[@id=\"searchlist\"]")
        for item in items:
            url = "https://www.qichacha.com" + item.xpath("./a/@href").extract()[0]
            yield scrapy.Request(url=url, callback=self.parse_item)
        next_url = response.xpath("//ul[contains(@class, \"pagination\")]/li/a/@href")
        if next_url:
            next_url = "https://www.qichacha.com" + response.xpath("//ul[contains(@class, \"pagination\")]/li/a[@class=\"next\"]/@href").extract()[0]
            print(next_url)
            time.sleep(10)
            yield scrapy.Request(url=next_url, callback=self.get_items)
        else:
            province_urls = response.xpath("//div[@class=\"row\"]/div[1]/div/dl/dd")
            for province_url in province_urls:
                url = "https://www.qichacha.com" + province_url.xpath("./a/@href")[0]
                time.sleep(10)
                yield scrapy.Request(url, callback=self.get_items)

