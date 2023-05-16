#介绍、回复规则

import time
from datetime import datetime
import pytz
import random

from nonebot import on_command,on, on_fullmatch, on_keyword
from nonebot.rule import to_me, keyword, fullmatch
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Event, PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER



#自我介绍
rule_sayhi1 = keyword("使用方法", "介绍", "自我介绍")
rule_sayhi_all = rule_sayhi1 & to_me()

rules_hi = on(rule=rule_sayhi_all)
@rules_hi.handle()
async def say_hi():
    await rules_hi.send("(｡･∀･)ﾉﾞ 你好喵♪~\n"+
                     "我是来自维多利亚的天才猫猫bot--迷迭香二号喵♪~\n"+
                     "你可以叫我迷迭香猫猫或者香香喵♪~\n"+
                     "是 @青灯 的女儿喵♪~，但是现在很多机能还在开发中喵♪！\n"+
                     "会努力变强的喵♪！\n"+
                     "----------------------\n"+
                     "@猫猫 或者 私聊猫猫，然后使用“/”或者直接叫“猫猫”输入指令喵♪~\n"+
                     "输入“猫猫 全部指令”查看全部功能喵♪~\n"+
                     "----------------------\n")
    
    await rules_hi.finish()
    



#全部指令
rules_seeall = on_keyword("全部指令", rule=to_me())

@rules_seeall.handle()
async def rtn_weather():
    await rules_seeall.send("猫猫的全部指令喵♪~\n"+
                            "----------------------\n"+
                            "查看天气喵♪~\n"+
                            "    叫猫猫后输入“天气”与城市名喵♪~\n"+
                            "    我会回复天气信息的喵♪~\n"+
                            "----------------------\n"+
                            "猫猫便签喵♪~\n"+
                            "   叫猫猫后输入“便签”即可喵♪~\n"+
                            "   目前支持记录、更新、删除喵♪~\n"+
                            "   私聊猫猫使用喵♪~\n"+
                            "---------------------\n"+
                            "当前季度番剧更新表喵♪~\n"+
                            "   叫猫猫后输入“番剧”即可喵♪~\n"
                            "---------------------\n"+
                            "查找b站用户喵♪~\n"+
                            "   叫猫猫后输入“查用户” 或 “找用户”喵♪~\n"+
                            "   然后输入想要查找的用户信息即可喵♪~\n"+
                            "---------------------\n"+
                            "发出一张随机图片喵♪~\n"+
                            "   叫猫猫后输入“随机图片” 或 “美图”喵♪~\n"+
                            "   猫猫就会从pixiv搬运一张随机图片喵♪~"+
                            "   猫猫色图功能当然也有喵♪~\n"+
                            "   但是群聊打咩喵♪！\n"+
                            "---------------------\n")
    
    await rules_seeall.finish()
    


#打招呼
rule_insa1 = keyword("迷迭香猫猫", "香香", "香香~", "在么猫猫", "迷迭香猫猫~", "猫~猫~", "在吗猫猫"\
                     , "早", "午", "晚好", "晚上")
rule_insa_all = to_me() & rule_insa1

insanya = on(rule=rule_insa_all)

@insanya.handle()
async def insanyas():
    now_time_cn = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%H:%M")

    if 6 <= int(now_time_cn[0: 2]) <= 10:
        await insanya.send("早上好喵♪~，今天也是元气满满的一天喵♪~")
    elif 10 < int(now_time_cn[0: 2]) <= 14:
        await insanya.send("中午好喵♪~，记得按时吃饭喵♪~")
    elif 14 < int(now_time_cn[0: 2]) <= 18:
        await insanya.send("下午好喵♪~，今天的的学业或工作有认真对待喵♪？")
    elif 18 < int(now_time_cn[0: 2]) <= 24:
        await insanya.send("晚上好喵♪~，今天也是一个不眠夜喵♪？")
    else:
        await insanya.send("凌晨好喵♪~，快去睡觉喵♪！")
    
    await insanya.finish()

insanya_night = on_keyword("晚安", rule=to_me())

@insanya_night.handle()
async def insanyanigth():
    now_time_cn = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%H:%M")

    if 18 <= int(now_time_cn[0: 2]) <= 5:
        await insanya_night.send("晚安喵♪~\n做个好好梦喵♪~")
        await insanya_night.finish()
    else:
        await insanya_night.send("你是怎么在这个点睡得着觉的喵♪！\n起床喵♪！")
        await insanya_night.finish()



#随机数
random_nya = on_keyword("随机数", rule=to_me())

@random_nya.handle()
async def random_num():
    ints = random.randint(1, 6)
    await random_nya.send("随机数喵♪： " + str(ints))
    await random_nya.finish()