'''
系统设置 Schemas
'''


from core.security import args_security_check_config
from pydantic import BaseModel, Field


# /api/v1/settings/get POST 接口 schemas
class SettingsGetRequest(BaseModel):
    name: args_security_check_config['web_env_fields'] = Field(..., description='系统设置名称')     # type: ignore[reportUndefinedVariable]


# /api/v1/settings/set POST 接口 schemas
class SettingsSetRequest(BaseModel):
    name: args_security_check_config['web_env_fields'] = Field(..., description='系统设置名称')     # type: ignore[reportUndefinedVariable]
    value: str | bool | int | None = Field(..., description='系统设置值')
