#番剧时间表
#素材来源于yuc.wiki
#注意：网站为个人维护，所写格式不恒定，每季度应该更新爬虫

# -*- coding: utf-8 -*-

import datetime
import time

from nonebot import on, on_command, on_message
from nonebot.rule import to_me, keyword
from nonebot.params import Keyword, Command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, PrivateMessageEvent, GroupMessageEvent


from .run import monday_anime, tuesday_anime, wednesday_anime, thursday_anime, friday_anime, saturday_anime, sunday_anime



rule1 = to_me()
rule2 = keyword("番剧", "动漫", "番", "番剧更新", "番更新", "番剧时间", "番剧时间表", "番剧播出")
rules = rule1 & rule2

timetable = on(rule=rules)

@timetable.handle()
async def showtimetable(bot: Bot, event: MessageEvent):
    await timetable.send("猫猫会列出今天更新的番剧喵♪~")

    time.sleep(0.01)
    weekday = datetime.datetime.today().weekday() + 1

    if weekday == 1:
        msg_send = ""
        today_anime_name, today_anime_time, today_anime_picture = monday_anime()   #番的名字,时间，图片
        for name, times, url in zip(today_anime_name, today_anime_time, today_anime_picture):
            msg_send += f"[CQ:image,file={url}]\n{name} {times}"

        if isinstance(event, GroupMessageEvent):
            await bot.send_group_msg(group_id=event.group_id,
                                    message="今天是周一喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
        elif isinstance(event, PrivateMessageEvent):
            await bot.send_private_msg(user_id=event.user_id,
                                    message="今天是周一喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)

    elif weekday == 2:
        msg_send = ""
        today_anime_name, today_anime_time, today_anime_picture = tuesday_anime()   #番的名字,时间，图片
        for name, times, url in zip(today_anime_name, today_anime_time, today_anime_picture):
            msg_send += f"[CQ:image,file={url}]\n{name} {times}"

        if isinstance(event, GroupMessageEvent):
            await bot.send_group_msg(group_id=event.group_id,
                                    message="今天是周二喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
        elif isinstance(event, PrivateMessageEvent):
            await bot.send_private_msg(user_id=event.user_id,
                                    message="今天是周二喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
    elif weekday == 3:
        msg_send = ""
        today_anime_name, today_anime_time, today_anime_picture = wednesday_anime()   #番的名字,时间，图片
        for name, times, url in zip(today_anime_name, today_anime_time, today_anime_picture):
            msg_send += f"[CQ:image,file={url}]\n{name} {times}"

        if isinstance(event, GroupMessageEvent):
            await bot.send_group_msg(group_id=event.group_id,
                                    message="今天是周三喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
        elif isinstance(event, PrivateMessageEvent):
            await bot.send_private_msg(user_id=event.user_id,
                                    message="今天是周三喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
    elif weekday == 4:
        msg_send = ""
        today_anime_name, today_anime_time, today_anime_picture = thursday_anime()   #番的名字,时间，图片
        for name, times, url in zip(today_anime_name, today_anime_time, today_anime_picture):
            msg_send += f"[CQ:image,file={url}]\n{name} {times}"

        if isinstance(event, GroupMessageEvent):
            await bot.send_group_msg(group_id=event.group_id,
                                    message="今天是周四喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
        elif isinstance(event, PrivateMessageEvent):
            await bot.send_private_msg(user_id=event.user_id,
                                    message="今天是周四喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
    elif weekday == 5:
        msg_send = ""
        today_anime_name, today_anime_time, today_anime_picture = friday_anime()   #番的名字,时间，图片
        for name, times, url in zip(today_anime_name, today_anime_time, today_anime_picture):
            msg_send += f"[CQ:image,file={url}]\n{name} {times}"

        if isinstance(event, GroupMessageEvent):
            await bot.send_group_msg(group_id=event.group_id,
                                    message="今天是周五喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
        elif isinstance(event, PrivateMessageEvent):
            await bot.send_private_msg(user_id=event.user_id,
                                    message="今天是周五喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)

    elif weekday == 6:
        msg_send = ""
        today_anime_name, today_anime_time, today_anime_picture = saturday_anime()   #番的名字,时间，图片
        for name, times, url in zip(today_anime_name, today_anime_time, today_anime_picture):
            msg_send += f"[CQ:image,file={url}]\n{name} {times}"

        if isinstance(event, GroupMessageEvent):
            await bot.send_group_msg(group_id=event.group_id,
                                    message="今天是周六喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
        elif isinstance(event, PrivateMessageEvent):
            await bot.send_private_msg(user_id=event.user_id,
                                    message="今天是周六喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
    
    elif weekday == 7:
        msg_send = ""
        today_anime_name, today_anime_time, today_anime_picture = sunday_anime()   #番的名字,时间，图片
        for name, times, url in zip(today_anime_name, today_anime_time, today_anime_picture):
            msg_send += f"[CQ:image,file={url}]\n{name} {times}"

        if isinstance(event, GroupMessageEvent):
            await bot.send_group_msg(group_id=event.group_id,
                                    message="今天是周日喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)
        elif isinstance(event, PrivateMessageEvent):
            await bot.send_private_msg(user_id=event.user_id,
                                    message="今天是周日喵♪~\n有这些番剧更新了喵♪\n"+
                                "---------------------\n"+
                                msg_send)

    await timetable.finish()