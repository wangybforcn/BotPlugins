#便签插件喵

#未添加定时提醒功能，数量限制功能

# -*-coding:utf-8 -*-
import time
import sqlite3
import pytz
from datetime import datetime

from nonebot import on_command, on, MatcherGroup
from nonebot.rule import to_me, keyword
from nonebot.adapters import Message, Event, Bot
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg, Keyword, EventPlainText, Arg, ArgStr, ArgPlainText, RawCommand
from typing import Annotated
from nonebot.permission import SUPERUSER

#会话触发
rule1 = keyword("便签")
rule_all = to_me() & rule1
ntc_start = on(rule=rule_all)

#连接数据库
database = sqlite3.connect('./qds_bot/plugins/notice/memory_data.db')
cur = database.cursor()

table_name = "notices"
cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
res = cur.fetchone()
#检测是否存在notice表，不存在则创建
if  res:
    pass
else:
    cur.execute('''CREATE TABLE notices
                        (ids TEXT PRIMARY KEY, user_id INTEGER, datas TEXT, time TEXT, time_second TEXT)''')

cur.close()
database.close()

user_id = 0


#前言
@ntc_start.handle()
async def notices(event: Event, msgevent: MessageEvent, bot: Bot):
    global user_id

    now_user = event.get_user_id()
    user_id = now_user

    if msgevent.message_type == "private":

        #检查superuser
        if user_id in bot.config.superusers:
            await ntc_start.send("这是猫猫便签的超级用户界面喵♪！\n"+
                                "----------------------\n"+
                                "输入“/start”后下一个消息将会记录为便签喵♪~\n"+
                                "输入“/show”后将展示所有便签喵♪~\n"+
                                "输入“/showall”后展示所有用户的所有便签喵♪\n"+
                                "在展示模式下输入“/delete”后进入删除模式喵♪~，可以删除便签喵♪~\n"+
                                "在展示模式下输入“/update”进入修改模式喵♪~，可以修改改便签内容喵♪~\n"+
                                "输入其他则退出便签功能喵♪~\n"+
                                "----------------------")
        
        else:
            await ntc_start.send("欢迎使用猫猫的临时便签功能喵♪~\n"+
                                "----------------------\n"+
                                "输入“/start”后下一个消息将会记录为便签喵♪~\n"+
                                "输入“/show”后将展示所有便签喵♪~\n"+
                                "在展示模式下输入“/delete”后进入删除模式喵♪~，可以删除便签喵♪~\n"+
                                "在展示模式下输入“/update”进入修改模式喵♪~，可以修改改便签内容喵♪~\n"+
                                "输入其他则退出便签功能喵♪~\n"+
                                "----------------------")
        
    else:
        await ntc_start.send("请在私聊中使用便签功能喵♪~\n群聊打咩喵♪！")
        await ntc_start.finish()
        
#获取回复
@ntc_start.got("key1", prompt="请输入指令喵♪~")
async def howtorun(bot: Bot, keys: str = ArgPlainText("key1")):
    time.sleep(0.01)
    if "/start" in keys:
        await ntc_start.send("你的下个消息将会被记录成为便签喵♪~\n"+
                        "请输入便签内容喵♪~\n"+
                        "----------------------")
        
    elif keys == "/show":
        await ntc_start.send("下面将展示出你的所有便签喵♪~\n"+
                             "----------------------")
        time.sleep(0.01)
        
        #展示用户便签内容
        database = sqlite3.connect('./qds_bot/plugins/notice/memory_data.db')
        cur = database.cursor()

        #查询数据并返回一个元组
        cur.execute("SELECT datas, time, ROW_NUMBER() OVER(ORDER BY time_second ASC) AS n_id \
                    FROM notices \
                    WHERE user_id=(?) \
                    ORDER BY time ASC", (user_id, ))
        showtable = cur.fetchall()

        #i[0]与i[1]根据输出位查询的输出位置不同而不同
        message = ""
        for i in showtable:
            message += f"便签id: {i[2]}    记录时间: {i[1]} \n {i[0]} \n----------------------\n"

        await ntc_start.send(message)
        time.sleep(0.01)
        await ntc_start.send("----------------------\n"+
                             "接下来要进行什么操作喵♪？\n"+
                             "输入“/update”可以修改便签内容喵♪~\n"+
                             "输入“/delete”可以删除便签喵♪~\n"+
                             "输入其他内容退出便签功能喵♪~")
        time.sleep(0.01)
        cur.close()
        database.close()

        await ntc_start.finish()
    
    #超级用户的用于所有数据库的管控
    elif keys == "/showall" and user_id in bot.config.superusers:
         #展示所有用户便签内容
        database = sqlite3.connect('./qds_bot/plugins/notice/memory_data.db')
        cur = database.cursor()

        #查询数据并返回一个元组
        cur.execute("SELECT user_id, datas, time, ROW_NUMBER() OVER(ORDER BY time_second ASC) AS n_id \
                    FROM notices", ( ))
        showtable = cur.fetchall()

        message = ""
        for i in showtable:
            message += f"便签id: {i[3]}\n记录者id: {i[0]}    记录时间: {i[2]} \n {i[1]} \n----------------------\n"

        await ntc_start.send(message)
        time.sleep(0.01)
        await ntc_start.send("----------------------\n"+
                             "输入“/deletemore”可以进入管理员删除模式喵♪~\n"+
                             "输入其他内容退出便签功能喵♪~")
    
        time.sleep(0.01)
        cur.close()
        database.close()

        await ntc_start.finish()

    else:
        await ntc_start.send("便签功能关闭喵♪~")
        await ntc_start.finish()


#写便签
@ntc_start.got("key2")
async def wtirenotice(notice: str = ArgPlainText("key2")):

    now_time_cn = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%m-%d")
    now_time_cn_s = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%m-%d-%h-%M-%S")
    now_time_cn_second = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%m-%d-%h-%M-%S")

    #数据库操作
    database = sqlite3.connect('./qds_bot/plugins/notice/memory_data.db')
    cur = database.cursor()

    #应该使用开始事务和提交事务
    cur.execute("BEGIN TRANSACTION")
    cur.execute("INSERT INTO notices(ids, user_id, datas, time, time_second) VALUES (?, ?, ?, ?, ?)", 
                    (now_time_cn_s, user_id, notice, str(now_time_cn), str(now_time_cn_second)))
    database.commit()

    cur.close()
    database.close()

    await ntc_start.send("----------------------\n"+
                        "便签记录好了喵♪~")
    await ntc_start.finish()


#删除和修改
todo = 0
update_and_delete = on_command("update", aliases={"delete", "deletemore"})

@update_and_delete.handle()
async def updateanddelete(command: Annotated[str, RawCommand()]):
    global todo
    if command == "/update":
        await update_and_delete.send("输入便签id来选择要更新的便签喵♪~\n"+
                                     "如果输入的内容不包含便签id就会退出便签功能喵♪~")
        todo = 1
    elif command == "/delete":
        await update_and_delete.send("输入需要删除的便签id来删除这个便签喵♪~\n"+
                                     "如果输入的内容不包含便签id就会退出便签功能喵♪~")
        todo = 2
    elif command == "/deletemore":
        await update_and_delete.send("输入一个或多个需要删除的便签id来删除这个便签喵♪~\n"+
                                     "多个需要删除的id请用“，”隔开喵♪~")
        todo = 3
    else:
        await ntc_start.send("便签功能关闭喵♪~")
        await ntc_start.finish()


#删除
n_id = 0
@update_and_delete.got("key3")
async def updatenotice(key: str = ArgPlainText("key3")):
    global todo, n_id

    if todo == 2:
        await update_and_delete.send("删除id为" + key + "的便签喵♪~")

        database = sqlite3.connect('./qds_bot/plugins/notice/memory_data.db')
        cur = database.cursor()
        cur.execute("SELECT datas, ROW_NUMBER() OVER(ORDER BY time_second ASC) AS n_id \
                    FROM notices WHERE user_id=(?)", (user_id, )) 
        n_id_find = cur.fetchall()
        n_id_data = ""
        for item in n_id_find:
            if str(item[1]) == key:
                n_id_data = str(item[0])

        cur.execute("BEGIN TRANSACTION")
        cur.execute("DELETE FROM notices WHERE user_id=(?) AND datas=(?)"\
                    , (user_id,n_id_data))
        database.commit()

        await update_and_delete.send("便签id为" + key + "的便签已删除喵♪~")

        cur.close()
        database.close()
        await update_and_delete.finish()
    
    elif todo == 1:
        await update_and_delete.send("修改id为" + key + "的便签内容喵♪~\n"+
                                     "我将记录你的下一条消息喵♪~\n"+
                                     "请将修改后的消息发送给我喵♪~")
        n_id = int(key)


    #管理员删除
    elif todo == 3:
        await update_and_delete.send("删除id为" + key + "的便签喵♪~")

        n_id_list = key.split(",")

        database = sqlite3.connect('./qds_bot/plugins/notice/memory_data.db')
        cur = database.cursor()

        cur.execute("SELECT datas, ROW_NUMBER() OVER(ORDER BY time_second ASC) AS n_id \
                    FROM notices ", ( )) 
        n_id_find = cur.fetchall()

        n_id_data = []

        for item in n_id_find:
            if str(item[1]) in n_id_list:
                n_id_data += str(item[0])

                cur.execute("BEGIN TRANSACTION")
                cur.execute("DELETE FROM notices WHERE datas=(?)"\
                            , (n_id_data))
                database.commit()

        await update_and_delete.send("便签id为" + key + "的便签已删除喵♪~")

        cur.close()
        database.close()
        await update_and_delete.finish()

    else:
        await update_and_delete.send("输入的内容不是便签id喵♪~\n"+
                                     "便签功能推出喵♪~")
        await update_and_delete.finish()



#修改
@update_and_delete.got("key4")
async def updatenotice2(key: str = ArgPlainText("key4")):
    global n_id

    database = sqlite3.connect('./qds_bot/plugins/notice/memory_data.db')
    cur = database.cursor()

    cur.execute("SELECT datas, ROW_NUMBER() OVER(ORDER BY time_second ASC) AS n_id \
                    FROM notices WHERE user_id=(?)", (user_id,))
    n_id_find = cur.fetchall()

    n_id_data = ""
    for item in n_id_find:
        if str(item[1]) == str(n_id):   
            n_id_data = str(item[0])

    cur.execute("BEGIN TRANSACTION")
    cur.execute("UPDATE notices SET datas=(?) \
                WHERE user_id=(?) AND datas=(?)", (key, user_id, n_id_data))
    database.commit()

    cur.close()
    database.close()

    await update_and_delete.send("便签内容修改完成喵♪~")
    await update_and_delete.finish() 