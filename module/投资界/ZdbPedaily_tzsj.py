import time
import sys
sys.path.append("../")
from Utils_1 import Util


"""
    数据来源：投资界
    来源地址：https://zdb.pedaily.cn/inv/
    数据描述：投资界投资事件信息
    目标表中文名：投资事件信息表、投资事件主要人物表，投资事件股东信息表
    目标表英文名：INV_EVT_INF、INV_EVT_MAIN_PSN_INF、INV_EVT_SHH_INF
    数据量：0 - 1 （万条）
    作者：mcg
    状态：完成 
    记录时间：2019.08.02
"""


class ZdbPedaily_tzsj:
    def __init__(self):
        self.urls = ["https://zdb.pedaily.cn/inv/p{}/".format(i) for i in range(1, 770)]
        self.util = Util()

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "__uid=1452122016; __fromtype=0; ARRAffinity=197ae5372184c64aeca47f780a2e053f3a50366e2bda392cd4bfa3b38e39a929; Hm_lvt_25919c38fb62b67cfb40d17ce3348508=1564455299,1564997145,1565057017,1565061687; BAIDU_SSP_lcr=https://www.baidu.com/link?url=mXXXmWT7-LUN6gg9o-kkJIw_k0SkPj9aL3XGvS6wRVmJjG_3dfydZul0mdFS1rSa&wd=&eqid=cf1c52fe000195ab000000065d48f231; __utma=23980325.1444638820.1563415171.1565057028.1565061688.26; __utmc=23980325; __utmz=23980325.1565061688.26.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; Hm_lpvt_25919c38fb62b67cfb40d17ce3348508={}; __utmb=23980325.5.10.1565061688",
            "Host": "zdb.pedaily.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

    def get_shareholder(self, id_code, detail_html):
        shareholder_info = detail_html.xpath("//table[@class=\"shareholder-info\"]/tbody/tr")
        if shareholder_info:
            for si in shareholder_info:
                shareholder_name = si.xpath("./td[1]/text()")[0]
                shareholder_type = si.xpath("./td[2]/text()")[0]
                if si.xpath("./td[3]/text()"):
                    shareholder_money = si.xpath("./td[3]/text()")[0]
                else:
                    shareholder_money = ""
                crawl_time = self.util.get_now_time()
                sql_sharholder = "insert into INV_EVT_SHH_INF(ID,SHH_INF,SHH_TYP,SSCR_CTRB_AMT,INPT_DT) " \
                                 "values('%s', '%s', '%s', '%s','%s')" % (
                    id_code, shareholder_name, shareholder_type, shareholder_money, crawl_time)

                self.util.insert2mysql("股东信息", sql_sharholder)

    def get_main_people(self, id_code, detail_html):
        main_people = detail_html.xpath("//div[@class=\"business-people\"]/ul/li")
        if main_people:
            for p in main_people:
                mp_name = p.xpath("./h3/text()")[0]
                mp_position = p.xpath("./p/text()")[0]

                crawl_time = self.util.get_now_time()

                sql_main_people = "insert into INV_EVT_MAIN_PSN_INF(ID, MAIN_PPL_NM, MAIN_PPL_POS, INPT_DT) values('%s', '%s', '%s','%s')" % (
                    id_code, mp_name, mp_position, crawl_time)
                self.util.insert2mysql("主要人物", sql_main_people)

    def get_detail_info(self, detail_url):
        self.headers["Cookie"] = self.headers["Cookie"].format(self.util.get_stamp())
        detail_res = self.util.get_req(url=detail_url, headers=self.headers)
        print(detail_res.status_code)
        if detail_res.status_code == 200:
            detail_html = self.util.get_xpath_obj(detail_res)
            # 详情页信息获取
            company_name = detail_html.xpath("//h1/text()")[0]
            company_base = detail_html.xpath("//div[@class=\"box-fix-l\"]/div/ul/li[1]/text()")[0]
            company_reg_loc = detail_html.xpath("//div[@class=\"box-fix-l\"]/div/ul/li[2]/text()")[0]
            company_bound_date = detail_html.xpath("//div[@class=\"box-fix-l\"]/div/ul/li[3]/text()")[0]
            company_industry = detail_html.xpath("//div[@class=\"box-fix-l\"]/div/ul/li[4]/text()")[0]
            if detail_html.xpath("//div[@class=\"box-fix-l\"]/div/ul/li[@class=\"link\"]/a/text()"):
                company_site = detail_html.xpath("//div[@class=\"box-fix-l\"]/div/ul/li[@class=\"link\"]/a/text()")[0]
            else:
                company_site = ""
            if detail_html.xpath('//div[@class="box-fix-l"]/p/text()'):
                company_intro = detail_html.xpath('//div[@class="box-fix-l"]/p/text()')[0]
            elif detail_html.xpath('//div[@class="box-fix-l"]/p/span/text()'):
                company_intro = detail_html.xpath('//div[@class="box-fix-l"]/p/span/text()')[0]
            elif detail_html.xpath('//div[@class="box-fix-l"]/pre/text()'):
                company_intro = detail_html.xpath('//div[@class="box-fix-l"]/pre/text()')[0]
            elif detail_html.xpath('//div[@class="box-fix-l"]/div/div/text()'):
                company_intro = detail_html.xpath('//div[@class="box-fix-l"]/div/div/text()')[0]
            elif detail_html.xpath('//div[@class="box-fix-l"]/div/text()'):
                company_intro = detail_html.xpath('//div[@class="box-fix-l"]/div/text()')[0]
            elif detail_html.xpath('//div[@id="cke_pastebin"]//text()'):
                company_intro = detail_html.xpath('//div[@id="cke_pastebin"]//text()')[0]
            elif detail_html.xpath('//div[@class="box-fix-l"]/ul/text()'):
                company_intro = detail_html.xpath('//div[@class="box-fix-l"]/ul/text()')[0]
            else:
                company_intro = ""

            if detail_html.xpath("//div[@id=\"business\"]"):
                legal_person = detail_html.xpath("//table[@class=\"base-info\"]/tr[1]/td[2]/text()")[0]
                founded_time = detail_html.xpath("//table[@class=\"base-info\"]/tr[1]/td[4]/text()")[0]
                registered_capital = detail_html.xpath("//table[@class=\"base-info\"]/tr[2]/td[2]/text()")[0]
                operational_authority = detail_html.xpath("//table[@class=\"base-info\"]/tr[2]/td[4]/text()")[0]
                registered_num = detail_html.xpath("//table[@class=\"base-info\"]/tr[3]/td[2]/text()")[0]
                approval_date = detail_html.xpath("//table[@class=\"base-info\"]/tr[3]/td[4]/text()")[0]

                organizational_code = detail_html.xpath("//table[@class=\"base-info\"]/tr[4]/td[2]/text()")[0]
                creditfcode = detail_html.xpath("//table[@class=\"base-info\"]/tr[4]/td[4]/text()")[0]
                identification_number = detail_html.xpath("//table[@class=\"base-info\"]/tr[5]/td[2]/text()")[0]
                registration_authority = detail_html.xpath("//table[@class=\"base-info\"]/tr[5]/td[4]/text()")[0]
                enterprise_type = detail_html.xpath("//table[@class=\"base-info\"]/tr[6]/td[2]/text()")[0]
            else:
                legal_person = ""
                founded_time = ""
                registered_capital = ""
                operational_authority = ""
                registered_num = ""
                approval_date = ""

                organizational_code = ""
                creditfcode = ""
                identification_number = ""
                registration_authority = ""
                enterprise_type = ""
            id_code = self.util.MD5(company_name + creditfcode)
            # 融资事件 信息处理
            for rz_html in detail_html.xpath("//div[@class=\"list-invest\"]/ul/li"):
                if rz_html.xpath("./div[@class=\"view\"]/a/@href")[0].startswith("http"):
                    rz_url = rz_html.xpath("./div[@class=\"view\"]/a/@href")[0]  # 融资事件新开页
                else:
                    rz_url = "https://zdb.pedaily.cn" + rz_html.xpath("./div[@class=\"view\"]/a/@href")[0]  # 融资事件新开页
                print(rz_url)
                rz_res = self.util.get_req(url=rz_url, headers=self.headers)
                if rz_res.status_code == 200:
                    rz_html = self.util.get_xpath_obj(rz_res.text)
                    # 投资事件 信息获取
                    rz_title = rz_html.xpath("//h1/text()")[0]
                    rz_info = "".join(rz_html.xpath("//div[@class=\"info\"]/ul/li//text()"))
                    rz_intro = rz_html.xpath("//div[@id=\"desc\"]/p/text()")[0]

                    crawl_time = self.util.get_now_time()

                    sql_rzsj = """insert into INV_EVT_INF(ID,CMP_NM,ORG_TOT_DEPT,REG_PLC_PNT,CMP_SET_UP_TM,AFL_IDT,FORML_WEB,CMP_INTRO,LVRG_NM,LVRG_INF,LVGR_DTL,LGP_INF,SET_UP_TM,REG_CPT,OPR_RIT,REG_NBR,APRV_TM,ORG_ORG_CD_NBR,SOC_CRD_CD,TAX_PSN_RCG_NBR,REG_INSTT,ENTP_TYP,INPT_DT
                                                                            )values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
                                                                            """ % (id_code,
                                                                                   company_name,
                                                                                   company_base,
                                                                                   company_reg_loc,
                                                                                   company_bound_date,
                                                                                   company_industry,
                                                                                   company_site,
                                                                                   company_intro,
                                                                                   rz_title,
                                                                                   rz_info,
                                                                                   rz_intro,
                                                                                   legal_person,
                                                                                   founded_time,
                                                                                   registered_capital,
                                                                                   operational_authority,
                                                                                   registered_num,
                                                                                   approval_date,
                                                                                   organizational_code,
                                                                                   creditfcode,
                                                                                   identification_number,
                                                                                   registration_authority,
                                                                                   enterprise_type,
                                                                                   crawl_time)
                    self.util.insert2mysql("融资公司信息", sql_rzsj)
            self.get_main_people(id_code, detail_html)
            self.get_shareholder(id_code, detail_html)

    def get_items_list(self, res):
        html = self.util.get_xpath_obj(res)
        for li in html.xpath("//ul[@id=\"inv-list\"]/li"):
            time.sleep(2)
            # 详情页获取
            if li.xpath("./div[1]/a/@href"):
                detail_url = "https://zdb.pedaily.cn" + li.xpath("./div[1]/a/@href")[0]  # 地址获取
            else:
                continue
            print(detail_url)
            self.get_detail_info(detail_url)

    def run(self):
        self.headers["Cookie"] = self.headers["Cookie"].format(self.util.get_stamp())
        for url in self.urls:
            print("列表页：" + url + "开始爬取")
            res = self.util.get_req(url=url, headers=self.headers)  # 列表页列表获取
            self.get_items_list(res)


if __name__ == '__main__':
    while True:
        z = ZdbPedaily_tzsj()
        z.run()
        time.sleep(86400)
