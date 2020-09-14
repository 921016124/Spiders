import requests
from lxml import etree
from pymongo import MongoClient
from 网贷平台.UA import User_Agent
import random
"""
1. 处理ssl 证书问题
2. 解决ISO-8859-1编码问题
3. 利用捕获异常机制，处理编码问题。处理/u2003 编码问题
4. 利用正则解决xpath无法提取值的问题。
5. 解决UA被判断为爬虫程序的反反爬虫问题
"""


class Wdzj:
    def __init__(self):
        self.headers = {
                    "User-Agent": "",
                    "Connection": "keep-alive",
                }
        self.url = "https://www.wdzj.com/dangan/search?filter&currentPage=1"
        self.timeout = 20

    @staticmethod
    def mongo():
        # Python 操作 MongoDB
        conn_mongo = MongoClient("127.0.0.1", 27017)
        db = conn_mongo.SunLine  # 连接 mydb 数据库，没有则自动创建
        return db.wdzj_1  # 使用test_set集合，没有则自动创建

    def run(self):
        currentnum = 1
        my_set = self.mongo()
        while True:
            print("第{}页开始爬取".format(currentnum))
            ua = random.choice(User_Agent)
            self.headers["User-Agent"] = ua  # 解决UA被判断为爬虫程序的反反爬虫问题
            response = requests.get(url=self.url, headers=self.headers, timeout=self.timeout, verify=True)  # 处理ssl 证书问题

            html = etree.HTML(response.text)
            items = html.xpath("//ul[@class=\"terraceList\"]/li")
            for item in items:
                s_item = {}
                item_url = item.xpath(".//h2/a/@href")[0]
                item_name = item_url.split("/")[2]
                detail_url = "https://www.wdzj.com/dangan/{}/gongshang/".format(item_name)

                ua = random.choice(User_Agent)
                self.headers["User-Agent"] = ua  # 解决UA被判断为爬虫程序的反反爬虫问题
                detail_response = requests.get(url=detail_url, headers=self.headers, timeout=self.timeout, verify=True).text.encode("ISO-8859-1").decode("utf-8")  # 解决ISO-8859-1编码问题
                detail_html = etree.HTML(detail_response)

                # 工商信息
                try:
                    if detail_html.xpath("//h1/text()"):
                        s_item["平台名称"] = detail_html.xpath("//h1/text()")[0].strip()
                    else:
                        s_item["平台名称"] = ""
                except UnicodeEncodeError:
                    # 利用捕获异常机制，处理编码问题。处理/u2003 编码问题
                    s_item["平台名称"] = detail_html.xpath("//h1/text()")[0].decode("ignore").strip()
                # 系别
                if detail_html.xpath("//div[@class=\"bq-box\"]/span/text()"):
                    s_item["系别"] = detail_html.xpath("//div[@class=\"bq-box\"]/span//text()")[0].strip()
                else:
                    s_item["系别"] = ""
                try:
                    if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[1]/td[2]/text()"):
                        s_item["公司名称"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[1]/td[2]/text()")[0].strip()
                    else:
                        s_item["公司名称"] = ""
                except UnicodeEncodeError:
                    s_item["公司名称"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[1]/td[2]/text()")[0]\
                        .decode("ignore").strip()  # 利用捕获异常机制，处理编码问题。处理/u2003 编码问题
                if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[2]/td[2]/text()"):
                    s_item["法人代表"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[2]/td[2]/text()")[0].strip()
                else:
                    s_item["法人代表"] = ""
                if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[4]/td[4]/text()"):
                    s_item["开业日期"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[4]/td[4]/text()")[0].strip()
                else:
                    s_item["开业日期"] = ""
                if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[5]/td[2]/text()"):
                    s_item["状态"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[5]/td[2]/text()")[0].strip()
                else:
                    s_item["状态"] = ""
                if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[6]/td[4]/text()"):
                    s_item["核准日期"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[6]/td[4]/text()")[0].strip()
                else:
                    s_item["核准日期"] = ""
                    # 股权信息
                s_item["股权信息"] = ";".join([i.strip() for i in detail_html.xpath(
                    "//div[@id=\"gqInfoBox\"]/div[@class=\"table-ic-box\"]/table/tbody[1]/tr/td[1]/text()")])

                # 股权信息
                s_item["股权信息"] = ";".join(detail_html.xpath(
                    "//div[@id=\"gqInfoBox\"]/div[@class=\"table-ic-box\"]/table/tbody[1]/tr/td[1]/text()")).strip()

                # 异常经营
                exception_info = detail_html.xpath(
                    "//div[@class=\"containerBox\"]/div[last()]/div/table/tbody[1]/tr/td[2]/text()")
                if exception_info:
                    s_item["列入经营异常原因"] = exception_info[0].strip()
                else:
                    s_item["列入经营异常原因"] = ""
                exception_RegiDate = detail_html.xpath(
                    "//div[@class=\"containerBox\"]/div[last()]/div/table/tbody[1]/tr/td[3]/text()")
                if exception_RegiDate:
                    s_item["列入日期"] = exception_RegiDate[0].strip()
                else:
                    s_item["列入日期"] = ""
                exception_RegiOffice = detail_html.xpath(
                    "//div[@class=\"containerBox\"]/div[last()]/div/table/tbody[1]/tr/td[4]/text()")
                if exception_RegiOffice:
                    s_item["决定机关(列入)"] = exception_RegiOffice[0].strip()
                else:
                    s_item["决定机关(列入)"] = ""

                s_item["详情地址"] = detail_url

                if s_item["公司名称"] != "-" and s_item["公司名称"] != "":
                    print(s_item["公司名称"])
                    my_set.insert_one(s_item)
            print("第{}页爬取结束".format(currentnum))
            if html.xpath("//div[@class=\"pageList\"]/a[contains(text(),\"下一页\")]"):
                import re
                # 利用正则解决xpath无法提取值的问题。
                currentnum = re.findall(r'class="pageindex" currentNum="(.*?)">下一页</a>', response.text)[0]
                self.url = "https://www.wdzj.com/dangan/search?filter&currentPage={}".format(currentnum)
            else:
                break


if __name__ == '__main__':
    w = Wdzj()
    w.run()
