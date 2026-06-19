'''
数字员工管理 handler
'''


import re
from datetime import datetime

from _utils.archive import check_archive_valid, extract_archive
from _utils.file import judge_file_size_is_valid
from _utils.func import desensitize
from _utils.image import check_avatar_valid
from core.decorator import _handler
from core.security import args_security_check_config
from fastapi import Request, UploadFile
from models.model import Model
from services.robots.manage import (
    clone_from_robots,
    create_robots,
    delete_robots,
    download_robots,
    get_robots_avatar,
    get_robots_config,
    get_robots_env_config,
    get_robots_items,
    get_robots_memory,
    get_robots_model_config,
    get_robots_path,
    get_robots_rule,
    import_robots,
    robots_skills_import,
    save_robots_config,
    save_robots_env_config,
    save_robots_memory,
    save_robots_model_config,
    save_robots_rule,
    update_robots,
    upload_robots_avatar,
)
from services.skills import (
    get_skills_category_items,
    get_skills_path_list,
    get_skills_path
)
from services.tasks.hermes import get_hermes_sessions
from services.tasks.task import get_tasks_items
from services.tasks.scheduler import get_scheduler_jobs_items
from sqlalchemy.orm import Session


@_handler
def handler_manage_get_robots_rule(
    request: Request,
    name: str
):
    '''
    获取数字员工规则 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = get_robots_rule(
        name=name
    )

    return result


@_handler
def handler_manage_save_robots_rule(
    request: Request,
    name: str,
    content: str
):
    '''
    保存数字员工规则 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = save_robots_rule(
        name=name,
        content=content
    )

    return result


@_handler
def handler_manage_get_robots_memory(
    request: Request,
    name: str
):
    '''
    获取数字员工记忆 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = get_robots_memory(
        name=name
    )

    return result


@_handler
def handler_manage_save_robots_memory(
    request: Request,
    name: str,
    content: str
):
    '''
    保存数字员工记忆 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = save_robots_memory(
        name=name,
        content=content
    )

    return result


@_handler
def handler_manage_get_robots_config(
    request: Request,
    name: str
):
    '''
    获取数字员工配置 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = get_robots_config(
        name=name
    )

    return result


@_handler
def handler_manage_save_robots_config(
    request: Request,
    name: str,
    content: str
):
    '''
    保存数字员工配置 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = save_robots_config(
        name=name,
        content=content
    )

    return result


@_handler
def handler_manage_get_robots_env_config(
    request: Request,
    name: str
):
    '''
    获取数字员工环境配置 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = get_robots_env_config(
        name=name
    )

    return result


@_handler
def handler_manage_save_robots_env_config(
    request: Request,
    name: str,
    content: str
):
    '''
    保存数字员工环境配置 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = save_robots_env_config(
        name=name,
        content=content
    )

    return result


@_handler
def handler_manage_robots_skills_import(
    request: Request,
    name: str,
    skills_list: list[str],
    category: str = None
):
    '''
    导入数字员工技能 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None

    if category is not None and not re.match(args_security_check_config['name']['regex'], category):
        return False, 'skills_category_not_found', None
    
    if category is not None and category not in get_skills_category_items(name)[-1]:
        return False, 'skills_category_not_found', None
    
    for skill in skills_list:
        status, msg, _ = get_skills_path(skill, None)
        if not status:
            return False, msg, None
        
        exist_skills_path_list = get_skills_path_list(name)[-1]
        if skill in [ele.name for ele in exist_skills_path_list]:
            return False, 'import_skill_exists', None    
    
    result = robots_skills_import(
        name=name,
        skills_list=skills_list,
        category=category
    )

    return result

@_handler
def handler_manage_get_robots_items(
    request: Request,
    page: int = 1,
    size: int = 10,
    name: str = None,
    description: str = None,
    author: str = None,
    department: str = None,
    ranks: list[args_security_check_config['rank_scope']] = None,     # type: ignore[reportUndefinedVariable]
    qualities: list[args_security_check_config['quality_scope']] = None,     # type: ignore[reportUndefinedVariable]
    start_created_time: datetime = None,
    end_created_time: datetime = None,
    start_updated_time: datetime = None,
    end_updated_time: datetime = None,
    order_by: args_security_check_config['robots_order_by'] = 'updated_time',   # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc'   # type: ignore[reportUndefinedVariable]
):
    '''
    获取数字员工列表 handler
    '''
    result = get_robots_items(
        page=page,
        size=size,
        name=name,
        description=description,
        author=author,
        department=department,
        ranks=ranks,
        qualities=qualities,
        start_created_time=start_created_time,
        end_created_time=end_created_time,
        start_updated_time=start_updated_time,
        end_updated_time=end_updated_time,
        order_by=order_by,
        order_type=order_type
    )

    for ele in result[-1]['items']:
        del ele['path']

    return result


@_handler
def handler_manage_create_robots(
    request: Request,
    db: Session,
    name: str,
    description: str,
    department: str,
    reasoning_effort: args_security_check_config['reasoning_effort'],     # type: ignore[reportUndefinedVariable]
    max_turns: int,
    model_config_id: str
):
    '''
    创建数字员工 handler
    '''
    status, msg, data = get_robots_path(name)
    if status:
        return False, msg, data
    
    model_record = db.get(Model, model_config_id)
    if not model_record:
        return False, 'model_config_not_found', None
    
    result = create_robots(
        db=db,
        name=name,
        description=description,
        department=department,
        reasoning_effort=reasoning_effort,
        max_turns=max_turns,
        model_config_id=model_config_id
    )

    return result


@_handler
def handler_manage_update_robots(
    request: Request,
    db: Session,
    name: str,
    rename: str,
    description: str,
    department: str,
    reasoning_effort: args_security_check_config['reasoning_effort'],     # type: ignore[reportUndefinedVariable]
    max_turns: int,
    model_config_id: str = None
):
    '''
    更新数字员工 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    model_record = db.get(Model, model_config_id)
    if model_config_id is not None and not model_record:
        return False, 'model_config_not_found', None
    
    result = update_robots(
        db=db,
        name=name,
        rename=rename,
        description=description,
        department=department,
        reasoning_effort=reasoning_effort,
        max_turns=max_turns,
        model_config_id=model_config_id
    )

    return result


@_handler
def handler_manage_delete_robots(
    request: Request,
    db: Session,
    names: list[str]
):
    '''
    删除数字员工 handler
    '''
    for name in names:
        status, msg, _ = get_robots_path(name)
        if not status:
            return False, msg, None
        
        running_pending_tasks = get_tasks_items(
            db=db,
            page=0,
            statuses=['running', 'pending'],
            robots=[name]
        )[-1]['items']
        
        if not running_pending_tasks:
            pass
        else:
            return False, 'robots_is_running_or_pending', None
        
        session_ids = [ item['id'] for item in get_hermes_sessions(name=name, page=0)[-1] ]
        for session_id in session_ids:
            scheduler_jobs = get_scheduler_jobs_items(
                db=db,
                page=0,
                project_id=session_id
            )[-1]['items']
            
            if not scheduler_jobs:
                pass
            else:
                return False, 'scheduler_job_exist', None
    
    result = delete_robots(
        db=db,
        names=names
    )

    return result


@_handler
def handler_manage_import_robots(
    request: Request,
    db: Session,
    uf: UploadFile,
    model_config_id: str
):
    '''
    导入数字员工 handler
    '''
    status, msg, _ = judge_file_size_is_valid(uf)
    if not status:
        return False, msg, None

    if not re.match(args_security_check_config['short_uuid']['regex'], model_config_id):
        return False, "String should match pattern '^[2-9a-zA-Z]{22}$'", None

    model_record = db.get(Model, model_config_id)
    if model_config_id is not None and not model_record:
        return False, 'model_config_not_found', None
    
    status, msg, _ = check_archive_valid(uf)
    if not status:
        return False, msg, None
    
    status, msg, data = extract_archive(uf)
    if not status:
        return False, msg, None

    result = import_robots(
        db=db,
        tmp_robots_path=data,
        model_config_id=model_config_id
    )

    return result


@_handler
def handler_manage_clone_from_robots(
    request: Request,
    name: str,
    clone_name: str
):
    '''
    克隆数字员工 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    status, msg, data = get_robots_path(clone_name)
    if status:
        return False, msg, data
    
    result = clone_from_robots(
        name=name,
        clone_name=clone_name
    )

    return result


def handler_manage_download_robots(
    request: Request,
    name: str,
):
    '''
    下载数字员工 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = download_robots(
        name=name
    )[-1]
    
    return result


@_handler
def handler_manage_get_robots_model_config(
    request: Request,
    name: str,
    coordinator: bool = False
):
    '''
    获取数字员工/协调器模型配置 handler
    '''
    if coordinator:
        if name not in ['agbox-coordinator-async', 'agbox-coordinator-sync']:
            return False, 'coordinator_not_found', None
    else:
        status, msg, _ = get_robots_path(name)
        if not status:
            return False, msg, None
    
    status, msg, data = get_robots_model_config(
        name=name,
        coordinator=coordinator
    )

    if status:
        data['api_key'] = desensitize(data['api_key'])
        return status, msg, data
    else:
        return True, 'success', {}


@_handler
def handler_manage_save_robots_model_config(
    request: Request,
    db: Session,
    name: str,
    model_config_id: str,
    coordinator: bool = False
):
    '''
    保存数字员工/协调器模型配置 handler
    '''
    if coordinator:
        if name not in ['agbox-coordinator-async', 'agbox-coordinator-sync']:
            return False, 'coordinator_not_found', None
    else:
        status, msg, _ = get_robots_path(name)
        if not status:
            return False, msg, None
        
    model_record = db.get(Model, model_config_id)
    if not model_record:
        return False, 'model_config_not_found', None
    
    result = save_robots_model_config(
        db=db,
        name=name,
        model_config_id=model_config_id,
        coordinator=coordinator
    )
    
    return result


@_handler
def handler_manage_upload_robots_avatar(
    request: Request,
    uf: UploadFile,
    name: str
):
    '''
    上传数字员工头像 handler
    '''
    status, msg, _ = judge_file_size_is_valid(uf, is_image=True)
    if not status:
        return False, msg, None
    
    if not re.match(args_security_check_config['name']['regex'], name):
        return False, "String should match pattern '^[a-zA-Z0-9_]+$'", None
    
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    status, msg, _ = check_avatar_valid(uf)
    if not status:
        return False, msg, None
    
    result = upload_robots_avatar(
        uf=uf,
        name=name
    )
    
    return result


def handler_manage_get_robots_avatar(
    request: Request,
    name: str
):
    '''
    获取数字员工头像 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None
    
    result = get_robots_avatar(
        name=name
    )[-1]

    return result