import time
import sys
sys.path.append("../")
from Utils_1 import Util
import pymysql
from lxml import etree
import requests
import http
from Utils_1.UA import User_Agent
import random


"""
    数据来源：中华人民共和国商务部
    来源地址：http://femhzs.mofcom.gov.cn/fecpmvc/pages/fem/CorpJWList_nav.pageNoLink.html?session=T&sp=1&sp=S+_t1.CORP_CDE%2C+_t1.id&sp=T&sp=S
    数据描述：境外投资企业（机构）备案结果公开名录列表
    目标表中文名：境外投资企业公开名录列表
    目标表英文名：EXT_INV_ENTP_LST_INF
    数据量：3 - 4 (万条)
    作者：mcg
    状态：完成
    记录时间：2019.08.02
    备注：对于cookie值，可以再优化。
"""


class FemhzsMofcomGov:
    def __init__(self):
        self.base_url = "http://femhzs.mofcom.gov.cn/fecpmvc/pages/fem/CorpJWList_nav.pageNoLink.html?" \
                        "session=T&sp={}&sp=S+_t1.CORP_CDE%2C+_t1.id&sp=T&sp=S"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "JSESSIONID=ACBDC30A40FD783627A075ADB9440B4D; insert_cookie=56224592  ",
            "Host": "femhzs.mofcom.gov.cn",
            "Referer": "http://femhzs.mofcom.gov.cn/fecpmvc/pages/fem/CorpJWList.html",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/75.0.3770.100 Safari/537.36",
        }
        self.f_headers = {
            "Host": "femhzs.mofcom.gov.cn",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "http://www.mofcom.gov.cn/publicService.shtml",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        self.util = Util()
        self.conn = self.util.MySQL()

        self.page = 0

    def insert2mysql(self, sql):
        try:
            self.conn.cursor().execute(sql)
            self.conn.commit()
            print("插入成功")
        except pymysql.err.IntegrityError:
            print("插入失败，数据重复")
            self.conn.rollback()
        except pymysql.err.ProgrammingError:
            print("数据异常，已回滚")
            self.conn.rollback()

    def run(self):
        first_req = requests.get(url="http://femhzs.mofcom.gov.cn/fecpmvc/pages/fem/CorpJWList.html",
                                           headers=self.f_headers)
        cookies = first_req.headers["Set-Cookie"].replace(" Path=/fecpmvc,", "").replace("; path=/", "")
        try:
            page = etree.HTML(first_req.text).xpath(
                "//em[@class=\"m-page-total-num\"]/text()")[0]
        except TimeoutError:
            time.sleep(10)
            page = etree.HTML(first_req.text).xpath(
                "//em[@class=\"m-page-total-num\"]/text()")[0]
        except http.client.RemoteDisconnected:
            time.sleep(10)
            self.headers["User-Agent"] = random.choice(User_Agent)
            page = etree.HTML(first_req.text).xpath(
                "//em[@class=\"m-page-total-num\"]/text()")[0]
        print("共有：{} 页".format(page))
        for i in range(1, int(page)):
            print(i)
            data = {
                "session": "T",
                "sp": i,
                "sp": "S _t1.CORP_CDE, _t1.id",
                "sp": "T",
                "sp": "S",
            }
            self.headers["Cookie"] = cookies
            url = self.base_url.format(i)
            try:
                res = requests.get(url=url, headers=self.headers, data=data, timeout=15)
            except TimeoutError:
                time.sleep(10)
                res = requests.get(url=url, headers=self.headers, data=data, timeout=15)
            time.sleep(2)
            if res.status_code == 200:
                print("请求成功，开始解析")
                html = etree.HTML(res.text)
                for tr in html.xpath("//table[@class=\"m-table\"]/tbody/tr"):
                    company_name = tr.xpath("./td[1]/text()")[0].strip()
                    investor_name = tr.xpath("./td[2]/text()")[0].strip()
                    country = tr.xpath("./td[3]/text()")[0].strip()
                    # 公司名称编码作为id
                    md5_company = self.util.MD5(company_name)
                    # 获取当前时间
                    otherStyleTime = self.util.get_now_time()

                    sql = "insert into EXT_INV_ENTP_LST_INF(ID, OVS_INV_ENTP_NM, OVS_INV_NM, INV_CNR, INPT_DT)values('%s','%s','%s','%s','%s')" % (md5_company, company_name, investor_name, country, otherStyleTime)
                    self.insert2mysql(sql)
            else:
                print("请求失败， HTTP Code:{}".format(res.status_code))


if __name__ == '__main__':
    while True:
        f = FemhzsMofcomGov()
        f.run()
        time.sleep(86400)
