'''
任务管理 project handler
'''


from datetime import datetime

from core.decorator import _handler
from core.security import args_security_check_config
from fastapi import Request
from models.project import Project
from services.robots.manage import get_robots_path
from services.tasks.project import (
    create_projects,
    delete_projects,
    get_projects_items,
    update_projects_record,
)
from services.tasks.scheduler import get_scheduler_jobs_items
from services.tasks.task import get_tasks_items
from sqlalchemy.orm import Session


@_handler
def handler_project_create_projects(
    request: Request,
    db: Session,
    name: str,
    description: str,
    robots: list[str]
) -> tuple[bool, str, list[dict] | None]:
    '''
    创建项目 handler
    '''
    for robot in robots:
        status, msg, _ = get_robots_path(robot)
        if not status:
            return False, msg, None
    
    result = create_projects(
        db=db,
        name=name,
        description=description,
        robots=robots
    )

    return result


@_handler
def handler_project_update_projects(
    request: Request,
    db: Session,
    id: str,
    name: str,
    description: str,
    robots: list[str]
) -> tuple[bool, str, list[dict] | None]:
    '''
    更新项目 handler
    '''
    project_record = db.get(Project, id)
    if not project_record:
        return False, 'project_id_not_found', None
    
    for robot in robots:
        status, msg, _ = get_robots_path(robot)
        if not status:
            return False, msg, None
    
    result = update_projects_record(
        db=db,
        id=id,
        name=name,
        description=description,
        robots=robots
    )

    return result


@_handler
def handler_project_delete_projects(
    request: Request,
    db: Session,
    ids: list[str]
) -> tuple[bool, str, list[dict] | None]:
    '''
    删除项目 handler
    '''
    for id in ids:
        project_record = db.get(Project, id)
        if not project_record:
            return False, 'project_id_not_found', None

        running_pending_tasks = get_tasks_items(
            db=db,
            page=0,
            statuses=['running', 'pending'],
            project_id=id
        )[-1]['items']

        if not running_pending_tasks:
            pass
        else:
            return False, 'task_is_running_or_pending', None
        
        scheduler_jobs = get_scheduler_jobs_items(
            db=db,
            page=0,
            project_id=id
        )[-1]['items']
        
        if not scheduler_jobs:
            pass
        else:
            return False, 'scheduler_job_exist', None

    result = delete_projects(
        db=db,
        ids=ids
    )

    return result


@_handler
def handler_project_get_projects_items(
    request: Request,
    db: Session,
    page: int = 1,
    size: int = 10,
    name: str = None,
    description: str = None,
    robots: list[str] = None,
    history_robots: list[str] = None,
    start_created_time: datetime = None,
    end_created_time: datetime = None,
    start_updated_time: datetime = None,
    end_updated_time: datetime = None,
    order_by: args_security_check_config['projects_order_by'] = 'updated_time',     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc'     # type: ignore[reportUndefinedVariable]
) -> tuple[bool, str, list[dict] | None]:
    '''
    获取项目列表 handler
    '''
    result = get_projects_items(
        db=db,
        page=page,
        size=size,
        name=name,
        description=description,
        robots=robots,
        history_robots=history_robots,
        start_created_time=start_created_time,
        end_created_time=end_created_time,
        start_updated_time=start_updated_time,
        end_updated_time=end_updated_time,
        order_by=order_by,
        order_type=order_type
    )

    return result