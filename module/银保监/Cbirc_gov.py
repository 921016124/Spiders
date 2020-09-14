import requests
from lxml import etree
import json
def get_html():
    url = "http://www.cbirc.gov.cn/cn/static/data/DocInfo/SelectByDocId/data_docId=883813.json"
    headers = {
        "Accept": "*/*",
        "Referer": "http://www.cbirc.gov.cn/cn/view/pages/ItemDetail.html?docId=883813",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    res = requests.get(url=url, headers=headers)
    n_res = json.loads(res.text)
    html = etree.HTML(n_res['data']['docClob'])
    print(n_res['data']['docClob'])

if __name__ == '__main__':
    get_html()