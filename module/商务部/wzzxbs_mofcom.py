import requests
from Utils_1 import Util
import re
from lxml import etree
import time
from my_fake_useragent import UserAgent
import pymysql
import socket
socket.setdefaulttimeout(20)


class WzzxbsMofocom:
    def __init__(self):
        self.url = "http://wzzxbs.mofcom.gov.cn/WebProSP/infoPub/record/loadRecordData.action"
        self.detail_base_url = "http://wzzxbs.mofcom.gov.cn/WebProSP/infoPub/record/loadEntpRecordDetails.action?params.recordId={}&time={}"
        self.headers = {
            "Accept": "application/json, text/javascript, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Length": "169",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "insert_cookie=32151754",
            "Host": "wzzxbs.mofcom.gov.cn",
            "Origin": "http://wzzxbs.mofcom.gov.cn",
            "Referer": "http://wzzxbs.mofcom.gov.cn/WebProSP/app/infoPub/entpRecord",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.detail_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "insert_cookie=32151754",
            "Host": "wzzxbs.mofcom.gov.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        self.data = {
            "params.entpName": "",
            "page.currentPage": "",
            "page.limit": "2000",
            "page.option": "next",
            "page.start": "",
            "page.rowCount": "",
            "listGrid.col": "1:showRecordInfo(0),2,3,4",
            "listGrid.type": "link,ro,ro,ro"
        }
        self.detail_data = {
            "params.recordId": "",
            "time": ""
        }
        self.util = Util()
        self.user_agent = UserAgent()

    def parse_18(self, detail_html, business_type):
        # 一、备案情况
        item_content = detail_html.xpath("//div[@class=\"Table1\"]/table/tr[3]/td/text()")[0].replace("\xe5", "")  # 变更事项
        # print(item_content)
        item_date = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[4]/td/text()")[0].replace("\xe5", "")  # 完成备案时间
        # print(item_date)
        item_number = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[5]/td/text()")[0].replace("\xe5", "")  # 备案号
        # print(item_number)

        # 二、外商投资企业基本信息
        comp_name = detail_html.xpath("//div[@class=\"Table1\"]/table/tr[7]/td/text()")[0].replace("\ue07e", "").replace("\xe5", "")  # 公司名称
        # print(comp_name)
        regi_addr = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[8]/td/text()")[0].replace('\u3bbe', '').replace('\ue07e', '').replace("\xe5", "").replace("\ue096", "")  # 注册地址
        # print(regi_addr)
        try:
            crit_code = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[9]/td/text()")[0].replace("\xe5", "")  # 统一社会信用代码
        except IndexError:
            crit_code = ""
        # print(crit_code)
        comp_type = re.findall(r'checked="checked"/> (.*?)&#13;',
                               str(etree.tostring(
                                   detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[10]/td")[0],
                                   encoding='utf-8'), 'utf-8')
                               .strip().replace("\xe5", "")
                               , re.S)[0]  # 企业类型
        # print(comp_type)
        operating_period = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[11]/td/text()")[0].strip().replace("\xe5", "")  # 经营期限
        # print(operating_period)
        try:
            investment_industry = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[12]/td/text()")[0].replace("\xe5", "")  # 投资行业
        except Exception:
            investment_industry = ""
        # print(investment_industry)
        business_scope = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[13]/td/text()")[0].replace("\xe5", "").replace("\xe5", "")  # 经营范围
        # print(business_scope)
        try:
            total_investment = \
            str.split(detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[14]/td/text()")[0], " ")[0].replace(
                "\xa0", "").replace("\xe5", "").replace("\ue07e", "")
        except IndexError:
            total_investment = ""
        # print(total_investment)
        registered_capital = str.split(detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[15]/td/text()")[0], " ")[
            0].replace("\xa0", "").replace("\xe5", "").replace("\ue07e", "")  # 注册资本
        # print(registered_capital)
        try:
            legal_representative = \
            str.split(detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[16]/td/text()")[0], " ")[0].replace(
                "\xa0", "").replace("\xe5", "").replace("\ue07e", "").replace("\u4b72", " ")  # 法定代表人
        except IndexError:
            legal_representative = ""
        # print(legal_representative)
        md5_id = comp_name + business_type + item_date + item_number
        cols = (self.util.MD5(item_number), business_type, item_content, item_date, item_number,
                comp_name, regi_addr, crit_code, comp_type, operating_period, investment_industry,
                business_scope, total_investment, registered_capital, pymysql.escape_string(legal_representative),
                self.util.MD5(md5_id), self.util.get_now_time())
        s = self.get_sql(cols)
        self.util.insert2mysql(comp_name, s)
        return md5_id, item_number

    def parse_17(self, detail_html, business_type):
        item_content = ""  # 变更事项
        item_date = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[3]/td/text()")[0].replace("\xe5", "")  # 完成备案时间
        # print(item_date)
        item_number = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[4]/td/text()")[0].replace("\xe5", "")  # 备案号
        # print(item_number)

        # 二、外商投资企业基本信息
        comp_name = detail_html.xpath("//div[@class=\"Table1\"]/table/tr[6]/td/text()")[0].replace("\ue07e", "").replace("\xe5", "")  # 公司名称
        # print(comp_name)
        regi_addr = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[7]/td/text()")[0].replace('\u3bbe', '').replace('\ue07e', '').replace("\xe5", "").replace("\ue096", "")  # 注册地址
        # print(regi_addr)
        try:
            crit_code = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[8]/td/text()")[0].replace("\xe5", "")  # 统一社会信用代码
        except IndexError:
            crit_code = ""
        # print(crit_code)
        comp_type = re.findall(r'checked="checked"/> (.*?)&#13;',
                               str(etree.tostring(
                                   detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[9]/td")[0],
                                   encoding='utf-8'), 'utf-8')
                               # .replace("&#13;", "").replace("<input", "").replace("\n", "")
                               .strip().replace("\xe5", ""), re.S)[0]  # 企业类型
        # print(comp_type)
        operating_period = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[10]/td/text()")[0].strip().replace("\xe5", "")  # 经营期限
        # print(operating_period)
        try:
            investment_industry = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[11]/td/text()")[0].replace("\xe5", "")  # 投资行业
        except Exception:
            investment_industry = ""
        # print(investment_industry)
        business_scope = detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[12]/td/text()")[0].replace("\xe5", "").replace("\xe5", "")  # 经营范围
        # print(business_scope)
        try:
            total_investment = \
            str.split(detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[13]/td/text()")[0], " ")[0].replace(
                "\xa0", "").replace("\xe5", "")  # 投资总额
        except IndexError:
            total_investment = ""
        # print(total_investment)
        registered_capital = str.split(detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[14]/td/text()")[0], " ")[
            0].replace("\xa0", "").replace("\xe5", "")  # 注册资本
        # print(registered_capital)
        try:
            legal_representative = \
            str.split(detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr[15]/td/text()")[0], " ")[0].replace(
                "\xa0", "").replace("\xd6", "").replace("\xe5", "")  # 法定代表人
        except IndexError:
            legal_representative = ""
        # print(legal_representative)
        md5_id = comp_name + business_type + item_date + item_number
        cols = (self.util.MD5(item_number), business_type, item_content, item_date, item_number,
         comp_name, regi_addr, crit_code, comp_type, operating_period, investment_industry,
         business_scope, total_investment, registered_capital, pymysql.escape_string(legal_representative),
         self.util.MD5(md5_id),
         self.util.get_now_time())
        self.util.insert2mysql(comp_name, self.get_sql(cols))
        return md5_id, item_number

    def get_sql(self, col_tuple):
        info_sql = """
                            insert into wzzxbs_mofcom_info(
                            id,
                            business_type,
                            item_content,
                            item_date,
                            item_number,
                            comp_name,
                            regi_addr,
                            crit_code,
                            comp_type,
                            operating_period,
                            investment_industry,
                            business_scope,
                            total_investment,
                            registered_capital,
                            legal_representative,
                            cust_id,
                            craw_time
                            )values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
                        """ % col_tuple
        return info_sql

    def parse_invesment_info(self, detail_html, md5_id, n):
        for mes in detail_html.xpath("//div[@class=\"Table1\"]/table/tr[{}]/table/tr".format(n))[1:]:
            name_of_investor = str.split(mes.xpath("./td[1]/text()")[0], " ")[0]\
                .replace("\ue07e", "")\
                .replace("\xe5", "")\
                .replace("\xd6", "")
            # print(name_of_investor)
            different_countries = mes.xpath("./td[2]/text()")[0].replace("\xe5", "")
            # print(different_countries)
            amount_invested = str.split(mes.xpath("./td[3]/text()")[0], " ")[0]\
                .replace("\xa0", "")\
                .replace("\xd6", "")\
                .replace("\xe5", "")\
                .replace("\ue07e", "")
            # print(amount_invested)
            investment_sql = """
                insert into wzzxbs_mofcom_investment_info(
                id,
                name_of_investor,
                different_countries,
                amount_invested,
                cust_id,
                craw_time
                )values('%s', '%s', '%s', '%s', '%s', '%s')
            """ % (
                   self.util.MD5(name_of_investor + different_countries + amount_invested),
                   pymysql.escape_string(name_of_investor),
                   different_countries,
                   amount_invested,
                   self.util.MD5(md5_id),
                   self.util.get_now_time())
            self.util.insert2mysql("投资信息|", investment_sql)

    def parse(self, num):
        self.data["page.currentPage"] = str(num)
        if num:
            self.data["page.start"] = str((int(num) - 1) * 2000)
        while True:
            try:
                page_req = requests.post(url=self.url, headers=self.headers, data=self.data)
                items = self.util.get_json_obj(page_req.text)["rows"]
                page_req.close()

                for item in items:  # item
                    business_type = item["data"][1]
                    item_code = re.findall(r'showRecordInfo\(\"(.*?)\"\)', item["data"][0])[0]
                    detail_url = self.detail_base_url.format(item_code, self.util.get_stamp())  # 详情页请求连接
                    print(detail_url)
                    self.detail_data["params.recordId"] = item_code
                    self.detail_data["time"] = self.util.get_stamp()
                    while True:
                        try:
                            detail_req = requests.get(url=detail_url, headers=self.detail_headers,
                                                      data=self.detail_data)  # 详情页请求
                            detail_html = self.util.get_xpath_obj(detail_req.text)
                            detail_req.close()
                            if len(detail_html.xpath("//div[@class=\"Table1\"]/table[1]/tr")) == 18:
                                try:
                                    md5_id, item_number = self.parse_18(detail_html, business_type)
                                    self.parse_invesment_info(detail_html, md5_id, 18)
                                except Exception as e18:
                                    print("e18" + str(e18))
                                    print("问题在此处被捕获了")
                            else:
                                try:
                                    md5_id, item_number = self.parse_17(detail_html, business_type)
                                    # 三、外商投资企业投资者基本信息
                                    self.parse_invesment_info(detail_html, md5_id, 17)
                                except Exception as e17:
                                    print("e17" + str(e17))
                                    print("问题在此处被捕获了")
                            break
                        except requests.exceptions.ChunkedEncodingError as e:
                            print("e" + str(e))
                        except Exception as e1:
                            print("e1" + str(e1))
                            print("==>远程关闭连接，休息等待中。。。")
                            time.sleep(300)
                    time.sleep(1.5)
                break
            except requests.exceptions.ChunkedEncodingError as e2:
                print("e2" + str(e2))
            except Exception as e3:
                print("e3" + str(e3))
                print("=====>远程关闭连接，休息等待中。。。")
                time.sleep(300)

    def main(self):
        req = requests.post(url=self.url, headers=self.headers, data=self.data)  # 初始数据请求
        res_json = self.util.get_json_obj(req.text)
        self.data["page.rowCount"] = res_json["rowCount"]
        for i in range(29, int(res_json["rowCount"])):
            print("#####{}#####".format(i))
            self.parse(i)
            time.sleep(30)


if __name__ == '__main__':
    wm = WzzxbsMofocom()
    wm.main()
