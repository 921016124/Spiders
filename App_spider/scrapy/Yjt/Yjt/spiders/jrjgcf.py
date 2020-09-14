# -*- coding: utf-8 -*-
import re
import time
import scrapy
import sys
sys.path.append("E:/Spider/Projects/SunLine/App_spider/")
sys.path.append("../")
from items import JrjgcfItem
from Utils_1 import Util
import settings
"""
    通过scrapy 对 app 企业预警通
    本爬虫为金融监管处罚部分的抓取
    可以抓取，有需要可以通过scrapy 的方式快速抓取 。
"""


class JrjgcfSpider(scrapy.Spider):
    name = 'jrjgcf'
    allowed_domains = ['app.finchina.com']
    start_urls = ['https://app.finchina.com/finchinaAPP/getOrgFamilyCreaditData_SE.action?selTopRecommended=%E9%87%91%E8%9E%8D%E7%9B%91%E7%AE%A1%E5%A4%84%E7%BD%9A&skip=1']

    def __init__(self):
        super(JrjgcfSpider, self).__init__()
        self.u = Util()
        self.detail_headers = {
            "Host": "app.finchina.com",
            "client": "finchina",
            "system": "v4.3.1.551,13.2.3,iOS,iPhone,iPhone,iPhone11,8",
            "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
            "Accept-Language": "zh-Hans-CN;q=1.0",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Referer": "https://app.finchina.com/finchinaAPP/f9/creditArchives/creditDetail.html?user=20191212160004_15561585051&id={}&getContent=0&token=ee7d9333-95fe-4530-b901-e05b35211cf4&companyName={}",
            "token": "0c6a8e27-d8a7-4d4a-8a78-4b89a98dcd6c",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.page = 1

    def parse(self, response):
        if self.u.get_json_obj(response.body)["returncode"] == 0:
            datas = self.u.get_json_obj(response.body)["data"]
            while True:
                if len(datas):
                    for data in datas:
                        id_code = data["infoId"]
                        name = data["related"][0]["name"]
                        type = data["type"]
                        time.sleep(0.2)
                        self.detail_headers["Referer"] = self.detail_headers["Referer"].format(id_code, self.u.url_encode(name))
                        self.detail_headers["User-Agent"] = settings.random_ua()

                        yield scrapy.Request(
                            url="https://app.finchina.com/finchinaAPP/getOrgFamilyCreaditDataContentDetails.action?"
                                "type={}&getContent=0&id={}".format(type, id_code),
                            headers=self.detail_headers,
                            callback=self.parse_detail)

                self.page += 1
                time.sleep(3)
                yield \
                    scrapy.Request(
                        url="https://app.finchina.com/finchinaAPP/getOrgFamilyCreaditData_SE.action?"
                            "selTopRecommended=%E9%87%91%E8%9E%8D%E7%9B%91%E7%AE%A1%E5%A4%84%E7%BD%9A&skip={}".format(self.page)
                        , callback=self.parse
                    )
                break
        else:
            print("响应错误！！！")

    def parse_detail(self, response):
        item = JrjgcfItem()
        detail_datas = self.u.get_json_obj(response.body)["data"]
        for i in detail_datas:
            print("*" * 100)
            item["pub_date"] = i["it0026_006"]  # 披露日期
            item["about_people"] = i["it0026_005"]  # 当事人
            item["handle_people"] = i["it0026_016"]  # 处理人
            item["punish_type"] = i["risk"][0]["name"]  # 处罚类型
            item["irregularities"] = i["it0026_009"]  # 违法行为
            item["punish_content"] = i["it0026_011"]  # 处罚内容
            item["symbol_num"] = i["it0026_017"]  # 文号
            item["file_url"] = i["file"][0]["fileUrl"]
            item["file_name"] = i["file"][0]["fileName"]
            print("*" * 100)
            yield item
