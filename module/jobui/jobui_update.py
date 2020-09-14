# coding:utf-8
import time
import datetime
import sys
import re
import os
import pymysql
sys.path.append("../")
from Utils_1 import Util

"""
    解决了 公司地址不包含区级信息造成的因区级筛选而遗漏的问题。 --2020。1。5
"""


class Jobui:
    def __init__(self):
        self.util = Util()
        self.url = "https://www.jobui.com/changecity/?from=http://www.jobui.com/cmp?keyword=&area=%E6%B7%B1%E5%9C%B3"
        self.headers = {
                            "Accept": "text/html,application/xhtml+xml,"
                            "application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Accept-Language": "zh-CN,zh;q=0.9",
                            "Cache-Control": "no-cache",
                            "Connection": "keep-alive",
                            "Host": "www.jobui.com",
                            "Pragma": "no-cache",
                            "Referer": "https://www.jobui.com/cmp",
                            "Cookie": "jobui_p=1565753151227_21067661; jobui_user_passport=yk15764787441006; jobui_area=%25E7%258F%25A0%25E6%25B5%25B7; Hm_lvt_8b3e2b14eff57d444737b5e71d065e72=1576719314,1576744537,1576805924,1577020459; Hm_lpvt_8b3e2b14eff57d444737b5e71d065e72=1577028389; TN_VisitCookie=344; TN_VisitNum=1",
                            "Upgrade-Insecure-Requests": "1",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
        self.sleep_time = 0.1
        self.data_num = 0

    def load(self):
        if os.path.exists("Scrapyed.txt"):
            with open("Scrapyed.txt", 'r', encoding="utf8") as f:
                return f.read()
        else:
            print("文件不存在！！！！")

    # 处理数据的总方法
    def parse(self): 
        req_area = self.util.get_req(url=self.url, headers=self.headers)
        res_html = self.util.get_xpath_obj(req_area.text)
        every_url = "https:" + res_html.xpath("//dl[@class=\"j-change\"]/dd[11]/a[1]/@href")[0] # 遍历多行dd（省份）
        self.data_num = 0
        print(res_html.xpath("//dl[@class=\"j-change\"]/dd[11]/a[1]//text()")[0])
        # print("每个城市的url: " + every_url)
        self.parse_area_page(self.util.get_req(url=every_url, headers=self.headers))
        print("此地区共抓取公司数量为：" + str(self.data_num))

    # 处理地区页面
    def parse_area_page(self, response):
        area_html = self.util.get_xpath_obj(response.text)
        hangye = area_html.xpath("//div[@class=\"job-select-box\"]/ul/li[1]/div/div/a/text()")
        xingzhi = area_html.xpath("//div[@class=\"job-select-box\"]/ul/li[2]/div/div/a/text()")
        guimo = ["少于50", "50-99", "100-499", "500-999", "1000-4999", "5000-9999", "10000以上"]
        for a in hangye[1:]:
            for b in xingzhi[1:]:
                use_url = response.request.url + "&industry={}".format(self.util.url_encode(a)) \
                                               + "&type={}".format(self.util.url_encode(b))
                # print(use_url)  # https://www.jobui.com/cmp?area=哈尔滨&industry=新能源&worker=10000以上&type=民营公司
                r = self.util.get_req(url=use_url, headers=self.headers)
                time.sleep(self.sleep_time)
                if self.util.get_xpath_obj(r.text).xpath("//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()"):
                    data_count1 = self.util.get_xpath_obj(r.text).xpath("//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()")[1].strip()
                    print("{}-{} 共有：{} 条数据".format(a, b, data_count1))
                    if int(data_count1) >= 1000:
                        for c in guimo:
                            use_url = use_url + "&worker={}".format(self.util.url_encode(c))
                            print(use_url)
                            r = self.util.get_req(url=use_url, headers=self.headers)
                            time.sleep(self.sleep_time)
                            if self.util.get_xpath_obj(r.text).xpath(
                                "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()"):
                                data_count2 = self.util.get_xpath_obj(r.text).xpath(
                                    "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()")[1].strip()
                                print("{}-{}-{} 共有：{} 条数据".format(a, b, c, data_count2))
                                if int(data_count2) >= 1000:
                                    tese = self.util.get_xpath_obj(r.text).xpath(
                                        "//div[@class=\"job-select-box\"]/ul/li[last()]/div/div/a/text()")
                                    for d in tese[1:]:
                                        use_url = use_url + "&impression={}".format(self.util.url_encode(d))
                                        r = self.util.get_req(url=use_url, headers=self.headers)
                                        time.sleep(self.sleep_time)
                                        if self.util.get_xpath_obj(r.text).xpath(
                                            "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()"):
                                            data_count3 = self.util.get_xpath_obj(r.text).xpath(
                                                "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()")[1].strip()
                                            if int(data_count3) > 1000:
                                                print("排列组合后数据大于一千， 具体数量： " + data_count3)
                                            else:
                                                print("{}-{}-{}-{} 共有：{} 条数据".format(a, b, c, d, data_count3))
                                                self.parse_list_page(use_url)
                                        else:
                                            self.parse_list_page(use_url)
                                else:
                                    self.parse_list_page(use_url)
                    else:
                        self.parse_list_page(use_url)

    # 处理 每一个列表页的方法
    def parse_list_page(self, line):
        for i in range(1, 51):
            print("第{}页开始抓取".format(i))
            page_url = line + "&n={}".format(i)
            rep = self.util.get_xpath_obj(self.util.get_req(url=page_url, headers=self.headers))
            if rep.xpath("//div[@class=\"c-company-list\"]"):  # 此部分提取规则未修改 -- 2019.12.16
                for item in rep.xpath("//div[@class=\"c-company-list\"]")[:-1]:
                    detail_url = item.xpath("./div[@class=\"company-content-box\"]/div/div[1]/a/@href")
                    self.data_num += 1
                    if str.split(detail_url[0], "/")[-2] not in self.load():
                        if len(detail_url) > 0:
                            url = "https://www.jobui.com" + detail_url[0]
                            try:
                                self.handle_data(self.util.get_req(url=url, headers=self.headers))
                            except TimeoutError:
                                print("超时了！！！")
                            except Exception:
                                print("188 行出错了！！")
                                time.sleep(5)
                                self.handle_data(self.util.get_req(url=url, headers=self.headers))
                            time.sleep(1)
                    else:
                        # print("{} 该数据已入库".format(item.xpath("./div[@class=\"company-content-box\"]/div/div[1]/a/@title")[0].replace("怎么样", "")))
                        pass
                    time.sleep(0.1)
                if len(rep.xpath("//div[@class=\"c-company-list\"]")) <= 20:
                    return False
            else:
                print("该页无数据。。")
                return False
            print("第{}页抓取完毕！！".format(i))

    # 处理公司信息
    def handle_data(self, res):

        # print("-" * 100)
        # print(res.request.url)
        # print(res.status_code)
        if res.status_code == 200:
            response = self.util.get_xpath_obj(res.text)
            if len(response.xpath("//div[@class=\"intro\"]//div[@class=\"company-info-item\"]")) == 3:  # 不确定有没有len() = 2 或是其他数量的情况
                title = response.xpath("//h1/a/text()")[0].strip().replace("\u2022", "")
                if response.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()"):
                    brief_intro = response.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()")[0].strip()
                else:
                    brief_intro = ""
                xingzhi = "".join(response.xpath("//div[@class=\"company-nature\"]/text()")).strip()
                guimo = "".join(response.xpath("//div[@class=\"company-worker\"]/text()")).strip()
                hangye = ";".join([i.strip()
                                                for i in response.xpath("//div[@class=\"company-info-item\"][2]/span/a/text()")
                                               ]).strip()
                # item_info["rongzi"] = response.xpath("//div[@id=\"navTab\"]/div/a[last()]/div[1]/text()")[0]
                quancheng = "".join([i for i in response.xpath("//div[@class=\"company-info-item\"][3]/text()")
                                                  if len(i.strip()) > 1]).strip().replace("...", "")
                try:
                    intro = "".join(response.xpath("//*[@id=\"textShowMore\"]/text()")).strip()
                except IndexError:
                    intro = ""
            else:
                title = ""
                brief_intro = ""
                xingzhi = ""
                guimo = ""
                hangye = ""
                quancheng = ""
                intro = ""
            id_code = self.util.MD5(quancheng)
            comp_code = str.split(res.request.url, "/")[-2]
            crawl_time = self.util.get_now_time()
            job_info = response.xpath("//div[@id=\"navTab\"]//a[2]/div[@class=\"banner-nav-slash\"]/text()")[0].strip()
            if job_info == "///":
                job_count = 0
            else:
                job_count = int(job_info.replace("个", "").strip())
            job_count = job_count
            if job_count > 0:
                if job_count % 15 == 0:
                    page = int(job_count / 15) + 1
                else:
                    page = int(job_count / 15) + 2
                for i in range(1, page):
                    job_url = res.request.url + "jobs/p{}/".format(i)
                    self.handle_jobs(self.util.get_req(url=job_url, headers=self.headers))
                    time.sleep(0.1)
            rz = response.xpath("//div[@id=\"navTab\"]/div/a[last()]/@href")[0]  # 融资信息详情页地址，无域名
            if "financing" in rz:
                rongzi = response.xpath("//div[@id=\"navTab\"]/div/a[last()]/div[1]/text()")[0]
                self.handle_rz_info(self.util.get_req(url="https://www.jobui.com" + rz, headers=self.headers))
                time.sleep(0.1)
            else:
                rongzi = ""
            t = (id_code, title, brief_intro, xingzhi, guimo, hangye, rongzi, quancheng, pymysql.escape_string(intro), job_count, comp_code, crawl_time,)
            self.util.insert2mysql("（企业信息）" + title, self.sql_info(t))
            with open("./Scrapyed.txt", 'a', encoding="utf8") as f:
                f.write(str.split(res.request.url, "/")[-2] + "\n")
        else:
            print(res.status_code)
            return False

    # 处理招聘信息
    def handle_jobs(self, res):
        # print(res.request.url)
        response = self.util.get_xpath_obj(res.text)
        while True:
            try:
                for item_node in response.xpath(
                        "//div[@class=\"j-joblist\"]/div[@class=\"c-job-list\"]//div[@class=\"job-simple-content\"]"):
                    comp_code = str.split(res.request.url, "/")[-4]
                    crawl_time = self.util.get_now_time()
                    job_name = item_node.xpath("./div[1]/a/h3/text()")[0]
                    job_location = item_node.xpath("./div[2]/div/span[1]/text()")[0]
                    job_xueli = ""
                    job_year = ""
                    job_xingzhi = ""
                    job_money = ""
                    for p in item_node.xpath("./div[2]/div/span[2]/text()")[0].split(" | "):
                        if "在读" in p:
                            job_xueli = p
                        if p in ["初中以上", "中专以上", "高中以上", "大专以上", "本科以上", "硕士以上", "应届毕业生"]:
                            job_xueli = p
                            continue
                        if "年" in p:
                            job_year = p
                            continue
                        if p in ["全职", "实习"]:
                            job_xingzhi = p
                            continue
                        for m in ["万", "元", "K", "-", "k", "～"]:
                            if m in p:
                                job_money = p
                                break
                    id_code = self.util.MD5(comp_code + job_name + job_location)
                    t_job = (id_code, job_name, job_location, job_xueli, job_year, job_xingzhi, job_money, comp_code, crawl_time)
                    self.util.insert2mysql(job_name, self.sql_job(t_job))
                break
            except Exception as e:
                print(e)
                time.sleep(10)

    # 处理融资信息
    def handle_rz_info(self, res):
        print("+" * 100)
        # print(res.request.url)
        response = self.util.get_xpath_obj(res.text)
        # for rz_item in response.xpath("//div[@class=\"m-box\"]/div[2]"):
        for rz_item in response.xpath("//div[@class=\"m-box\"]/div[2]/div[@class=\"c-finace-list\"]"):
            try:
                rz_stage, money = str.split(rz_item.xpath("./div/div/h3/text()")[0], ",")
                rz_money = money.strip()
            except IndexError:
                rz_stage = rz_money = ""
            try:
                # 借鉴元组拆分，可以将解压出来的元素分成两部分，一部分是第一个，剩下的都是第二个。
                rz_edate, *people = str.split(rz_item.xpath("./div/div/p[@class=\"finace-desc\"]/text()")[0], ",")
                rz_compy = ";".join(str.split(people[0], "，")).strip()
            except IndexError:
                rz_edate = rz_compy = ""
            id_code = self.util.MD5(response.xpath("//h1[@id=\"companyH1\"]/a/text()")[0] + rz_stage)
            comp_code = str.split(res.request.url, "/")[-3]
            crawl_time = self.util.get_now_time()
            t_rz = (id_code, rz_stage, rz_money, rz_edate, rz_compy, comp_code, crawl_time)
            self.util.insert2mysql(rz_stage, self.sql_rz(t_rz))

    def sql_info(self, tuple):
        sql_info = """
                    insert into tmp_jobui_info_n(id, title, brief_intro, 
                                        xingzhi, guimo, hangye, 
                                        rongzi, quancheng, 
                                        intro, job_count, comp_code, crawl_time) 
                                        values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
                    """ % tuple
        return sql_info

    def sql_job(self, tuple):
        sql_job = """
                        insert into tmp_jobui_job_n(id, job_name, job_location, 
                                            job_xueli, job_year, 
                                            job_xingzhi, job_money, comp_code, crawl_time) 
                                            values('%s','%s','%s','%s','%s','%s','%s','%s','%s') 
                    """ % tuple
        return sql_job

    def sql_rz(self, tuple):
        sql_rz = """
                    insert into tmp_jobui_rz(id, rz_stage, rz_money, rz_edate, 
                                            rz_compy, comp_code, crawl_time) 
                                            values('%s','%s','%s','%s','%s','%s','%s') 
            """ % tuple
        return sql_rz


if __name__ == '__main__':

    j = Jobui()
    # res = j.util.get_req(url="https://www.jobui.com/company/9914359/", headers=j.headers)
    # j.handle_data(res)
    j.parse()