'''
文件管理 handler
'''


import re
import shortuuid
import shutil

from _utils.file import check_path_is_in_parent, judge_file_size_is_valid, save_file_content
from core.config import settings
from core.decorator import _handler
from core.security import args_security_check_config
from fastapi import Request
from services.robots.manage import get_robots_path
from services.files import (
    get_dir_tree,
    read_file,
    save_file,
    create_file,
    delete_file,
    rename_file,
    download_dir,
    download_file,
    upload_file,
)
from services.skills import get_skills_path, get_skills_info
from fastapi import UploadFile


@_handler
def handler_files_get_dir_tree(
    request: Request,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    robot: str = None
):
    '''
    获取目录树 handler
    '''
    if scope == 'skills':
        if robot is not None:
            status, msg, _ = get_robots_path(robot)
            if not status:
                return False, msg, None
    
        status, msg, _ = get_skills_path(name, robot)
        if not status:
            return False, msg, None
    
    if scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
    
        if not root_path.exists():
            return False, 'path_not_found', None
    
    result = get_dir_tree(
        name=name,
        scope=scope,
        robot=robot
    )

    return result


@_handler
def handler_files_read_file(
    request: Request,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    robot: str = None
):
    '''
    读取文件内容 handler
    '''
    if scope == 'skills':
        if robot is not None:
            status, msg, _ = get_robots_path(robot)
            if not status:
                return False, msg, None
    
        if scope == 'skills':
            status, msg, root_path = get_skills_path(name, robot)
            if not status:
                return False, msg, None
    
    if scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
    
        if not root_path.exists():
            return False, 'path_not_found', None
        
    path = root_path / file_path
    status, msg, _ = check_path_is_in_parent(path, root_path)
    if not status:
        return False, msg, None

    if not path.exists():
        return False, 'path_not_found', None
    
    if not path.is_file():
        return False, 'path_not_file', None
    
    result = read_file(
        name=name,
        scope=scope,
        file_path=file_path,
        robot=robot
    )

    return result


@_handler
def handler_files_save_file(
    request: Request,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    content: str,
    robot: str = None
):
    '''
    保存文件内容 handler
    '''
    if scope == 'skills':
        if robot is not None:
            status, msg, _ = get_robots_path(robot)
            if not status:
                return False, msg, None
    
        status, msg, root_path = get_skills_path(name, robot)
        if not status:
            return False, msg, None
        
        if file_path == 'SKILL.md':
            temp_check_path = settings.TEMP_DIR / shortuuid.uuid()
            temp_check_path.mkdir(exist_ok=True)
            save_file_content(
                path=temp_check_path / file_path,
                content=content
            )
            status, msg, data = get_skills_info(temp_check_path)
            shutil.rmtree(temp_check_path)
            if not status:
                return False, msg, None
            
            if data['name'] != name:
                return False, 'skill_name_cannot_be_changed', None
    
    if scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
    
        if not root_path.exists():
            return False, 'path_not_found', None
        
    path = root_path / file_path
    status, msg, _ = check_path_is_in_parent(path, root_path)
    if not status:
        return False, msg, None
    
    if not path.exists():
        return False, 'path_not_found', None
    
    if not path.is_file():
        return False, 'path_not_file', None
    
    result = save_file(
        name=name,
        scope=scope,
        file_path=file_path,
        content=content,
        robot=robot
    )
    
    return result


@_handler
def handler_files_delete_file(
    request: Request,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    robot: str = None
):
    '''
    删除文件/目录 handler
    '''
    if scope == 'skills':
        if file_path == 'SKILL.md':
            return False, 'path_invalid', None
        
        if robot is not None:
            status, msg, _ = get_robots_path(robot)
            if not status:
                return False, msg, None
    
        status, msg, root_path = get_skills_path(name, robot)
        if not status:
            return False, msg, None
    
    if scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
    
        if not root_path.exists():
            return False, 'path_not_found', None
    
    path = root_path / file_path
    status, msg, _ = check_path_is_in_parent(path, root_path)
    if not status:
        return False, msg, None
    
    if not path.exists():
        return False, 'path_not_found', None
    
    result = delete_file(
        name=name,
        scope=scope,
        file_path=file_path,
        robot=robot
    )
    
    return result


@_handler
def handler_files_create_file(
    request: Request,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    type: args_security_check_config['file_type'],     # type: ignore[reportUndefinedVariable]
    robot: str = None
):
    '''
    创建文件/目录 handler
    '''
    if scope == 'skills':
        if file_path == 'SKILL.md':
            return False, 'path_invalid', None
        
        if robot is not None:
            status, msg, _ = get_robots_path(robot)
            if not status:
                return False, msg, None

        status, msg, root_path = get_skills_path(name, robot)
        if not status:
            return False, msg, None
    
    if scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
    
        if not root_path.exists():
            return False, 'path_not_found', None
    
    path = root_path / file_path
    status, msg, _ = check_path_is_in_parent(path, root_path)
    if not status:
        return False, msg, None
    
    if path.exists():
        return False, 'path_exists', None
    
    result = create_file(
        name=name,
        scope=scope,
        file_path=file_path,
        type=type,
        robot=robot
    )

    return result


@_handler
def handler_files_rename_file(
    request: Request,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    rename_file_path: str,
    robot: str = None
):
    '''
    重命名文件/目录 handler
    '''
    if scope == 'skills':
        if file_path == 'SKILL.md':
            return False, 'path_invalid', None

        if robot is not None:
            status, msg, _ = get_robots_path(robot)
            if not status:
                return False, msg, None
    
        status, msg, root_path = get_skills_path(name, robot)
        if not status:
            return False, msg, None
    
    if scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
    
        if not root_path.exists():
            return False, 'path_not_found', None
    
    path = root_path / file_path
    status, msg, _ = check_path_is_in_parent(path, root_path)
    if not status:
        return False, msg, None
    
    if not path.exists():
        return False, 'path_not_found', None
    
    rename_path = root_path / rename_file_path

    status, msg, _ = check_path_is_in_parent(rename_path, root_path)
    if not status:
        return False, msg, None
    
    if rename_path.exists():
        return False, 'path_exists', None
    
    result = rename_file(
        name=name,
        scope=scope,
        file_path=file_path,
        rename_file_path=rename_file_path,
        robot=robot
    )
    
    return result


def handler_files_download_dir(
    request: Request,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    robot: str = None
):
    '''
    下载目录 handler
    '''
    if scope == 'skills':
        if robot is not None:
            status, msg, _ = get_robots_path(robot)
            if not status:
                return False, msg, None
        
        status, msg, root_path = get_skills_path(name, robot)
        if not status:
            return False, msg, None
    
    if scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
    
        if not root_path.exists():
            return False, 'path_not_found', None
    
    result = download_dir(
        name=name,
        scope=scope,
        robot=robot
    )[-1]
    
    return result


def handler_files_download_file(
    request: Request,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    robot: str = None
):
    '''
    下载文件 handler
    '''
    if scope == 'skills':
        if robot is not None:
            status, msg, _ = get_robots_path(robot)
            if not status:
                return False, msg, None
        
        status, msg, root_path = get_skills_path(name, robot)
        if not status:
            return False, msg, None
    
    if scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
    
        if not root_path.exists():
            return False, 'path_not_found', None
    
    path = root_path / file_path
    status, msg, _ = check_path_is_in_parent(path, root_path)
    if not status:
        return False, msg, None
    
    if not path.exists():
        return False, 'path_not_found', None
    
    if not path.is_file():
        return False, 'path_not_file', None
    
    result = download_file(
        name=name,
        scope=scope,
        file_path=file_path,
        robot=robot
    )[-1]
    
    return result


@_handler
def handler_files_upload_file(
    request: Request,
    uf: UploadFile,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    robot: str = None
):
    '''
    上传文件 handler
    '''
    status, msg, _ = judge_file_size_is_valid(uf)
    if not status:
        return False, msg, None
    
    if not re.match(args_security_check_config['name']['regex'], name):
        return False, "String should match pattern '^[a-zA-Z0-9_]+$'", None
    
    if scope not in ['skills', 'workspaces']:
        return False, 'scope_invalid', None
    
    if scope == 'skills':
        if file_path == 'SKILL.md':
            return False, 'path_invalid', None
        
        if robot is not None:
            if not re.match(args_security_check_config['name']['regex'], robot):
                return False, "String should match pattern '^[a-zA-Z0-9_]+$'", None
            
            status, msg, _ = get_robots_path(robot)
            if not status:
                return False, msg, None
        
        status, msg, root_path = get_skills_path(name, robot)
        if not status:
            return False, msg, None
    
    if scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
    
        if not root_path.exists():
            return False, 'path_not_found', None
    
    path = root_path / file_path
    status, msg, _ = check_path_is_in_parent(path, root_path)
    if not status:
        return False, msg, None
    
    if path.exists():
        return False, 'path_exists', None
    
    result = upload_file(
        uf=uf,
        name=name,
        scope=scope,
        file_path=file_path,
        robot=robot
    )
    
    return result