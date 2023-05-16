import time
from typing import Annotated
import sqlite3

from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.adapters import Message, Event,Bot
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import CommandArg, Keyword, EventPlainText, Fullmatch
from nonebot.permission import SUPERUSER



msg = on_keyword(("test", "测试"), rule=to_me())

@msg.handle()
async def msg_speak(bot: Bot, event: Event):
    await msg.send("Running test ---")

    user_id = event.get_user_id()
    bot_id = bot.self_id
    await msg.send("Testing user_id: " + str(user_id) + "\n"
                   "Testing bot_id: " + str(bot_id))  
    
    await msg.send("Testing database surch")

    database = sqlite3.connect('./qds_bot/plugins/notice/memory_data.db')
    cur = database.cursor()
    cur.execute("SELECT datas, ROW_NUMBER() OVER(ORDER BY time ASC) AS n_id \
                    FROM notices WHERE user_id=(?)", (event.get_user_id(),)) 
    n_id_find = cur.fetchall()
    print("搜索结果：")
    print(n_id_find)
    print(type(n_id_find[1]))

    n_id_data = ""
    for item in n_id_find:
        if str(item[1]) == "1":
            n_id_data = str(item[0])
            print("文本内容")
            print(str(n_id_data))

    cur.execute("BEGIN TRANSACTION")
    cur.execute("DELETE FROM notices WHERE user_id=(?) AND datas=(?)", (event.get_user_id(),n_id_data))
    database.commit()


    cur.close()
    database.close()

    await msg.finish()
