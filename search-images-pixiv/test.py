import requests
import re
import bs4

url = "https://yuc.wiki/202307/"    #后方数字为番剧季度

headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ko;q=0.5',
}

response = requests.get(url, headers=headers)


htmlall = bs4.BeautifulSoup(response.content.decode(), 'lxml')

monday_position = htmlall.body.find("td", class_="date2")
tuesday_position = monday_position.find_next("td", class_="date2")
div_date_line = tuesday_position.find_next("div", class_="div_date")

#print(str(div_date_line))


search_line = r"(https://[^\s]+)\.jpg"

pic_link_disearch = div_date_line.find("img")['src']

print(str(pic_link_disearch))

pic_link = re.findall(search_line, str(pic_link_disearch))
pic_link_1 = str(pic_link[0]) + ".jpg"

print(str(pic_link_1))