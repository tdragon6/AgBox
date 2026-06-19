'''
任务管理 session API
'''


from core.database import get_db
from fastapi import APIRouter, Body, Depends, Request
from handler.tasks.session import (
    handler_session_create_robots_sessions,
    handler_session_delete_robots_sessions,
    handler_session_get_robots_items,
    handler_session_get_robots_sessions,
    handler_session_get_robots_sessions_messages_items,
    handler_session_rename_robots_sessions,
)
from schemas.tasks.session import (
    SessionCreateRobotsSessionsRequest,
    SessionDeleteRobotsSessionsRequest,
    SessionRenameRobotsSessionsRequest,
    SessionRobotsSessionsMessagesRequest,
    SessionRobotsSessionsRequest,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/robots/items', summary='获取所有数字员工列表', description='获取所有数字员工列表')
def getRobotsItems(
    request: Request
) -> dict:
    '''
    获取所有数字员工列表
    '''
    result = handler_session_get_robots_items(
        request=request
    )

    return result


@router.post('/robots/sessions', summary='获取指定数字员工，所有会话', description='获取指定数字员工，所有会话')
def getRobotsSessions(
    request: Request,
    req: SessionRobotsSessionsRequest = Body()
) -> dict:
    '''
    获取指定数字员工，所有会话
    '''
    result = handler_session_get_robots_sessions(
        request=request,
        name=req.name,
        coordinator=req.coordinator,
        ignore_coordinator_filter=req.ignore_coordinator_filter,
        title=req.title
    )

    return result


@router.post('/robots/sessions/messages', summary='获取指定数字员工，指定会话消息', description='获取指定数字员工，指定会话消息')
def getRobotsSessionsMessages(
    request: Request,
    req: SessionRobotsSessionsMessagesRequest = Body()
) -> dict:
    '''
    获取指定数字员工，指定会话消息
    '''
    result = handler_session_get_robots_sessions_messages_items(
        request=request,
        name=req.name,
        session_id=req.session_id,
        page=req.page,
        size=req.size,
        roles=req.roles,
        content=req.content,
        coordinator=req.coordinator
    )

    return result


@router.post('/robots/sessions/rename', summary='重命名指定数字员工，指定会话', description='重命名指定数字员工，指定会话')
def renameRobotsSessions(
    request: Request,
    req: SessionRenameRobotsSessionsRequest = Body()
) -> dict:
    '''
    重命名指定数字员工，指定会话
    '''
    result = handler_session_rename_robots_sessions(
        request=request,
        name=req.name,
        session_id=req.session_id,
        title=req.title
    )

    return result


@router.post('/robots/sessions/create', summary='创建指定数字员工会话', description='创建指定数字员工会话')
def createRobotsSessions(
    request: Request,
    req: SessionCreateRobotsSessionsRequest = Body()
) -> dict:
    '''
    创建指定数字员工会话
    '''
    result = handler_session_create_robots_sessions(
        request=request,
        names=req.names
    )

    return result


@router.post('/robots/sessions/delete', summary='删除指定数字员工，指定会话', description='删除指定数字员工，指定会话')
def deleteRobotsSessions(
    request: Request,
    db: Session = Depends(get_db),
    req: SessionDeleteRobotsSessionsRequest = Body()
) -> dict:
    '''
    删除指定数字员工，指定会话
    '''
    result = handler_session_delete_robots_sessions(
        request=request,
        db=db,
        name=req.name,
        session_ids=req.session_ids
    )

    return result