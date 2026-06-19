'''
收件箱 Schemas
'''


from datetime import datetime
from typing import Annotated

from core.security import args_security_check_config
from pydantic import BaseModel, Field, StringConstraints


# /api/v1/inbox/items POST 接口 schemas
class InboxItemsRequest(BaseModel):
    page: int = Field(1, description='页码')
    size: int = Field(10, description='每页数量')
    robot: str = Field(None, description='数字员工名称')
    types: list[args_security_check_config['inbox_type']] = Field(None, description='通知类型')     # type: ignore[reportUndefinedVariable]
    message: str = Field(None, description='任务消息')
    statuses: list[args_security_check_config['inbox_status']] = Field(None, description='任务状态')     # type: ignore[reportUndefinedVariable]
    is_read: bool = Field(None, description='是否已读')
    coordinator: bool = Field(None, description='是否为协调器')
    start_created_time: datetime = Field(None, description='起始创建时间')
    end_created_time: datetime = Field(None, description='结束创建时间')
    start_updated_time: datetime = Field(None, description='起始更新时间')
    end_updated_time: datetime = Field(None, description='结束更新时间')
    order_by: args_security_check_config['inbox_order_by'] = Field('updated_time', description='排序字段')     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = Field('desc', description='排序类型')     # type: ignore[reportUndefinedVariable]


# /api/v1/inbox/update/read/status POST 接口 schemas
class InboxUpdateReadStatusRequest(BaseModel):
    ids: list[Annotated[str, StringConstraints(pattern=args_security_check_config['short_uuid']['regex'])]] = Field(..., description='收件箱ID列表')


# /api/v1/inbox/delete POST 接口 schemas
class InboxDeleteRequest(BaseModel):
    ids: list[Annotated[str, StringConstraints(pattern=args_security_check_config['short_uuid']['regex'])]] = Field(..., description='收件箱ID列表')
