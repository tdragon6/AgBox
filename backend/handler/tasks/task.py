'''
任务管理 task handler
'''

import re
from datetime import datetime

from _utils.file import check_path_is_in_parent, judge_file_size_is_valid, get_bytes_type
from core.decorator import _handler
from core.security import args_security_check_config
from core.config import settings
from fastapi import Request, UploadFile
from models.task import Task
from models.project import Project
from services.robots.manage import get_robots_model_config, get_robots_path
from services.tasks.hermes import get_hermes_sessions
from services.tasks.task import (
    cancel_tasks,
    get_tasks_items,
    get_tasks_results,
    get_tasks_robots_messages_items,
    run_tasks,
    update_tasks_record,
    upload_paste_image,
    get_paste_image,
)
from core.database import Session, db_session


@_handler
def handler_task_get_tasks_results(
    request: Request,
    db: Session,
    id: str
):
    '''
    获取指定任务结果 handler
    '''
    task_record = db.get(Task, id)
    if not task_record:
        return False, 'task_not_found', None

    result = get_tasks_results(
        db=db,
        id=id
    )

    return result


@_handler
def handler_task_cancel_tasks(
    request: Request,
    db: Session,
    ids: list[str]
) -> tuple[bool, str, str | None]:
    '''
    取消指定任务 handler
    '''
    for id in ids:
        task_record = db.get(Task, id)
        if not task_record:
            return False, 'task_not_found', None
        
        if task_record.status not in ['pending', 'running']:
            return False, 'task_is_finished', None

    result = cancel_tasks(
        db=db,
        ids=ids
    )

    return result


@_handler
def handler_task_run_tasks(
    request: Request,
    name: str,
    session_id: str,
    message: str,
    priority: args_security_check_config['priority'] = 'P3',     # type: ignore[reportUndefinedVariable]
    coordinator: bool = False
):
    '''
    执行指定数字员工/协调器，指定会话任务 handler
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
    if not status:
        return False, msg, None
    
    if not data['is_online']:
        return False, 'model_config_error', None
    
    # 若是项目任务，还需判断参与本次任务的数字员工模型配置是否有效
    if coordinator:
        with db_session() as db:
            robots = db.get(Project, session_id).robots
        
        for robot in robots:
            status, msg, data = get_robots_model_config(
                name=robot
            )
            if not status:
                return False, msg, None
            
            if not data['is_online']:
                return False, 'model_config_error', None

    session_ids = [
        item['id'] for item in get_hermes_sessions(
            name=name,
            page=0,
            coordinator=coordinator
        )[-1]
    ]

    if session_id not in session_ids:
        return False, 'project_id_not_found', None

    result = run_tasks(
        name=name,
        session_id=session_id,
        message=message,
        priority=priority,
        coordinator=coordinator
    )
    
    return result


@_handler
def handler_task_get_tasks_robots_messages_items(
    request: Request,
    db: Session,
    id: str,
    name: str,
    page: int = 1,
    size: int = 10,
    roles: list[args_security_check_config['hermes_messages_role']] = None,     # type: ignore[reportUndefinedVariable]
    content: str = None,
    coordinator: bool = False
):
    '''
    获取指定任务，指定数字员工/协调器消息 handler
    '''
    task_record = db.get(Task, id)
    if not task_record:
        return False, 'task_not_found', None
    
    if coordinator:
        if name not in ['agbox-coordinator-async', 'agbox-coordinator-sync']:
            return False, 'coordinator_not_found', None
    else:
        status, msg, _ = get_robots_path(name)
        if not status:
            return False, msg, None

    result = get_tasks_robots_messages_items(
        db=db,
        id=id,
        name=name,
        page=page,
        size=size,
        roles=roles,
        content=content,
        coordinator=coordinator
    )
    
    return result


@_handler
def handler_task_update_tasks_priority(
    request: Request,
    db: Session,
    id: str,
    priority: args_security_check_config['priority']     # type: ignore[reportUndefinedVariable]
):
    '''
    更新指定任务优先级 handler
    '''
    task_record = db.get(Task, id)
    if not task_record:
        return False, 'task_not_found', None
    
    if task_record.status != 'pending':
        return False, 'task_is_not_pending', None
    
    result = update_tasks_record(
        db=db,
        id=id,
        priority=priority
    )
    
    return result


@_handler
def handler_task_get_tasks_items(
    request: Request,
    db: Session,
    page: int = 1,
    size: int = 10,
    message: str = None,
    project_id: str = None,
    types: list[args_security_check_config['task_type']] = None,     # type: ignore[reportUndefinedVariable]
    priorities: list[args_security_check_config['priority']] = None,    # type: ignore[reportUndefinedVariable]
    statuses: list[args_security_check_config['task_status']] = None,     # type: ignore[reportUndefinedVariable],
    robots: list[str] = None,
    triggers: list[args_security_check_config['trigger']] = None,     # type: ignore[reportUndefinedVariable]
    start_created_time: datetime = None,
    end_created_time: datetime = None,
    start_updated_time: datetime = None,
    end_updated_time: datetime = None,
    order_by: args_security_check_config['tasks_order_by'] = 'updated_time',     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc'     # type: ignore[reportUndefinedVariable]
):
    '''
    获取全部或指定会话任务列表 handler
    '''
    result = get_tasks_items(
        db=db,
        page=page,
        size=size,
        message=message,
        project_id=project_id,
        types=types,
        priorities=priorities,
        statuses=statuses,
        robots=robots,
        triggers=triggers,
        start_created_time=start_created_time,
        end_created_time=end_created_time,
        start_updated_time=start_updated_time,
        end_updated_time=end_updated_time,
        order_by=order_by,
        order_type=order_type
    )

    return result


@_handler
def handler_task_upload_paste_image(
    request: Request,
    uf: UploadFile,
    session_id: str
):
    '''
    上传粘贴图片 handler
    '''
    status, msg, _ = judge_file_size_is_valid(uf, is_image=True)
    if not status:
        return False, msg, None
    
    if not re.match(args_security_check_config['session_id']['regex'], session_id):
        return False, "String should match pattern '^\\d{8}_\\d{6}_[0-9a-f]{6}$'", None
    
    uf.file.seek(0)
    status, msg, data = get_bytes_type(uf.file.read(2048))
    uf.file.seek(0)
    if not status:
        return False, msg, None
    
    if data['file_type'] != 'image':
        return False, 'mime_type_not_valid', None
    
    result = upload_paste_image(
        uf=uf,
        session_id=session_id
    )
    
    return result


def handler_task_get_paste_image(
    request: Request,
    session_id: str,
    file_name: str
):
    '''
    获取粘贴图片 handler
    '''
    root_path = settings.WORKSPACE_DIR / session_id
    
    if not root_path.exists():
        return False, 'path_not_found', None
    
    path = root_path / '.pastes' / file_name
    status, msg, _ = check_path_is_in_parent(path, root_path / '.pastes')
    if not status:
        return False, msg, None
    
    if not path.exists():
        return False, 'path_not_found', None
    
    if not path.is_file():
        return False, 'path_not_file', None
    
    result = get_paste_image(
        session_id=session_id,
        file_name=file_name
    )[-1]
    
    return result
