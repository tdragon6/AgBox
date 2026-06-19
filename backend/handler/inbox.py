'''
收件箱 handler
'''

from datetime import datetime

from core.decorator import _handler
from core.security import args_security_check_config
from fastapi import Request
from models.inbox import Inbox
from services.inbox import (
    get_inbox_items,
    get_robots_inbox_unread_count,
    update_inbox_read_status,
    delete_inbox_record
)
from sqlalchemy.orm import Session


@_handler
def handler_get_inbox_items(
    request: Request,
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
):
    '''
    获取全部或指定收件箱通知列表 handler
    '''
    result = get_inbox_items(
        db=db,
        page=page,
        size=size,
        robot=robot,
        types=types,
        message=message,
        statuses=statuses,
        is_read=is_read,
        coordinator=coordinator,
        start_created_time=start_created_time,
        end_created_time=end_created_time,
        start_updated_time=start_updated_time,
        end_updated_time=end_updated_time,
        order_by=order_by,
        order_type=order_type
    )

    return result


@_handler
def handler_get_robots_inbox_unread_count(
    request: Request,
    db: Session
):
    '''
    获取收件箱未读消息数量 handler
    '''
    result = get_robots_inbox_unread_count(
        db=db
    )

    return result


@_handler
def handler_update_inbox_read_status(
    request: Request,
    db: Session,
    ids: list[str]
):
    '''
    更新收件箱通知已读状态 handler
    '''
    for id in ids:
        inbox_record = db.get(Inbox, id)
        if not inbox_record:
            return False, 'inbox_not_found', None
    
    result = update_inbox_read_status(
        db=db,
        ids=ids
    )

    return result


@_handler
def handler_delete_inbox(
    request: Request,
    db: Session,
    ids: list[str]
):
    '''
    删除收件箱通知 handler
    '''
    for id in ids:
        inbox_record = db.get(Inbox, id)
        if not inbox_record:
            return False, 'inbox_not_found', None
    
    result = delete_inbox_record(
        db=db,
        ids=ids
    )

    return result