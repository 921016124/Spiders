import requests
import sys
import time
import re
import pymysql
import random
from Utils_1 import Util
sys.path.append("../")


class Jobui:
    def __init__(self):
        self.url = "https://www.jobui.com/cmp?area=%E5%85%A8%E5%9B%BD&keyword="
        self.base_url = "https://www.jobui.com/cmp?" \
                        "area=%E5%85%A8%E5%9B%BD&industry={}&worker={}&impression={}&type={}&n={}"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,"
                      "application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "jobui_p=1565753151227_21067661; "
                      "jobui_area=%25E6%25B7%25B1%25E5%259C%25B3; "
                      "Hm_lvt_8b3e2b14eff57d444737b5e71d065e72=1565753152,1567047709,1567585344; "
                      "PHPSESSID=kkdnm8jingh5vq1g7e1ora7pe3; "
                      "jobui_img_logo=vbBZkTB2kbhlgdb8yFiTPdmw4wCW3uKOYJ%2F4lauoW4o%3D; "
                      "TN_VisitCookie=42; TN_VisitNum=33; Hm_lpvt_8b3e2b14eff57d444737b5e71d065e72=1567585986",
            "Host": "www.jobui.com",
            "Pragma": "no-cache",
            "Referer": "https://www.jobui.com/cmp",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        self.u = Util()
        self.cursor = self.u.MySQL().cursor()
        self.data = {
            "area": "全国",
            "keyword": ""
        }
        self.base_data = {
            "area": "全国",
            "industry": "",
            "worker": "",
            "impression": "",
            "type": ""
        }
        self.re_try_list = []
        self.proxies = self.get_proxy()

    def get_proxy(self):
        sql = "select ip, tp from ip_pool where tof = '1';"
        self.cursor.execute(sql)
        proxy = self.cursor.fetchall()
        proxies = {}
        for p in range(len(proxy)):
            proxies[proxy[p][0]] = proxy[p][1]
        return proxies

    def handle_data(self, req):
        if req.status_code == 200:
            html = self.u.get_xpath_obj(req.text)
            if html.xpath("//div[@class=\"no-result\"]"):
                print(">>>>>页面无数据")
            else:
                urls = ["https://www.jobui.com" + i for i in html.xpath("//div[@class=\"company-segmetation\"]/a/@href")]
                for url in urls:
                    print(url)
                    try:
                        # 解决多余警告
                        requests.packages.urllib3.disable_warnings()
                        proxy_key = random.choice(list(self.proxies.keys()))
                        print("<{}>".format(proxy_key))
                        proxies = {proxy_key: self.proxies[proxy_key]}
                        detail_req = requests.get(url=url, headers=self.headers, proxies=proxies, verify=False)
                    except requests.exceptions.ConnectionError:
                        self.re_try_list.append(url)
                        print("网页未被请求到，已加入重试列表。")
                        continue
                    print("详情页请求完成，响应代码为：{}".format(detail_req.status_code))
                    detail_html = self.u.get_xpath_obj(detail_req.text)
                    if len(detail_html.xpath("//div[@class=\"intro\"]/div/dl/dt")) == 4:
                        title = detail_html.xpath("//h1/a/text()")[0].strip()
                        if detail_html.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()"):
                            brief_intro = detail_html.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()")[0].strip()
                        else:
                            brief_intro = ""
                        xingzhi, guimo = detail_html.xpath("//div[@class=\"intro\"]/div/dl/dd[1]/text()")[0].split(" / ")
                        hangye = ";".join([i.strip() for i in detail_html.xpath("//div[@class=\"intro\"]/div/dl/dd[2]/a/text()")])
                        rongzi = detail_html.xpath("//div[@class=\"intro\"]/div/dl/dd/dd[@class=\"gray3\"]/text()")[0].strip()
                        quancheng = detail_html.xpath("//div[@class=\"intro\"]/div/dl/dd[@class=\"gray3\"]/text()")[0].strip()
                        intro = "".join(detail_html.xpath("//*[@id=\"textShowMore\"]/text()")).strip()
                    if len(detail_html.xpath("//div[@class=\"intro\"]/div/dl/dt")) == 3:
                        title = detail_html.xpath("//h1/a/text()")[0].strip()
                        if detail_html.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()"):
                            brief_intro = detail_html.xpath("//div[@class=\"company-banner-segmetation\"]/p/text()")[0].strip()
                        else:
                            brief_intro = ""
                        xingzhi, guimo = detail_html.xpath("//div[@class=\"intro\"]/div/dl/dd[1]/text()")[0].split(" / ")
                        hangye = ";".join([i.strip() for i in detail_html.xpath("//div[@class=\"intro\"]/div/dl/dd[2]/a/text()")])
                        rongzi = ""
                        quancheng = detail_html.xpath("//div[@class=\"intro\"]/div/dl/dd[@class=\"gray3\"]/text()")[0].strip()
                        intro = "".join(detail_html.xpath("//*[@id=\"textShowMore\"]/text()")).strip()
                    else:
                        quancheng= ""
                        title = ""
                        brief_intro = ""
                        xingzhi = ""
                        guimo = ""
                        hangye = ""
                        rongzi = ""
                        quancheng = ""
                        intro = ""
                    id_code = self.u.MD5(quancheng)
                    crawl_time = self.u.get_now_time()
                    sql = "insert into tmp_jobui(id, title, brief_intro, xingzhi, guimo, hangye, rongzi, quancheng, intro, crawl_time) " \
                          "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                          % (id_code, title, brief_intro, xingzhi,
                             guimo, hangye, rongzi, quancheng,
                             pymysql.escape_string(intro), crawl_time)
                    self.u.insert2mysql(title, sql)
                    print("-" * 100)
                    # time.sleep(3)
        else:
                print("请求失败,错误代码为:{}".format(req.status_code))

    def re_try(self):
        for rt in self.re_try_list:
            industry = re.findall(r'industry=(.*?)&', rt)[0]
            worker = re.findall(r'worker=(.*?)&', rt)[0]
            impression = re.findall(r'impression=(.*?)&', rt)[0]
            type = re.findall(r'type=(.*?)&', rt)[0]
            n = re.findall(r'n=(.*?)', rt)[0]

            self.base_data["industry"] = industry
            self.base_data["worker"] = worker
            self.base_data["impression"] = impression
            self.base_data["type"] = type
            self.base_data["n"] = n
            try:
                proxy_key = random.choice(list(self.proxies.keys()))
                print("<{}>".format(proxy_key))
                proxies = {proxy_key: self.proxies[proxy_key]}
                requests.packages.urllib3.disable_warnings()
                r = requests.get(url=rt, headers=self.headers, data=self.base_data, proxies=proxies)
                self.handle_data(r)
            except requests.exceptions.ConnectionError:
                self.re_try_list.append(rt)
                continue

    def main(self):
        proxy_key = random.choice(list(self.proxies.keys()))
        print("<{}>".format(proxy_key))
        proxies = {proxy_key: self.proxies[proxy_key]}
        try:
            requests.packages.urllib3.disable_warnings()
            res = requests.get(url=self.url, headers=self.headers, data=self.data, proxies=proxies, verify=False)
            print("请求状态码：" + str(res.status_code))
        except Exception as e:
            print("request has Error,Mes:" + str(e))
            time.sleep(300)
            proxy_key = random.choice(list(self.proxies.keys()))
            print("<{}>".format(proxy_key))
            proxies = {proxy_key: self.proxies[proxy_key]}
            requests.packages.urllib3.disable_warnings()
            res = requests.get(url=self.url, headers=self.headers, data=self.data, proxies=proxies, verify=False)
        if res.status_code == 200:
            html = self.u.get_xpath_obj(res.text)
            hangye = html.xpath("//div[@class=\"job-select-box\"]/ul/li[1]/div/div/a/text()")
            xingzhi = html.xpath("//div[@class=\"job-select-box\"]/ul/li[2]/div/div/a/text()")
            guimo = html.xpath("//div[@class=\"job-select-box\"]/ul/li[3]/div/div/a/text()")
            tese = html.xpath("//div[@class=\"job-select-box\"]/ul/li[4]/div/div/a/text()")
            for a in hangye[1:]:
                # time.sleep(10)
                for b in xingzhi[1:]:
                    # time.sleep(10)
                    for c in guimo[1:]:
                        # time.sleep(10)
                        for d in tese[1:]:
                            # time.sleep(5)
                            for i in range(1, 51):
                                # 构建请求地址
                                print("开始构建请求地址")
                                # time.sleep(2)
                                use_url = self.base_url.format(self.u.url_encode(a),
                                                               self.u.url_encode(c),
                                                               self.u.url_encode(d),
                                                               self.u.url_encode(b),
                                                               i)
                                # 构建请求参数列表
                                self.base_data["industry"] = a
                                self.base_data["worker"] = c
                                self.base_data["impression"] = d
                                self.base_data["type"] = b
                                try:
                                    proxy_key = random.choice(list(self.proxies.keys()))
                                    print("<{}>".format(proxy_key))
                                    proxies = {proxy_key: self.proxies[proxy_key]}
                                    requests.packages.urllib3.disable_warnings()
                                    r = requests.get(url=use_url, headers=self.headers, data=self.base_data, proxies=proxies)
                                except requests.exceptions.ConnectionError:
                                    self.re_try_list.append(use_url)
                                    continue
                                self.handle_data(r)
                            # time.sleep(10)
            self.re_try()
        elif res.status_code == 403:
            print("403 Forbidden")


if __name__ == '__main__':
    j = Jobui()
    j.main()




