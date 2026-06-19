'''
文件管理 Schemas
此处技能 name 的校验包括了 session ID 的校验
'''


from core.security import args_security_check_config
from pydantic import BaseModel, Field


# /api/v1/files/tree POST 接口 schemas
class FilesDirTreeRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='目录名称')
    scope: args_security_check_config['scope'] = Field(..., description='目录作用域')     # type: ignore[reportUndefinedVariable]
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/files/read POST 接口 schemas
class FilesFileReadRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='目录名称')
    scope: args_security_check_config['scope'] = Field(..., description='目录作用域')     # type: ignore[reportUndefinedVariable]
    file_path: str = Field(..., description='文件路径')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/files/save POST 接口 schemas
class FilesFileSaveRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='目录名称')
    scope: args_security_check_config['scope'] = Field(..., description='目录作用域')     # type: ignore[reportUndefinedVariable]
    file_path: str = Field(..., description='文件路径')
    content: str = Field(..., description='文件内容')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/files/delete POST 接口 schemas
class FilesFileDeleteRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='目录名称')
    scope: args_security_check_config['scope'] = Field(..., description='目录作用域')     # type: ignore[reportUndefinedVariable]
    file_path: str = Field(..., description='文件路径')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/files/create POST 接口 schemas
class FilesFileCreateRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='目录名称')
    scope: args_security_check_config['scope'] = Field(..., description='目录作用域')     # type: ignore[reportUndefinedVariable]
    file_path: str = Field(..., description='文件路径')
    type: args_security_check_config['file_type'] = Field(..., description='文件/目录对象类型')     # type: ignore[reportUndefinedVariable]
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/files/rename POST 接口 schemas
class FilesFileRenameRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='目录名称')
    scope: args_security_check_config['scope'] = Field(..., description='目录作用域')     # type: ignore[reportUndefinedVariable]
    file_path: str = Field(..., description='文件路径')
    rename_file_path: str = Field(..., description='重命名文件路径')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/files/download GET 接口 schemas
class FilesDirDownloadRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='目录名称')
    scope: args_security_check_config['scope'] = Field(..., description='目录作用域')     # type: ignore[reportUndefinedVariable]
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')


# /api/v1/files/file/download POST 接口 schemas
class FilesFileDownloadRequest(BaseModel):
    name: str = Field(..., pattern=args_security_check_config['name']['regex'], description='目录名称')
    scope: args_security_check_config['scope'] = Field(..., description='目录作用域')     # type: ignore[reportUndefinedVariable]
    file_path: str = Field(..., description='文件路径')
    robot: str = Field(None, pattern=args_security_check_config['name']['regex'], description='数字员工')