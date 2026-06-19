'''
任务管理 project API
'''


from core.database import get_db
from fastapi import APIRouter, Body, Depends, Request
from handler.tasks.project import (
    handler_project_create_projects,
    handler_project_delete_projects,
    handler_project_get_projects_items,
    handler_project_update_projects,
)
from schemas.tasks.project import (
    ProjectCreateRequest,
    ProjectDeleteRequest,
    ProjectItemsRequest,
    ProjectUpdateRequest,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/create', summary='创建项目', description='创建项目')
def createProjects(
    request: Request,
    db: Session = Depends(get_db),
    req: ProjectCreateRequest = Body()
) -> dict:
    '''
    创建项目
    '''
    result = handler_project_create_projects(
        request=request,
        db=db,
        name=req.name,
        description=req.description,
        robots=req.robots
    )

    return result


@router.post('/update', summary='更新项目', description='更新项目')
def updateProjects(
    request: Request,
    db: Session = Depends(get_db),
    req: ProjectUpdateRequest = Body()
) -> dict:
    '''
    更新项目
    '''
    result = handler_project_update_projects(
        request=request,
        db=db,
        id=req.id,
        name=req.name,
        description=req.description,
        robots=req.robots
    )

    return result


@router.post('/delete', summary='删除项目', description='删除项目')
def deleteProjects(
    request: Request,
    db: Session = Depends(get_db),
    req: ProjectDeleteRequest = Body()
) -> dict:
    '''
    删除项目
    '''
    result = handler_project_delete_projects(
        request=request,
        db=db,
        ids=req.ids
    )

    return result


@router.post('/items', summary='获取项目列表', description='获取项目列表')
def getProjectsItems(
    request: Request,
    db: Session = Depends(get_db),
    req: ProjectItemsRequest = Body(default_factory=ProjectItemsRequest)
) -> dict:
    '''
    获取项目列表
    '''
    result = handler_project_get_projects_items(
        request=request,
        db=db,
        page=req.page,
        size=req.size,
        name=req.name,
        description=req.description,
        robots=req.robots,
        history_robots=req.history_robots,
        start_created_time=req.start_created_time,
        end_created_time=req.end_created_time,
        start_updated_time=req.start_updated_time,
        end_updated_time=req.end_updated_time,
        order_by=req.order_by,
        order_type=req.order_type
    )

    return result
