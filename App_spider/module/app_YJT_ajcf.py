import requests
import time
import sys
import os
sys.path.append("../")
from Utils_2 import Util
import pdfkit

"""
    手机app预警通 的诚信大数据 安监处罚的抓取 
"""


class Yjt:
    def __init__(self):
        self.u = Util()
        self.url = "https://app.finchina.com/finchinaAPP/getOrgFamilyCreaditData_SE.action?selTopRecommended=%E5%AE%89%E7%9B%91%E5%A4%84%E7%BD%9A&skip={}"
            #"https://app.finchina.com/finchinaAPP/getBondsDefaultDynamics.action?pageNum={}&pageSize=15"
        self.file = "Scrapyed_ajcf.txt"
        self.headers = {
            "Host": "app.finchina.com",
            "client": "finchina",
            "system": "v4.3.1.551,13.2.3,iOS,iPhone,iPhone,iPhone11,8",
            "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
            "Accept-Language": "zh-Hans-CN;q=1.0",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Referer": "https://app.finchina.com/finchinaAPP/f9/creditArchives/creditDetail.html?user=20191212160004_15561585051&id={}&getContent=0&token=d92c8173-ed6d-4069-8e1c-7a81b5e1af3c&companyName={}",
            "token": "d92c8173-ed6d-4069-8e1c-7a81b5e1af3c",
            "X-Requested-With": "XMLHttpRequest"
        }

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding="utf8") as f:
                return f.read()
        else:
            print("文件不存在！！！！")

    def main(self):
        for i in range(1, 11):
            print("第{}页".format(i))
            req = requests.get(url=self.url.format(i), headers=self.headers)
            # print(req.text)
            self.parse(req, i)
            time.sleep(10)

    def parse(self, response, i):
        try:
            if self.u.get_json_obj(response.text)["returncode"] == 0:
                datas = self.u.get_json_obj(response.text)["data"]
                # print(datas)
                if len(datas):
                    for data in datas:
                        id_code = data["infoId"]
                        name = data["related"][0]["name"]
                        type = data["type"]
                        if id_code not in self.load():
                            self.headers["Referer"] = self.headers["Referer"].format(id_code, self.u.url_encode(name))
                            self.headers["User-Agent"] = self.u.get_random_ua()
                            self.parse_detail(
                                requests.get(
                                    url="https://app.finchina.com/finchinaAPP/getOrgFamilyCreaditDataContentDetails.action?type={}&getContent=0&id={}".format(type, id_code), headers=self.headers))
                            with open(self.file, 'a', encoding="utf8") as f:
                                f.write(id_code + "\n")
                        else:
                            print("...")
                        time.sleep(5)
                    print("-" * 100)
                else:
                    exit("数据抓取完成")
            else:
                print(self.u.get_json_obj(response.text)["returncode"])
                print("响应错误！！！")
                time.sleep(30)
                req = requests.get(url=self.url.format(i), headers=self.headers)
                self.parse(req, i)
        except IndexError as e:
            print(e)
            time.sleep(30)
            req = requests.get(url=self.url.format(i), headers=self.headers)
            self.parse(req, i)

    def parse_detail(self, response):
        detail_datas = self.u.get_json_obj(response.text)["data"]
        for i in detail_datas:
            print("*" * 100)
            id = i["infoid"]
            pub_date = i["it0026_006"]  # 披露日期
            about_people = i["it0026_005"]  # 当事人
            handle_people = i["it0026_016"]  # 处理人
            punish_type = i["risk"][0]["name"]  # 处罚类型
            irregularities = i["it0026_009"]  # 违法行为
            punish_content = i["it0026_011"]  # 处罚内容
            symbol_num = i["source"]  # 文号
            file_url = i["file"][0]["fileUrl"]
            file_name = i["file"][0]["fileName"].replace(":", "_").replace("*", "")
            print("id: " + id + "\n"
                  + "pub_date: " + pub_date + "\n"
                  + "about_people: " + about_people + "\n"
                  + "handle_people: " + handle_people + "\n"
                  + "punish_type: " + punish_type + "\n"
                  + "irregularities: " + irregularities + "\n"
                  + "punish_content: " + punish_content + "\n"
                  + "symbol_num: " + symbol_num + "\n"
                  + "file_url: " + file_url + "\n"
                  + "file_name: " + file_name
                  )
            if file_url:
                if str.endswith(file_url, "pdf"):
                    if os.path.exists('./Files/ajcf/{}.pdf'.format(file_name)):
                        pass
                    else:
                        with open('./Files/ajcf/{}.pdf'.format(file_name), "wb+") as f:
                            f.write(requests.get(url=file_url).content)
                            print(file_name + " 保存完成！")
                elif str.endswith(file_url, "html") | str.endswith(file_url, "htm"):
                    if os.path.exists('./Files/ajcf/{}.pdf'.format(file_name)):
                        pass
                    else:
                        options = {
                            'encoding': "UTF-8",
                        }
                        try:
                            confg = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
                            pdfkit.from_url(file_url, './Files/ajcf/{}.pdf'.format(file_name), configuration=confg, options=options)
                        except Exception as e:
                            print(e)
                elif str.endswith(file_url, "doc"):
                    if os.path.exists('./Files/ajcf/{}.doc'.format(file_name)):
                        pass
                    else:
                        with open('./Files/ajcf/{}.doc'.format(file_name), "wb+") as f:
                            f.write(requests.get(url=file_url).content)
                            print(file_name + " 保存完成！")

            ajcf_data = (
                            id, pub_date, about_people,
                            handle_people, punish_type,
                            irregularities, punish_content, symbol_num, file_url,
                            file_name, self.u.get_now_time())
            self.u.insert2mysql(about_people, self.ajcf_sql(ajcf_data))

    def ajcf_sql(self, data):
        sql = """insert into 
        yjt_ajcf(id, pub_date, about_people,handle_people, punish_type, irregularities, 
        punish_content, symbol_num, file_url, file_name, crawl_time) 
        values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % data
        return sql


if __name__ == '__main__':
    while True:
        yjt = Yjt()
        yjt.main()
        print("此阶段抓取结束，等待下次抓取。。。")
        time.sleep(1800)
