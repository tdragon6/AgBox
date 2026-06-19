'''
任务管理 project Schemas
'''


from datetime import datetime
from typing import Annotated

from core.security import args_security_check_config
from pydantic import BaseModel, Field, StringConstraints


# /api/v1/projects/create POST 接口 schemas
class ProjectCreateRequest(BaseModel):
    name: str = Field(..., description='项目名称')
    description: str = Field(..., description='项目描述')
    robots: list[Annotated[str, StringConstraints(pattern=args_security_check_config['name']['regex'])]] = Field(..., description='数字员工名称列表')


# /api/v1/projects/update POST 接口 schemas
class ProjectUpdateRequest(BaseModel):
    id: str = Field(..., pattern=args_security_check_config['session_id']['regex'], description='项目ID')
    name: str = Field(..., description='项目名称')
    description: str = Field(..., description='项目描述')
    robots: list[Annotated[str, StringConstraints(pattern=args_security_check_config['name']['regex'])]] = Field(..., description='数字员工名称列表')


# /api/v1/projects/delete POST 接口 schemas
class ProjectDeleteRequest(BaseModel):
    ids: list[Annotated[str, StringConstraints(pattern=args_security_check_config['session_id']['regex'])]] = Field(..., description='项目ID列表')


# /api/v1/projects/items POST 接口 schemas
class ProjectItemsRequest(BaseModel):
    page: int = Field(1, description='页码')
    size: int = Field(10, description='每页数量')
    name: str = Field(None, description='项目名称')
    description: str = Field(None, description='项目描述')
    robots: list[Annotated[str, StringConstraints(pattern=args_security_check_config['name']['regex'])]] = Field(None, description='数字员工名称列表')
    history_robots: list[Annotated[str, StringConstraints(pattern=args_security_check_config['name']['regex'])]] = Field(None, description='历史数字员工名称列表')
    start_created_time: datetime = Field(None, description='起始创建时间')
    end_created_time: datetime = Field(None, description='结束创建时间')
    start_updated_time: datetime = Field(None, description='起始更新时间')
    end_updated_time: datetime = Field(None, description='结束更新时间')
    order_by: args_security_check_config['projects_order_by'] = Field('updated_time', description='排序字段')     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = Field('desc', description='排序类型')     # type: ignore[reportUndefinedVariable]