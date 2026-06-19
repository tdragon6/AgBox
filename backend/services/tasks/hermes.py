'''
任务管理 hermes 业务逻辑
'''


import traceback
import secrets
import sqlite3
from datetime import datetime

from core.config import settings
from core.logger import logger
from core.security import args_security_check_config
from hermes_state import SessionDB
from services.robots.manage import get_robots_path


def get_hermes_sessions_db(
    name: str,
    coordinator: bool = False
) -> tuple[bool, str, SessionDB]:
    '''
    获取会话数据库
    '''
    if coordinator:
        db_path = settings.COORDINATOR_DIR / name / 'state.db'
    else:
        db_path = get_robots_path(name)[-1] / 'state.db'
    
    session_db = SessionDB(
        db_path=db_path
    )
    
    return True, 'success', session_db
    

def create_hermes_sessions(
    names: list[str],
    session_id: str = None,
    coordinator: bool = False,
    title: str = None
) -> tuple[bool, str, dict]:
    '''
    创建会话
    '''
    if not session_id:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_suffix = secrets.token_hex(3)
        session_id = f'{timestamp}_{random_suffix}'
    
    for name in names:
        session_db = get_hermes_sessions_db(name, coordinator)[-1]
        
        session_db.create_session(
            session_id=session_id,
            source='cli'
        )

        if not coordinator:            
            rename_hermes_sessions(
                name=name,
                session_id=session_id,
                title=session_id if title is None else title
            )
    
    return True, 'success', {'session_id': session_id}


def get_hermes_sessions(
    name: str,
    page: int = 1,
    limit: int = 10,
    coordinator: bool = False,
    ignore_coordinator_filter: bool = False,
    title: str = None
) -> tuple[bool, str, list[dict]]:
    '''
    获取会话
    '''
    session_db = get_hermes_sessions_db(name, coordinator)[-1]
    
    if page > 0:
        offset = (page - 1) * limit
    else:
        limit = 999999
        offset = 0
    
    items = session_db.list_sessions_rich(
        limit=limit,
        offset=offset,
        include_children=True
    )

    cost_keys = settings.HERMES_MODEL_COST_KEYS

    need_keys = [
        'id',
        'title'
    ] + cost_keys

    result = []

    for item in items:
        if item['parent_session_id'] is not None:
            continue
        
        if not item['title']:
            item['title'] = item['id']
        
        if not ignore_coordinator_filter and not coordinator and item['title'].startswith(settings.COORDINATOR_MARK):
            continue
        
        if title is not None and title not in item['title']:
            continue
        
        keys = list(item.keys())

        for key in keys:
            if key not in need_keys:
                del item[key]
            if key in cost_keys and item[key] is None:
                item[key] = 0
        
        result.append(item)
    
    # 加上子会话 cost
    all_session_ids = session_db.list_sessions_rich(
        limit=999999,
        offset=0,
        include_children=True
    )

    for item in result:
        child_session_ids = find_child_session_ids(
            all_session_ids=all_session_ids,
            session_id=item['id']
        )

        for child_session_id in child_session_ids:
            child_item = session_db.get_session(session_id=child_session_id)
            for key in cost_keys:
                item[key] += child_item[key] if child_item[key] is not None else 0
    
    return True, 'success', result


def find_child_session_ids(
    all_session_ids: list[dict],
    session_id: str,
    child_session_ids: list[str] = []
) -> list[str]:
    '''
    递归查找子会话ID
    '''
    for item in all_session_ids:
        if item['parent_session_id'] == session_id:
            child_session_ids.append(item['id'])

            return find_child_session_ids(
                all_session_ids=all_session_ids,
                session_id=item['id'],
                child_session_ids=child_session_ids
            )
    
    return child_session_ids


def delete_hermes_sessions(
    name: str,
    session_ids: list[str],
    coordinator: bool = False
) -> tuple[bool, str, dict]:
    '''
    删除会话
    '''
    session_db = get_hermes_sessions_db(name, coordinator)[-1]

    all_session_ids = session_db.list_sessions_rich(
        limit=999999,
        offset=0,
        include_children=True
    )
    
    for session_id in session_ids:
        child_session_ids = find_child_session_ids(
            all_session_ids=all_session_ids,
            session_id=session_id
        )

        session_db.delete_session(session_id=session_id)
        
        for child_session_id in child_session_ids:
            session_db.delete_session(session_id=child_session_id)
    
    result = {'name': name, 'session_ids': session_ids}
    
    return True, 'success', result


def rename_hermes_sessions(
    name: str,
    session_id: str,
    title: str
) -> tuple[bool, str, dict]:
    '''
    重命名会话
    '''
    db_path = get_robots_path(name)[-1] / 'state.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(
            'UPDATE sessions SET title = ? WHERE id = ?',
            (title, session_id)
        )
        
        conn.commit()

        result = {'name': name, 'session_id': session_id, 'title': title}

        return True, 'success', result
    except:
        logger.error(traceback.format_exc())
        conn.rollback()
        return False, 'rename_session_failed', None
    finally:
        conn.close()
    

def get_hermes_sessions_messages(
    name: str,
    session_id: str,
    roles: list[args_security_check_config['hermes_messages_role']] = None,     # type: ignore[reportUndefinedVariable]
    content: str = None,
    coordinator: bool = False
) -> tuple[bool, str, list[dict]]:
    '''
    获取会话消息
    '''
    session_db = get_hermes_sessions_db(name, coordinator)[-1]

    items = session_db.get_messages(session_id)

    all_session_ids = session_db.list_sessions_rich(
        limit=999999,
        offset=0,
        include_children=True
    )

    child_session_ids = find_child_session_ids(
        all_session_ids=all_session_ids,
        session_id=session_id
    )

    for child_session_id in child_session_ids:
        items += session_db.get_messages(child_session_id)

    need_keys = [
        'role',
        'content',
        'timestamp',
        'reasoning'
    ]

    result = []
    
    for item in items:
        if roles is not None and item['role'] not in roles:
            continue
        if content is not None and content not in item['content']:
            continue
        
        item['timestamp'] = datetime.fromtimestamp(int(item['timestamp']))
        keys = list(item.keys())

        for key in keys:
            if key not in need_keys:
                del item[key]
        
        result.append(item)
    
    return True, 'success', result