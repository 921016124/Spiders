# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PedailySpider(CrawlSpider):
    name = 'pedaily'
    allowed_domains = ['www.pedaily.cn']
    start_urls = ['https://www.pedaily.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'inv/'), callback='parse_inv', follow=True),
        Rule(LinkExtractor(allow=r'ipo/'), callback='parse_ipo', follow=True),
        Rule(LinkExtractor(allow=r'ma/'), callback='parse_ma', follow=True),
        Rule(LinkExtractor(allow=r'pe/'), callback='parse_pe', follow=True),
        Rule(LinkExtractor(allow=r'all/'), callback='parse_all', follow=True),
        Rule(LinkExtractor(allow=r'enterprise/'), callback='parse_enterprise', follow=True),
        Rule(LinkExtractor(allow=r'people/'), callback='parse_people', follow=True),
        Rule(LinkExtractor(allow=r'/enterprise/show/\d+/'), callback='parse_detail', follow=True),
    )

    def parse_inv(self, response):
        pass

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
