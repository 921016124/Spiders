import requests
import time
import pymysql
from lxml import etree
import hashlib
import re

"""
    数据来源：国家税务总局湖南省税务局网站
    来源地址：http://hunan.chinatax.gov.cn/zhuanti/qsgg/article_list.jsp?pagenum=1&&type=1&city_id=-1
    数据描述：湖南省税务局欠税信息公告
    目标表中文名：欠税信息表
    目标表英文名：OWE_TAX_INF
    数据量：3 - 4（万条）
    作者：mcg
    状态：完成
    记录时间：2019.08.02
"""

def insert2mysql(id_num, ns_name, ns_code, fr_name, fr_id_type, fr_id_num, addr, qs_type, qs_money,new_money, pub_time):
	now = int(time.time())
	timeArray = time.localtime(now)
	otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray) 

	sql = "insert into OWE_TAX_INF(" \
		  "ID,TAX_PSN_NM,TAX_PSN_RCG_NBR,LGL_RPRS_PSN_NM,LGL_RPRS_PSN_DOC_TYP,LGL_RPRS_PSN_DOC_NBR,OPR_PLC_PNT,OWE_TAX_TYP,OWE_TAX_BAL,CUR_NEW_HPN_OWE_TAX_BAL,ISU_TM,INPT_DT" \
		  ") VALUES('%s', '%s','%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s')" %(id_num, ns_name, ns_code, fr_name, fr_id_type, fr_id_num, addr, qs_type, qs_money, new_money, pub_time,  otherStyleTime)
	try:
		conn_mysql.cursor().execute(sql)
		conn_mysql.commit()  # 实现采集网址入库，下一步进行对采集网址数据的判断，判断是否在库，如果在判断是否已经爬取。

		print("插入成功", fr_name)
	except pymysql.err.IntegrityError:
		print("数据重复！！", fr_name)
		conn_mysql.rollback()


if __name__ == '__main__':
	while True:
		conn_mysql = pymysql.connect(host="127.0.0.1", port=3307, user="root", passwd="root@123", db="WCS")
		base_url = "http://hunan.chinatax.gov.cn/zhuanti/qsgg/article_list.jsp?pagenum={}&&type=1&city_id=-1"
		headers = {
			"Connection": "keep-alive",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
		}
		data = {
			"city_id": "-1",
			"pagenum": 3,
			"type": "1",
		}
		res = requests.get(url="http://hunan.chinatax.gov.cn/zhuanti/qsgg/article_list.jsp?&type=1&city_id=-1", headers=headers).text
		html = etree.HTML(res)
		h = html.xpath('//table[@class="clstbldata"]/tr[last()]/td/a[last()]/@href')[0]
		page = re.findall(r'pagenum=(\d+)', h)[0]

		for i in range(1, int(page) + 1):
			print("第{}页开始爬取".format(i))
			res = requests.get(url=base_url.format(i), headers=headers).text
			html = etree.HTML(res)
			items = html.xpath('//table[@class="clstbldata"]/tr')
			for item in items[:-1]:
				try:
					ns_name = item.xpath("./td[1]/text()")[0]
					ns_code = item.xpath("./td[2]/text()")[0]
					fr_name = item.xpath("./td[3]/text()")[0]
					fr_id_type = item.xpath("./td[4]/text()")[0].replace("201|", "")
					fr_id_num = item.xpath("./td[5]/text()")[0]
					addr = item.xpath("./td[6]/text()")[0]
					qs_type = item.xpath("./td[7]/text()")[0]
					qs_money = item.xpath("./td[8]/text()")[0] + "元"
					new_money = item.xpath("./td[9]/text()")[0]
					pub_time = item.xpath("./td[10]/text()")[0]
				except IndexError:
					continue
				m2 = hashlib.md5()
				md = fr_name + qs_type + qs_money
				m2.update(md.encode('utf-8'))
				id_num = m2.hexdigest()

				insert2mysql(id_num, ns_name, ns_code, fr_name, fr_id_type, fr_id_num, addr, qs_type, qs_money, new_money, pub_time)
				time.sleep(0.1)
			time.sleep(1)
		time.sleep(86400)

