import requests
from lxml import etree
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
    return db.wdzj  # 使用test_set集合，没有则自动创建


currentNum = 1
url = "https://www.wdzj.com/dangan/search?filter&currentPage=1"
my_set = Mongo()

while True:
    print("第{}页开始爬取".format(currentNum))
    response = requests.get(url=url, headers=headers, verify=True)

    html = etree.HTML(response.text)
    items = html.xpath("//ul[@class=\"terraceList\"]/li")
    for item in items:
        s_item ={}
        item_url = item.xpath(".//h2/a/@href")[0]
        item_name = item_url.split("/")[2]
        detail_url = "https://www.wdzj.com/dangan/{}/gongshang/".format(item_name)

        detail_response = requests.get(url=detail_url, headers=headers, verify=True).text.encode("ISO-8859-1").decode("utf-8")
        detail_html = etree.HTML(detail_response)

        # 工商信息
        if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[1]/td[2]/text()"):
            s_item["公司名称"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[1]/td[2]/text()")[0]
        else:
            s_item["公司名称"] = ""
        if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[2]/td[2]/text()"):
            s_item["法人代表"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[2]/td[2]/text()")[0]
        else:
            s_item["法人代表"] = ""
        if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[4]/td[4]/text()"):
            s_item["开业日期"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[4]/td[4]/text()")[0]
        else:
            s_item["开业日期"] = ""
        if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[5]/td[2]/text()"):
            s_item["在营（开业）企业"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[5]/td[2]/text()")[0]
        else:
            s_item["在营（开业）企业"] = ""
        if detail_html.xpath("//div[@class=\"lcen\"]/table/tr[6]/td[4]/text()"):
            s_item["核准日期"] = detail_html.xpath("//div[@class=\"lcen\"]/table/tr[6]/td[4]/text()")[0]
        else:
            s_item["核准日期"] = ""
            # 股权信息
        s_item["股权信息"] = ";".join(detail_html.xpath("//div[@id=\"gqInfoBox\"]/div[@class=\"table-ic-box\"]/table/tbody[1]/tr/td[1]/text()"))

        # 异常经营
        exception_info = detail_html.xpath("//div[@class=\"containerBox\"]/div[last()]/div/table/tbody[1]/tr/td[2]/text()")
        if exception_info:
            s_item["列入经营异常原因"] = exception_info[0]
        else:
            s_item["列入经营异常原因"] = ""
        exception_RegiDate = detail_html.xpath("//div[@class=\"containerBox\"]/div[last()]/div/table/tbody[1]/tr/td[3]/text()")
        if exception_RegiDate:
            s_item["列入日期"] = exception_RegiDate[0]
        else:
            s_item["列入日期"] = ""
        exception_RegiOffice = detail_html.xpath("//div[@class=\"containerBox\"]/div[last()]/div/table/tbody[1]/tr/td[4]/text()")
        if exception_RegiOffice:
            s_item["决定机关(列入)"] = exception_RegiOffice[0]
        else:
            s_item["决定机关(列入)"] = ""
        # exception_OutReason = detail_html.xpath("//div[@class=\"containerBox\"]/div[last()]/div/table/tbody[1]/tr/td[5]/text()")
        # if exception_OutReason:
        #     s_item["移除经营异常原因"] = exception_OutReason[0]
        # else:
        #     s_item["移除经营异常原因"] = ""
        # exception_OutDate = detail_html.xpath("//div[@class=\"containerBox\"]/div[last()]/div/table/tbody[1]/tr/td[6]/text()")
        # if exception_OutDate:
        #     s_item["移除日期"] = exception_OutDate[0]
        # else:
        #     s_item["移除日期"] = ""
        # exception_OutOffice = detail_html.xpath("//div[@class=\"containerBox\"]/div[last()]/div/table/tbody[1]/tr/td[7]/text()")
        # if exception_OutOffice:
        #     s_item["决定机关(移除)"] = exception_OutOffice[0]
        # else:
        #     s_item["决定机关(移除)"] = ""

        print(s_item["公司名称"])
        # print("法人: " + s_item["法人"])
        # print("开业日期: " + s_item["开业日期"])
        # print("状态: " + s_item["状态"])
        # print("核准日期：" + s_item["核准日期"])
        #
        # print("股权信息：" + s_item["股权信息"])
        #
        # print("列入经营异常原因：" + s_item["列入经营异常原因"])
        # print("列入日期：" + s_item["列入日期"])
        # print("决定机关（列入）：" + s_item["exception_RegiOffice"])
        # print("移除经营异常原因：" + s_item["exception_OutReason"])
        # print("移除日期：" + s_item["exception_OutDate"])
        # print("决定机关（移除）：" + s_item["exception_OutOffice"])
        my_set.insert_one(s_item)
    print("第{}页爬取结束".format(currentNum))
    if html.xpath("//div[@class=\"pageList\"]/a[contains(text(),\"下一页\")]"):
        import re
        currentNum = re.findall(r'class="pageindex" currentNum="(.*?)">下一页</a>', response.text)[0]
        url = "https://www.wdzj.com/dangan/search?filter&currentPage={}".format(currentNum)
    else:
        break
