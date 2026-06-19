'''
任务管理 session Schemas
'''


from typing import Annotated

from core.security import args_security_check_config
from pydantic import BaseModel, Field, StringConstraints


# /api/v1/tasks/session/robots/sessions POST 接口 schemas
class SessionRobotsSessionsRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    coordinator: bool = Field(False, description='是否为协调器')
    ignore_coordinator_filter: bool = Field(False, description='是否忽略过滤协调器会话')
    title: str = Field(None, description='数字员工会话标题')


# /api/v1/tasks/session/robots/sessions/messages POST 接口 schemas
class SessionRobotsSessionsMessagesRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    session_id: str = Field(..., pattern=args_security_check_config['session_id']['regex'], description='数字员工会话ID')
    page: int = Field(1, description='分页页码')
    size: int = Field(10, description='分页每页数量')
    roles: list[args_security_check_config['hermes_messages_role']] = Field(None, description='数字员工消息角色列表')     # type: ignore[reportUndefinedVariable]
    content: str = Field(None, description='数字员工消息内容')
    coordinator: bool = Field(False, description='是否为协调器')


# /api/v1/tasks/session/robots/sessions/rename POST 接口 schemas
class SessionRenameRobotsSessionsRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    session_id: str = Field(..., pattern=args_security_check_config['session_id']['regex'], description='数字员工会话ID')
    title: str = Field(..., description='数字员工会话标题')


# /api/v1/tasks/session/robots/sessions/create POST 接口 schemas
class SessionCreateRobotsSessionsRequest(BaseModel):
    names: list[Annotated[str, StringConstraints(pattern=args_security_check_config['name']['regex'])]] = Field(..., description='数字员工名称列表')


# /api/v1/tasks/session/robots/sessions/delete POST 接口 schemas
class SessionDeleteRobotsSessionsRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    session_ids: list[Annotated[str, StringConstraints(pattern=args_security_check_config['session_id']['regex'])]] = Field(..., description='数字员工会话ID列表')
