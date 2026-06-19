'''
任务管理 session handler
'''


from core.decorator import _handler
from core.security import args_security_check_config
from fastapi import Request
from services.robots.manage import get_robots_items, get_robots_path
from services.tasks.hermes import get_hermes_sessions, rename_hermes_sessions
from services.tasks.session import get_robots_sessions_messages_items, create_robots_sessions, delete_robots_sessions
from services.tasks.task import get_tasks_items
from services.tasks.scheduler import get_scheduler_jobs_items
from sqlalchemy.orm import Session


@_handler
def handler_session_get_robots_items(
    request: Request
):
    '''
    获取数字员工列表 handler
    '''
    result = get_robots_items(
        page=0
    )[-1]

    for item in result['items']:
        for key in list(item.keys()):
            if key not in ['name', 'description', 'rank', 'quality']:
                del item[key]
            
            if key == 'description':
                item[key] = item[key][:20] + '...' if len(item[key]) > 20 else item[key]

    return True, 'success', result


@_handler
def handler_session_get_robots_sessions(
    request: Request,
    name: str,
    coordinator: bool = False,
    ignore_coordinator_filter: bool = False,
    title: str = None
):
    '''
    获取指定数字员工会话 handler
    '''
    if coordinator:
        if name not in ['agbox-coordinator-async', 'agbox-coordinator-sync']:
            return False, 'coordinator_not_found', None
    else:
        status, msg, _ = get_robots_path(name)
        if not status:
            return False, msg, None
    
    result = get_hermes_sessions(
        name=name,
        page=0,
        coordinator=coordinator,
        ignore_coordinator_filter=ignore_coordinator_filter,
        title=title
    )[-1]

    # for item in result:
    #     for key in list(item.keys()):
    #         if key not in ['id', 'title']:
    #             del item[key]

    return True, 'success', result
        

@_handler
def handler_session_get_robots_sessions_messages_items(
    request: Request,
    name: str,
    session_id: str,
    page: int = 1,
    size: int = 10,
    roles: list[args_security_check_config['hermes_messages_role']] = None,     # type: ignore[reportUndefinedVariable]
    content: str = None,
    coordinator: bool = False
):
    '''
    获取指定数字员工，指定会话消息 handler
    '''
    if coordinator:
        if name not in ['agbox-coordinator-async', 'agbox-coordinator-sync']:
            return False, 'coordinator_not_found', None
    else:
        status, msg, _ = get_robots_path(name)
        if not status:
            return False, msg, None

    sessions_ids = [
        item['id'] for item in get_hermes_sessions(
            name=name,
            page=0,
            coordinator=coordinator,
            ignore_coordinator_filter=True
        )[-1]
    ]
    if session_id not in sessions_ids:
        return False, 'project_id_not_found', None
    
    result = get_robots_sessions_messages_items(
        name=name,
        session_id=session_id,
        page=page,
        size=size,
        roles=roles,
        content=content,
        coordinator=coordinator
    )
    
    return result


@_handler
def handler_session_rename_robots_sessions(
    request: Request,
    name: str,
    session_id: str,
    title: str
):
    '''
    重命名指定数字员工，指定会话标题 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None

    session_ids = [ item['id'] for item in get_hermes_sessions(name=name, page=0)[-1] ]
    if session_id not in session_ids:
        return False, 'project_id_not_found', None

    result = rename_hermes_sessions(
        name=name,
        session_id=session_id,
        title=title
    )
    
    return result


@_handler
def handler_session_create_robots_sessions(
    request: Request,
    names: list[str]
):
    '''
    创建指定数字员工会话 handler
    '''
    for name in names:
        status, msg, _ = get_robots_path(name)
        if not status:
            return False, msg, None

    result = create_robots_sessions(
        names=names
    )
    
    return result


@_handler
def handler_session_delete_robots_sessions(
    request: Request,
    db: Session,
    name: str,
    session_ids: list[str]
):
    '''
    删除指定数字员工，指定会话 handler
    '''
    status, msg, _ = get_robots_path(name)
    if not status:
        return False, msg, None

    for session_id in session_ids:
        _session_ids = [ item['id'] for item in get_hermes_sessions(name=name, page=0)[-1] ]
        if session_id not in _session_ids:
            return False, 'project_id_not_found', None
        
        running_pending_tasks = get_tasks_items(
            db=db,
            page=0,
            statuses=['running', 'pending'],
            project_id=session_id
        )[-1]['items']

        if not running_pending_tasks:
            pass
        else:
            return False, 'task_is_running_or_pending', None
        
        scheduler_jobs = get_scheduler_jobs_items(
            db=db,
            page=0,
            project_id=session_id
        )[-1]['items']
        
        if not scheduler_jobs:
            pass
        else:
            return False, 'scheduler_job_exist', None

    result = delete_robots_sessions(
        db=db,
        name=name,
        session_ids=session_ids
    )

    return result