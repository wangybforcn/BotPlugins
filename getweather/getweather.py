
#首先，我不想写注释！！！！！！！

import requests
from bs4 import BeautifulSoup


def get_weather(city):

    c = city

    #爬的google搜索的天气
    url = 'https://www.google.com/search?q='

    kw = {
        'q': str(c) + "天气"
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ko;q=0.5',
    }

    response = requests.get(url, headers=headers,params=kw)

    
    #上面为爬虫部分
    #下面为关键字检索部分


    soup = BeautifulSoup(response.content.decode(), 'lxml')

    if generalinfo := soup.body.find(class_='UQt4rd'):   #天气图表，并添加城市检测
        soup2 = BeautifulSoup(str(generalinfo), 'lxml')     #图标/气温/湿度/风速/降雨的那行
        

        tmpr = soup2.find(class_='wob_t q8U8x').get_text()  #温度
        rain = soup2.find('span', id='wob_pp').get_text()   #降雨概率
        hum = soup2.find('span', id='wob_hm').get_text()    #湿度
        all = soup2.find('img', id='wob_tci')   #图片以及文字天气描述
        all_alt = all.get("alt")



        now_weather = {
            'iscity': 1,    #检测是否为城市，是1否0
            'tmpr': tmpr,
            'rain': rain,
            'hum': hum,
            'all': all_alt,
        }

        return now_weather
    
    else:
        now_weather = {
            'iscity': 0,
        }

        return now_weather
