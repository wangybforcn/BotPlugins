#查询啊b用户

#-*- coding=utf-8 -*-

from .get_info import get_bili_user_info

from nonebot import on
from nonebot.rule import to_me, keyword
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import ArgPlainText

import time
import re

rule1 = keyword("查用户", "用户查询", "查询用户", "查找用户", "找用户")
rule2 = to_me()

rule_all = rule1 & rule2

search_bili_user = on(rule=rule_all)

@search_bili_user.got("key1", prompt="请告诉我需要查找的内容喵♪~\n我会返回默认顺序的前六条b站用户信息喵♪~\n" +
                                "这会耗费一些时间喵♪~")
async def return_data(bot: Bot, event: MessageEvent, key: str = ArgPlainText("key1")):
    await search_bili_user.send(f"好的喵♪~\n正在查找和 {key} 相关的用户内容喵♪~")

    user_names, user_links, user_imgs, user_fans = get_bili_user_info(key)

    time.sleep(0.1)

    msgs = ""

    for name, link, img, fans in zip(user_names, user_links, user_imgs, user_fans):
        try:
            imgs = re.match("(.+\.jpg)", img).group()

        except AttributeError:
            imgs = re.match("(.+\.gif)", img).group()
            
        msgs += f"[CQ:image,file={imgs}]\n{name}\n{fans}\n{link}\n"

    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
                                    message="这是搜索结果喵♪~\n----------------------" +
                                    msgs + "\n---------------------")
    elif isinstance(event, PrivateMessageEvent):
            await bot.send_private_msg(user_id=event.user_id,
                                    message="这是搜索结果喵♪~\n----------------------" +
                                    msgs + "\n---------------------")
    
    search_bili_user.finish()