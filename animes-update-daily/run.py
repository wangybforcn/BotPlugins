# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime
import re

#获取现在月份、年度
now_time_cn_month = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%m")
now_time_cn_year = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y")

#匹配番剧时间表
def get_month(now_month):
    if 1 <= int(now_month) < 4:
        return "01"
    elif 4 <= int(now_month) < 7:
        return "04"
    elif 7 <= int(now_month) < 10:
        return "07"
    else:
        return "10"

month = get_month(now_time_cn_month)
year = str(now_time_cn_year)

#网站每季度格式不一样，记得重新写
url = "https://yuc.wiki/" + year + month + "/"    #后方数字为番剧季度

headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ko;q=0.5',
}

response = requests.get(url, headers=headers)
htmlall = BeautifulSoup(response.content.decode(), 'lxml')

#周一到周日，包括网络放送s
monday_position = htmlall.body.find("td", class_="date2")    #找到第一个class=date2的那行/周一
tuesday_position = monday_position.find_next("td", class_="date2")    #找到下一行class=date2的行/周二
wednesday_position = tuesday_position.find_next("td", class_="date2")   #周三
thursday_position = wednesday_position.find_next("td", class_="date2")  #周四
friday_position = thursday_position.find_next("td", class_="date2") #周五
saturday_position = friday_position.find_next("td", class_="date2") #周六
sunday_position = saturday_position.find_next("td", class_="date2") #周日
webcast_position = sunday_position.find_next("td", class_="date2")  #网络放送

#使用函数递归完成遍历的操作
#输入日期标签（周一 火，这种）的位置
def recursion_func(first_day_position):

    #标签行迭代
    div_date_line = first_day_position.find_next("div", class_="div_date")  #找到需要输出的上一个div
    output_name_line = div_date_line.find_next("div").find("td") #输出行,番剧名字
    output_time_line = div_date_line.find(class_="imgep")   #番剧当日播出时间
    output_picture_line = div_date_line.find("img")['src'] #封面图 

    search_line = r"(https://[^\s]+)\.jpg"
    pic_link = re.findall(search_line, str(output_picture_line))
    output_pic_link = str(pic_link[0]) + ".jpg" 

    #将内容输出到列表result中
    result_name = [output_name_line.get_text()]
    result_time = [output_time_line.get_text()]
    result_picture = [output_pic_link]

    #负责循环次数，递归调用循环直到如下条件
    search_line = output_name_line.find_next("div")
    if search_line.has_attr("style") and "clear:both" not in search_line.get("style"):
        sub_result_name, sub_result_time, sub_result_picture = recursion_func(div_date_line)
        result_name += sub_result_name
        result_time += sub_result_time
        result_picture += sub_result_picture
    
    return result_name, result_time, result_picture


#网络放送有一个标签不同：div_date_
"""
def recursion_func_web(first_day_position):

    #标签行迭代
    div_date_line = first_day_position.find_next("div", class_="div_date_")  #找到需要输出的上一个div
    output_line = div_date_line.find_next("div").find(class_="date_title_") #输出行

    #将内容输出到列表result中
    result = [output_line.get_text()]

    #负责循环次数，递归调用循环直到如下条件
    search_line = output_line.find_next("div")
    if search_line.has_attr("style") and "clear:both" not in search_line.get("style"):
        result += recursion_func_web(div_date_line)
    
    return result
"""

#周一到周日以及网络放送的返回
def monday_anime():
    return recursion_func(monday_position)

def tuesday_anime():
    return recursion_func(tuesday_position)

def wednesday_anime():
    return recursion_func(wednesday_position)

def thursday_anime():
    return recursion_func(thursday_position)

def friday_anime():
    return recursion_func(friday_position)

def saturday_anime():
    return recursion_func(saturday_position)

def sunday_anime():
    return recursion_func(sunday_position)

"""
def webcast_anime():
    return recursion_func_web(webcast_position)
"""