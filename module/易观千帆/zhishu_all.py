import requests
import random
from 网贷平台.UA import User_Agent
import json
from pymongo import MongoClient


class ZhiShuAll:
    def __init__(self):
        self.url = "http://zhishu.analysys.cn/public/qianfan/topRank/listTopRank?page={}&pageSize=200&cateId=&tradeId="
        self.headers = {
            "User-Agent": "",
            "Connection": "keep-alive",
        }
        self.data = {
            "page": 1,
            "pageSize": 200,
            "cateId": "",
            "tradeId": "",
        }

    @staticmethod
    def mongo():
        # Python 操作 MongoDB
        conn_mongo = MongoClient("127.0.0.1", 27017)
        db = conn_mongo.SunLine  # 连接 mydb 数据库，没有则自动创建
        return db.zhishu_all  # 使用test_set集合，没有则自动创建

    def run(self):
        my_set = self.mongo()
        for page in range(1, 43):
            ua = random.choice(User_Agent)
            self.headers["User-Agent"] = ua
            self.data["page"] = page
            url = self.url.format(page)
            print(self.data)
            print(url)
            resonse = requests.get(url=url, headers=self.headers, data=self.data).text
            res = json.loads(resonse)
            for i in res["datas"]["list"]:
                s_item = {}
                try:
                    s_item["APP名称"] = i["appName"]
                except UnicodeEncodeError:
                    s_item["APP名称"] = i["appName"].encode("EUC_KR")
                s_item["所属行业"] = i["cateName"] + ">" + i["tradeName"]
                if i["developCompanyFullName"] is not None:
                    s_item["开发商"] = i["developCompanyFullName"]
                else:
                    s_item["开发商"] = ""
                if i["monthActiveNums"] is not None:
                    s_item["月指数(万)"] = round(i["monthActiveNums"], 1)
                else:
                    s_item["月指数(万)"] = "--"
                if i["monthActiveNumsRatio"] is not None:
                    if round(i["monthActiveNumsRatio"] * 100, 1) > 0:
                        s_item["上升指数(月)"] = "+" + str(round(i["monthActiveNumsRatio"] * 100, 1)) + "%"
                    else:
                        s_item["上升指数(月)"] = str(round(i["monthActiveNumsRatio"] * 100, 1)) + "%"
                else:
                    s_item["上升指数(月)"] = "--"
                if i["dayActiveNums"] is not None:
                    s_item["日指数(万)"] = round(i["dayActiveNums"], 1)
                else:
                    s_item["日指数(万)"] = "--"
                if i["dayActiveNumsRatio"] is not None:
                    if round(i["dayActiveNumsRatio"] * 100, 1) > 0:
                        s_item["上升指数(日)"] = "+" + str(round(i["dayActiveNumsRatio"] * 100, 1)) + "%"
                    else:
                        s_item["上升指数(日)"] = str(round(i["dayActiveNumsRatio"] * 100, 1)) + "%"
                else:
                    s_item["上升指数(日)"] = "--"

                my_set.insert_one(s_item)
                print("-" * 50)


if __name__ == '__main__':
    zhishu_all = ZhiShuAll()
    zhishu_all.run()
