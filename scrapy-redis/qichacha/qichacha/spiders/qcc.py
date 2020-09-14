# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider


class QccSpider(RedisSpider):
    name = 'qcc'
    allowed_domains = ['www.qichacha.com']
    redis_key = "qcc:start_urls"

    def parse(self, response):
        try:
            locations = ["https://www.qichacha.com" + i for i in response.xpath("//div[@class=\"panel b-a padder\"][2]/div/div[@class=\"pills-after\"]/a/@href").extract()]
            for loc in locations:
                print(loc)
                yield scrapy.Request(url=loc, callback=self.parse_list)
        except:
            yield scrapy.Request(url=response.request.url, callback=self.parse_list)

    def parse_list(self, response):
        items = response.xpath("//section[@id=\"searchlist\"]/table/tbody/tr")
        cookies = {
            "UM_distinctid":"169d3bba2842b2-05304a460c818c-7a1437-144000-169d3bba285831",
        "zg_did":"%7B%22did%22%3A%20%22169d3bba3f2345-0876df1f768158-7a1437-144000-169d3bba3f3a1f%22%7D",
        "_uab_collina":"155403548384500317787525",
        "acw_tc":"6f0c58ce15540354820011000e38ee47a520b1d99877b5b7b6bb599861",
        "QCCSESSID":"bq3vrr5p156ndo7mojv1sgk4k5",
        "hasShow":1,
        "Hm_lvt_3456bee468c83cc63fb5147f119f1075":"1556523083,1556528798,1556586912,1556587268",
        "CNZZDATA1254842228":"453305125-1554033918-https%253A%252F%252Fwww.baidu.com%252F%7C1556604543",
        "zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f":"%7B%22sid%22%3A%201556606491439%2C%22updated%22%3A%201556606825981%2C%22info%22%3A%201556073452257%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22dafb20bd273c29be3cb1a0b6a9686972%22%7D",
        "Hm_lpvt_3456bee468c83cc63fb5147f119f1075":1556606826,}
        for item in items:
            detail_url = "https://www.qichacha.com" + item.xpath("./td/a/@href").extract()[0]
            print("item_url: "+detail_url)
        next_url = response.xpath("//a[@class=\"next\"]/@href")
        if next_url:
            url = "https://www.qichacha.com" + next_url.extract()[0]
            yield scrapy.Request(url)