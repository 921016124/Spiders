"""
url =  https://hf.anjuke.com/
method:post
"""
import requests
from lxml import etree
from pymongo import MongoClient


def Mongo():
    # Python 操作 MongoDB
    conn_mongo = MongoClient("127.0.0.1", 27017)
    db = conn_mongo.SunLine  # 连接 mydb 数据库，没有则自动创建
    return db.LianJia  # 使用test_set集合，没有则自动创建
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36",
            "Connection": "keep-alive",
        }
urls = ["https://sz.lianjia.com/xiaoqu/pg{}/?from=rec".format(i) for i in range(31)]


def request(url, headers=headers):
    while True:
        try:
            return requests.get(url=url, headers=headers)
        except Exception as e:
            print(e)
            print("网络已断开，请等待网络链接。。。。")
            import time
            time.sleep(10)


for url in urls:
    response = request(url=url)
    html = etree.HTML(response.text)
    items = html.xpath("//ul[@class=\"listContent\"]/li")
    for item in items:
        s_item = {}
        xiaoqu_url = item.xpath("./div[@class=\"info\"]/div[@class=\"title\"]/a/@href")[0]
        detail_response = request(url=xiaoqu_url, headers=headers)
        detail_html = etree.HTML(detail_response.text)
        xiaoqu_name = detail_html.xpath("//h1[@class=\"detailTitle\"]/text()")[0].encode('utf-8').decode()
        junjia = "".join(detail_html.xpath("//div[contains(@class,\"xiaoquPrice\")]/div[@class=\"fl\"]//text()")[:2])
        niandai = detail_html.xpath("//div[@class=\"xiaoquOverview\"]/div[contains(@class,\"xiaoquDescribe\")]/div[@class=\"xiaoquInfo\"]/div[1]/span[2]/text()")[0].encode('utf-8').decode()
        kaifashang = detail_html.xpath("//div[@class=\"xiaoquOverview\"]/div[contains(@class,\"xiaoquDescribe\")]/div[@class=\"xiaoquInfo\"]/div/span[contains(text(), \"开发商\")]/../span[2]/text()")[0].encode('utf-8').decode()
        s_item["xiaoqu_name"] = xiaoqu_name
        s_item["junjia"] = junjia
        s_item["niandai"] = niandai
        s_item["kaifashang"] = kaifashang
        my_set = Mongo()
        my_set.insert_one(s_item)
        print(xiaoqu_name)
        print(junjia)
        print(niandai)
        print(kaifashang)
        print("-" * 50)
