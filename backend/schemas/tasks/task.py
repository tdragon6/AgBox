'''
任务管理 task Schemas
'''


from datetime import datetime
from typing import Annotated

from core.security import args_security_check_config
from pydantic import BaseModel, Field, StringConstraints


# /api/v1/tasks/result POST 接口 schemas
class TaskResultRequest(BaseModel):
    id: str = Field(..., pattern=args_security_check_config['short_uuid']['regex'], description='任务ID')


# /api/v1/tasks/cancel POST 接口 schemas
class TaskCancelTasksRequest(BaseModel):
    ids: list[Annotated[str, StringConstraints(pattern=args_security_check_config['short_uuid']['regex'])]] = Field(..., description='任务ID列表')


# /api/v1/tasks/run POST 接口 schemas
class TaskRunTasksRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    session_id: str = Field(..., pattern=args_security_check_config['session_id']['regex'], description='数字员工会话ID')
    message: str = Field(..., description='任务消息')
    priority: args_security_check_config['priority'] = Field('P3', description='任务优先级')     # type: ignore[reportUndefinedVariable]
    coordinator: bool = Field(False, description='是否为协调器')


# /api/v1/tasks/messages POST 接口 schemas
class TaskMessagesItemsRequest(BaseModel):
    id: str = Field(..., pattern=args_security_check_config['short_uuid']['regex'], description='任务ID')
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    page: int = Field(1, description='页码')
    size: int = Field(10, description='每页数量')
    roles: list[args_security_check_config['hermes_messages_role']] = Field(None, description='数字员工消息角色列表')     # type: ignore[reportUndefinedVariable]
    content: str = Field(None, description='数字员工消息内容')
    coordinator: bool = Field(False, description='是否为协调器')


# /api/v1/tasks/update/priority POST 接口 schemas
class TaskUpdateTasksPriorityRequest(BaseModel):
    id: str = Field(..., pattern=args_security_check_config['short_uuid']['regex'], description='任务ID')
    priority: args_security_check_config['priority'] = Field(..., description='任务优先级')     # type: ignore[reportUndefinedVariable]


# /api/v1/tasks/items POST 接口 schemas
class TaskItemsRequest(BaseModel):
    page: int = Field(1, description='页码')
    size: int = Field(10, description='每页数量')
    message: str = Field(None, description='任务消息')
    project_id: str = Field(None, pattern=args_security_check_config['session_id']['regex'], description='数字员工会话ID/项目ID')
    types: list[args_security_check_config['task_type']] = Field(None, description='任务类型列表')     # type: ignore[reportUndefinedVariable]
    priorities: list[args_security_check_config['priority']] = Field(None, description='任务优先级列表')     # type: ignore[reportUndefinedVariable]
    statuses: list[args_security_check_config['task_status']] = Field(None, description='任务状态列表')     # type: ignore[reportUndefinedVariable]
    robots: list[Annotated[str, StringConstraints(pattern=args_security_check_config['name']['regex'])]] = Field(None, description='数字员工名称列表')
    triggers: list[args_security_check_config['trigger']] = Field(None, description='触发来源列表')     # type: ignore[reportUndefinedVariable]
    start_created_time: datetime = Field(None, description='起始创建时间')
    end_created_time: datetime = Field(None, description='结束创建时间')
    start_updated_time: datetime = Field(None, description='起始更新时间')
    end_updated_time: datetime = Field(None, description='结束更新时间')
    order_by: args_security_check_config['tasks_order_by'] = Field('updated_time', description='排序字段')     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = Field('desc', description='排序类型')     # type: ignore[reportUndefinedVariable]


# /api/v1/tasks/paste/get GET 接口 schemas
class TaskGetPasteImageRequest(BaseModel):
    session_id: str = Field(..., pattern=args_security_check_config['session_id']['regex'], description='数字员工会话ID')
    file_name: str = Field(..., description='粘贴图片文件名')