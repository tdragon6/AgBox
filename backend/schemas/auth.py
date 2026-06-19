'''
认证 Schemas
'''


from core.security import args_security_check_config
from pydantic import BaseModel, Field


# /api/v1/user/login POST 接口 schemas
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32, pattern=args_security_check_config['name']['regex'], description='用户名')
    password: str = Field(..., min_length=6, max_length=128, description='密码')
