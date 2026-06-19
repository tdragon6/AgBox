'''
任务管理 scheduler service
'''


import traceback
import re
from datetime import datetime

import shortuuid
from core.logger import logger
from core.scheduler import scheduler
from core.security import args_security_check_config
from models.project import Project
from services.tasks.hermes import get_hermes_sessions
from services.tasks.task import run_tasks
from sqlalchemy.orm import Session


def create_scheduler_jobs(
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
    priority: args_security_check_config['priority'],     # type: ignore[reportUndefinedVariable]
    coordinator: bool = False,
    id: str = None
) -> tuple[bool, str, dict]:
    '''
    创建定时任务
    '''
    now_time = datetime.now()

    kwargs = {
        'metadata': {
            'name': name,
            'description': description,
            'created_time': now_time if not id else scheduler.get_job(id).kwargs['metadata']['created_time'],
            'updated_time': now_time,
            'minute': minute,
            'hour': hour,
            'day': day,
            'week': week,
            'month': month,
        },
        'name': robot,
        'project_id': project_id,
        'message': message,
        'priority': priority,
        'coordinator': coordinator
    }

    if not id:
        id = shortuuid.uuid()
    
    scheduler.add_job(
        id=id,
        func=run_scheduler_jobs,
        kwargs=kwargs,
        trigger='cron',
        minute=minute,
        hour=hour,
        day=day,
        day_of_week=week,
        month=month,
        replace_existing=True
    )

    return True, 'success', {'id': id}


def get_scheduler_jobs_items(
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
    project_id: str = None,
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
    scheduler_jobs_list = []

    jobs = scheduler.get_jobs()

    for job in jobs:
        job_id = job.id

        job_metadata = job.kwargs['metadata']
        job_name = job_metadata['name']
        if name is not None and name.lower() not in job_name.lower():
            continue
        
        job_description = job_metadata['description']
        if description is not None and description.lower() not in job_description.lower():
            continue
        
        job_created_time = job_metadata['created_time']
        if start_created_time is not None and job_created_time < start_created_time:
            continue
        if end_created_time is not None and job_created_time > end_created_time:
            continue
        
        job_updated_time = job_metadata['updated_time']
        if start_updated_time is not None and job_updated_time < start_updated_time:
            continue
        if end_updated_time is not None and job_updated_time > end_updated_time:
            continue
        
        job_robot = job.kwargs['name']
        if robot is not None and robot.lower() not in job_robot.lower():
            continue
        
        job_project_id = job.kwargs['project_id']
        if project_id is not None and project_id != job_project_id:
            continue
        
        job_coordinator = job.kwargs['coordinator']
        
        if job_coordinator:
            project_name = db.get(Project, job_project_id).name
            if mount_name is not None and mount_name.lower() not in project_name.lower():
                continue
        else:
            is_continue = False
            for item in get_hermes_sessions(
                name=job_robot,
                page=0
            )[-1]:
                if job_project_id == item['id']:
                    session_title = item['title']
                    if mount_name is not None and mount_name.lower() not in session_title.lower():
                        is_continue = True
                    break
            if is_continue:
                continue

        job_message = job.kwargs['message']
        if message is not None and message.lower() not in job_message.lower():
            continue
        
        job_priority = job.kwargs['priority']
        if priorities is not None and job_priority not in priorities:
            continue

        if coordinator is not None and coordinator != job_coordinator:
            continue
        
        job_next_run_time = job.next_run_time.replace(tzinfo=None) if job.next_run_time is not None else None
        if start_next_run_time is not None and (job_next_run_time is None or job_next_run_time < start_next_run_time):
            continue
        if end_next_run_time is not None and (job_next_run_time is None or job_next_run_time > end_next_run_time):
            continue
        
        job_is_paused = job.next_run_time is None
        if is_paused is not None and job_is_paused != is_paused:
            continue
        
        item = {
            'id': job_id,
            'name': job_name,
            'description': job_description,
            'created_time': job_created_time,
            'updated_time': job_updated_time,
            'robot': job_robot,
            'mount_name': project_name if job_coordinator else session_title,
            'project_id': job_project_id,
            'message': job_message,
            'priority': job_priority,
            'coordinator': job_coordinator,
            'next_run_time': job_next_run_time,
            'is_paused': job_is_paused,
            'minute': job_metadata['minute'],
            'hour': job_metadata['hour'],
            'day': job_metadata['day'],
            'week': job_metadata['week'],
            'month': job_metadata['month'],
        }

        for ele in job.trigger.fields:
            item[ele.name] = str(ele)
        
        scheduler_jobs_list.append(item)
    
    total = len(scheduler_jobs_list)

    scheduler_jobs_list = sorted(scheduler_jobs_list, key=lambda x: x[order_by], reverse=order_type == 'desc')
    
    if page > 0:
        skip = (page - 1) * size
    else:
        skip = None

    scheduler_jobs_list = scheduler_jobs_list[skip:skip + size] if skip is not None else scheduler_jobs_list
    
    result = {
        'items': scheduler_jobs_list,
        'total': total,
        'page': page,
        'size': size
    }

    return True, 'success', result


def pause_scheduler_jobs(
    ids: list[str]
) -> tuple[bool, str, dict]:
    '''
    暂停定时任务
    '''
    for id in ids:
        scheduler.pause_job(id)
    
    return True, 'success', {'ids': ids}


def resume_scheduler_jobs(
    ids: list[str]
) -> tuple[bool, str, dict]:
    '''
    恢复定时任务
    '''
    for id in ids:
        scheduler.resume_job(id)
    
    return True, 'success', {'ids': ids}


def delete_scheduler_jobs(
    ids: list[str]
) -> tuple[bool, str, dict]:
    '''
    删除定时任务
    '''
    for id in ids:
        scheduler.remove_job(id)
    
    return True, 'success', {'ids': ids}


def run_scheduler_jobs(
    metadata: dict,
    name: str,
    project_id: str,
    message: str,
    priority: args_security_check_config['priority'] = 'P3',     # type: ignore[reportUndefinedVariable]
    coordinator: bool = False
) -> tuple[bool, str, dict | None]:
    '''
    运行定时任务
    '''
    scheduler_message_suffix = "\nNote: This is user input for a scheduled task. Please accurately determine whether this task needs to be associated with the context of historical tasks based on the user's input. It can be processed independently without referring to historical messages, or it can be processed in conjunction with historical messages as needed."

    status, msg, data = run_tasks(
        name=name,
        session_id=project_id,
        message=message + scheduler_message_suffix,
        priority=priority,
        coordinator=coordinator,
        trigger='scheduler'
    )

    log_msg = f'run scheduler job success.\nmetadata: {metadata}\nname: {name}\nproject_id: {project_id}\nmessage: {message}\npriority: {priority}\ncoordinator: {coordinator}\nmsg: {msg}\ndata: {data}'
    
    if status:
        logger.info(log_msg)
    else:
        logger.error(log_msg)


def validate_single_cron_field(
    field: str,
    value: str
) -> tuple[bool, str, None]:
    '''
    校验 cron 参数
    '''
    if len(value.strip()) == 0:
        return False, 'cron_field_invalid', None
    
    CRON_FIELD_RANGES = {
        'minute': [0, 59],
        'hour': [0, 23],
        'day': [1, 31],
        'month': [1, 12],
        'day_of_week': [0, 6]
    }

    min_val, max_val = CRON_FIELD_RANGES[field]

    CRON_FIELD_REGEX = re.compile(r'^(\*|\d+|\d+-\d+|\d+(?:,\d+)+|\*/\d+)$')
    
    if not CRON_FIELD_REGEX.match(value):
        return False, 'cron_field_invalid', None

    try:
        if value == '*':
            return True, 'success', None

        elif value.startswith('*/'):
            step = int(value.split('/')[1])
            if step <= 0:
                return False, 'cron_field_invalid', None
            
            return True, 'success', None

        elif '-' in value:
            start, end = map(int, value.split('-'))
            if start > end:
                return False, 'cron_field_invalid', None
            if not ( min_val <= start <= max_val ) or not ( min_val <= end <= max_val ):
                return False, 'cron_field_invalid', None
            
            return True, 'success', None

        elif ',' in value:
            nums = list(map(int, value.split(',')))
            for num in nums:
                if not ( min_val <= num <= max_val ):
                    return False, 'cron_field_invalid', None
            return True, 'success', None
        
        else:
            num = int(value)
            if not ( min_val <= num <= max_val ):
                return False, 'cron_field_invalid', None
            
            return True, 'success', None

    except:
        logger.error(traceback.format_exc())
        return False, 'cron_field_invalid', None


def validate_cron_fields(
    minute: str,
    hour: str,
    day: str,
    month: str,
    day_of_week: str
) -> tuple[bool, str, None]:
    '''
    校验所有 cron 参数
    '''
    fields = {
        'minute': minute,
        'hour': hour,
        'day': day,
        'month': month,
        'day_of_week': day_of_week
    }

    for key, value in fields.items():
        status, msg, _ = validate_single_cron_field(key, value)
        if not status:
            return False, msg, None
    
    return True, 'success', None