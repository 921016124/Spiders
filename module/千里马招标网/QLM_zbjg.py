import re
import sys
sys.path.append("../")
from Utils_1 import Util
import time


"""
    数据来源：千里马招标网
    来源地址：http://www.qianlima.com/zbjg/p1
    数据描述：千里马招标网招标结果信息
    目标表中文名：招标结果信息表
    目标表英文名：INVT_PUB_BID_RSL_INF
    数据量：0 - 1 （万条）
    作者：mcg
    状态：完成 
    记录时间：2019.08.02
"""


class Qlm_zbjg:
    def __init__(self):
        self.base_url = "http://www.qianlima.com/zbjg/p{}"
        self.page = 200
        self.util = Util()
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "__jsluid_h=144847f002c5e67a5b7bf1888f49e19c; UM_distinctid=16c02c0e9b53d5-083f7603340745-e343166-144000-16c02c0e9b6403; gr_user_id=bfb0c075-bcf5-4e05-a943-8b3448f39a0d; Hm_lvt_0a38bdb0467f2ce847386f381ff6c0e8=1563432734; LXB_REFER=www.baidu.com; bridgeid=59454367; keywordUnit=40461; keywords=%E5%8D%83%E9%87%8C%E9%A9%AC%E6%8B%9B%E6%A0%87%E7%BD%91; CNZZDATA1277608403=172402465-1563412202-%7C1563498692; BAIDU_SSP_lcr=https://www.baidu.com/link?url=BUcmE5CDcuTFAv7tI05xeq_80sbO-X-vNsQ1yhUvF_DGdoPt-o7VQs8t7AYRpXBm&wd=&eqid=da58e9c4000e34dc000000065d312603; Hm_lvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1563414294,1563432734,1563432760,1563502122; qlm_old=\"http://www.qianlima.com/zb/detail/20190719_139475196.html\"; Hm_lpvt_0a38bdb0467f2ce847386f381ff6c0e8=1563502180; qlm_username=15561585051; qlm_password=RCf8ujm8K3EfguKmBCouKpgCKK7uopgU; rem_login=1; qlmll_his=\",139475750,139491436,139497668,139475763,139475196,139264733,139264636,139269995,\"; seo_refUrl=\"http://www.directlyaccess.com\"; seo_curUrl=\"http://www.qianlima.com/common/cat.jsp\"; CNZZDATA1848524=cnzz_eid%3D430053542-1563409337-%26ntime%3D1563503598; fromWhereUrl=\"http://www.qianlima.com/zbjg/\"; seo_intime=\"2019-07-19 10:57:07\"; Hm_lpvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1563506743",
            "Host": "www.qianlima.com",
            "Referer": "http://www.qianlima.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        }

    def get_url_mysql(self):
        for i in range(200):
            url = self.base_url.format(i)
            res = self.util.get_req(url=url, headers=self.headers)

            html = self.util.get_xpath_obj(res)
            for dl in html.xpath("//div[@class=\"sevenday_list\"]/dl"):
                detail_url = dl.xpath("./dt/a/@href")[0].strip()
                sql = "insert into qlm_zbjg_url(url,status) values ('%s','0')" % detail_url
                self.util.insert2mysql(detail_url, sql)
        self.util.MySQL().close()

    def get_mess(self):
        conn = self.util.MySQL()
        cursor = conn.cursor()
        sql = "select url from qlm_zbjg_url where status=0;"
        cursor.execute(sql)
        for detail_url in cursor.fetchall():
            print(detail_url[0])
            detail_html = self.util.get_xpath_obj(self.util.get_req(url=detail_url[0], headers=self.headers).text)
            try:
                detail_title = detail_html.xpath("//h2/text()")[0]
                detail_location = "".join(detail_html.xpath("//span[@class=\"site\"]/a//text()"))
                detail_status = detail_html.xpath("//span[@class=\"zhuangtai\"]//text()")[0].replace("状态：", "")
                detail_date = detail_html.xpath("//span[@class=\"d2\"]/text()")[0]
                detail_content = re.findall(r'<div id="wen".*?</div>', self.util.get_req(url=detail_url[0]
                                                                                         , headers=self.headers)
                                            .text
                                            , re.S)[0].replace("\"", "\\\"").replace("\'", "\\\'")
                record_id = self.util.MD5(detail_title + detail_location)
                crawl_time = self.util.get_now_time()
                sql = """insert into INVT_PUB_BID_PRP_INF(ID,TTL,ZON,STS,INVT_PUB_BID_CNTNT,ISU_TM,DTL_LINK,INPT_DT)
                                                    values('%s','%s','%s','%s','%s','%s','%s','%s')""" \
                      % (record_id,
                         detail_title,
                         detail_location,
                         detail_status,
                         detail_date,
                         detail_content,
                         detail_url[0],
                         crawl_time)
                up_sql = "update qlm_zbjg_url set status = 1  where url = '{}';".format(detail_url[0])
                self.util.insert2mysql(detail_title, sql, up_sql)
                conn.commit()
            except IndexError as e:
                print("详情页请求失败")
                time.sleep(86400)
                q = Qlm_zbjg()
                q.run()

    def run(self):
        self.get_url_mysql()
        self.get_mess()


if __name__ == '__main__':
    q = Qlm_zbjg()
    q.run()
