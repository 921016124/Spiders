import time
from lxml import etree
from 网贷平台.UA import User_Agent
from pymongo import MongoClient
import requests
import random
import json


class ZhiShu:
    def __init__(self):
        self.url = "http://zhishu.analysys.cn/public/qianfan/appSearch/searchData"
        self.keywords = ["快递/配送", "外卖", "旅游预订"]
        self.data = {
            "words": "",
            "pageType": "all",
            "page": 1,
            "pageSize": 50,
        }
        self.headers = {
            "User-Agent": "",
            "Connection": "keep-alive",
        }

    @staticmethod
    def mongo():
        # Python 操作 MongoDB
        conn_mongo = MongoClient("127.0.0.1", 27017)
        db = conn_mongo.SunLine  # 连接 mydb 数据库，没有则自动创建
        return db.zhishu  # 使用test_set集合，没有则自动创建

    def run(self):
        my_set = self.mongo()
        for keyword in self.keywords:
            num = 0
            self.data["page"] = 1
            self.data["words"] = keyword
            ua = random.choice(User_Agent)
            self.headers["User-Agent"] = ua
            resonse = requests.post(url=self.url, headers=self.headers, data=self.data).text
            res = json.loads(resonse)
            try:
                pages = res["datas"]["totalPage"]
            except KeyError:
                print(self.data)
                exit()
            for page in range(1, pages + 1):
                ua = random.choice(User_Agent)
                self.data["page"] = page
                self.headers["User-Agent"] = ua
                res = requests.post(url=self.url, headers=self.headers, data=self.data).text
                res = json.loads(res)
                for i in res["datas"]["list"]:
                    s_item = {}
                    try:
                        s_item["APP名称"] = i["appName"]
                    except UnicodeEncodeError:
                        s_item["APP名称"] = i["appName"].encode("EUC_KR")
                    s_item["所属行业"] = i["tradeName"]
                    if i["developCompanyFullName"] is not None:
                        s_item["开发商"] = i["developCompanyFullName"]
                    else:
                        s_item["开发商"] = ""
                    if i["monthActiveNums"] is not None:
                        s_item["月指数(万)"] = round(i["monthActiveNums"], 1)
                    else:
                        s_item["月指数(万)"] = "--"
                    if i["monthActiveNumsRatio"] is not None:
                        s_item["上升指数"] = str(round(i["monthActiveNumsRatio"] * 100, 1)) + "%"
                    else:
                        s_item["上升指数"] = "--"
                    num += 1
                    my_set.insert_one(s_item)

                    print("-" * 50)
                print(self.data["words"] + "\t第{}页完成".format(page))
            print(num)


if __name__ == '__main__':
    zhishu = ZhiShu()
    zhishu.run()