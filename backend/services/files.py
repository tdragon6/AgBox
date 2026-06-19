'''
文件管理 业务逻辑
'''


import shutil

from _utils.archive import zip_dir
from _utils.file import (
    get_directory_tree,
    get_file_content,
    save_file_content,
    get_file_type,
)
from services.skills import get_skills_path
from core.config import settings
from core.security import args_security_check_config
from fastapi import UploadFile
from fastapi.responses import StreamingResponse


def get_dir_tree(
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    获取目录树
    '''
    if scope == 'skills':
        path = get_skills_path(name, robot)[-1]
    elif scope == 'workspaces':
        path = settings.WORKSPACE_DIR / name

    result = get_directory_tree(path)
    
    return result


def read_file(
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    robot: str = None
) -> tuple[bool, str, str | dict | None]:
    '''
    读取文件内容
    '''
    if scope == 'skills':
        path = get_skills_path(name, robot)[-1] / file_path
    elif scope == 'workspaces':
        path = settings.WORKSPACE_DIR / name / file_path

    status, msg, result = get_file_content(path)
    if status and result['file_type'] != 'file':
        result['content'] = file_path
    
    return status, msg, result


def save_file(
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    content: str,
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    保存文件内容
    '''
    if scope == 'skills':
        path = get_skills_path(name, robot)[-1] / file_path
    elif scope == 'workspaces':
        path = settings.WORKSPACE_DIR / name / file_path
    
    save_file_content(path, content)

    result = {'name': name, 'scope': scope, 'file_path': file_path, 'robot': robot}

    return True, 'success', result


def create_file(
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    type: args_security_check_config['file_type'],     # type: ignore[reportUndefinedVariable]
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    创建文件/目录
    '''
    if scope == 'skills':
        path = get_skills_path(name, robot)[-1] / file_path
    elif scope == 'workspaces':
        path = settings.WORKSPACE_DIR / name / file_path

    if type == 'dir':
        path.mkdir(exist_ok=True)
    else:
        path.touch(exist_ok=True)

    result = {'name': name, 'scope': scope, 'file_path': file_path, 'type': type, 'robot': robot}
   
    return True, 'success', result


def delete_file(
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    删除文件/目录
    '''
    if scope == 'skills':
        path = get_skills_path(name, robot)[-1] / file_path
    elif scope == 'workspaces':
        path = settings.WORKSPACE_DIR / name / file_path

    if path.is_file():
        path.unlink()
    
    if path.is_dir():
        shutil.rmtree(path)

    result = {'name': name, 'scope': scope, 'file_path': file_path, 'robot': robot}
   
    return True, 'success', result


def rename_file(
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    rename_file_path: str,
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    重命名文件/目录
    '''
    if scope == 'skills':
        root_path = get_skills_path(name, robot)[-1]
        path = root_path / file_path
    elif scope == 'workspaces':
        root_path = settings.WORKSPACE_DIR / name
        path = root_path / file_path
    
    rename_path = root_path / rename_file_path

    path.replace(rename_path)
    
    result = {'name': name, 'scope': scope, 'file_path': file_path, 'rename_file_path': rename_file_path, 'robot': robot}
   
    return True, 'success', result


def download_dir(
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    robot: str = None
) -> tuple[bool, str, StreamingResponse]:
    '''
    下载目录
    '''
    if scope == 'skills':
        path = get_skills_path(name, robot)[-1]
    elif scope == 'workspaces':
        path = settings.WORKSPACE_DIR / name
    
    zip_buffer = zip_dir(path, None)
    
    result = StreamingResponse(
        zip_buffer,
        media_type='application/zip',
        headers={
            'Content-Disposition': f'attachment; filename={path.name}.zip'
        }
    )

    return True, 'success', result


def download_file(
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    robot: str = None
) -> tuple[bool, str, StreamingResponse]:
    '''
    下载文件
    '''
    if scope == 'skills':
        path = get_skills_path(name, robot)[-1] / file_path
    elif scope == 'workspaces':
        path = settings.WORKSPACE_DIR / name / file_path
    
    mime_type = get_file_type(path)[-1]['mime_type']
    
    result = StreamingResponse(
        open(path, 'rb'),
        media_type=mime_type,
        headers={
            'Content-Disposition': f'attachment; filename={path.name}'
        }
    )

    return True, 'success', result


def upload_file(
    uf: UploadFile,
    name: str,
    scope: args_security_check_config['scope'],     # type: ignore[reportUndefinedVariable]
    file_path: str,
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    上传文件
    '''
    if scope == 'skills':
        path = get_skills_path(name, robot)[-1] / file_path
    elif scope == 'workspaces':
        path = settings.WORKSPACE_DIR / name / file_path
    
    with path.open('wb') as f:
        f.write(uf.file.read())
    
    result = {'name': name, 'scope': scope, 'file_path': file_path, 'robot': robot}
   
    return True, 'success', result