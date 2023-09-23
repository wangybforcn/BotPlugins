#p站搜索图片
#p站随机涩图
#从每日排行里找， 随机日期，随机图片

# -*- coding=utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exc
from selenium.common.exceptions import NoSuchElementException
from func_timeout import func_set_timeout
import requests
import time
import pytz
from datetime import datetime
import random
import json
import re

#程序超时时间
@func_set_timeout(45)

def random_pictures(types):
    
    print("\nRunning random_pictures()...")

    #只统计最近5年的
    now_time_cn = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y%m%d")
    """
    年份now_time_cn[:4]
    月份now_time_cn[4:6]
    日now_time_cn[6:]
    """
    random_day = random.randint(1, 28)
    random_month = random.randint(1, 12)
    random_year = random.randint(int(now_time_cn[:4]) - 5, int(now_time_cn[:4]))

    #同年时月份不能超过
    if random_year == int(now_time_cn[:4]):
        random_month = random.randint(1, int(now_time_cn[4:6]))

        #同月时日期不能超过
        if random_month == int(now_time_cn[4:6]):
            random_day = random.randint(1, int(now_time_cn[6:]) - 1)

    random_month = "{:02d}".format(random_month)
    random_day = "{:02d}".format(random_day)
    random_date = str(random_year) + str(random_month) + str(random_day)
    random_date = int(random_date)


    #获取排行榜网页
    #更改tags：一般/r18/女性受欢迎/男性受欢迎
    #r18tag在mode后加_r18即可
    if types == 1:  #一般
        url = f"https://www.pixiv.net/ranking.php?mode=daily&date={random_date}"
    elif types == 2:    #r18
        url = f"https://www.pixiv.net/ranking.php?mode=daily_r18&date={random_date}"
    elif types == 3:    #男性欢迎
        url = f"https://www.pixiv.net/ranking.php?mode=male&date={random_date}"
    else:   #女性欢迎(4)
        url = f"https://www.pixiv.net/ranking.php?mode=female&date={random_date}"


    #url = f"https://www.pixiv.net/ranking.php?mode=daily_r18&date=20200215"

    print("    Getting daily url complete...")
    print("        Daily url: " + url)

    #浏览器初始化
    opts = webdriver.ChromeOptions()
   
    
    #无头模式
    #root下跑
    #防止devtools问题
    opts.add_argument("-no-sandbox")
    opts.add_argument("-disable-dev-shm-usage")
    
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    

    #防止机器人识别
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])

    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(options=opts)

    #登录cookie，刷新
    #调试路径和bot路径
    with open("./qds_bot/plugins/search-images-pixiv/cookies.txt", "r", encoding="utf-8") as f:
    #with open("./search-images-pixiv/cookies.txt", "r", encoding="utf-8") as f:
        cookielist = json.loads(f.read())


    driver.get(url=url)
    
    #登录cookie
    cookie_list = []
    for cookie in cookielist:
        cookiedict = {
            "domain": cookie.get('domain'),
            #"expiry": cookie.get('expiry'),    该参数无效
            "httpOnly": cookie.get('httpOnly'),
            "name": cookie.get("name"),
            "path": "/",
            "sameSite": "Lax",
            "secure": cookie.get("secure"),
            "value": cookie.get("value"),
        }

        cookie_list.append(cookiedict)

        driver.add_cookie(cookie_dict=cookiedict)


    driver.refresh()

    #等待加载
    WebDriverWait(driver, 4).until(exc.visibility_of_element_located((By.XPATH, "//div[@class='ranking-items adjust']")))
    #拖动滚动条一次
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #等待拖动后加载
    time.sleep(2)
    
    #现在在每日排行榜界面
    print("    Getting image url...")
    #随机出排行榜上的图片链接
    #如果图片的排名（属性id）不存在则重新获取
    while True:
        
        try:
            intlog = 0

            #获取随机id
            random_int = random.randint(1, 100)
            pic_src = driver.find_element(By.XPATH, f"//div[@class='ranking-items adjust']/section[@id='{random_int}']/div[2]/a").get_attribute("href")

            print("        Getting random rank id complete...")
            print("            Now image url: " + pic_src)

            #进入选中图片页面
            driver.get(pic_src)

            #等待tag加载
            WebDriverWait(driver, 6).until(exc.visibility_of_element_located((By.XPATH, "//footer[@class='sc-1u8nu73-4 iIqZwB']")))

            #检查页数是否大于4，大于4则直接重新跑
            print("        Checking pages is more than 4...")
            try:
                pages = driver.find_element(By.XPATH, "//div[@class='sc-1mr081w-0 kZlOCw']").text
                if int(pages[2:]) > 4:

                    print("            Pages is more than 4... Back to daily rank web and getting image url again...")
                    #返回ranking界面
                    driver.back()
                    WebDriverWait(driver, 6).until(exc.visibility_of_element_located((By.XPATH, "//div[@class='ranking-items adjust']")))
                    #拖动滚动条一次
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(3)

                    continue
            except (ValueError, NoSuchElementException):
                pass
            print("            Image pages is less than 4 or dont have pages...")
            
            #检查是否有漫画标签
            #tag中存在漫画则返回ranking界面
            #不存在则直接返回
            print("        Chacking is '#manga' in footer...")
            footers = driver.find_element(By.XPATH, "//footer[@class='sc-1u8nu73-4 iIqZwB']").text
            if "manga" in footers:
                print("            Image footer have '#manga'... Back to daily rank web and change image url...")

                #返回ranking界面
                driver.back()
                WebDriverWait(driver, 6).until(exc.visibility_of_element_located((By.XPATH, "//div[@class='ranking-items adjust']")))
                #拖动滚动条一次
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(3)
                
                continue
            else:
                #直接退出
                print("            Image don't have '#mange'... Break...")
                break

            """
            try:
                driver.find_element(By.XPATH, "//div[@class='sc-1mr081w-0 kZlOCw']")
                continue
            except NoSuchElementException:
                break
            """
        except NoSuchElementException:
            #NoSuchElementException用于防止不存在id
            print(f"        There's no id {random_int} in daily rank...  Getting image url again...")
            continue
    
    print("    Getting image url complete...")
    print("        Image url: " + pic_src)

    #获取画师id，图片id
    print("    Getting image info...")
    name = driver.find_element(By.XPATH, "//a[@class='sc-d98f2c-0 sc-10gpz4q-6 fATptn']/div").text
    pid = pic_src[31:]
    
    #存在标签页变量为1，不存在为0（判断是否多图）
    try:
        driver.find_element(By.XPATH, "//div[@role='presentation']/div/div/div/div/div/div[@class='sc-1mr081w-0 kZlOCw']")
        intlog = 1
    except NoSuchElementException:
        intlog = 0

    #print(intlog)

    """
    print(footers)
    print(pic_src)
    print(intlog)
    """

    #等待图片加载
    WebDriverWait(driver, 10).until(exc.visibility_of_element_located((By.XPATH, "//div[@role='presentation']"))) 
               
    #返回图片链接
    #压缩
    #pic = driver.find_element(By.XPATH, "//img[@class='sc-1qpw8k9-1 jOmqKq']").get_attribute("src")

    print("    Getting big image url...")

    #非压缩
    #多图则在打开大图时多点击一次
    if intlog == 0:
        driver.find_element(By.XPATH, "//img[@class='sc-1qpw8k9-1 jOmqKq']").click()
    if intlog == 1:
        actionpar = driver.find_element(By.XPATH, "//img[@class='sc-1qpw8k9-1 jOmqKq']")
        action = ActionChains(driver).move_to_element(actionpar)
        action.click().perform()
        time.sleep(2)
        action.move_by_offset(0, -50).click().perform()
  

    #等待大图加载
    time.sleep(3)
    while True:
        try:
            time.sleep(2)
            pic = driver.find_element(By.XPATH, "//div[@class='sc-1pkrz0g-1 cKLKGN']/img").get_attribute("src")
            break
        except NoSuchElementException:
            continue
    

    print("    Getting big image url complete...")
    print("        Big image url: " + pic)


    print("Running requesting...")

    #header和禁用警告
    headers = {'Referer': 'https://www.pixiv.net/'}
    #urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    #verify禁用证书
    session = requests.Session()
    session.headers.update(headers)
    #session.verify = False
    #pics = requests.get(url=pic, headers=headers, verify=False, timeout=timeout)

    pics = session.get(pic) 


    print("    Sorting image...")
    
    #将内容存到图片文件中
    with open("./qds_bot/plugins/search-images-pixiv/1.jpg", "wb+") as picture:
    #with open("./search-images-pixiv/1.jpg", "wb+") as picture:
        picture.write(pics.content)
        f.close()
        
        print("    Image sort completed...")

    if pic == None:
        print("    No Image...")

    driver.close()

    return name, pid

#random_pictures(1)



#关键字搜索图片
def search_img(tags):

    #构建搜索的url
    if tags.length == 1:
        url = f"https://www.pixiv.net/tags/{tags}/artworks?p=2&s_mode=s_tag"
    elif tags.length == 0:
        pic = None
        return pic
    else:
        all_tags = "%20".join(tags)
        url = f"https://www.pixiv.net/tags/{all_tags}/artworks?p=2&s_mode=s_tag"
    

    #浏览器初始化
    opts = webdriver.ChromeOptions()
   
    
    #无头模式
    #root下跑
    #防止devtools问题
    opts.add_argument("-no-sandbox")
    opts.add_argument("-disable-dev-shm-usage")

    """
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    """

    #防止机器人识别
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(options=opts)

    #登录cookie，刷新
    #调试路径和bot路径
    with open("./qds_bot/plugins/search-images-pixiv/cookies.txt", "r", encoding="utf-8") as f:
    #with open("./search-images-pixiv/cookies.txt", "r", encoding="utf-8") as f:
        cookielist = json.loads(f.read())


    driver.get(url=url)

    #登录cookie
    cookie_list = []
    for cookie in cookielist:
        cookiedict = {
            "domain": cookie.get('domain'),
            #"expiry": cookie.get('expiry'),    该参数无效
            "httpOnly": cookie.get('httpOnly'),
            "name": cookie.get("name"),
            "path": "/",
            "sameSite": "Lax",
            "secure": cookie.get("secure"),
            "value": cookie.get("value"),
        }

        cookie_list.append(cookiedict)

        driver.add_cookie(cookie_dict=cookiedict)


    driver.refresh()