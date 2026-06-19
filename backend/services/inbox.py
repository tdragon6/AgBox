'''
收件箱 业务逻辑
'''


import traceback
from datetime import datetime

import shortuuid
from core.database import Session
from core.logger import logger
from core.security import args_security_check_config
from fastapi.encoders import jsonable_encoder
from models.inbox import Inbox
from sqlalchemy import delete, func, or_, select


def get_inbox_items(
    db: Session,
    page: int = 1,
    size: int = 10,
    robot: str = None,
    types: list[args_security_check_config['inbox_type']] = None,     # type: ignore[reportUndefinedVariable]
    message: str = None,
    statuses: list[args_security_check_config['inbox_status']] = None,     # type: ignore[reportUndefinedVariable]
    is_read: bool = None,
    coordinator: bool = None,
    start_created_time: datetime = None,
    end_created_time: datetime = None,
    start_updated_time: datetime = None,
    end_updated_time: datetime = None,
    order_by: args_security_check_config['inbox_order_by'] = 'updated_time',     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc'     # type: ignore[reportUndefinedVariable]
) -> tuple[bool, str, dict]:
    '''
    根据查询条件获取收件箱列表
    '''
    stmt = select(Inbox)

    if robot:
        stmt = stmt.where(Inbox.robot == robot)
    if types:
        stmt = stmt.where(Inbox.type.in_(types))
    if message:
        stmt = stmt.where(Inbox.message.contains(message))
    if statuses:
        stmt = stmt.where(Inbox.status.in_(statuses))
    if is_read is not None:
        stmt = stmt.where(Inbox.is_read == is_read)
    if coordinator is not None:
        stmt = stmt.where(Inbox.coordinator == coordinator)
    if start_created_time:
        stmt = stmt.where(Inbox.created_time >= start_created_time)
    if end_created_time:
        stmt = stmt.where(Inbox.created_time <= end_created_time)
    if start_updated_time:
        stmt = stmt.where(Inbox.updated_time >= start_updated_time)
    if end_updated_time:
        stmt = stmt.where(Inbox.updated_time <= end_updated_time)
    
    if stmt.whereclause is not None:
        total = db.scalar(
            select(func.count()).where(stmt.whereclause)
        )
    else:
        total = db.scalar(
            select(func.count()).select_from(Inbox)
        )

    updated_time_column = getattr(Inbox, 'updated_time')

    if order_by == 'updated_time':
        stmt = stmt.order_by(
            updated_time_column.desc() if order_type == 'desc' else updated_time_column
        )
    else:
        order_column = getattr(Inbox, order_by)
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


def get_robots_inbox_unread_count(
    db: Session
) -> tuple[bool, str, dict | None]:
    '''
    获取收件箱未读消息数量
    '''
    items = get_inbox_items(
        db=db,
        page=0,
    )[-1]['items']

    count_dict = {}
    
    for item in items:
        count_dict.setdefault(
            item['robot'],
            {
                'count': 0,
                'coordinator': item['coordinator']
            }
        )
        if not item['is_read']:
            count_dict[item['robot']]['count'] += 1
    
    result = []

    for robot in count_dict.keys():
        result.append({
            'robot': robot,
            'count': count_dict[robot]['count'],
            'coordinator': count_dict[robot]['coordinator']
        })
    
    result.sort(
        key=lambda item: (
            0 if item['robot'] == 'agbox-coordinator-sync' and item['coordinator'] else
            1 if item['robot'] == 'agbox-coordinator-async' and item['coordinator'] else
            2
        )
    )

    return True, 'success', result


def create_inbox_record(
    db: Session,
    robot: str,
    type: args_security_check_config['inbox_type'],     # type: ignore[reportUndefinedVariable]
    message: str,
    status: str,     # type: ignore[reportUndefinedVariable]
    result: str,
    is_read: bool = False,
    coordinator: bool = False
) -> tuple[bool, str, dict | None]:
    '''
    创建收件箱通知
    '''
    id = shortuuid.uuid()
    
    inbox_record = Inbox(
        id=id,
        robot=robot,
        type=type,
        message=message,
        status=status,
        result=result,
        is_read=is_read,
        coordinator=coordinator,
    )

    try:
        db.add(inbox_record)
        db.commit()
        return True, 'success', {'id': id}
    except:
        logger.error(traceback.format_exc())
        return False, 'create_inbox_record_failed', None
    

def update_inbox_read_status(
    db: Session,
    ids: list[str]
) -> tuple[bool, str, dict | None]:
    '''
    更新指定收件箱通知已读状态
    '''
    for id in ids:
        inbox_record = db.get(Inbox, id)
        inbox_record.is_read = True
    
    try:
        db.commit()
        db.refresh(inbox_record)
        return True, 'success', {'ids': ids}
    except:
        logger.error(traceback.format_exc())
        db.rollback()
        return False, 'update_inbox_read_status_failed', None


def delete_inbox_record(
    db: Session,
    ids: list[str]
) -> tuple[bool, str, dict | None]:
    '''
    删除指定收件箱通知
    '''
    if not ids:
        return True, 'success', ids
    
    or_conditions = []

    for id in ids:
        or_conditions.append(Inbox.id == id)
    
    stmt = delete(Inbox).where(
        or_(*or_conditions)
    )
    
    try:
        db.execute(stmt)
        db.commit()
        return True, 'success', {'ids': ids}
    except:
        logger.error(traceback.format_exc())
        db.rollback()
        return False, 'delete_inbox_record_failed', None
    