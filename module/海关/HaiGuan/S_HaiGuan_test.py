import sys
sys.path.append("/opt/")
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from lxml import etree
import base64
import cv2
import random
from Spiders.Utils_1 import Util
import os


class HaiGuan:
    def __init__(self, comp_name):
        self.url = "http://credit.customs.gov.cn/"
        self.comp_name = comp_name
        self.u = Util()

    def get_image(self, driver, img_xpath, img_name):
        strs = etree.HTML(driver.page_source).xpath(img_xpath)[0]
        str = strs.replace("data:image/jpg;base64,", "")
        imgdata = base64.b64decode(str)
        file = open(img_name, 'wb')
        file.write(imgdata)
        file.close()

    def is_similar(self, img):
        for i in range(0, 130):
            for j in range(0, 260):
                s = img[i, j].tolist()
                # if s[0] != 0 and s[1] <= 30 and s[2] == 0:
                if s[0] != 0 and s[1] <= 10 and s[2] <= 10:
                    return j

    def success_slide(self, driver):
        t = driver.find_elements_by_xpath(
            '//div[contains(@id, "layui-layer")]/div[@class="layui-layer-btn layui-layer-btn-"]/a')  
        if t:
            print("没有符合条件的数据,请检查输入条件后重试")
            conn = self.u.MySQL()
            up_sql = "update EXT_INV_ENTP_LST_INF set status = '1' where OVS_INV_NM LIKE '%{}%';".format("%".join([i for i in self.comp_name]))
            # print(up_sql)
            conn.cursor().execute(up_sql)
            conn.commit()
            driver.close()
        else:
            time.sleep(5)
            js_list = self.u.get_xpath_obj(driver.page_source).xpath(
                "//div[@id=\"coplist\"]/div[@class=\"sub2-bg\"]/@onclick")

            for js in js_list:
                if len(js_list) > 1:
                    handles = driver.window_handles
                    time.sleep(1)
                    driver.switch_to_window(handles[0])
                    time.sleep(1)
                    driver.execute_script("window.open(\"{}\")".format(driver.current_url))
                    handles = driver.window_handles
                    time.sleep(3)
                    driver.switch_to_window(handles[1])
                    time.sleep(1)
                    driver.refresh()
                    time.sleep(2)
                driver.execute_script(js)
                time.sleep(10)
                driver.execute_script(
                    """
                        var dataObj = localStorage.getItem(\"rowData\");
                        alert(dataObj);
                    """)
                time.sleep(2)
                data = self.u.get_json_obj(driver.switch_to.alert.text)
                time.sleep(1)
                driver.switch_to.alert.accept()
                t = ";".join(i.strip() for i in self.u.get_xpath_obj(driver.page_source)
                             .xpath("//*[@id=\"copInfoForm\"]/table/tbody/tr[8]/td[2]/text()"))[1:]

                from HaiGuanCredit import HaiGuanCredit
                hgc = HaiGuanCredit()
                hgc.handle_data(data, t, self.comp_name)
                time.sleep(5)
                driver.execute_script("window.close();")
            print("本次验证结束！！~")
            time.sleep(5)

    def slide(self, driver, loc, num):
        print(">>>>>第{}次滑动解锁开始！<<<<<".format(num))
        s = driver.find_elements_by_xpath('//div[@class="layui-layer-content"]/div[@id="slideBar"]')  # 验证图片的获取
        if s:
            # 生成x的移动轨迹点
            track_list = self.get_track(loc)
            # 找到滑动的圆球
            element = driver.find_element_by_xpath("//*[@id=\"slideBtn\"]")
            location = element.location
            # 获得滑动圆球的高度
            y = location['y']
            # 鼠标点击元素并按住不放
            print("第一步,点击元素")
            ActionChains(driver).click_and_hold(on_element=element).perform()
            time.sleep(0.15)
            print("第二步，拖动元素")
            for track in track_list:
                ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track + 21, yoffset=y - 445).perform()
                time.sleep(random.randint(10, 50) / 1500)
            for _ in range(5):
                ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y - 445).perform()

            print("第三步，释放鼠标")
            time.sleep(1)
            # 释放鼠标
            ActionChains(driver).release(on_element=element).perform()
            print("释放完毕")
            print(">>>>>第{}次滑动解锁结束！<<<<<".format(num))
            if s:  # 如果验证存在的话
                num += 1
                if num <= 5:
                    print("滑动解锁失败")
                    loc += 8
                    time.sleep(5)
                    self.slide(driver, loc, num)
                else:
                    time.sleep(5)
                    if driver.find_element_by_id("slideBar").is_displayed():
                        if driver.find_element_by_id("refreshBtn").is_displayed():
                            driver.find_element_by_xpath("//div[@id=\"refreshBtn\"]").click()
                        print(">>>验证码已更换")
                        time.sleep(2)
                        num = 1
                        im_a = self.handle_image(driver)
                        self.slide(driver, int(self.is_similar(im_a)) + 47, num)
                    else:
                        print("滑动解锁成功")
                        self.success_slide(driver)
            else:
                print("滑动解锁成功")
                self.success_slide(driver)
        else:
            print(">>>>>第{}次滑动解锁结束！<<<<<".format(num))
            print("滑动解锁成功")
            self.success_slide(driver)

    def get_track(self, length):
        list = []
        # 间隔通过随机范围函数来获得,每次移动一步或者两步
        x = random.randint(1, 3)
        # 生成轨迹并保存到list内
        while length-x >= 5:
            list.append(x)
            length = length-x
            x = random.randint(2, 5)
        # 最后五步都是一步步移动
        for i in range(length):
            list.append(1)
        return list

    def handle_image(self, driver):
        img_xpath = "//img[@id=\"slideImg\"]/@src"
        self.get_image(driver, img_xpath, "1.jpg")
        img = cv2.imread("1.jpg")
        try:
            im2 = cv2.resize(img, (260, 130), )
            cv2.imwrite("2.jpg", im2)
        except cv2.error:
            return None
        return im2

    def get_start(self):
        # 打开火狐浏览器
        options = webdriver.ChromeOptions()
        # options.add_argument('disable-infobars')
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        # options.add_argument('--disable-setuid-sandbox')
        try:
            driver = webdriver.Chrome(options=options)
            # driver = webdriver.PhantomJS()
            # 用火狐浏览器打开网页
        except selenium.common.exceptions.TimeoutException:
            time.sleep(10)
            driver = webdriver.Chrome(options=options)
        except selenium.common.exceptions.webdriverexception:
            time.sleep(30)
            driver = webdriver.Chrome(options=options)

        driver.get(self.url)
        time.sleep(2)
        input = driver.find_element_by_id("ID_codeName")
        input.send_keys(self.comp_name)
        submit = driver.find_element_by_class_name("serch_ico1")
        time.sleep(1)
        submit.click()
        # driver.maximize_window()
        time.sleep(5)
        return driver

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
        print("程序出错，正在重启~~~")

    def main(self):
        print("企业信息查询开始")
        num = 1
        # 初始化浏览器并得到页面
        driver = self.get_start()
        # 得到图片并处理
        if self.handle_image(driver) is not None:
            im2 = self.handle_image(driver)
            # 进入滑动验证部分
            self.slide(driver, int(self.is_similar(im2)) + 47, num)
        else:
            self.restart_program()
        driver.quit()
        print("一次查询结束")


if __name__ == '__main__':
    hg = HaiGuan("深圳市金利洁科技有限公司")
    hg.main()
