'''
任务管理 project handler
'''


from datetime import datetime

from core.decorator import _handler
from core.scheduler import scheduler
from core.security import args_security_check_config
from fastapi import Request
from services.robots.manage import get_robots_path
from services.tasks.hermes import get_hermes_sessions
from services.tasks.scheduler import (
    create_scheduler_jobs,
    delete_scheduler_jobs,
    get_scheduler_jobs_items,
    pause_scheduler_jobs,
    resume_scheduler_jobs,
    validate_cron_fields,
)
from services.tasks.task import get_tasks_items
from sqlalchemy.orm import Session


@_handler
def handler_scheduler_create_scheduler_jobs(
    request: Request,
    minute: str,
    hour: str,
    day: str,
    week: str,
    month: str,
    name: str,
    description: str,
    robot: str,
    project_id: str,
    message: str,
    priority: args_security_check_config['priority'] = 'P3',     # type: ignore[reportUndefinedVariable]
    coordinator: bool = False,
    id: str = None
) -> tuple[bool, str, list[dict]]:
    '''
    创建定时任务
    '''
    status, msg, _ = validate_cron_fields(
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=week
    )
    if not status:
        return False, msg, None
    
    if coordinator:
        if robot not in ['agbox-coordinator-async', 'agbox-coordinator-sync']:
            return False, 'coordinator_not_found', None
    else:
        status, msg, _ = get_robots_path(robot)
        if not status:
            return False, msg, None
        
    sessions_ids = [
        item['id'] for item in get_hermes_sessions(
            name=robot,
            page=0,
            coordinator=coordinator
        )[-1]
    ]
    if project_id not in sessions_ids:
        return False, 'project_id_not_found', None
    
    result = create_scheduler_jobs(
        minute=minute,
        hour=hour,
        day=day,
        week=week,
        month=month,
        name=name,
        description=description,
        robot=robot,
        project_id=project_id,
        message=message,
        priority=priority,
        coordinator=coordinator,
        id=id
    )

    return result


@_handler
def handler_scheduler_get_scheduler_jobs_items(
    request: Request,
    db: Session,
    page: int = 1,
    size: int = 10,
    name: str = None,
    description: str = None,
    start_created_time: datetime = None,
    end_created_time: datetime = None,
    start_updated_time: datetime = None,
    end_updated_time: datetime = None,
    robot: str = None,
    mount_name: str = None,
    message: str = None,
    priorities: list[args_security_check_config['priority']] = None,     # type: ignore[reportUndefinedVariable]
    coordinator: bool = None,
    start_next_run_time: datetime = None,
    end_next_run_time: datetime = None,
    is_paused: bool = None,
    order_by: args_security_check_config['scheduler_order_by'] = 'updated_time',     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc'     # type: ignore[reportUndefinedVariable]
) -> tuple[bool, str, list[dict]]:
    '''
    获取定时任务列表
    '''
    result = get_scheduler_jobs_items(
        db=db,
        page=page,
        size=size,
        name=name,
        description=description,
        start_created_time=start_created_time,
        end_created_time=end_created_time,
        start_updated_time=start_updated_time,
        end_updated_time=end_updated_time,
        robot=robot,
        mount_name=mount_name,
        message=message,
        priorities=priorities,
        coordinator=coordinator,
        start_next_run_time=start_next_run_time,
        end_next_run_time=end_next_run_time,
        is_paused=is_paused,
        order_by=order_by,
        order_type=order_type
    )
    
    return result


@_handler
def handler_scheduler_pause_scheduler_jobs(
    request: Request,
    ids: list[str]
) -> tuple[bool, str, list[dict]]:
    '''
    暂停定时任务
    '''
    for id in ids:
        job = scheduler.get_job(id)
        if not job:
            return False, 'scheduler_job_not_found', None
    
    result = pause_scheduler_jobs(
        ids=ids
    )
    
    return result


@_handler
def handler_scheduler_resume_scheduler_jobs(
    request: Request,
    ids: list[str]
) -> tuple[bool, str, list[dict]]:
    '''
    恢复定时任务
    '''
    for id in ids:
        job = scheduler.get_job(id)
        if not job:
            return False, 'scheduler_job_not_found', None
    
    result = resume_scheduler_jobs(
        ids=ids
    )
    
    return result


@_handler
def handler_scheduler_delete_scheduler_jobs(
    request: Request,
    db: Session,
    ids: list[str]
) -> tuple[bool, str, list[dict]]:
    '''
    删除定时任务
    '''
    for id in ids:
        job = scheduler.get_job(id)
        if not job:
            return False, 'scheduler_job_not_found', None
        
        project_id = job.kwargs['project_id']
        
        running_pending_tasks = get_tasks_items(
            db=db,
            page=0,
            statuses=['running', 'pending'],
            project_id=project_id
        )[-1]['items']
        
        if not running_pending_tasks:
            pass
        else:
            return False, 'task_is_running_or_pending', None

    result = delete_scheduler_jobs(
        ids=ids
    )
    
    return result