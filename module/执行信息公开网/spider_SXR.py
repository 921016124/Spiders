import requests
from lxml import etree
import time
import json
import urllib
from pymongo import MongoClient
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36",
            "Connection": "keep-alive",
        }


def Mongo():
    # Python 操作 MongoDB
    conn_mongo = MongoClient("127.0.0.1", 27017)
    db = conn_mongo.SunLine  # 连接 mydb 数据库，没有则自动创建
    return db.SXR  # 使用test_set集合，没有则自动创建


def get_yanzheng_pic(html):
    yanzheng_Pic = "http://zxgk.court.gov.cn/zhzxgk/" + html.xpath("//img[@id=\"captchaImg\"]/@src")[0]

    yz_pic = requests.get(url=yanzheng_Pic, headers=headers).content
    with open("yanzhen.jpg", 'wb') as fp:
        fp.write(yz_pic)


start_response = requests.get(url="http://zxgk.court.gov.cn/zhzxgk/", headers=headers)
start_html = etree.HTML(start_response.text)
get_yanzheng_pic(start_html)

captchaId = start_html.xpath("//input[@id=\"captchaId\"]/@value")[0]
# name = input("请输入失信被执行人的完整姓名：")
yanzheng = input("请参照本目录下《yanzheng.jpg》 输入验证码：")



data = {
    "pName": "边强",
    "pCardNum": "",
    "selectCourtId": 0,
    "pCode": yanzheng,
    "captchaId": captchaId,
    "searchCourtName": "全国法院（包含地方各级法院）",
    "selectCourtArrange": 1,
    "currentPage": 1,  # data["currentPage"] =
}
r = requests.post(url="http://zxgk.court.gov.cn/zhzxgk/searchZhcx.do", headers=headers, data=data)
res = r.text[1:-1]
html = etree.HTML(r.text)
res = json.loads(res)
encode_name = urllib.parse.quote("边强")
end = res["totalPage"] + 2
for it in range(2, end):  # 页循环
    for i in res["result"]:  # 数据循环
        s_item = {}
        encode_fileName = urllib.parse.quote(i["caseCode"].strip())  # 完成对单页的案号的获取
        crawl_url = "http://zxgk.court.gov.cn/zhzxgk/detailZhcx.do?pnameNewDel=" + encode_name + "&cardNumNewDel=&j_captchaNewDel="+yanzheng+"&caseCodeNewDel=" + encode_fileName + "&captchaIdNewDel=" + captchaId  # 生成失信记录的详情页请求地址
        # 拿到搜索结果中的一条数据，进行数据抽取
        print("请求开始！~~~")
        try:
            crawl_response = requests.get(url=crawl_url, headers=headers, timeout=10)
            crawl_html = etree.HTML(crawl_response.text)
            print("请求成功")
        except requests.exceptions.ConnectionError as e:
            print("请求失败！网络超时")


        # 存入对象
        if crawl_html.xpath("//td[@id=\"inameDetail\"]/text()"):
            s_item["被执行人"] = crawl_html.xpath("//td[@id=\"inameDetail\"]/text()")[0]
        else:
            if crawl_html.xpath("//td[@id=\"pnameDetail\"]/text()"):
                s_item["被执行人"] = crawl_html.xpath("//td[@id=\"pnameDetail\"]/text()")[0]
            else:
                if crawl_html.xpath("//td[@id=\"xmDetail\"]/text()"):
                    s_item["被执行人"] = crawl_html.xpath("//td[@id=\"xmDetail\"]/text()")[0]
                else:
                    s_item["被执行人"] = ""

        if crawl_html.xpath("//td[@id=\"sexDetail\"]/text()"):
            s_item["性别"] = crawl_html.xpath("//td[@id=\"sexDetail\"]/text()")[0].replace("性", "")
        else:
            if crawl_html.xpath("//td[@id=\"Detail\"]/text()"):
                s_item["性别"] = crawl_html.xpath("//td[@id=\"Detail\"]/text()")[0].replace("性", "")
            else:
                if crawl_html.xpath("//td[@id=\"xmDetail\"]/text()"):
                    s_item["性别"] = crawl_html.xpath("//td[@id=\"xmDetail\"]/text()")[0].replace("性", "")
                else:
                    s_item["性别"] = ""
        if crawl_html.xpath("//td[@id=\"cardNumDetail\"]/text()"):
            s_item["身份证号码/组织机构代码"] = crawl_html.xpath("//td[@id=\"cardNumDetail\"]/text()")[0]
        else:
            if crawl_html.xpath("//td[@id=\"pnameDetail\"]/text()"):
                s_item["身份证号码/组织机构代码"] = crawl_html.xpath("//td[@id=\"partyCardNumDetail\"]/text()")[0]
            else:
                if crawl_html.xpath("//td[@id=\"sfzhmDetail\"]/text()"):
                    s_item["身份证号码/组织机构代码"] = crawl_html.xpath("//td[@id=\"sfzhmDetail\"]/text()")[0]
                else:
                    s_item["身份证号码/组织机构代码"] = ""
        if crawl_html.xpath("//td[@id=\"courtNameDetail\"]/text()"):
            s_item["执行法院"] = crawl_html.xpath("//td[@id=\"courtNameDetail\"]/text()")[0]
        else:
            if crawl_html.xpath("//td[@id=\"execCourtNameDetail\"]/text()"):
                s_item["执行法院"] = crawl_html.xpath("//td[@id=\"execCourtNameDetail\"]/text()")[0]
            else:
                if crawl_html.xpath("//td[@id=\"zxfymcDetail\"]/text()"):
                    s_item["执行法院"] = crawl_html.xpath("//td[@id=\"zxfymcDetail\"]/text()")[0]
                else:
                    s_item["执行法院"] = ""
        if crawl_html.xpath("//td[@id=\"areaNameDetail\"]/text()"):
            s_item["省份"] = crawl_html.xpath("//td[@id=\"areaNameDetail\"]/text()")[0]
        else:
            s_item["省份"] = ""
        if crawl_html.xpath("//td[@id=\"gistIdDetail\"]/text()"):
            s_item["执行依据文号"] = crawl_html.xpath("//td[@id=\"gistIdDetail\"]/text()")[0]
        else:
            s_item["执行依据文号"] = ""
        if crawl_html.xpath("//td[@id=\"regDateDetail\"]/text()"):
            s_item["立案时间"] = crawl_html.xpath("//td[@id=\"regDateDetail\"]/text()")[0]
        else:
            if crawl_html.xpath("//td[@id=\"larqDetail\"]/text()"):
                s_item["立案时间"] = crawl_html.xpath("//td[@id=\"larqDetail\"]/text()")[0]
            else:
                s_item["立案时间"] = ""
        if i["caseCode"].strip():
            s_item["案号"] = i["caseCode"].strip()
        else:
            if crawl_html.xpath("//td[@id=\"caseCodeDetail\"]/text()") :
                s_item["案号"] = crawl_html.xpath("//td[@id=\"caseCodeDetail\"]/text()")
            else:
                s_item["案号"] = ""
        if crawl_html.xpath("//td[@id=\"gistUnitDetail\"]/text()"):
            s_item["做出执行依据单位"] = crawl_html.xpath("//td[@id=\"gistUnitDetail\"]/text()")[0]
        else:
            s_item["做出执行依据单位"] = ""
        if crawl_html.xpath("//td[@id=\"dutyDetail\"]/text()"):
            s_item["生效法律文书确定的义务"] = crawl_html.xpath("//td[@id=\"dutyDetail\"]/text()")[0]
        else:
            s_item["生效法律文书确定的义务"] = ""
        if crawl_html.xpath("//td[@id=\"performanceDetail\"]/text()"):
            s_item["被执行人的履行情况"] = crawl_html.xpath("//td[@id=\"performanceDetail\"]/text()")[0]
        else:
            s_item["被执行人的履行情况"] = ""
        if crawl_html.xpath("//td[@id=\"disruptTypeNameDetail\"]/text()"):
            s_item["失信被执行人行为具体情形"] = crawl_html.xpath("//td[@id=\"disruptTypeNameDetail\"]/text()")[0]
        else:
            s_item["失信被执行人行为具体情形"] = ""
        if crawl_html.xpath("//td[@id=\"publishDateDetail\"]/text()"):
            s_item["发布时间"] = crawl_html.xpath("//td[@id=\"publishDateDetail\"]/text()")[0]
        else:
            s_item["发布时间"] = ""
        if crawl_html.xpath("//td[@id=\"sqzxbdjeDetail\"]/text()"):
            s_item["执行标的"] = crawl_html.xpath("//td[@id=\"sqzxbdjeDetail\"]/text()")[0]
        else:
            if crawl_html.xpath("//td[@id=\"execMoneyDetail\"]/text()"):
                s_item["执行标的"] = crawl_html.xpath("//td[@id=\"execMoneyDetail\"]/text()")[0]
            else:
                s_item["执行标的"] = ""
        if crawl_html.xpath("//td[@id=\"swzxbdjeDetail\"]/text()"):
            s_item["未履行金额"] = crawl_html.xpath("//td[@id=\"swzxbdjeDetail\"]/text()")[0]
        else:
            s_item["未履行金额"] = ""
        print(s_item)

        my_set = Mongo()
        my_set.insert_one(s_item)
        time.sleep(2)
    data["currentPage"] = it
    r = requests.post(url="http://zxgk.court.gov.cn/zhzxgk/searchZhcx.do", headers=headers, data=data)
    res = r.text[1:-1]
    html = etree.HTML(r.text)
    try:
        res = json.loads(res)
    except json.decoder.JSONDecodeError as e:
        print(res)
        continue
    print("第{}页执行完毕".format(int(it) - 1))
