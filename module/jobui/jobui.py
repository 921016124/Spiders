import requests
from lxml import etree
import datetime

url1 = "https://www.jobui.com/cmp?area=%E5%93%88%E5%B0%94%E6%BB%A8&industry=%E4%BA%92%E8%81%94%E7%BD%91%2F%E7%94%B5%E5%AD%90%E5%95%86%E5%8A%A1"
url2 = "https://www.jobui.com/jobs?cityKw=%E5%93%88%E5%B0%94%E6%BB%A8&industry=%E4%BA%92%E8%81%94%E7%BD%91%2F%E7%94%B5%E5%AD%90%E5%95%86%E5%8A%A1&jobKw=&n=2"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "jobui_p=1565753151227_21067661; jobui_user_passport=yk15764787441006; Hm_lvt_90d68bd37705477f2f6f689b11d8aa3a=1577598664; Hm_lvt_95b31cf3e73a1ea2e42e77ac1912a5eb=1577080717,1577258071,1577673952; Hm_lvt_8b3e2b14eff57d444737b5e71d065e72=1584601507; PHPSESSID=tkh18sb8oogmuiki098pegp2m7; __gads=ID=874ecc61ee6ab3d1:T=1584607045:S=ALNI_Mb2w8ZsFZLXoWyKCnCWfpmb1Y_12g; job-subscribe-guide=1; jobui_area=%25E5%2593%2588%25E5%25B0%2594%25E6%25BB%25A8; jobui_area_tmp=%25E5%2593%2588%25E5%25B0%2594%25E6%25BB%25A8; TN_VisitCookie=1102; TN_VisitNum=29; Hm_lpvt_8b3e2b14eff57d444737b5e71d065e72=1584612072",
    "Host": "www.jobui.com",
    "If-Modified-Since": "Thu, 19 Mar 2020 09:58:47 GMT",
    "Referer": "https://www.jobui.com/cmp?keyword=&area=%E5%93%88%E5%B0%94%E6%BB%A8",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}


def get_company_count():
    res = requests.get(url=url1,headers=headers)
    return etree.HTML(res.text).xpath("//span[@class='fr']/span/text()")[0].strip()


def get_job_count():
    res = requests.get(url=url2,headers=headers)
    return etree.HTML(res.text).xpath("//span[@class='sort-cut-result']/span/text()")[0].strip()


def each_get_data():
    c_count = get_company_count()
    j_count = get_job_count()
    data = c_count + '-' + j_count + '\n'
    with open('count_of_company_job.txt', 'a',encoding='utf-8') as f:
        f.write(data)

    print('今日数据写入成功！')

if __name__ == '__main__':
    print("程序已启动，等到零时开始抓取！")
    while True:
        now = datetime.datetime.now()
        h, m = 0, 0
        if now.hour == h and now.minute == m:
            each_get_data()

