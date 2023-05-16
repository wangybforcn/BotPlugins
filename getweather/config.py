#getweather插件配置文件
from pydantic import BaseModel

class Config(BaseModel):
    is_enabled: bool = True
    set_run: bool = True   #用于防止启用插件后多跑一次