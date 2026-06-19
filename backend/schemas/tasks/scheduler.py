'''
任务管理 scheduler Schemas
'''


from datetime import datetime
from typing import Annotated

from core.security import args_security_check_config
from pydantic import BaseModel, Field, StringConstraints


# /api/v1/scheduler/create POST 接口 schemas
class SchedulerCreateRequest(BaseModel):
    minute: str = Field(..., description='分钟')
    hour: str = Field(..., description='小时')
    day: str = Field(..., description='日')
    week: str = Field(..., description='周')
    month: str = Field(..., description='月')
    name: str = Field(..., description='定时任务名称')
    description: str = Field(..., description='定时任务描述')
    robot: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    project_id: str = Field(..., pattern=args_security_check_config['session_id']['regex'], description='项目/会话ID')
    message: str = Field(..., description='任务消息')
    priority: args_security_check_config['priority'] = Field('P3', description='任务优先级')     # type: ignore[reportUndefinedVariable]
    coordinator: bool = Field(False, description='是否为协调器')


# /api/v1/scheduler/update POST 接口 schemas
class SchedulerUpdateRequest(BaseModel):
    minute: str = Field(..., description='分钟')
    hour: str = Field(..., description='小时')
    day: str = Field(..., description='日')
    week: str = Field(..., description='周')
    month: str = Field(..., description='月')
    name: str = Field(..., description='定时任务名称')
    description: str = Field(..., description='定时任务描述')
    robot: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    project_id: str = Field(..., pattern=args_security_check_config['session_id']['regex'], description='项目/会话ID')
    message: str = Field(..., description='任务消息')
    priority: args_security_check_config['priority'] = Field('P3', description='任务优先级')     # type: ignore[reportUndefinedVariable]
    coordinator: bool = Field(False, description='是否为协调器')
    id: str = Field(..., pattern=args_security_check_config['short_uuid']['regex'], description='定时任务ID')
    

# /api/v1/scheduler/items GET 接口 schemas
class SchedulerItemsRequest(BaseModel):
    page: int = Field(1, description='页码')
    size: int = Field(10, description='每页数量')
    name: str = Field(None, description='定时任务名称')
    description: str = Field(None, description='定时任务描述')
    start_created_time: datetime = Field(None, description='起始创建时间')
    end_created_time: datetime = Field(None, description='结束创建时间')
    start_updated_time: datetime = Field(None, description='起始更新时间')
    end_updated_time: datetime = Field(None, description='结束更新时间')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    mount_name: str = Field(None, description='挂载名称')
    message: str = Field(None, description='任务消息')
    priorities: list[args_security_check_config['priority']] = Field(None, description='任务优先级列表')     # type: ignore[reportUndefinedVariable]
    coordinator: bool = Field(None, description='是否为协调器')
    start_next_run_time: datetime = Field(None, description='起始下次运行时间')
    end_next_run_time: datetime = Field(None, description='结束下次运行时间')
    is_paused: bool = Field(None, description='定时任务是否暂停')
    order_by: args_security_check_config['scheduler_order_by'] = Field('updated_time', description='排序字段')     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = Field('desc', description='排序类型')     # type: ignore[reportUndefinedVariable]


# /api/v1/scheduler/pause POST 接口 schemas
class SchedulerPauseRequest(BaseModel):
    ids: list[Annotated[str, StringConstraints(pattern=args_security_check_config['short_uuid']['regex'])]] = Field(..., description='定时任务ID列表')


# /api/v1/scheduler/resume POST 接口 schemas
class SchedulerResumeRequest(BaseModel):
    ids: list[Annotated[str, StringConstraints(pattern=args_security_check_config['short_uuid']['regex'])]] = Field(..., description='定时任务ID列表')


# /api/v1/scheduler/delete POST 接口 schemas
class SchedulerDeleteRequest(BaseModel):
    ids: list[Annotated[str, StringConstraints(pattern=args_security_check_config['short_uuid']['regex'])]] = Field(..., description='定时任务ID列表')