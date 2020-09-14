import requests
import time

from lxml import etree
import re
import hashlib
import pymysql
"""
    数据来源：中国招标网
    来源地址：http://zb.yfb.qianlima.com/yfbsemsite/mesinfo/zbpglist
    数据描述：中国招标网招标信息名录
    目标表中文名：招标信息表 
    目标表英文名：INVT_PUB_BID_INF
    数据量：12 - 13 （万条）
    作者：mcg
    状态：完成 
    记录时间：2019.08.02
"""

base_url = "http://zb.yfb.qianlima.com/yfbsemsite/mesinfo/zbpglist"
headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "zh-CN,zh;q=0.9",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"Content-Length": "252",
	"Content-Type": "application/x-www-form-urlencoded",
	"Cookie": "yfbsemsite.session.id=f7432fdc8f8541b293b54732e0577ea4; __jsluid_h=c04a3e74d799f86141d5a70902d69c72; Hm_lvt_a31e80f5423f0ff316a81cf4521eaf0d=1562577700; LXB_REFER=www.baidu.com; pageSize=15; pageNo=18; Hm_lpvt_a31e80f5423f0ff316a81cf4521eaf0d=1562578178",
	"Host": "zb.yfb.qianlima.com",
	"Origin": "http://zb.yfb.qianlima.com",
	"Referer": "http://zb.yfb.qianlima.com/yfbsemsite/mesinfo/zbpglist",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
}
province = {
	"1": "安徽",
	"2": "北京",
	"3": "福建",
	"4": "甘肃",
	"5": "广东",
	"6": "广西",
	"7": "贵州",
	"8": "海南",
	"9": "河北",
	"10": "河南",
	"11": "黑龙江",
	"12": "湖北",
	"13": "湖南",
	"14": "吉林",
	"15": "江苏",
	"16": "江西",
	"17": "辽宁",
	"18": "内蒙古",
	"19": "宁夏",
	"20": "青海",
	"21": "山东",
	"22": "山西",
	"23": "陕西",
	"24": "上海",
	"25": "四川",
	"26": "天津",
	"27": "西藏",
	"28": "新疆",
	"29": "云南",
	"30": "浙江",
	"31": "重庆"
}
data = {
	"pageNo":"1",
	"pageSize":"15",
	"searchword":"",
	"searchword2":"", 
	"hotword":"",
	"provinceId":"1",
	"provinceName":"安徽",
	"areaId":"1",
	"areaName":"安徽",
	"infoType":"",
	"infoTypeName":"",
	"timeType":"0",
	"timeTypeName":"",
	"searchType":"2",
	"clearAll":"false",
	"e_keywordid":"116479021368",
	"e_creative":"28381598848",
	"flag":"1",
	"source": "baidu",
}
conn_mysql = pymysql.connect(host="127.0.0.1", port=3307, user="root", passwd="root@123", db="WCS")


def insert2mysql(ztb_date, ztb_area, ztb_type, ztb_title):
	now = int(time.time())
	timeArray = time.localtime(now)
	otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray) 

	m2 = hashlib.md5()   
	m2.update(ztb_title.encode('utf-8'))   
	id_num = m2.hexdigest()
	sql = "insert into INVT_PUB_BID_INF(ID,DT,ZON,PRJ_TYP,INVT_PUB_BID_TTL,INPT_DT) VALUES('%s', '%s','%s', '%s', '%s', '%s')" % (id_num, ztb_date, ztb_area, ztb_type, ztb_title,otherStyleTime)
	try:
		conn_mysql.cursor().execute(sql)
		conn_mysql.commit()  # 实现采集网址入库，下一步进行对采集网址数据的判断，判断是否在库，如果在判断是否已经爬取。

		print("插入成功")
	except pymysql.err.IntegrityError:
		print("数据重复！！")
		conn_mysql.rollback()
	except IndexError as e:
		print(IndexError, ztb_title)

page = re.findall(r'<a href="javascript:">当前 \d+页/(\d+)页共', requests.post(url=base_url, headers=headers, data=data).text)[0]
for i in range(int(page) + 1):
	for provinceId, provinceName in province.items():
		data["provinceId"] = provinceId
		data["areaId"] = provinceId
		data["provinceName"] = provinceName
		data["areaName"] = provinceName
		
		res = requests.post(url=base_url, headers=headers, data=data).text

		html = etree.HTML(res)
		ztb_mes = html.xpath("//table[@id=\"contentTable\"]/tbody/tr")
		for ztb in ztb_mes:
			ztb_date = ztb.xpath("./td[1]/text()")[0].replace("'", "").strip().strip()
			ztb_area = ztb.xpath("./td[2]/text()")[0].strip().strip()
			ztb_type = ztb.xpath("./td[3]/text()")[0].strip().strip()
			ztb_title = "".join(ztb.xpath("./td[4]//text()")).strip()
			insert2mysql(ztb_date, ztb_area, ztb_type, ztb_title)
			print(ztb_date, "\t", ztb_area, "\t", ztb_type, "\t", ztb_title, "\n")
			time.sleep(1)