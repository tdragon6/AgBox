'''
技能管理 handler
'''


import re

from _utils.archive import check_archive_valid, extract_archive
from _utils.file import judge_file_size_is_valid
from core.decorator import _handler
from core.security import args_security_check_config
from fastapi import Request, UploadFile
from services.robots.manage import get_robots_path
from services.skills import (
    create_skills_category,
    delete_skills,
    delete_skills_category,
    get_skills_category_items,
    get_skills_items,
    get_skills_path,
    get_skills_root_dir,
    get_skillsmp_items,
    import_skills,
    install_skills_from_skillsmp,
    rename_skills_category,
)


@_handler
def handler_import_skills(
    request: Request,
    uf: UploadFile,
    category: str = None
):
    '''
    导入技能 handler
    '''
    status, msg, _ = judge_file_size_is_valid(uf)
    if not status:
        return False, msg, None
        
    if category is not None and not re.match(args_security_check_config['name']['regex'], category):
        return False, 'skills_category_not_found', None
    
    if category is not None and category not in get_skills_category_items(None)[-1]:
        return False, 'skills_category_not_found', None
    
    status, msg, _ = check_archive_valid(uf)
    if not status:
        return False, msg, None
    
    status, msg, data = extract_archive(uf)
    if not status:
        return False, msg, None
    
    result = import_skills(
        tmp_skills_path=data,
        category=category
    )

    return result


@_handler
def handler_get_skills_category_items(
    request: Request,
    robot: str = None
):
    '''
    获取技能分类 handler
    '''
    if robot is not None:
        status, msg, _ = get_robots_path(robot)
        if not status:
            return False, msg, None
    
    result = get_skills_category_items(robot)

    return result


@_handler
def handler_delete_skills_category(
    request: Request,
    category: str,
    robot: str = None
):
    '''
    删除技能分类 handler
    '''
    if robot is not None:
        status, msg, _ = get_robots_path(robot)
        if not status:
            return False, msg, None
    
    if category not in get_skills_category_items(robot)[-1]:
        return False, 'skills_category_not_found', None
    
    skills_root_dir = get_skills_root_dir(robot)[-1]
    category_dir = skills_root_dir / category

    if any(item.is_dir() for item in category_dir.iterdir()):
        return False, 'skills_category_not_empty', None
    
    result = delete_skills_category(
        category=category,
        robot=robot
    )

    return result


@_handler
def handler_create_skills_category(
    request: Request,
    category: str,
    robot: str = None
):
    '''
    创建技能分类 handler
    '''
    if robot is not None:
        status, msg, _ = get_robots_path(robot)
        if not status:
            return False, msg, None
    
    if category in get_skills_category_items(robot)[-1]:
        return False, 'skills_category_exists', None
    
    result = create_skills_category(
        category=category,
        robot=robot
    )
    
    return result


@_handler
def handler_rename_skills_category(
    request: Request,
    old_category: str,
    new_category: str,
    robot: str = None
):
    '''
    重命名技能分类 handler
    '''
    if robot is not None:
        status, msg, _ = get_robots_path(robot)
        if not status:
            return False, msg, None
    
    if old_category not in get_skills_category_items(robot)[-1]:
        return False, 'skills_category_not_found', None
    
    if new_category in get_skills_category_items(robot)[-1]:
        return False, 'skills_category_exists', None

    result = rename_skills_category(
        old_category=old_category,
        new_category=new_category,
        robot=robot
    )
    return result


@_handler
def handler_get_skills_items(
    request: Request,
    page: int = 1,
    size: int = 10,
    name: str = None,
    description: str = None,
    category: str = None,
    is_script: bool = None,
    order_by: args_security_check_config['skills_order_by'] = 'name',     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc',     # type: ignore[reportUndefinedVariable]
    robot: str = None
):
    '''
    获取技能列表 handler
    '''
    if robot is not None:
        status, msg, _ = get_robots_path(robot)
        if not status:
            return False, msg, None
    
    # if category is not None and category not in get_skills_category_items(robot)[-1]:
    #     return False, 'skills_category_not_found', None

    result = get_skills_items(
        page=page,
        size=size,
        name=name,
        description=description,
        category=category,
        is_script=is_script,
        order_by=order_by,
        order_type=order_type,
        robot=robot
    )

    for ele in result[-1]['items']:
        del ele['path']

    return result


@_handler
def handler_delete_skills(
    request: Request,
    names: list[str],
    robot: str = None
):
    '''
    删除技能 handler
    '''
    if robot is not None:
        status, msg, _ = get_robots_path(robot)
        if not status:
            return False, msg, None
    
    for name in names:
        status, msg, _ = get_skills_path(name, robot)
        if not status:
            return False, msg, None
        
    result = delete_skills(
        names=names,
        robot=robot
    )

    return result


@_handler
def handler_get_skillsmp_items(
    request: Request,
    q: str,
    page: int = 1,
    limit: int = 20,
    sortBy: args_security_check_config['skillsmp_sort_by'] = 'recent',     # type: ignore[reportUndefinedVariable]
    category: str = None,
    occupation: str = None
):
    '''
    获取 skillsmp 技能列表 handler
    '''
    result = get_skillsmp_items(
        q=q,
        page=page,
        limit=limit,
        sortBy=sortBy,
        category=category,
        occupation=occupation
    )
    
    return result


@_handler
def handler_install_skills_from_skillsmp(
    request: Request,
    url: str,
    category: str = None
):
    '''
    从 skillsmp 安装技能 handler
    '''
    if category is not None and category not in get_skills_category_items(None)[-1]:
        return False, 'skills_category_not_found', None
    
    result = install_skills_from_skillsmp(
        url=url,
        category=category
    )
    
    return result