#google搜索
#烂尾了，现在暂时不想写


# -*- coding: utf-8 -*- 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exc
from selenium.common.exceptions import NoSuchElementException

import time


def google_search(inp):
    #输入关键字并搜索

    url = "https://www.google.com/"

    opt = webdriver.ChromeOptions()
    """
    opt.add_argument("--headless")
    opt.add_argument("--disable-gpu")
    """
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])


    driver = webdriver.Chrome(options=opt) 
    driver.get(url=url)

    driver.find_element(By.XPATH, "//textarea[@class='gLFyf']").send_keys(inp)
    driver.find_element(By.XPATH, "//textarea[@class='gLFyf']").send_keys(Keys.ENTER)

    #等待加载完成
    WebDriverWait(driver, 4).until(
        exc.visibility_of_element_located((By.XPATH, "//div[@class='MjjYud']"))
    )

    #搜索结果
    driver.find_element(By.XPATH, "//div[@class='MjjYud']")


    while True:
        time.sleep(1)

    driver.close()

