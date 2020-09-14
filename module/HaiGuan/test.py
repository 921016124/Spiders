from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = webdriver.PhantomJS()

driver.get(url="https://www.qichacha.com/user_login?back=%2F")
driver.find_element_by_id("normalLogin").click()
with open("test.txt", 'w', encoding="utf-8") as fp:
    fp.write(driver.page_source)