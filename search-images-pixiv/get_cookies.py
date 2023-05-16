from selenium import webdriver
import os
import time
import json
import urllib3
import urllib.parse
import urllib.request
from nonebot.adapters.onebot.v11 import MessageSegment
import eventlet
import requests

 
def browser_initial():
    """"
    进行浏览器初始化
    """
    browser = webdriver.Chrome()
    log_url = "https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=pc&view_type=page"
    return log_url,browser
 
def get_cookies(log_url,browser):
    """
    获取cookies保存至本地
    """
    browser.get(log_url)
    time.sleep(20)     # 进行扫码
    dictCookies = browser.get_cookies()    # 获取list的cookies
    jsonCookies = json.dumps(dictCookies) #  转换成字符串保存
    
    #打开plugins时路径正确
    with open('./search-images-pixiv/cookies.txt', 'w+', encoding='utf-8') as f:
        f.write(jsonCookies)


tur = browser_initial()
get_cookies(tur[0], tur[1])



#true_path = "file:///E:/bots/QDs-bot/qds_bot/plugins/search-images-pixiv/1.jpg"
