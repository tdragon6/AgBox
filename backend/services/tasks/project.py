'''
任务管理 project 业务逻辑
'''


import shortuuid
import shutil
import traceback
from datetime import datetime

from _utils.file import init_git_repo
from core.config import settings
from core.database import Session
from core.logger import logger
from core.security import args_security_check_config
from fastapi.encoders import jsonable_encoder
from models.project import Project
from services.tasks.hermes import create_hermes_sessions, delete_hermes_sessions, rename_hermes_sessions
from services.tasks.task import delete_tasks_record, get_tasks_items
from sqlalchemy import delete, func, or_, select


def create_projects(
    db: Session,
    name: str,
    description: str,
    robots: list[str]
) -> tuple[bool, str, dict | None]:
    '''
    创建项目
    '''
    # 创建协调器会话
    session_id = create_hermes_sessions(
        names=['agbox-coordinator-async', 'agbox-coordinator-sync'],
        coordinator=True
    )[-1]['session_id']

    # 创建数字员工会话
    create_hermes_sessions(
        names=robots,
        session_id=session_id,
        title=settings.COORDINATOR_MARK + '-' + shortuuid.uuid()
    )
    
    # 创建工作区
    workspace_path = settings.WORKSPACE_DIR / session_id
    workspace_path.mkdir(exist_ok=True)
    
    init_git_repo(
        repo_dir=workspace_path
    )

    project_record = Project(
        id=session_id,
        name=name,
        description=description,
        robots=robots,
        history_robots=robots
    )

    try:
        db.add(project_record)
        db.commit()
        return True, 'success', {'id': session_id}
    except:
        logger.error(traceback.format_exc())
        return False, 'create_project_record_failed', None


def update_projects_record(
    db: Session,
    id: str,
    name: str = None,
    description: str = None,
    robots: list[str] = None,
    history_robots: list[str] = None
) -> tuple[bool, str, dict | None]:
    '''
    更新指定项目
    '''
    project_record = db.get(Project, id)

    if name:
        project_record.name = name
    if description:
        project_record.description = description
    if robots is not None:
        project_record.robots = robots
        new_robots = []
        for robot in robots:
            if robot not in project_record.history_robots:
                new_robots.append(robot)
        
        new_history_robots = project_record.history_robots + new_robots
        project_record.history_robots = new_history_robots
    # 提供一种 history_robots 覆盖更新方式
    if history_robots is not None:
        project_record.history_robots = history_robots
    
    try:
        db.commit()
        db.refresh(project_record)

        if new_robots != []:
            create_hermes_sessions(
                names=new_robots,
                session_id=id,
                title=settings.COORDINATOR_MARK + '-' + shortuuid.uuid()
            )
        
        return True, 'success', {'id': id}
    except:
        logger.error(traceback.format_exc())
        db.rollback()
        return False, 'update_project_record_failed', None


def delete_projects_record(
    db: Session,
    ids: list[str]
) -> tuple[bool, str, dict | None]:
    '''
    删除指定项目记录
    '''
    if not ids:
        return True, 'success', ids
    
    or_conditions = []

    for id in ids:
        or_conditions.append(Project.id == id)
    
    stmt = delete(Project).where(
        or_(*or_conditions)
    )
    
    try:
        db.execute(stmt)
        db.commit()
        return True, 'success', {'ids': ids}
    except:
        logger.error(traceback.format_exc())
        db.rollback()
        return False, 'delete_project_record_failed', None


def delete_projects(
    db: Session,
    ids: list[str]
) -> tuple[bool, str, dict]:
    '''
    删除指定项目
    '''
    # 删除数字员工会话
    for id in ids:
        project_record = db.get(Project, id)
        names = project_record.history_robots
        print(names)
        for name in names:
            delete_hermes_sessions(
                name=name,
                session_ids=[id]
            )
    
    # 删除协调器会话
    for name in ['agbox-coordinator-async', 'agbox-coordinator-sync']:
        delete_hermes_sessions(
            name=name,
            session_ids=[id],
            coordinator=True
        )
    
    # 删除任务记录
    task_ids = []
    for id in ids:
        for item in get_tasks_items(db=db, page=0, project_id=id)[-1]['items']:
            task_ids.append(item['id'])

    delete_tasks_record(
        db=db,
        ids=task_ids
    )
    
    # 删除项目记录
    delete_projects_record(
        db=db,
        ids=ids
    )

    # 删除工作区
    for id in ids:
        shutil.rmtree(settings.WORKSPACE_DIR / id)
    
    return True, 'success', {'ids': ids}


def get_projects_items(
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
    order_by: args_security_check_config['tasks_order_by'] = 'updated_time',     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc'     # type: ignore[reportUndefinedVariable]
) -> tuple[bool, str, dict]:
    '''
    根据查询条件获取项目列表
    '''
    stmt = select(Project)

    if name:
        stmt = stmt.where(Project.name.contains(name))
    if description:
        stmt = stmt.where(Project.description.contains(description))
    if robots:
        for robot in robots:
            stmt = stmt.where(Project.robots.contains(robot))
    if history_robots:
        for robot in history_robots:
            stmt = stmt.where(Project.history_robots.contains(robot))
    if start_created_time:
        stmt = stmt.where(Project.created_time >= start_created_time)
    if end_created_time:
        stmt = stmt.where(Project.created_time <= end_created_time)
    if start_updated_time:
        stmt = stmt.where(Project.updated_time >= start_updated_time)
    if end_updated_time:
        stmt = stmt.where(Project.updated_time <= end_updated_time)
    
    if stmt.whereclause is not None:
        total = db.scalar(
            select(func.count()).where(stmt.whereclause)
        )
    else:
        total = db.scalar(
            select(func.count()).select_from(Project)
        )

    order_column = getattr(Project, order_by, 'updated_time')
    stmt = stmt.order_by(order_column.desc() if order_type == 'desc' else order_column,)

    if page > 0:
        skip = (page - 1) * size
        stmt = stmt.offset(skip).limit(size)

    items = db.execute(stmt).scalars().all()

    result = jsonable_encoder(
        {
            'items': items,
            'total': total,
            'page': page,
            'size': size
        }
    )

    return True, 'success', result

   