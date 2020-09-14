# coding:utf-8
import time
import sys
import re
import os
import pymysql
import pymongo
sys.path.append("../")
from Utils_1 import Util
from multiprocessing import Process
from multiprocessing import JoinableQueue


class JobuiProcess(object):
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
        self.sleep_time = 0.3

        # 多进程初始化队列
        self.url_queue = JoinableQueue()
        self.resp_queue = JoinableQueue()
        self.item_queue = JoinableQueue()

        # mongo config
        self.mongo_host = "mongodb://localhost:27017/"
        self.mongo_client = "SunLine"
        self.mongo_db = "jobui"

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
        for dd in res_html.xpath("//dl[@class=\"j-change\"]/dd")[-1:]:  # 遍历多行dd（省份）
            for area in dd.xpath("./a")[-1:]:  # 遍历行内区域（市级）
                every_url = "https:" + area.xpath("./@href")[0]  # 按照城市列表分别请求和处理
                print(area.xpath("./text()")[0])
                # print("每个城市的url: " + every_url)
                self.parse_area_page(self.util.get_req(url=every_url, headers=self.headers))

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
                r = self.util.get_req(url=use_url, headers=self.headers)
                # time.sleep(self.sleep_time)
                if self.util.get_xpath_obj(r.text).xpath(
                        "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()"):
                    data_count1 = self.util.get_xpath_obj(r.text).xpath(
                        "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()")[1].strip()
                    print("{}-{} 共有：{} 条数据".format(a, b, data_count1))
                    if int(data_count1) >= 1000:
                        for c in guimo:
                            use_url = use_url + "&worker={}".format(self.util.url_encode(c))
                            print(use_url)
                            r = self.util.get_req(url=use_url, headers=self.headers)
                            # time.sleep(self.sleep_time)
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
                                        # time.sleep(self.sleep_time)
                                        if self.util.get_xpath_obj(r.text).xpath(
                                                "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()"):
                                            data_count3 = self.util.get_xpath_obj(r.text).xpath(
                                                "//div[@class=\"m-title-box\"]/div/span[@class=\"fr\"]//text()")[
                                                1].strip()
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
            if rep.xpath("//div[@class=\"c-company-list\"]"):
                for item in rep.xpath("//div[@class=\"c-company-list\"]")[:-1]:
                    detail_url = item.xpath("./div[@class=\"company-content-box\"]/div/div[1]/a/@href")
                    self.url_queue.put("https://www.jobui.com" + detail_url[0])  # 公司信息添加到url队列中。
                    # print("添加成功！！")
                if len(rep.xpath("//div[@class=\"c-company-list\"]")) <= 20:
                    return False
            else:
                return False

    # 处理公司信息
    def handle_data(self):
        item = {}
        print("*" * 100)

        while True:
            try:
                time.sleep(self.sleep_time)
                url = self.url_queue.get()
                response = self.util.get_req(url=url, headers=self.headers)
                if response.status_code != 200:
                    self.url_queue.put(response.url)
            except Exception as e:
                raise e
            else:
                res_html = self.util.get_xpath_obj(response.text)
                if len(res_html.xpath(
                        "//div[@class=\"intro\"]//div[@class=\"company-info-item\"]")) == 3:  # 不确定有没有len() = 2 或是其他数量的情况
                    item["title"] = res_html.xpath("//h1/a/text()")[0].strip().replace("\u2022", "")
                    if response.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()"):
                        item["brief_intro"] = res_html.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()")[0].strip()
                    else:
                            item["brief_intro"] = ""

                    item["xingzhi"] = "".join(res_html.xpath("//div[@class=\"company-nature\"]/text()")).strip()
                    item["guimo"] = "".join(res_html.xpath("//div[@class=\"company-worker\"]/text()")).strip()
                    item["hangye"] = ";".join([i.strip()
                                       for i in res_html.xpath("//div[@class=\"company-info-item\"][2]/span/a/text()")
                                       ]).strip()
                    item["quancheng"] = "".join([i for i in res_html.xpath("//div[@class=\"company-info-item\"][3]/text()")
                                         if len(i.strip()) > 1]).strip().replace("...", "")
                    try:
                        item["intro"] = "".join(res_html.xpath("//*[@id=\"textShowMore\"]/text()")).strip()
                    except IndexError:
                        item["intro"] = ""
                else:
                    item["title"] = ""
                    item["brief_intro"] = ""
                    item["xingzhi"] = ""
                    item["guimo"] = ""
                    item["hangye"] = ""
                    item["quancheng"] = ""
                    item["intro"] = ""
                item["id_code"] = self.util.MD5(item["quancheng"])
                item["comp_code"] = str.split(response.request.url, "/")[-2]
                item["crawl_time"] = self.util.get_now_time()
                job_info = res_html.xpath("//div[@id=\"navTab\"]//a[2]/div[@class=\"banner-nav-slash\"]/text()")[
                    0].strip()
                if job_info == "///":
                    job_count = 0
                else:
                    job_count = int(job_info.replace("个", "").strip())
                item["job_count"] = job_count
                if job_count > 0:
                    if job_count % 15 == 0:
                        page = int(item["job_count"] / 15) + 1
                    else:
                        page = int(item["job_count"] / 15) + 2
                    for i in range(1, page):
                        job_url = response.request.url + "jobs/p{}/".format(i)
                        self.handle_jobs(self.util.get_req(url=job_url, headers=self.headers))
                        time.sleep(0.1)
                rz = res_html.xpath("//div[@id=\"navTab\"]/div/a[last()]/@href")[0]  # 融资信息详情页地址，无域名
                if "financing" in rz:
                    item["rongzi"] = res_html.xpath("//div[@id=\"navTab\"]/div/a[last()]/div[1]/text()")[0]
                    self.handle_rz_info(self.util.get_req(url="https://www.jobui.com" + rz, headers=self.headers))
                    time.sleep(0.1)
                else:
                    item["rongzi"] = ""
                self.item_queue.put(item)
                # self.util.insert2mysql("（企业信息）" + title, self.sql_info(t))
                with open("./Scrapyed.txt", 'a', encoding="utf8") as f:
                    f.write(str.split(response.request.url, "/")[-2] + "\n")
            self.url_queue.task_done()  # 计数-1

    def insert2mongoDB(self, item):
        myclient = pymongo.MongoClient(self.mongo_host)
        mydb = myclient[self.mongo_client]
        mycol = mydb[self.mongo_db]
        x = mycol.insert_one(item)

    def save_item(self):
        while True:
            item = self.item_queue.get()
            self.insert2mongoDB(item)
            self.item_queue.task_done()

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
                    t_job = (
                    id_code, job_name, job_location, job_xueli, job_year, job_xingzhi, job_money, comp_code,
                    crawl_time)
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

    def run(self):
        process_list = []
        # 构造url列表
        for _ in range(100):
            t_parse_url_list = Process(target=self.parse)
            t_parse_url_list.daemon = True
            t_parse_url_list.start()
            t_parse_url_list.join()

        # 发送请求，获取响应
        for i in range(5):
            ti_parse_url = Process(target=self.handle_data)
            process_list.append(ti_parse_url)

        for p in process_list:
            p.daemon = True  # 设置守护线程
            p.start()

        for q in [self.url_queue, self.resp_queue]:
            q.join()  # 让主线程阻塞，队列没释放之前不能结束任务

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
    j = JobuiProcess()
    # res = j.util.get_req(url="https://www.jobui.com/company/9914359/", headers=j.headers)
    # j.handle_data(res)
    j.run()