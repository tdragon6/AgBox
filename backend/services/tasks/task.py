'''
任务管理 task 业务逻辑
'''


import random
import threading
import traceback
from datetime import datetime, timezone

import json_repair
import shortuuid
from _utils.process import ProcessWorkerThread
from _utils.file import get_file_type, get_bytes_type
from core.config import settings
from core.database import Session, db_session
from core.logger import logger
from core.security import args_security_check_config
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from models.project import Project
from models.task import Task
from services.robots.manage import get_robots_info, get_robots_items, update_robots
from services.tasks.hermes import get_hermes_sessions_messages
from services.inbox import create_inbox_record
from sqlalchemy import delete, func, or_, select


def get_worker_by_thread_id(
    thread_id: int
) -> tuple[bool, str, ProcessWorkerThread | None]:
    '''
    通过线程ID获取 ProcessWorkerThread 对象
    '''
    for t in threading.enumerate():
        if t.ident == thread_id and isinstance(t, ProcessWorkerThread):
            return True, 'success', t
    return False, '', None


def stop_worker_by_thread_id(
    thread_id: int
) -> tuple[bool, str, int | None]:
    '''
    通过线程ID停止 worker
    '''
    status, _, worker = get_worker_by_thread_id(thread_id)
    if status:
        worker.stop()
        return True, 'success', thread_id
    else:
        return False, '', None


def get_tasks_items(
    db: Session,
    page: int = 1,
    size: int = 10,
    message: str = None,
    project_id: str = None,
    types: list[args_security_check_config['task_type']] = None,     # type: ignore[reportUndefinedVariable]
    priorities: list[args_security_check_config['priority']] = None,    # type: ignore[reportUndefinedVariable]
    statuses: list[args_security_check_config['task_status']] = None,     # type: ignore[reportUndefinedVariable]
    robots: list[str] = None,
    triggers: list[args_security_check_config['trigger']] = None,     # type: ignore[reportUndefinedVariable]
    start_created_time: datetime = None,
    end_created_time: datetime = None,
    start_updated_time: datetime = None,
    end_updated_time: datetime = None,
    order_by: args_security_check_config['tasks_order_by'] = 'updated_time',     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc'     # type: ignore[reportUndefinedVariable]
) -> tuple[bool, str, dict]:
    '''
    根据查询条件获取任务列表
    '''
    stmt = select(Task)

    if message:
        stmt = stmt.where(Task.message.contains(message))
    if project_id:
        stmt = stmt.where(Task.project_id == project_id)
    if types:
        stmt = stmt.where(Task.type.in_(types))
    if statuses:
        stmt = stmt.where(Task.status.in_(statuses))
    if priorities:
        stmt = stmt.where(Task.priority.in_(priorities))
    if robots:
        for robot in robots:
            stmt = stmt.where(Task.robots.contains(robot))
    if triggers:
        stmt = stmt.where(Task.trigger.in_(triggers))
    if start_created_time:
        stmt = stmt.where(Task.created_time >= start_created_time)
    if end_created_time:
        stmt = stmt.where(Task.created_time <= end_created_time)
    if start_updated_time:
        stmt = stmt.where(Task.updated_time >= start_updated_time)
    if end_updated_time:
        stmt = stmt.where(Task.updated_time <= end_updated_time)
    
    if stmt.whereclause is not None:
        total = db.scalar(
            select(func.count()).where(stmt.whereclause)
        )
    else:
        total = db.scalar(
            select(func.count()).select_from(Task)
        )

    updated_time_column = getattr(Task, 'updated_time')

    if order_by == 'updated_time':
        stmt = stmt.order_by(
            updated_time_column.desc() if order_type == 'desc' else updated_time_column
        )
    else:
        order_column = getattr(Task, order_by)
        stmt = stmt.order_by(
            order_column.desc() if order_type == 'desc' else order_column,
            updated_time_column.desc() if order_type == 'desc' else updated_time_column
        )

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


def create_tasks_record(
    db: Session,
    message: str,
    project_id: str,
    type: args_security_check_config['task_type'],     # type: ignore[reportUndefinedVariable]
    priority: args_security_check_config['priority'],     # type: ignore[reportUndefinedVariable]
    status: args_security_check_config['task_status'],     # type: ignore[reportUndefinedVariable]
    robots: list[str],
    trigger: args_security_check_config['trigger'] = 'user',     # type: ignore[reportUndefinedVariable]
) -> tuple[bool, str, dict | None]:
    '''
    创建任务
    '''
    id = shortuuid.uuid()

    task_record = Task(
        id=id,
        message=message,
        project_id=project_id,
        type=type,
        priority=priority,
        status=status,
        robots=robots,
        trigger=trigger
    )

    try:
        db.add(task_record)
        db.commit()
        return True, 'success', {'id': id}
    except:
        logger.error(traceback.format_exc())
        return False, 'create_task_record_failed', None
    

def update_tasks_record(
    db: Session,
    id: str,
    priority: args_security_check_config['priority'] = None,     # type: ignore[reportUndefinedVariable]
    status: args_security_check_config['task_status'] = None,     # type: ignore[reportUndefinedVariable]
    robots: list[str] = None,
    result: str = None,
    thread_id: int = None,
    created_time: datetime = None,
    updated_time: datetime = None,
) -> tuple[bool, str, dict | None]:
    '''
    更新指定任务记录
    '''
    task_record = db.get(Task, id)
    
    if priority:
        task_record.priority = priority
    if status:
        task_record.status = status
    if robots:
        task_record.robots = robots
    if result:
        task_record.result = result
    if thread_id:
        task_record.thread_id = thread_id
    if created_time:
        task_record.created_time = created_time
    if updated_time:
        task_record.updated_time = updated_time
    else:
        task_record.updated_time = datetime.now(timezone.utc)
    
    try:
        db.commit()
        db.refresh(task_record)
        return True, 'success', {'id': id}
    except:
        logger.error(traceback.format_exc())
        db.rollback()
        return False, 'update_task_record_failed', None


def delete_tasks_record(
    db: Session,
    ids: list[str]
) -> tuple[bool, str, dict | None]:
    '''
    删除指定任务记录
    '''
    if not ids:
        return True, 'success', ids
    
    or_conditions = []

    for id in ids:
        or_conditions.append(Task.id == id)
    
    stmt = delete(Task).where(
        or_(*or_conditions)
    )
    
    try:
        db.execute(stmt)
        db.commit()
        return True, 'success', {'ids': ids}
    except:
        logger.error(traceback.format_exc())
        db.rollback()
        return False, 'delete_task_record_failed', None
    

def get_tasks_results(
    db: Session,
    id: str
) -> tuple[bool, str, str]:
    '''
    获取指定任务结果
    '''
    task_record = db.get(Task, id)

    return True, 'success', task_record.result


def cancel_tasks(
    db: Session,
    ids: list[str]
) -> tuple[bool, str, dict]:
    '''
    取消指定任务
    '''
    for id in ids:
        status = db.get(Task, id).status
        if status == 'pending':
            delete_tasks_record(db, [id])
        
        if status == 'running':
            thread_id = db.get(Task, id).thread_id
            stop_worker_by_thread_id(thread_id)
        
            stop_status = db.get(Task, id).status
            if stop_status == 'running':
                update_tasks_record(
                    db=db,
                    id=id,
                    status='interrupted'
                )
    
    return True, 'success', {'ids': ids}


def run_tasks(
    name: str,
    session_id: str,
    message: str,
    priority: args_security_check_config['priority'] = 'P3',     # type: ignore[reportUndefinedVariable]
    coordinator: bool = False,
    trigger: args_security_check_config['trigger'] = 'user',     # type: ignore[reportUndefinedVariable]
) -> tuple[bool, str, dict | None]:
    '''
    执行指定数字员工/协调器，指定会话任务
    '''
    with db_session() as db:
        record = get_tasks_items(
            db=db,
            page=0,
            statuses=['running'],
            project_id=session_id
        )[-1]['items']

    if not record:
        status = 'running'
    else:
        status = 'pending'

    if coordinator:
        with db_session() as db:
            robots = db.get(Project, session_id).robots

        if name == 'agbox-coordinator-sync':
            message = f'{{"name":null,"message":"{message}"}}'

        message += generate_coordinator_suffix_messages(
            robots=robots,
            session_id=session_id,
            coordinator_name=name
        )
        
        task_type = name
    else:
        robots = [name]
        task_type = 'session'
        
    with db_session() as db:
        _status, msg, data = create_tasks_record(
            db=db,
            message=message,
            project_id=session_id,
            type=task_type,
            priority=priority,
            status=status,
            robots=robots,
            trigger=trigger
        )

    if not _status:
        return False, msg, None
    
    if status == 'running':
        run_chat_process(
            task_id=data['id'],
            name=name,
            session_id=session_id,
            message=message,
            coordinator=coordinator
        )

    return True, 'success', {'id': data['id']}


def callback_tasks_finished(
    worker: ProcessWorkerThread,
    is_interrupted: bool = False
) -> None:
    '''
    任务完成回调
    '''
    task_id = worker.task_id
    stdout = worker.stdout
    stderr = worker.stderr
    returncode = worker.returncode
    
    with db_session() as db:
        task_record = db.get(Task, task_id)

    task_type = task_record.type
    if task_type == 'session':
        name = task_record.robots[0]
        coordinator = False
    else:
        name = task_type
        coordinator = True
    
    session_id = task_record.project_id

    # 上报任务结果
    if returncode != 0:
        if is_interrupted:
            status = 'interrupted'
        else:
            status = 'failed'
        result = ''
        if stdout is not None:
            result += stdout + '\n\n'
        if stderr is not None:
            result += stderr
    else:
        status = 'finished'
        result = get_hermes_sessions_messages(
            name=name,
            session_id=session_id,
            coordinator=coordinator
        )[-1][-1]['content']

        if coordinator and name == 'agbox-coordinator-sync':
            try:
                result = json_repair.loads(result)['message']
            except:
                logger.error(traceback.format_exc())
                pass
    
    with db_session() as db:
        update_tasks_record(
            db=db,
            id=task_id,
            status=status,
            result=result
        )
    
    # 推送收件箱任务完成消息
    create_inbox_record(
        db=db,
        robot=name,
        type='tasks',
        message=task_record.message,
        status=status,
        result=result,
        coordinator=coordinator
    )

    # 更新数字员工经验
    if not coordinator:
        need_upgrade_robots = [name]
    else:
        need_upgrade_robots = task_record.robots

    for robot in need_upgrade_robots:
        robot_path = settings.ROBOTS_DIR / robot
        robot_info = get_robots_info(robot_path)[-1]
        
        with db_session() as db:
            update_robots(
                db=db,
                name=robot,
                exp=robot_info['exp'] + random.randint(5, 10)
            )
        
        # 推送收件箱数字员工升级消息
        new_robot_info = get_robots_info(robot_path)[-1]
        if robot_info['rank'] != new_robot_info['rank']:
            create_inbox_record(
                db=db,
                robot=robot,
                type='upgrade',
                message=task_record.message,
                status='rank',
                result=new_robot_info['rank'],
                coordinator=False
            )
        if robot_info['quality'] != new_robot_info['quality']:
            create_inbox_record(
                db=db,
                robot=robot,
                type='upgrade',
                message=task_record.message,
                status='quality',
                result=new_robot_info['quality'],
                coordinator=False
            )

    # 从队列中取任务继续执行
    with db_session() as db:
        pending_tasks_record = get_tasks_items(
            db=db,
            project_id=session_id,
            statuses=['pending'],
            order_by='priority',
            order_type='asc'
        )[-1]['items']

    if not pending_tasks_record:
        pass
    else:
        item = pending_tasks_record[0]

        run_chat_process(
            task_id=item['id'],
            name=item['robots'][0] if item['type'] == 'session' else item['type'],
            session_id=session_id,
            message=item['message'],
            coordinator=False if item['type'] == 'session' else True
        )


def get_tasks_robots_messages_items(
    db: Session,
    id: str,
    name: str,
    page: int = 1,
    size: int = 10,
    roles: list[args_security_check_config['hermes_messages_role']] = None,     # type: ignore[reportUndefinedVariable]
    content: str = None,
    coordinator: bool = False
) -> tuple[bool, str, dict]:
    '''
    获取指定任务，指定数字员工/协调器消息
    '''
    session_id = db.get(Task, id).project_id
    created_time = db.get(Task, id).created_time
    updated_time = db.get(Task, id).updated_time

    messages = get_hermes_sessions_messages(
        name=name,
        session_id=session_id,
        roles=roles,
        content=content,
        coordinator=coordinator
    )[-1]

    start_line_num = None
    end_line_num = None
    
    for line_num, message in enumerate(messages):
        if message['timestamp'] < created_time:
            continue
        
        if message['role'] == 'user':
            if start_line_num is None:
                start_line_num = line_num
        
        if message['timestamp'] > updated_time:
            end_line_num = line_num
            break

    if start_line_num is not None:
        if end_line_num is not None:
            messages = messages[start_line_num : end_line_num]
        else:
            messages = messages[start_line_num:]
    else:
        messages = []

    total = len(messages)

    if page > 0:
        skip = (page - 1) * size
    else:
        skip = None

    messages = messages[skip:skip + size] if skip is not None else messages

    result = {
        'items': messages,
        'total': total,
        'page': page,
        'size': size
    }
    
    return True, 'success', result


def generate_coordinator_suffix_messages(
    robots: list[str],
    session_id: str,
    coordinator_name: str
) -> tuple[bool, str, str]:
    '''
    生成协调器后缀消息
    '''
    result = '\n\nList of digital employees available for this task:\n'

    for robot in robots:
        description = get_robots_items(
            name=robot
        )[-1]['items'][0]['description']
        result += f'- name: {robot}\n  - description: {description}\n\n'
    

    if coordinator_name == 'agbox-coordinator-async':
        result += '\nParameters when assigning tasks:\n'

        result += f'- python executable: {str(settings.PYTHON_EXECUTABLE)}\n'
        result += f'- robots_dir: {str(settings.ROBOTS_DIR)}\n'
        result += f'- work_dir: {str(settings.WORKSPACE_DIR / session_id)}\n'
        result += f'- session_id: {session_id}\n\n'

        result += 'Note: All output must be in the specified working directory. You should only plan tasks and assign them to individual digital employees via the `agbox-assign-task` skill, rather than executing tasks directly yourself.'
    
    if coordinator_name == 'agbox-coordinator-sync':
        result += f'\nNote: All output must be in the current working directory: {settings.WORKSPACE_DIR / session_id}. You should plan your tasks and output them as JSON strings instead of executing them directly.'
        result = '\n\nThe above is the JSON input format. This is the start of a new task. Below are the hints and points to note for this task. Please distinguish between the input and the hints.' + result
    
    result += ' Previously involved digital employees may be deleted, renamed, etc. New digital employees may be added to this task. Please be aware of these changes to digital employees and avoid confusion regarding past task contexts. The task planning should be based on the digital employee list provided for this task.'

    return result


def run_chat_process(
    task_id: str,
    name: str,
    session_id: str,
    message: str,
    coordinator: bool = False
) -> None:
    '''
    启动 chat 后台进程
    '''
    if coordinator and name == 'agbox-coordinator-sync':
            command = [
                str(settings.PYTHON_EXECUTABLE),
                str(settings.COORDINATOR_SYNC_SCRIPT_PATH),
                '--robots_dir', str(settings.ROBOTS_DIR),
                '--task_description', message,
                '--work_dir', str(settings.WORKSPACE_DIR / session_id),
                '--session_id', session_id,
            ]
            env={}
    else:
        command = [
            settings.HERMES_EXECUTABLE,
            'chat',
            *(['-w'] if coordinator else []),
            '--yolo',
            '-r',
            session_id,
            '-Q',
            '-q',
            message
        ]

        if coordinator:
            hermes_home = str(settings.COORDINATOR_DIR / name)
        else:
            hermes_home = str(settings.ROBOTS_DIR / name)
    
        env = {'HERMES_HOME': hermes_home}

    worker = ProcessWorkerThread(
        command=command,
        cwd=settings.WORKSPACE_DIR / session_id,
        env=env,
        task_id=task_id,
        callback=callback_tasks_finished
    )
    worker.start()

    with db_session() as db:
        update_tasks_record(
            db=db,
            id=task_id,
            status='running',
            thread_id=worker.ident,
            created_time=datetime.now(timezone.utc)
        )


def upload_paste_image(
    uf: UploadFile,
    session_id: str
) -> tuple[bool, str, str]:
    '''
    上传粘贴图片
    '''
    path = settings.WORKSPACE_DIR / session_id / '.pastes'

    if not path.exists():
        path.mkdir(exist_ok=True)
    
    uf.file.seek(0)
    ext = get_bytes_type(uf.file.read(2048))[-1]['ext']
    uf.file.seek(0)
    
    file_name = f'paste_{shortuuid.uuid()}.{ext}'
    file_path = path / file_name
    
    with file_path.open('wb') as f:
        f.write(uf.file.read())
    
    result = {
        'session_id': session_id,
        'file_name': file_name
    }
    return True, 'success', result


def get_paste_image(
    session_id: str,
    file_name: str
) -> tuple[bool, str, StreamingResponse]:
    '''
    获取粘贴图片
    '''
    path = settings.WORKSPACE_DIR / session_id / '.pastes' / file_name
    
    mime_type = get_file_type(path)[-1]['mime_type']

    result = StreamingResponse(
        path.open('rb'),
        media_type=mime_type,
        headers={
            'Content-Disposition': f'attachment; filename={file_name}'
        }
    )

    return True, 'success', result
