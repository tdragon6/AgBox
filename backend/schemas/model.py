'''
模型管理 Schemas
'''


from typing import Annotated

from core.security import args_security_check_config
from pydantic import BaseModel, Field, StringConstraints


# /api/v1/model/base_url POST 接口 schemas
class ModelProviderBaseUrlRequest(BaseModel):
    id: str = Field(..., description='模型提供商ID')


# /api/v1/model/list POST 接口 schemas
class ModelListRequest(BaseModel):
    api_key: str = Field(None, description='模型提供商 API Key')
    base_url: str = Field(..., pattern=args_security_check_config['url']['regex'], description='模型提供商 Base URL')


# /api/v1/model/create POST 接口 schemas
class ModelCreateRequest(BaseModel):
    name: str = Field(..., description='模型配置名称')
    provider_id: str = Field(..., description='模型提供商ID')
    model: str = Field(..., description='模型名称')
    base_url: str = Field(..., pattern=args_security_check_config['url']['regex'], description='模型提供商 Base URL')
    api_key: str = Field(None, description='模型提供商 API Key')


# /api/v1/model/update POST 接口 schemas
class ModelUpdateRequest(BaseModel):
    id: str = Field(..., pattern=args_security_check_config['short_uuid']['regex'], description='模型配置ID')
    name: str = Field(..., description='模型配置名称')
    provider_id: str = Field(..., description='模型提供商ID')
    model: str = Field(..., description='模型名称')
    base_url: str = Field(..., pattern=args_security_check_config['url']['regex'], description='模型提供商 Base URL')
    api_key: str = Field(None, description='模型提供商 API Key')


# /api/v1/model/items POST 接口 schemas
class ModelItemsRequest(BaseModel):
    keyword: str = Field(None, description='模型配置搜索关键词')
    is_online: bool = Field(None, description='模型配置是否在线')


# /api/v1/model/detail POST 接口 schemas
class ModelDetailRequest(BaseModel):
    id: str = Field(..., pattern=args_security_check_config['short_uuid']['regex'], description='模型配置ID')


# /api/v1/model/delete POST 接口 schemas
class ModelDeleteRequest(BaseModel):
    ids: list[Annotated[str, StringConstraints(pattern=args_security_check_config['short_uuid']['regex'])]] = Field(..., description='模型配置ID列表')
