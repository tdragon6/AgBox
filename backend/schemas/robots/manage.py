'''
数字员工管理 Schemas
'''


from datetime import datetime
from typing import Annotated

from core.security import args_security_check_config
from pydantic import BaseModel, Field, StringConstraints


# /api/v1/robots/manage/rule/read POST 接口 schemas
class ManageRobotsRuleReadRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')


# /api/v1/robots/manage/rule/save POST 接口 schemas
class ManageRobotsRuleSaveRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    content: str = Field(..., description='数字员工规则')


# /api/v1/robots/manage/memory/read POST 接口 schemas
class ManageRobotsMemoryReadRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')


# /api/v1/robots/manage/memory/save POST 接口 schemas
class ManageRobotsMemorySaveRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    content: str = Field(..., description='数字员工记忆')


# /api/v1/robots/manage/config/read POST 接口 schemas
class ManageRobotsConfigReadRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')


# /api/v1/robots/manage/config/save POST 接口 schemas
class ManageRobotsConfigSaveRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    content: str = Field(..., description='数字员工配置')


# /api/v1/robots/manage/env/read POST 接口 schemas
class ManageRobotsEnvReadRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')


# /api/v1/robots/manage/env/save POST 接口 schemas
class ManageRobotsEnvSaveRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    content: str = Field(..., description='数字员工环境变量')


# /api/v1/robots/manage/skills/import POST 接口 schemas
class ManageRobotsSkillsImportRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    skills_list: list[Annotated[str, StringConstraints(pattern=args_security_check_config['name']['regex'])]] = Field(..., description='数字员工技能列表')
    category: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工技能分类')


# /api/v1/robots/manage/items POST 接口 schemas
class ManageRobotsItemsRequest(BaseModel):
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

    
# /api/v1/robots/manage/create POST 接口 schemas
class ManageRobotsCreateRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    description: str = Field(..., description='数字员工描述')
    department: str = Field(..., description='数字员工部门')
    reasoning_effort: args_security_check_config['reasoning_effort'] = Field(..., description='数字员工推理努力')     # type: ignore[reportUndefinedVariable]
    max_turns: int = Field(..., description='每轮对话的最大迭代次数')
    model_config_id: str = Field(..., pattern=args_security_check_config['short_uuid']['regex'], description='数字员工模型配置ID')


# /api/v1/robots/manage/update POST 接口 schemas
class ManageRobotsUpdateRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    rename: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工新名称')
    description: str = Field(..., description='数字员工描述')
    department: str = Field(..., description='数字员工部门')
    reasoning_effort: args_security_check_config['reasoning_effort'] = Field(..., description='数字员工推理努力')     # type: ignore[reportUndefinedVariable]
    max_turns: int = Field(..., description='每轮对话的最大迭代次数')
    model_config_id: str = Field(None, pattern=args_security_check_config['short_uuid']['regex'], description='数字员工模型配置ID')


# /api/v1/robots/manage/delete POST 接口 schemas
class ManageRobotsDeleteRequest(BaseModel):
    names: list[Annotated[str, StringConstraints(pattern=args_security_check_config['name']['regex'])]] = Field(..., description='数字员工名称列表')


# /api/v1/robots/manage/clone POST 接口 schemas
class ManageRobotsCloneRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    clone_name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工克隆名称')


# /api/v1/robots/download GET 接口 schemas
class ManageRobotsDownloadRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')


# /api/v1/robots/manage/model/config POST 接口 schemas
class ManageRobotsModelConfigRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    coordinator: bool = Field(False, description='是否为协调器')


# /api/v1/robots/manage/model/config/save POST 接口 schemas
class ManageRobotsModelConfigSaveRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')
    model_config_id: str = Field(..., pattern=args_security_check_config['short_uuid']['regex'], description='数字员工模型配置ID')
    coordinator: bool = Field(False, description='是否为协调器')


# /api/v1/robots/manage/avatar GET 接口 schemas
class ManageRobotsAvatarRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='数字员工名称')