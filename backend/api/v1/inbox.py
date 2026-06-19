'''
收件箱 API
'''


from core.database import get_db
from fastapi import APIRouter, Body, Depends, Request
from handler.inbox import (
    handler_get_inbox_items,
    handler_get_robots_inbox_unread_count,
    handler_update_inbox_read_status,
    handler_delete_inbox,
)
from schemas.inbox import (
    InboxItemsRequest,
    InboxUpdateReadStatusRequest,
    InboxDeleteRequest,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/items', summary='获取收件箱消息', description='获取收件箱消息')
def getInboxItems(
    request: Request,
    db: Session = Depends(get_db),
    req: InboxItemsRequest = Body()
) -> dict:
    '''
    获取指定任务结果
    '''
    result = handler_get_inbox_items(
        request=request,
        db=db,
        page=req.page,
        size=req.size,
        robot=req.robot,
        types=req.types,
        message=req.message,
        statuses=req.statuses,
        is_read=req.is_read,
        coordinator=req.coordinator,
        start_created_time=req.start_created_time,
        end_created_time=req.end_created_time,
        start_updated_time=req.start_updated_time,
        end_updated_time=req.end_updated_time,
        order_by=req.order_by,
        order_type=req.order_type
    )

    return result


@router.get('/robots/count/unread', summary='获取收件箱未读消息数量', description='获取收件箱未读消息数量')
def getInboxUnreadCount(
    request: Request,
    db: Session = Depends(get_db),
) -> dict:
    '''
    获取收件箱未读消息数量
    '''
    result = handler_get_robots_inbox_unread_count(
        request=request,
        db=db
    )

    return result


@router.post('/update/read/status', summary='更新收件箱消息已读状态', description='更新收件箱消息已读状态')
def updateInboxReadStatus(
    request: Request,
    db: Session = Depends(get_db),
    req: InboxUpdateReadStatusRequest = Body()
) -> dict:
    '''
    更新收件箱消息已读状态
    '''
    result = handler_update_inbox_read_status(
        request=request,
        db=db,
        ids=req.ids
    )

    return result


@router.post('/delete', summary='删除收件箱消息', description='删除收件箱消息')
def deleteInboxRecord(
    request: Request,
    db: Session = Depends(get_db),
    req: InboxDeleteRequest = Body()
) -> dict:
    '''
    删除收件箱通知
    '''
    result = handler_delete_inbox(
        request=request,
        db=db,
        ids=req.ids
    )

    return result