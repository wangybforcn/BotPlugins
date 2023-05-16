#随机pixiv涩图和搜索pixiv涩图

# -*- coding="utf-8" -*-

from .search import random_pictures

from nonebot import on
from nonebot.rule import Rule, to_me, keyword
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, PrivateMessageEvent, GroupMessageEvent, MessageSegment
from nonebot.params import EventPlainText
from typing import Annotated
from func_timeout import func_set_timeout
from func_timeout.exceptions import FunctionTimedOut
import os
import urllib.parse
import urllib.request



rule_random_pic_1 = keyword("随机图片", "美图")
rule_random_pic_2 = to_me()
rule_random_pic = rule_random_pic_1 & rule_random_pic_2

random_pic = on(rule=rule_random_pic)

@random_pic.handle()
async def funcrandom(event: MessageEvent, bot: Bot, msg_all: Annotated[str, EventPlainText()]):
    await random_pic.send("猫猫正在逛pixiv喵♪~\n"+
                          "请稍后喵♪~")
    
    name = ""
    pid = ""

    try:
        if "男" in msg_all:
            name, pid = random_pictures(types=4)
        elif "女" in msg_all:
            name, pid = random_pictures(types=3)
        else:
            name, pid = random_pictures(types=1)
    except FunctionTimedOut:
        await random_pic.send("哎呀！猫猫忘了把图带回来了喵♪...\n"+
                               "下次一定喵♪~")
        await random_pic.finish() 
         
    #获取path
    #注意文件打开路径
    #应该在QDs-bot文件夹打开
    img_path = os.path.abspath("./qds_bot/plugins/search-images-pixiv/1.jpg")

    #使用urllib将本地路径转化为url
    #"E:\bots\QDs-bot\qds_bot\plugins\search-images-pixiv\1.png"
    url = urllib.request.pathname2url(img_path)
    #msgs = f"[CQ:image,file={img_url}]"
    cqcode = MessageSegment.image(file="file:" + url)

    if isinstance(event, GroupMessageEvent):
        print("Bot now sending image...")
        await bot.send_group_msg(group_id=event.group_id,
                                    message=f"随机图片喵♪！\n画师: {name}\npid： {pid}" + cqcode)
    elif isinstance(event, PrivateMessageEvent):
        print("Bot now sending image...")
        await bot.send_private_msg(user_id=event.user_id,
                                    message=f"随机图片喵♪！\n画师: {name}\npid： {pid}" + cqcode)
        
    await random_pic.finish()





#r18随机
rule_random_pic_1 = keyword("色图", "瑟图", "涩图")
rule_random_pic_2 = to_me()
rule_random_pic = rule_random_pic_1 & rule_random_pic_2

random_pic = on(rule=rule_random_pic)

@random_pic.handle()
async def funcrandom(event: MessageEvent, bot: Bot, msg_all: Annotated[str, EventPlainText()]):

    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
                                    message="群聊打咩喵♪！\n色图只能自己偷偷看喵♪！")
        await random_pic.finish()

    await random_pic.send("猫猫正在逛pixiv喵♪~\n"+
                          "请稍后喵♪~")
    
    try:
        name, pid = random_pictures(types=2)
    except FunctionTimedOut:
        await random_pic.send("冲...冲了喵♪！\n"+
                               "啊！图丢了喵♪...\n" +
                               "下次一起冲喵♪")
        await random_pic.finish() 
   
    #获取path
    #注意文件打开路径
    #应该在QDs-bot文件夹打开
    img_path = os.path.abspath("./qds_bot/plugins/search-images-pixiv/1.jpg")

    #使用urllib将本地路径转化为url
    #"E:\bots\QDs-bot\qds_bot\plugins\search-images-pixiv\1.png"
    url = urllib.request.pathname2url(img_path)
    #msgs = f"[CQ:image,file={img_url}]"
    cqcode = MessageSegment.image(file="file:" + url)

    if isinstance(event, PrivateMessageEvent):
        print("Bot now sending image...")
        await bot.send_private_msg(user_id=event.user_id,
                                        message=f"随机图片喵♪！\n画师: {name}\npid： {pid}" + cqcode)
        
    await random_pic.finish()
