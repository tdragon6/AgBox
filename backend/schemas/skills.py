'''
技能管理 Schemas
'''


from typing import Annotated

from core.security import args_security_check_config
from pydantic import BaseModel, Field, StringConstraints


# /api/v1/skills/category/items POST 接口 schemas
class SkillsCategoryItemsRequest(BaseModel):
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/skills/category/delete POST 接口 schemas
class SkillsCategoryDeleteRequest(BaseModel):
    category: str = Field(..., pattern=args_security_check_config['name']['regex'], description='技能分类')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/skills/category/create POST 接口 schemas
class SkillsCategoryCreateRequest(BaseModel):
    category: str = Field(..., pattern=args_security_check_config['name']['regex'], description='技能分类')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/skills/category/rename POST 接口 schemas
class SkillsCategoryRenameRequest(BaseModel):
    old_category: str = Field(..., pattern=args_security_check_config['name']['regex'], description='旧技能分类')
    new_category: str = Field(..., pattern=args_security_check_config['name']['regex'], description='新技能分类')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/skills/items POST 接口 schemas
class SkillsItemsRequest(BaseModel):
    page: int = Field(1, description='页码')
    size: int = Field(10, description='每页数量')
    name: str = Field(None, pattern=args_security_check_config['name']['regex'], description='技能名称')
    description: str = Field(None, description='技能描述')
    category: str = Field(None, pattern=args_security_check_config['name']['regex'], description='技能分类')
    is_script: bool = Field(None, description='是否为脚本')
    order_by: args_security_check_config['skills_order_by'] = Field('name', description='排序字段')     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = Field('desc', description='排序类型')     # type: ignore[reportUndefinedVariable]
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/skills/delete POST 接口 schemas
class SkillsDeleteRequest(BaseModel):
    names: list[Annotated[str, StringConstraints(pattern=args_security_check_config['name']['regex'])]] = Field(..., description='技能名称列表')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/skillsmp/items POST 接口 schemas
class SkillsmpItemsRequest(BaseModel):
    q: str = Field(..., description='查询关键词')
    page: int = Field(1, description='页码')
    limit: int = Field(20, le=args_security_check_config['skillsmp_max_limit'], description='每页数量')
    sortBy: Annotated[str, args_security_check_config['skillsmp_sort_by']] = Field('recent', description='排序字段')
    category: str = Field(None, pattern=args_security_check_config['name']['regex'], description='技能分类')
    occupation: str = Field(None, pattern=args_security_check_config['name']['regex'], description='职业分类')


# /api/v1/skillsmp/install POST 接口 schemas
class SkillsmpInstallRequest(BaseModel):
    url: str = Field(..., pattern=args_security_check_config['url']['regex'], description='待安装技能 url')
    category: str = Field(None, pattern=args_security_check_config['name']['regex'], description='技能分类')
