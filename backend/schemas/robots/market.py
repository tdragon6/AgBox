'''
数字员工市场 Schemas
'''


from datetime import datetime

from core.security import args_security_check_config
from pydantic import BaseModel, Field


# /api/v1/robots/market/items POST 接口 schemas
class MarketRobotsItemsRequest(BaseModel):
    page: int = Field(1, description='当前页码')
    size: int = Field(10, description='每页数量')
    name: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    description: str = Field(None, description='数字员工描述')
    author: str = Field(None, description='数字员工作者')
    department: str = Field(None, description='数字员工部门')
    ranks: list[args_security_check_config['rank_scope']] = Field(None, description='数字员工职级列表')     # type: ignore[reportUndefinedVariable]
    qualities: list[args_security_check_config['quality_scope']] = Field(None, description='数字员工品质列表')     # type: ignore[reportUndefinedVariable]
    start_created_time: datetime = Field(None, description='起始创建时间')
    end_created_time: datetime = Field(None, description='结束创建时间')
    start_updated_time: datetime = Field(None, description='起始更新时间')
    end_updated_time: datetime = Field(None, description='结束更新时间')
    order_by: args_security_check_config['robots_order_by'] = Field('updated_time', description='排序字段')     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = Field('desc', description='排序类型')     # type: ignore[reportUndefinedVariable]


# /api/v1/robots/market/install POST 接口 schemas
class MarketRobotsInstallRequest(BaseModel):
    url: str = Field(..., pattern=args_security_check_config['url']['regex'], description='待安装数字员工 url')
    model_config_id: str = Field(..., pattern=args_security_check_config['short_uuid']['regex'], description='数字员工模型配置ID')
