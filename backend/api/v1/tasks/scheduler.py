'''
任务管理 scheduler API
'''


from core.database import get_db
from fastapi import APIRouter, Body, Depends, Request
from handler.tasks.scheduler import (
    handler_scheduler_create_scheduler_jobs,
    handler_scheduler_delete_scheduler_jobs,
    handler_scheduler_get_scheduler_jobs_items,
    handler_scheduler_pause_scheduler_jobs,
    handler_scheduler_resume_scheduler_jobs,
)
from schemas.tasks.scheduler import (
    SchedulerCreateRequest,
    SchedulerDeleteRequest,
    SchedulerItemsRequest,
    SchedulerPauseRequest,
    SchedulerResumeRequest,
    SchedulerUpdateRequest,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/create', summary='创建定时任务', description='创建定时任务')
def createSchedulerJobs(
    request: Request,
    req: SchedulerCreateRequest = Body()
) -> dict:
    '''
    创建定时任务
    '''
    result = handler_scheduler_create_scheduler_jobs(
        request=request,
        minute=req.minute,
        hour=req.hour,
        day=req.day,
        week=req.week,
        month=req.month,
        name=req.name,
        description=req.description,
        robot=req.robot,
        project_id=req.project_id,
        message=req.message,
        priority=req.priority,
        coordinator=req.coordinator
    )

    return result


@router.post('/update', summary='更新定时任务', description='更新定时任务')
def updateSchedulerJobs(
    request: Request,
    req: SchedulerUpdateRequest = Body()
) -> dict:
    '''
    更新定时任务
    '''
    result = handler_scheduler_create_scheduler_jobs(
        request=request,
        minute=req.minute,
        hour=req.hour,
        day=req.day,
        week=req.week,
        month=req.month,
        name=req.name,
        description=req.description,
        robot=req.robot,
        project_id=req.project_id,
        message=req.message,
        priority=req.priority,
        coordinator=req.coordinator,
        id=req.id
    )

    return result


@router.post('/items', summary='获取定时任务列表', description='获取定时任务列表')
def getSchedulerJobsItems(
    request: Request,
    db: Session = Depends(get_db),
    req: SchedulerItemsRequest = Body(default_factory=SchedulerItemsRequest)
) -> dict:
    '''
    获取定时任务列表
    '''
    result = handler_scheduler_get_scheduler_jobs_items(
        request=request,
        db=db,
        page=req.page,
        size=req.size,
        name=req.name,
        description=req.description,
        start_created_time=req.start_created_time,
        end_created_time=req.end_created_time,
        start_updated_time=req.start_updated_time,
        end_updated_time=req.end_updated_time,
        robot=req.robot,
        mount_name=req.mount_name,
        message=req.message,
        priorities=req.priorities,
        coordinator=req.coordinator,
        start_next_run_time=req.start_next_run_time,
        end_next_run_time=req.end_next_run_time,
        is_paused=req.is_paused,
        order_by=req.order_by,
        order_type=req.order_type
    )

    return result


@router.post('/pause', summary='暂停定时任务', description='暂停定时任务')
def pauseSchedulerJobs(
    request: Request,
    req: SchedulerPauseRequest = Body()
) -> dict:
    '''
    暂停定时任务
    '''
    result = handler_scheduler_pause_scheduler_jobs(
        request=request,
        ids=req.ids
    )

    return result


@router.post('/resume', summary='恢复定时任务', description='恢复定时任务')
def resumeSchedulerJobs(
    request: Request,
    req: SchedulerResumeRequest = Body()
) -> dict:
    '''
    恢复定时任务
    '''
    result = handler_scheduler_resume_scheduler_jobs(
        request=request,
        ids=req.ids
    )

    return result


@router.post('/delete', summary='删除定时任务', description='删除定时任务')
def deleteSchedulerJobs(
    request: Request,
    db: Session = Depends(get_db),
    req: SchedulerDeleteRequest = Body()
) -> dict:
    '''
    删除定时任务
    '''
    result = handler_scheduler_delete_scheduler_jobs(
        request=request,
        db=db,
        ids=req.ids
    )

    return result