#快捷查询阿b用户
#爬虫部分
# -*- coding: utf-8 -*- 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exc
from selenium.common.exceptions import NoSuchElementException
import time


def get_bili_user_info(inp):
    #输入关键字并搜索

    url = "https://www.bilibili.com/"

    opt = webdriver.ChromeOptions()

    opt.add_argument("--headless")
    opt.add_argument("--disable-gpu")

    opt.add_experimental_option("excludeSwitches", ["enable-automation"])


    driver = webdriver.Chrome(options=opt) 
    driver.get(url=url)

    driver.find_element(By.XPATH, "//input[@class='nav-search-input']").send_keys(inp)
    driver.find_element(By.XPATH, "//div[@class='nav-search-btn']").click()

    driver.switch_to.window(driver.window_handles[1])
    #等待加载完成
    WebDriverWait(driver, 4).until(
        exc.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[2]/div/nav/ul/li[8]"))
    )

    #打开用户结果栏,等待结果加载完成
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[2]/div/nav/ul/li[8]/span/span[1]").click()

    WebDriverWait(driver, 4).until(
        exc.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div/div/h2/a"))
    )

    user_names = []
    user_links = []
    user_imgs = []
    user_fans = []
    #查询前六个用户，提供他们的头像名字视频数量用户链接
    for i in range(6):
        try:
            driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[{i+1}]/div/div/h2/a")
        except NoSuchElementException:
            break
        
        user_names.append(driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[{i+1}]/div/div/h2/a").text)
        user_links.append(driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[{i+1}]/div/div/h2/a").get_attribute("href"))
        user_imgs.append(driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[{i+1}]/div/a/div/div/div/div/img").get_attribute("data-src"))
        user_fans.append(driver.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[{i+1}]/div/div/p").text)
    

    driver.close()

    return user_names, user_links, user_imgs, user_fans
