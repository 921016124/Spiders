import os
import sys
BASE_DIR = os.path.abspath(__file__)
sys.path.insert(0, BASE_DIR)

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from Python_PJ.YDMPython3 import PJ
from lxml import etree
import base64
import time
import random
import numpy as np


class SJinChuKou:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.username = "17611134148"
        self.pwd = "zxcv1234"
        self.url = "https://www.qichacha.com/user_login"
        self.sleep = 2

    def login(self):
        username = self.driver.find_element_by_id("nameNormal")
        username.click()
        time.sleep(0.3)
        for u in self.username:
            username.send_keys(u)
            time.sleep(0.3)
        time.sleep(1)
        pwd = self.driver.find_element_by_id("pwdNormal")
        pwd.click()
        time.sleep(0.3)
        for p in self.pwd:
            pwd.send_keys(p)
            time.sleep(0.3)
        time.sleep(2)

        self.hd_yanzheng()
        time.sleep(10)

    def get_Captcha(self, img_code):
        imgdata = base64.b64decode(img_code.replace("data:image/jpg;base64,", ""))
        file = open('1.jpg', 'wb')
        file.write(imgdata)
        file.close()

    def hd_yanzheng(self):
        with open("test.txt", 'w', encoding="utf-8") as fp:
            fp.write(self.driver.page_source)
        element = self.driver.find_element_by_id("nc_1_n1z")
        try:

            track_list = self.get_track(308)
            print("第一步,点击元素")
            ActionChains(self.driver).click_and_hold(on_element=element).perform()
            time.sleep(0.15)
            print("第二步，拖动元素")
            for track in track_list:
                ActionChains(self.driver).move_to_element_with_offset(to_element=element, xoffset=track, yoffset=0).perform()
                time.sleep(random.randint(10, 40) / 100)
                html = etree.HTML(self.driver.page_source)
                if html.xpath("//div[@id=\"nc_1__imgCaptcha_img\"]/img"):
                    print("图片验证码出现了！")
                    time.sleep(self.sleep)
                    self.get_Captcha(html.xpath("//div[@id=\"nc_1__imgCaptcha_img\"]/img/@src")[0])
                    pj = PJ()
                    Crackcaptcha = pj.Po_Jie()  # get Captcha
                    print(Crackcaptcha)
                    # 验证通过后的提示和操作
                    self.driver.quit()
                    exit()
                if html.xpath("//div[@id=\"nc_1__scale_text\"]/span/b/text()") == "验证通过":
                    print("验证通过了！！！，\r开始你的表演吧！")
                    time.sleep(10)
                    self.driver.quit()
                    exit("请开始爬取数据")
                    # 验证通过后的操作。

        except selenium.common.exceptions.StaleElementReferenceException:
            print("滑的太快了")
            a = 0
            a += 1
            if a > 5:
                self.driver.quit()
                time.sleep(self.sleep)
                self.login()
            time.sleep(self.sleep)
            self.driver.refresh()
            self.login()
        except selenium.common.exceptions.NoSuchElementException:
            self.driver.refresh()
        time.sleep(1)
        print("第三步，释放鼠标")
        # 释放鼠标
        ActionChains(self.driver).release(on_element=element).perform()
        time.sleep(3)
        time.sleep(1)
        ActionChains(self.driver).release().perform()

    def get_track(self, length):
        pass
        list = []
        x = round(random.random(), 1)
        while length - x >= 5:
            list.append(x)
            length = length - x
            x = round(random.random(), 1)
        for i in np.around(length, 0, -0.1).astype(list):
            list.append(round(i))
        a = 0
        new_list = []
        for i in list:
            a += i
            new_list.append(a)
        return new_list

    def main(self):
        self.driver.get(self.url)
        self.driver.find_element_by_id("normalLogin").click()
        time.sleep(self.sleep)

        self.login()

        self.driver.quit()


if __name__ == '__main__':
    s = SJinChuKou()
    s.main()
