import os
import sys
BASE_DIR = os.path.abspath(__file__)
sys.path.insert(0, BASE_DIR)

import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
from PIL import Image
import time
from lxml import etree
import pymysql
import pytesseract



class JiaJi:
    def __init__(self):
        self.url = "http://zaojiasys.jianshe99.com/cecaopsys/queryAndSearch/view.do?op=queryUnitInfoInit"
        self.govID = ["110000", "120000", "130000", "140000", "150000", "210000", "220000", "230000", "310000", "320000", "330000", "340000", "350000", "360000", "370000", "410000", "420000", "430000", "440000", "450000", "460000", "500000", "510000", "520000", "530000", "540000", "610000", "620000", "630000", "640000", "650000", "0010113", "0010201", "0010202", "0010203", "0010204", "0010205", "0010206", "0010207", "0010208", "0010209", "0010210", "0010211", "0010212", "0010213", "0010214", "0010215", "0010216", "0010217", "0010218", "0010219", "0010220", "0010221", "0010222", "0010223", "0010224", "0010225", "0010226", "0010227", "0010228", "0010229", "0010230", "0010298", "0010299"]

    def connect_wxremit_db(self):
        return pymysql.connect(host='115.28.34.45',
                               port=3306,
                               user='root',
                               password='root',
                               database='opi')

    def insert_file_rec(self, compayname, certificatenumber, attributionmanagement):
        con = self.connect_wxremit_db()
        cur = con.cursor()
        try:
            sql_str = "INSERT INTO jianshe99(companName, certificateNumber, attributionManagement) " \
                      "VALUES ('%s', '%s', '%s')" % (compayname, certificatenumber, attributionmanagement)
            cur.execute(sql_str)
            con.commit()
            print("---插入成功！---")
        except:
            con.rollback()
            print("--当前数据已存在!--")
        finally:
            cur.close()
            con.close()

    def get_cap(self):
        img = Image.open("img.jpg").crop((760, 415, 840, 437)).convert("RGB")  # crop and convert to CAPTCHA
        img.save("./Python_PJ/Captcha.jpg")  # get CAPTCHA
        pj_code = self.Po_Jie()  # Handle String
        time.sleep(5)
        return pj_code  # return CAPTCHA

    def get_data(self, site):
        html = etree.HTML(site)
        try:

            items = html.xpath("//table[@class=\"lms\"]/tbody/tr")
            for item in items[1:]:
                companname = item.xpath("./td[2]/text()")[0]
                certificatenumber = item.xpath("./td[3]/text()")[0]
                attributionmanagement = item.xpath("./td[4]/text()")[0]
                self.insert_file_rec(companname, certificatenumber, attributionmanagement)
        except:
            print("——————页面无数据——————！")
        finally:
            print(">>>本页已完成！")

    def Po_Jie(self):
        # 图片二值化
        from PIL import Image
        img = Image.open('./Python_PJ/Captcha.jpg').convert('L')

        # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
        threshold = 200

        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        # 图片二值化
        photo = img.point(table, '1')
        photo.save("test2.jpg")

        image = Image.open("test2.jpg").convert("RGB")
        txt = pytesseract.image_to_string(image)

        return txt

    def main(self):
        for gov in self.govID:
            while True:
                try:
                    driver = webdriver.Chrome()
                    driver.get(url=self.url)  # get website
                    driver.save_screenshot("img.jpg")  # save ScreenImage
                    # get FormData
                    Select(driver.find_element_by_name("govID")).select_by_value(gov)
                    Select(driver.find_element_by_name("unit/view.do?op=queryUnitInfo")).select_by_value("")
                    pj_code = self.get_cap()
                    driver.find_element_by_id("loginValidate").send_keys(pj_code)
                    # commit FormData
                    driver.find_element_by_id("searchBtn").click()
                    time.sleep(2)
                    self.get_data(driver.page_source)

                    break
                except selenium.common.exceptions.NoSuchElementException:
                    driver.quit()
                except selenium.common.exceptions.UnexpectedAlertPresentException:
                    driver.switch_to_alert().accept()
                    driver.quit()
            driver.quit()


if __name__ == '__main__':
    while True:
        jj = JiaJi()
        jj.main()