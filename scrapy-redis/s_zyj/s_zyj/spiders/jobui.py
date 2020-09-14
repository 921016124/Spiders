# -*- coding: utf-8 -*-
import scrapy
import time
import sys
import re
sys.path.append("../")
from scrapy_redis.spiders import RedisSpider
from items import SrZyjItem, SrZyjJobItem, SrRzItem
from Zyj_Utils import Util
"""
    1. 职友集的scrapy-redis 爬虫程序

"""
util = Util()
headers = {
                    "Accept": "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Host": "www.jobui.com",
                    "Pragma": "no-cache",
                    "Referer": "https://www.jobui.com/cmp",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
cookies = {
                "jobui_p": "1565753151227_21067661",
                "jobui_area": "%25E6%25B7%25B1%25E5%259C%25B3",
                "Hm_lvt_90d68bd37705477f2f6f689b11d8aa3a": "1569814911",
                "Hm_lvt_8b3e2b14eff57d444737b5e71d065e72": "1569570793,1569721522,1569814920,1570502359",
                "jobui_img_logo": "vbBZkTB2kbhlgdb8yFiTPWvaJepQEaNYmroc0pkMFDk%3D",
                "PHPSESSID": "sdgc0hogioq0psu8cavltl9vd5",
                "Hm_lpvt_8b3e2b14eff57d444737b5e71d065e72": "1570502365",
                "TN_VisitCookie": "40",
                "TN_VisitNum": "2",
         }


class ZyjSpider(RedisSpider):
    name = 'jobui'
    allowed_domains = ['jobui.com']
    # start_urls = ['https://www.jobui.com/changecity/?from=http://www.jobui.com/cmp?keyword=&area=%E6%B7%B1%E5%9C%B3']
    redis_key = 'jobui:start_urls'

    def parse(self, response):
        # for dd in response.xpath("//dl[@class=\"j-change\"]/dd")[8:]:  # 遍历多行dd（省份）
        #     for area in dd.xpath("./a"):  # 遍历行内区域（市级）
        #         every_url = "https:" + area.xpath("./@href").extract()[0]  # 按照城市列表分别请求和处理
                # print(area.xpath("./text()").extract()[0])
                # print("每个城市的url: " + every_url)
        every_url = "https:" + response.xpath("//dl[@class=\"j-change\"]/dd[11]/a[1]/@href").extract()[0]  # 遍历多行dd（省份）
        yield scrapy.Request(url=every_url, headers=headers, cookies=cookies, callback=self.parse_area_page)

    # 处理每个地区的页面
    def parse_area_page(self, response):
        hangye = response.xpath("//div[@class=\"job-select-box\"]/ul/li[1]/div/div/a/text()").extract()
        xingzhi = response.xpath("//div[@class=\"job-select-box\"]/ul/li[2]/div/div/a/text()").extract()
        guimo = ["少于50", "50-99", "100-499", "500-999", "1000-4999", "5000-9999", "10000以上"]
        # print(hangye, xingzhi,guimo)
        for a in hangye[1:]:
            for b in xingzhi[1:]:
                use_url = response.url + "&industry={}".format(util.url_encode(a)) \
                                               + "&type={}".format(util.url_encode(b))
                # print(use_url)  # https://www.jobui.com/cmp?area=哈尔滨&industry=新能源&worker=10000以上&type=民营公司
                r1 = util.get_req(url=use_url, headers=headers)
                if util.get_xpath_obj(r1.text).xpath("//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()"):
                    data_count1 = util.get_xpath_obj(r1.text).xpath("//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()")[1].strip()
                    # print("{}-{} 共有：{} 条数据".format(a, b, data_count1))
                    if int(data_count1) >= 1000:
                        for c in guimo:
                            _u_url = use_url + "&worker={}".format(util.url_encode(c))
                            # print(use_url)
                            r2 = util.get_req(url=use_url, headers=headers)
                            if util.get_xpath_obj(r2.text).xpath(
                                "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()"):
                                data_count2 = util.get_xpath_obj(r2.text).xpath(
                                    "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()")[1].strip()
                                # print("{}-{}-{} 共有：{} 条数据".format(a, b, c, data_count2))
                                if int(data_count2) >= 1000:
                                    tese = util.get_xpath_obj(r2.text).xpath(
                                        "//div[@class=\"job-select-box\"]/ul/li[last()]/div/div/a/text()")
                                    for d in tese[1:]:
                                        u_url = _u_url + "&impression={}".format(util.url_encode(d))
                                        r3 = util.get_req(url=u_url, headers=headers)
                                        if util.get_xpath_obj(r3.text).xpath(
                                            "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()"):
                                            data_count3 = util.get_xpath_obj(r3.text).xpath(
                                                "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()")[1].strip()
                                            if int(data_count3) > 1000:
                                                pass
                                                # print("排列组合后数据大于一千， 具体数量： " + data_count3)
                                            else:
                                                # print("{}-{}-{}-{} 共有：{} 条数据".format(a, b, c, d, data_count3))
                                                yield scrapy.Request(url=u_url, headers=headers,
                                                                     cookies=cookies, callback=self.parse_list_page)
                                        else:
                                            yield scrapy.Request(url=u_url, headers=headers,
                                                                 cookies=cookies, callback=self.parse_list_page)
                                else:
                                    yield scrapy.Request(url=_u_url, headers=headers,
                                                         cookies=cookies, callback=self.parse_list_page)
                    else:
                        yield scrapy.Request(url=use_url, headers=headers,
                                             cookies=cookies, callback=self.parse_list_page)

    def parse_list_page(self, response):
        for i in range(1, 51):
            # print("第{}页开始抓取".format(i))
            page_url = response.url + "&n={}".format(i)
            rep = util.get_xpath_obj(util.get_req(url=page_url, headers=headers))
            if rep.xpath("//div[@class=\"c-company-list\"]"):  # 此部分提取规则未修改 -- 2019.12.16
                for item in rep.xpath("//div[@class=\"c-company-list\"]")[:-1]:
                    detail_url = item.xpath(
                        "./div[@class=\"company-content-box\"]/div/div[1]/a/@href")
                    if len(detail_url) > 0:
                        url = "https://www.jobui.com" + detail_url[0]
                        yield scrapy.Request(url=url,
                                             headers=headers,
                                             cookies=cookies,
                                             callback=self.handle_data)
                if len(rep.xpath("//div[@class=\"c-company-list\"]")) <= 20:
                    return False
            else:
                # print("该页无数据。。")
                return False
            # print("第{}页抓取完毕！！".format(i))

    # 处理公司信息
    def handle_data(self, response):
        # print("-" * 100)
        item_info = SrZyjItem()
        if len(response.xpath("//div[@class=\"intro\"]//div[@class=\"company-info-item\"]")) == 3:  # 不确定有没有len() = 2 或是其他数量的情况
            item_info["title"] = response.xpath("//h1/a/text()").extract()[0].strip()
            if response.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()"):
                item_info["brief_intro"] = response.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()").extract()[0].strip()
            else:
                item_info["brief_intro"] = ""
            item_info["xingzhi"] = "".join(response.xpath("//div[@class=\"company-nature\"]/text()").extract()).strip()
            item_info["guimo"] = "".join(response.xpath("//div[@class=\"company-worker\"]/text()").extract()).strip()
            item_info["hangye"] = ";".join([i.strip()
                                            for i in response.xpath("//div[@class=\"company-info-item\"][2]/span/a/text()")
                                           .extract()]).strip()
            item_info["quancheng"] = "".join([i for i in response.xpath("//div[@class=\"company-info-item\"][3]/text()")
                                             .extract() if len(i.strip()) > 1]).strip()
            try:
                item_info["intro"] = "".join(response.xpath("//*[@id=\"textShowMore\"]/text()").extract()).strip()
            except IndexError:
                item_info["intro"] = ""
        else:
            exit(response.url)
        item_info["id_code"] = util.MD5(item_info["quancheng"])
        item_info["comp_code"] = str.split(response.url, "/")[-2]
        item_info["crawl_time"] = util.get_now_time()
        job_info = response.xpath("//div[@id=\"navTab\"]//a[2]/div[@class=\"banner-nav-slash\"]/text()").extract()[0].strip()
        if job_info == "///":
            job_count = 0
        else:
            job_count = int(job_info.replace("个", "").strip())
        item_info["job_count"] = job_count
        if job_count > 0:
            if job_count % 15 == 0:
                page = int(job_count / 15) + 1
            else:
                page = int(job_count / 15) + 2
            for i in range(1, page):
                job_url = response.url + "jobs/p{}/".format(i)
                yield scrapy.Request(url=job_url, headers=headers, callback=self.handle_jobs)
        rz = response.xpath("//div[@id=\"navTab\"]/div/a[last()]/@href").extract()[0]  # 融资信息详情页地址，无域名
        if "financing" in rz:
            item_info["rongzi"] = response.xpath("//div[@id=\"navTab\"]/div/a[last()]/div[1]/text()").extract()[0]
            yield scrapy.Request(url="https://www.jobui.com" + rz, headers=headers, callback=self.handle_rz_info)
        else:
            item_info["rongzi"] = ""
        yield item_info

    # 处理招聘信息
    def handle_jobs(self, response):
        item_job = SrZyjJobItem()
        for item_node in response.xpath(
                "//div[@class=\"j-joblist\"]/div[@class=\"c-job-list\"]//div[@class=\"job-simple-content\"]"):

            item_job["comp_code"] = str.split(response.url, "/")[-4]
            item_job["crawl_time"] = util.get_now_time()

            item_job["job_name"] = item_node.xpath("./div[1]/a/h3/text()").extract()[0]
            item_job["job_location"] = item_node.xpath("./div[2]/div/span[1]/text()").extract()[0]

            item_job["job_xueli"] = ""
            item_job["job_year"] = ""
            item_job["job_xingzhi"] = ""
            item_job["job_money"] = ""
            for p in item_node.xpath("./div[2]/div/span[2]/text()").extract()[0].split(" | "):
                if "在读" in p:
                    item_job["job_xueli"] = p
                if p in ["初中以上", "中专以上", "高中以上", "大专以上", "本科以上", "硕士以上", "应届毕业生"]:
                    item_job["job_xueli"] = p
                    continue
                if "年" in p:
                    item_job["job_year"] = p
                    continue
                if p in ["全职", "实习"]:
                    item_job["job_xingzhi"] = p
                    continue
                for m in ["万", "元", "K", "-", "k", "～"]:
                    if m in p:
                        item_job["job_money"] = p
                        break
            item_job["id_code"] = util.MD5(item_job["job_name"] + item_job["job_location"])
            yield item_job

    # 处理融资信息
    def handle_rz_info(self, response):
        item_rz = SrRzItem()
        # print("+" * 100)
        # for rz_item in response.xpath("//div[@class=\"m-box\"]/div[2]"):
        for rz_item in response.xpath("//div[@class=\"m-box\"]/div[2]/div[@class=\"c-finace-list\"]"):
            try:
                item_rz["rz_stage"], money = str.split(rz_item.xpath("./div/div/h3/text()").extract()[0], ",")
                item_rz["rz_money"] = money.strip()
            except IndexError:
                item_rz["rz_stage"] = item_rz["rz_money"] = ""
            try:
                # 借鉴元组拆分，可以将解压出来的元素分成两部分，一部分是第一个，剩下的都是第二个。
                item_rz["rz_edate"], *people = str.split(rz_item.xpath("./div/div/p[@class=\"finace-desc\"]/text()").extract()[0], ",")
                item_rz["rz_compy"] = ";".join(str.split(people[0], "，")).strip()
            except IndexError:
                item_rz["rz_edate"] = item_rz["rz_compy"] = ""
            item_rz["id_code"] = util.MD5(response.xpath("//h1[@id=\"companyH1\"]/a/text()").extract()[0] + item_rz["rz_stage"])
            item_rz["comp_code"] = str.split(response.url, "/")[-3]
            item_rz["crawl_time"] = util.get_now_time()
            yield item_rz
'''
    
'''