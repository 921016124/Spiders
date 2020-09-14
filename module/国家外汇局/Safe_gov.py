import requests
from lxml import etree


class SafeGov(object):
    """
        此爬虫是为了平安银行-张文澜提出的，后期需要部署，需要长期运行 ，
        原网页链接：http://m.safe.gov.cn/safe/whxzcfxxcx/index.html
    """
    """
        TODO:
                1. 增加对结果页的翻页
                2. 增加入库部分代码
                3. 增加读取文件部分代码
    """
    def __init__(self):
        self.url = "http://m.safe.gov.cn/www/illegal/illegalQuery"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "24",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "JSESSIONID=22631293531D9EA0434E87B127C231C5; "
                      "X-Mapping-dkmommhp=1302614F04B9E598435B9969B334E0D7; gotopc=false; "
                      "__utrace=7946f827b25cb19de2acc9aba370821d",
            "Host": "m.safe.gov.cn",
            "Origin": "http://m.safe.gov.cn",
            "Referer": "http://m.safe.gov.cn/www/illegal/illegalQuery",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
        self.data = {
            "irregularityno": ""
        }
        self.detail_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,"
                      "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Cookie": "JSESSIONID=22631293531D9EA0434E87B127C231C5; "
                      "X-Mapping-dkmommhp=1302614F04B9E598435B9969B334E0D7; gotopc=false; "
                      "__utrace=7946f827b25cb19de2acc9aba370821d",
            "Host": "m.safe.gov.cn",
            "Referer": "http://m.safe.gov.cn/www/illegal/illegalQuery",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
        self.spider_queue = []

    def load(self):
        with open("credit_code.txt", 'r', encoding="utf-8") as f:
            return f.read()

    def parse(self):
        # i = input("代码：")
        self.data["irregularityno"] = "676660535"
        res = requests.post(url=self.url, headers=self.headers, data=self.data)
        ls_html = etree.HTML(res.text)
        # print(res.text)
        for ls in ls_html.xpath("//table/tr")[1:]:
            self.spider_queue.append("http://m.safe.gov.cn" + ls.xpath("./td[2]/a/@href")[0])

    def parse_item(self):
        for item_url in self.spider_queue:
            symbol = violation_nm = legal_person = lp_ID = registered_address = ""
            credit_code = administrative_organ_nm = penalty_time = illegal_tp = ""
            illegal_facts = punishment_basis = punishment_category = punishment_content = ""
            amount_penalty = forfeiture_amount = penalty_decision_date = deadline_for_publicity = ""
            remarks = ""
            detail_res = requests.get(url=item_url, headers=self.detail_headers)
            detail_html = etree.HTML(detail_res.text)
            for col in detail_html.xpath("//table/tr"):
                if col.xpath("./th/text()")[0] == "行政处罚决定书文号":
                    symbol = col.xpath("./td/text()")[0]  # 行政处罚决定书文号
                    print("行政处罚决定书文号: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "违规主体名称":
                    violation_nm = col.xpath("./td/text()")[0]
                    print("违规主体名称: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "法定代表人或负责人姓名":
                    legal_person = col.xpath("./td/text()")[0]
                    print("法定代表人或负责人姓名: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "法定代表人或负责人有效身份证件号码":
                    lp_ID = col.xpath("./td/text()")[0]
                    print("法定代表人或负责人有效身份证件号码: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "注册地址":
                    credit_code = col.xpath("./td/text()")[0]
                    print("注册地址	: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "统一社会信用代码或组织机构代码":
                    administrative_organ_nm = col.xpath("./td/text()")[0]
                    print("统一社会信用代码或组织机构代码: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "作出处罚决定的行政机关名称":
                    penalty_time = col.xpath("./td/text()")[0]
                    print("作出处罚决定的行政机关名称: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "处罚时间（时限）":
                    illegal_tp = col.xpath("./td/text()")[0]
                    print("处罚时间（时限）: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "违法行为类型":
                    illegal_facts = col.xpath("./td/text()")[0]
                    print("违法行为类型: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "违法事实":
                    illegal_facts = col.xpath("./td/text()")[0]
                    print("违法事实	: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "处罚依据":
                    punishment_basis = col.xpath("./td/text()")[0]
                    print("处罚依据: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "处罚类别":
                    punishment_category = col.xpath("./td/text()")[0]
                    print("处罚类别: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "处罚内容":
                    punishment_content = col.xpath("./td/text()")[0]
                    print("处罚内容	: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "处罚金额（万元）":
                    amount_penalty = col.xpath("./td/text()")[0]
                    print("处罚金额（万元）: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "没收金额（万元）":
                    forfeiture_amount = col.xpath("./td/text()")[0]
                    print("没收金额（万元）: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "处罚决定日期":
                    penalty_decision_date = col.xpath("./td/text()")[0]
                    print("处罚决定日期: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "公示截止期":
                    deadline_for_publicity = col.xpath("./td/text()")[0]  # 公示截止期
                    print("公示截止期: " + col.xpath("./td/text()")[0])
                elif col.xpath("./th/text()")[0] == "备注":
                    remarks = col.xpath("./td/text()")[0]  # 备注
                    print("备注: " + col.xpath("./td/text()")[0])


if __name__ == '__main__':
    sg = SafeGov()
    sg.parse()
    sg.parse_item()
