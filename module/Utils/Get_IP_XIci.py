import requests
import random
from lxml import etree

from SunLine.Utils.UA import keys

headers = {
    "User-Agent": random.choice(keys)
}
end = input("end:")
for i in range(1, int(end) + 1):
    url = "https://www.xicidaili.com/nn/" + str(i)
    print(url)
    response = requests.get(url, headers=headers, timeout=10)
    print(response.text)
    # html = etree.HTML(response.text)
    # items = html.xpath("//*[@id=\"ip_list\"]/tr[contains(@class,\"odd\") or contains(@class, \"\")]")
    # print(items)
    # for item in items:
    #     IP = item.xpath("./td[2]/text()")
    #     PORT = item.xpath("./td[3]/text()")
    #     print(IP, PORT)