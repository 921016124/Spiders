# -*- coding: utf-8 -*-
import scrapy
from items import SrRzItem
from Zyj_Utils import Util

util = Util()


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['https://www.jobui.com']
    start_urls = ['https://www.jobui.com/company/8203932/financing/']

    def parse(self, response):
        print("+" * 100)
        print(response.xpath("//div[@class=\"m-box\"]/div[2]/div[@class=\"c-finace-list\"][1]/div/div/h3/text()"))
        for rz_item in response.xpath("//div[@class=\"m-box\"]/div[2]/div[@class=\"c-finace-list\"]"):
            stage, money = str.split(rz_item.xpath("./div/div/h3/text()").extract()[0], ",")
            money = money.strip()
            date, *people = str.split(rz_item.xpath("./div/div/p[@class=\"finace-desc\"]/text()").extract()[0], ",")
            people = ";".join(str.split(people[0], "，")).strip()
            comp_code = str.split(response.request.url, "/")[-3]
