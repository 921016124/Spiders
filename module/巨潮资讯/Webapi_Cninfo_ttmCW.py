import requests
import time
import re

import sys
sys.path.append("../")
from Utils_1 import Util

"""
    数据来源：巨潮资讯-数据中心
    来源地址：http://webapi.cninfo.com.cn/#/dataBrowse 
    数据描述：个股ttm财务利润信息
    目标表中文名：个股ttm财务利润表
    目标表英文名：webapi_cninfo_ttmcw
    数据量：待定
    作者：mcg
    状态：完成，测试中
    记录时间：2019.08.02
"""


class WebapiCninfo:
    def __init__(self):
        self.get_code_key_h = {
            "Referer": "http://webapi.cninfo.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
            "Cache-Control": "max-age=0",
            "Accept": "image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Language": "zh-CN",
            "Accept-Encoding": "gzip, deflate",
            "Host": "webapi.cninfo.com.cn",
            "Connection": "Keep-Alive",
            "Cookie": "cninfo_user_browse=000002,gssz0000002,%E4%B8%87%20%20%E7%A7%91%EF%BC%A1; UC-JSESSIONID=E4307520E006F39592E00F72DAAEA7D9; pgv_pvid=194670220; Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b=1564557528,1564557544,1564557814,1564557966; __qc_wId=595; Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b={}",
        }
        self.get_loc_mess_h = {
            "Origin": "http://webapi.cninfo.com.cn",
            "Referer": "http://webapi.cninfo.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
            "Cache-Control": "max-age=0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN",
            "mcode": "",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "0",
            "Host": "webapi.cninfo.com.cn",
            "Connection": "Keep-Alive",
            "Pragma": "no-cache",
            "Cookie": "UC-JSESSIONID=E4307520E006F39592E00F72DAAEA7D9; cninfo_user_browse=000002,gssz0000002,%E4%B8%87%20%20%E7%A7%91%EF%BC%A1; __qc_wId=595; Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b={}; pgv_pvid=194670220; Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b=1564557966,1564558754,1564559126,{}; codeKey={}",
        }
        self.get_comp_name_h = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Cookie": "pgv_pvid=9659403051; cninfo_user_browse=000002,gssz0000002,%E4%B8%87%20%20%E7%A7%91%EF%BC%A1; UC-JSESSIONID=54EC36EB821D8FDBF427E3268AD8E2B7; __qc_wId=281; Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b=1564622577,1564623888,1564625108,{}; Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b={}; codeKey={}",
            "Host": "webapi.cninfo.com.cn",
            "mcode": "{}",
            "Origin": "http://webapi.cninfo.com.cn",
            "Referer": "http://webapi.cninfo.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.get_data_h = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Content-Length": "0",
                "Cookie": "pgv_pvid=9659403051; cninfo_user_browse=000002,gssz0000002,%E4%B8%87%20%20%E7%A7%91%EF%BC%A1; UC-JSESSIONID=54EC36EB821D8FDBF427E3268AD8E2B7; __qc_wId=281; codeKey={}; Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b=1564623888,1564625108,1564625230,{}; Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b={}",
                "Host": "webapi.cninfo.com.cn",
                "mcode": "{}",
                "Origin": "http://webapi.cninfo.com.cn",
                "Referer": "http://webapi.cninfo.com.cn/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
            }
        self.get_data_d = {
            "scode": "",
            "sdate": "",
            "edate": "",
            "type": "071001",
            "@column": "SECCODE,SECNAME,STARTDATE,ENDDATE,F001D,F002V,F003V,F006N,F007N,F008N,F009N,F010N,F011N,F012N,F013N,F014N,F015N,F016N,F017N,F018N,F019N,F020N,F021N,F022N,F023N,F024N,F025N,F026N,F027N,F028N,F029N,F030N,F031N,F033N,F034N,F035N,F036N,F037N,F038N,F039N,F040N,F041N,F042N,F043N,F044N,F045N,F046N,F047N,F048N,F049N,F050N,F051N",
        }
        self.get_comp_name_d = {
            "platetype": "{}",
            "platecode": "{}",
            "@orderby": "SECCODE:asc",
            "@column": "SECCODE,SECNAME",
        }
        self.session = requests.Session()
        self.util = Util()
        self.get_code_url = "http://webapi.cninfo.com.cn/api-cloud-platform/login/getVerfyCode"
        self.get_loc_url = "https://webapi.cninfo.com.cn/api/sysapi/p_sysapi1016"
        self.d_date = [i + j for i in ["2017", "2018", "2019"] for j in ["0331", "0630", "0930", "1231"]]

    def parse_json(self, content):
        content = self.util.get_json_obj(content)
        datas = content["records"][3]["children"]
        return ["http://webapi.cninfo.com.cn/{}?{}&@column=SECCODE,SECNAME"\
                .format(data["API"], data["PARAM"]) for data in datas]

    def parse_data(self, data):
        y = self.get_data_d["sdate"][:4]
        if self.get_data_d["sdate"][4:6] == "03":
            quarter = "第一季度"
        elif self.get_data_d["sdate"][4:6] == "06":
            quarter = "第二季度"
        elif self.get_data_d["sdate"][4:6] == "09":
            quarter = "第三季度"
        elif self.get_data_d["sdate"][4:6] == "12":
            quarter = "第四季度"
        else:
            quarter = "--"
        if isinstance(data, str):
            data = self.util.get_json_obj(data)
        for d in data["records"]:
            id_code = self.util.MD5(d["SECNAME"] + y + quarter)
            sql = """insert into  webapi_cninfo_ttmcw(id,
                    F046N,F027N,STARTDATE,F009N,F022N,F026N,F003V,F013N,F019N,F036N,
                    F042N,F031N,F001D,F045N,F008N,F010N,F021N,F051N,SECCODE,F025N,
                    F018N,F014N,F041N,F035N,F029N,F016N,F048N,F030N,F020N,F039N,
                    F050N,F024N,F011N,F007N,F034N,F044N,F049N,F015N,F040N,ENDDATE,
                    F028N,F047N,F017N,F038N,SECNAME,F037N,F012N,F006N,F023N,F043N,
                    F033N,F002V,y,quarter,crawl_time) 
                    values 
                    (
                    '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
                    '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
                    '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
                    '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
                    '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
                    '%s','%s','%s','%s','%s','%s')""" % (
                                        id_code,
                                        d["F046N"],
                                        d["F027N"],
                                        d["STARTDATE"],
                                        d["F009N"],
                                        d["F022N"],
                                        d["F026N"],
                                        d["F003V"],
                                        d["F013N"],
                                        d["F019N"],
                                        d["F036N"],
                                        d["F042N"],
                                        d["F031N"],
                                        d["F001D"],
                                        d["F045N"],
                                        d["F008N"],
                                        d["F010N"],
                                        d["F021N"],
                                        d["F051N"],
                                        d["SECCODE"],
                                        d["F025N"],
                                        d["F018N"],
                                        d["F014N"],
                                        d["F041N"],
                                        d["F035N"],
                                        d["F029N"],
                                        d["F016N"],
                                        d["F048N"],
                                        d["F030N"],
                                        d["F020N"],
                                        d["F039N"],
                                        d["F050N"],
                                        d["F024N"],
                                        d["F011N"],
                                        d["F007N"],
                                        d["F034N"],
                                        d["F044N"],
                                        d["F049N"],
                                        d["F015N"],
                                        d["F040N"],
                                        d["ENDDATE"],
                                        d["F028N"],
                                        d["F047N"],
                                        d["F017N"],
                                        d["F038N"],
                                        d["SECNAME"],
                                        d["F037N"],
                                        d["F012N"],
                                        d["F006N"],
                                        d["F023N"],
                                        d["F043N"],
                                        d["F033N"],
                                        d["F002V"],
                                        y,
                                        quarter,
                                        self.util.get_now_time()
                                        )
            # self.util.insert2mysql(d["SECNAME"], sql)
            time.sleep(0.3)

    def cut_comp_code(self, scode, codekey, ts, dd):
            # 请求数据的base_url
            data_url = "http://webapi.cninfo.com.cn/api/stock/p_stock2332?scode={}" \
                       "&sdate={}&edate={}&type=071001&" \
                       "@column=SECCODE,SECNAME,STARTDATE,ENDDATE,F001D,F002V,F003V,F006N,F007N," \
                       "F008N,F009N,F010N,F011N,F012N,F013N,F014N,F015N,F016N,F017N,F018N,F019N," \
                       "F020N,F021N,F022N,F023N,F024N,F025N,F026N,F027N,F028N,F029N,F030N,F031N," \
                       "F033N,F034N,F035N,F036N,F037N,F038N,F039N,F040N,F041N,F042N,F043N,F044N," \
                       "F045N,F046N,F047N,F048N,F049N,F050N,F051N".format(scode, dd, dd)
            stamp = self.util.get_stamp()  # 统一时间戳
            # 生成新的请求headers
            self.get_data_h["Cookie"] = self.get_data_h["Cookie"].format(codekey, stamp, stamp)
            self.get_data_h["mcode"] = self.get_data_h["mcode"].format(self.util.base64_encode(ts).decode("utf-8"))
            self.get_data_d["scode"] = scode
            try:
                data = self.session.post(url=data_url, headers=self.get_data_h, data=self.get_data_d).text
            except requests.exceptions.ConnectionError:
                time.sleep(30)
                data = self.session.post(url=data_url, headers=self.get_data_h, data=self.get_data_d).text

            self.parse_data(data)

    # 处理公司的json数据
    def parse_comp_json(self, json_res, codekey, ts):
        content = self.util.get_json_obj(json_res)
        ls_comp_code = []
        for c in content["records"]:
            ls_comp_code.append(c["SECCODE"])  # 得到公司代码

        if len(ls_comp_code) % 20 == 0:
            loop = int(len(ls_comp_code) / 20)
        else:
            loop = int(len(ls_comp_code) / 20)
        # 遍历季度
        for dd in self.d_date:
            print(dd)
            self.get_data_d["sdate"] = dd
            self.get_data_d["edate"] = dd
            s, e = 0, 20
            #  根据得到的公司编号，对其进行分割，每组20个，分别请求。
            for _ in range(loop):
                time.sleep(1.5)
                scode = ",".join(ls_comp_code[s:e])
                s += 20
                if e < len(ls_comp_code):
                    e += 20
                else:
                    e = len(ls_comp_code)

                self.cut_comp_code(scode, codekey, ts, dd)
            time.sleep(30)

    # 获取所有公司名称
    def get_comp_name(self, get_loc_res, codekey, ts):
        print(get_loc_res)
        # 获取公司名称
        for get_comp_name_url in self.parse_json(get_loc_res):
            # 处理请求参数
            self.get_comp_name_h["Cookie"] = self.get_comp_name_h["Cookie"] \
                .format(self.util.get_stamp(), self.util.get_stamp(), codekey)
            self.get_comp_name_h["mcode"] = self.get_comp_name_h["mcode"].format(self.util.base64_encode(ts))
            self.get_comp_name_d["platetype"] = self.get_comp_name_d["platetype"].format(
                re.findall(r'platetype=(\d+)&', get_comp_name_url)[0])
            self.get_comp_name_d["platecode"] = self.get_comp_name_d["platecode"].format(
                re.findall(r'platecode=(\d+)&', get_comp_name_url)[0])
            # 开始请求公司名称
            try:
                comp_name_res = self.session.post(url=get_comp_name_url,
                                              headers=self.get_comp_name_h,
                                              data=self.get_comp_name_d).text
            except TimeoutError:
                time.sleep(10)
                comp_name_res = self.session.post(url=get_comp_name_url,
                                                  headers=self.get_comp_name_h,
                                                  data=self.get_comp_name_d).text
            self.parse_comp_json(comp_name_res, codekey, ts)

    def main(self):
        # 请求网页，为得到本次会话的codekey 值
        self.get_code_key_h["Cookie"] = self.get_code_key_h["Cookie"].format(int(time.time()))  # 构造headers
        get_code_res = self.session.get(url=self.get_code_url, headers=self.get_code_key_h, verify=False)
        ts = int(time.time())  # 获取本次会话的时间戳
        codekey = re.findall(r'codeKey=(.*?);', get_code_res.headers["Set-Cookie"])[0]  # 得到codekey
        # 得到以地区分类的网页
        self.get_loc_mess_h["mcode"] = self.util.base64_encode(ts)
        self.get_loc_mess_h["Cookie"] = self.get_loc_mess_h["Cookie"]\
            .format(self.util.get_stamp(), self.util.get_stamp(), codekey)
        get_loc_res = self.session.post(url=self.get_loc_url, headers=self.get_loc_mess_h).text
        # 处理获取公司名称
        self.get_comp_name(get_loc_res, codekey, ts)


if __name__ == '__main__':
    wc = WebapiCninfo()
    wc.main()
