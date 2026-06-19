'''
任务管理 session 业务逻辑
'''


import shutil

from _utils.file import init_git_repo
from core.security import args_security_check_config
from core.config import settings
from core.database import Session
from services.tasks.hermes import create_hermes_sessions, delete_hermes_sessions, get_hermes_sessions_messages
from services.tasks.task import delete_tasks_record, get_tasks_items


def get_robots_sessions_messages_items(
    name: str,
    session_id: str,
    page: int = 1,
    size: int = 10,
    roles: list[args_security_check_config['hermes_messages_role']] = None,     # type: ignore[reportUndefinedVariable]
    content: str = None,
    coordinator: bool = False
) -> tuple[bool, str, list[dict]]:
    '''
    获取指定数字员工的指定会话消息
    '''
    messages = get_hermes_sessions_messages(
        name=name,
        session_id=session_id,
        roles=roles,
        content=content,
        coordinator=coordinator
    )[-1]

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


def create_robots_sessions(
    names: list[str]
) -> tuple[bool, str, dict]:
    '''
    创建指定数字员工会话
    '''
    session_id = create_hermes_sessions(
        names=names
    )[-1]['session_id']

    workspace_path = settings.WORKSPACE_DIR / session_id
    workspace_path.mkdir(exist_ok=True)
    
    init_git_repo(
        repo_dir=workspace_path
    )
    
    return True, 'success', {'session_id': session_id}


def delete_robots_sessions(
    db: Session,
    name: str,
    session_ids: list[str]
) -> tuple[bool, str, dict]:
    '''
    删除指定数字员工的指定会话
    '''
    # 删除任务记录
    task_ids = []
    for session_id in session_ids:
        for item in get_tasks_items(db=db, page=0, project_id=session_id)[-1]['items']:
            task_ids.append(item['id'])

    status, msg, _ = delete_tasks_record(
        db=db,
        ids=task_ids
    )
    if not status:
        return False, msg, None

    # 删除工作区
    for session_id in session_ids:
        workspace_dir = settings.WORKSPACE_DIR / session_id
        if workspace_dir.exists():
            shutil.rmtree(workspace_dir)

    # 删除 hermes 会话
    delete_hermes_sessions(
        name=name,
        session_ids=session_ids
    )
    
    result = {'name': name, 'session_ids': session_ids}

    return True, 'success', result
 