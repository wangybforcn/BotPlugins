#搜索今日天气
import time
from typing import Annotated, Tuple

from nonebot import on_command, on, get_driver
from nonebot.rule import to_me, keyword, Rule
from nonebot.adapters import Message, Event
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.params import CommandArg, Keyword, EventPlainText, Command
from nonebot.permission import SUPERUSER

from .getweather import get_weather
from .config import Config

_config = Config.parse_obj(get_driver().config)

#插件开关
weather_switch = on_command(("天气", "启用"), rule=to_me(),aliases={("天气", "禁用")}, priority=10, permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
#检测是否为管理员，若是管理员则不触发天气

@weather_switch.handle()
async def control(event: Event, cmd: Tuple[str, str] = Command()):

    weather,action = cmd

    
    if action == "启用":
        _config.is_enabled = True
        await weather_switch.send("getweather插件已启用喵♪~")
        _config.set_run = False
        

    elif action == "禁用":
        _config.is_enabled= False
        await weather_switch.send("getweather插件已禁用喵♪~")

    await weather_switch.finish()


#会话触发规则
async def is_enable() -> bool:
    return _config.is_enabled

async def is_run() -> bool:
    if _config.set_run == False:
        is_run = _config.set_run
        _config.set_run = True
        return is_run
    else:
        return _config.set_run


#会话触发规则/回复规则/程序主体
rule1 = Rule(is_enable, is_run)
rule2 = keyword("天气", "查天气", "查询天气")
rule_all = to_me() & rule2 & rule1

msg_2 = on(rule=rule_all, priority=15)

@msg_2.handle()
async def msg2(msg_all: Annotated[str, EventPlainText()], 
               msg_keyword: Annotated[str, Keyword()]):
    msg_rtn = msg_all.replace(msg_keyword, "", 1)

    if ".禁用" in msg_rtn or ".启用" in msg_rtn:
        await msg_2.send("没有这个权限喵♪~")
        await msg_2.finish()
    
    if city := msg_rtn:
        await msg_2.send(f"正在查找{city}的天气喵♪~")

        weather = get_weather(city)
        time.sleep(0.01)

        if weather["iscity"] == 1:
            await msg_2.send(f"这是{city}现在的天气喵♪~\n"+
                                    "当前温度" + weather['tmpr'] +"° " + weather['all']+
                                    " 湿度" + weather['hum'] + " 降水概率为" + weather['rain']+
                                    "\n希望您做好防护喵♪~")
        else:
            await msg_2.send(f"没有办法查到{city}的天气喵♪~\n"+
                                  f"{city}可能不是地名喵♪~")

    else:
        await msg_2.send("请输出需要查天气的地方喵♪~再来一次吧喵♪~")

    await msg_2.finish()
