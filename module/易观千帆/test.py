import requests
import random
from 网贷平台.UA import User_Agent
import json

url = "http://zhishu.analysys.cn/public/qianfan/topRank/listTopRank?page=42&pageSize=200"
data = {
            "page": 42,
            "pageSize": 200,
            "cateId": "",
            "tradeId": "",
        }
headers = {
            "User-Agent": "",
            "Connection": "keep-alive",
        }
resonse = requests.post(url=url, headers=headers, data=data).text
res = json.loads(resonse)
for i in range(1, res["datas"]["totalPage"] + 1):
    print(" * " * 50)
    data["page"] = i
    ua = random.choice(User_Agent)
    headers["User-Agent"] = ua
    print(data)
    resonse = requests.post(url=url, headers=headers, data=data).text
    res = json.loads(resonse)
    for i in res["datas"]["list"]:
        print(i["appName"])
