# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import time
import re
import requests
from lxml import etree
from qcc.items import QccItem


class Qcc1Spider(RedisSpider):
    name = 'qcc_1'
    allowed_domains = ['www.qichacha.com']
    redis_key = "qcc_1:start_urls"

    def parse(self, response):
        try:
            locations = ["https://www.qichacha.com" + i for i in response.xpath(
                "//div[@class=\"panel b-a padder\"][2]/div/div[@class=\"pills-after\"]/a/@href").extract()]
            for loc in locations:
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
            "CNZZDATA1254842228": "453305125-1554033918-https%253A%252F%252Fwww.baidu.com%252F%7C1556604543",
            "zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f":"%7B%22sid%22%3A%201556606491439%2C%22updated%22%3A%201556606825981%2C%22info%22%3A%201556073452257%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22dafb20bd273c29be3cb1a0b6a9686972%22%7D",
            "Hm_lpvt_3456bee468c83cc63fb5147f119f1075": 1556606826, }
        print("x" * 100)
        for item in items:
            detail_url = "https://www.qichacha.com" + item.xpath("./td/a/@href").extract()[0]

            yield scrapy.Request(url=detail_url,
                                 callback=self.parse_item,
                                 cookies=cookies,

                                 )
        next_url = response.xpath("//a[@class=\"next\"]/@href")
        if next_url:
            url = "https://www.qichacha.com" + next_url.extract()[0]
            yield scrapy.Request(url)

    def parse_item(self, response):
        s_item = QccItem()
        unique = re.findall(r'\_(.*?)\.', response.request.url)[0]
        title = response.xpath("//div[@class=\"row\"]/div[@class=\"content\"]/div/h1/text()").extract()
        if title:
            s_item["title"] = title[0]
        else:
            s_item["title"] = ""

        status = response.xpath("//div[@class=\"row\"]//section[@id=\"Cominfo\"]/table[2]/tr[2]/td[2]/text()").extract()
        if status:
            s_item["status"] = status[0].strip()
        else:
            s_item["status"] = ""
        Fa_Ren = response.xpath("//td[@class=\"ma_left\"]//a//text()").extract()
        if Fa_Ren:
            s_item["Fa_Ren"] = Fa_Ren[0]
        else:
            if response.xpath("//a[@class=\"bname\"]/h2/text()"):
                s_item["Fa_Ren"] = response.xpath("//a[@class=\"bname\"]/h2/text()").extract()[0]
            else:
                s_item["Fa_Ren"] = ""
        date = response.xpath("//div[@class=\"row\"]//section[@id=\"Cominfo\"]/table[2]/tr[2]/td[4]/text()").extract()
        if date:
            s_item["date"] = date[0].strip()
        else:
            s_item["date"] = ""
        tele = response.xpath(
            "//div[@class=\"dcontent\"]/div[@class=\"row\"][1]/span[1]/span[@class=\"cvlu\"][1]//text()").extract()

        if tele:
            s_item["tele"] = "".join(tele).replace("更多号码", "").strip()
        else:
            s_item["tele"] = ""
        Hang_Ye = response.xpath("//div[@class=\"row\"]//section[@id=\"Cominfo\"]/table[2]/tr[5]/td[4]/text()").extract()
        if Hang_Ye:
            s_item['Hang_ye'] = Hang_Ye[0].strip()
        else:
            s_item['Hang_ye'] = ""
        addr = response.xpath("//div[@class=\"row\"]//section[@id=\"Cominfo\"]/table[2]/tr[10]/td[2]/text()").extract()
        if addr:
            s_item["addr"] = addr[0].strip()
        else:
            s_item["addr"] = ""

        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        s_item["softs"] = ""

        s_item["crawl_time"] = otherStyleTime
        if response.xpath("//div[@class=\"company-nav\"]/div/a/h2[contains(text(),\"知识产权\")]"):
            if response.xpath("//*[@id=\"assets_title\"]/h2/../span/text()") != 0:
                # 处理软件著作部分
                soft_url = "https://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=assets"
                more_url = "https://www.qichacha.com/company_getinfos?unique={}&companyname={}&p={}&tab=assets&box=rjzzq"
                data = {
                    "unique": "",
                    "companyname": "",
                    "tab": "assets",
                }
                headers = {
                    "Connection": "keep-alive",
                    "Cookie": "UM_distinctid=169d3bba2842b2-05304a460c818c-7a1437-144000-169d3bba285831; zg_did=%7B%22did%22%3A%20%22169d3bba3f2345-0876df1f768158-7a1437-144000-169d3bba3f3a1f%22%7D; _uab_collina=155403548384500317787525; acw_tc=6f0c58ce15540354820011000e38ee47a520b1d99877b5b7b6bb599861; QCCSESSID=bq3vrr5p156ndo7mojv1sgk4k5; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1555491464,1556001146,1556006786,1556007406; CNZZDATA1254842228=453305125-1554033918-https%253A%252F%252Fwww.baidu.com%252F%7C1556071777; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1556073571; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201556073022197%2C%22updated%22%3A%201556073571495%2C%22info%22%3A%201556073452257%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%2284e02a05f73308cee338be8320f88a9c%22%7D",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                }

                data["unique"] = unique
                data["companyname"] = title[0]
                first_req_url = soft_url.format(unique, title[0])
                first_req = requests.get(url=first_req_url, headers=headers, data=data)  # 请求第一页著作权
                html = etree.HTML(first_req.text)
                zzq = html.xpath("//*[@id=\"rjzzqlist\"]/table/tr/td[2]/text()")

                while True:
                    if html.xpath(
                            "//section[@id=\"zzqlist\"]/div[@class=\"m-b\"]//ul[@class=\"pagination\"]/li/a[contains(text(), \">\")]/@href"):
                        next = html.xpath(
                            "//section[@id=\"zzqlist\"]/div[@class=\"m-b\"]//ul[@class=\"pagination\"]/li/a[contains(text(), \">\")]/@href")[0]
                        next_num = re.findall(r'getTabList\((\d+).*"zzq"\)', next)[0]
                        next_url = more_url.format(unique, title[0], next_num)  # url 构建
                        # data 补充
                        data["p"] = next_num
                        data["box"] = "rjzzq"
                        # 开始请求第二页
                        more_res = requests.get(url=next_url, headers=headers, data=data)
                        print("下一页请求成功")
                        html = etree.HTML(more_res.text)
                        more_zzq = html.xpath("//table/tr/td[2]/text()")
                        for i in more_zzq:
                            zzq.append(i)
                    else:
                        if html.xpath("//ul[@class=\"pagination\"]/li/a[contains(text(),\">\")]"):
                            next = html.xpath("//ul[@class=\"pagination\"]/li/a[contains(text(),\">\")]/@href")[0]
                            next_num = re.findall(r'getTabList\((\d+).*"rjzzq"\)', next)[0]
                            next_url = more_url.format(unique, title[0], next_num)  # url 构建
                            # data 补充
                            data["p"] = next_num
                            data["box"] = "rjzzq"
                            # 开始请求第二页
                            more_res = requests.get(url=next_url, headers=headers, data=data)
                            print("下一页请求成功")
                            html = etree.HTML(more_res.text)
                            more_zzq = html.xpath("//table/tr/td[2]/text()")
                            for i in more_zzq:
                                zzq.append(i)
                        else:
                            break
                data.pop("p")
                data.pop("box")
                s_item["softs"] = zzq
        else:
            if response.request.url:
                s_item["detail_url"] = response.request.url

        return s_item

    def parse_soft_more(self, response):
        pass