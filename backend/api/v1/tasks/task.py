'''
任务管理 task API
'''


from core.database import get_db
from fastapi import APIRouter, Body, Depends, Request, File, UploadFile, Form, Query
from fastapi.responses import JSONResponse
from handler.tasks.task import (
    handler_task_cancel_tasks,
    handler_task_get_tasks_items,
    handler_task_get_tasks_results,
    handler_task_get_tasks_robots_messages_items,
    handler_task_run_tasks,
    handler_task_update_tasks_priority,
    handler_task_upload_paste_image,
    handler_task_get_paste_image,
)
from schemas.tasks.task import (
    TaskCancelTasksRequest,
    TaskItemsRequest,
    TaskMessagesItemsRequest,
    TaskResultRequest,
    TaskRunTasksRequest,
    TaskUpdateTasksPriorityRequest,
    TaskGetPasteImageRequest,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/result', summary='获取指定任务结果', description='获取指定任务结果')
def getTasksResults(
    request: Request,
    db: Session = Depends(get_db),
    req: TaskResultRequest = Body()
) -> dict:
    '''
    获取指定任务结果
    '''
    result = handler_task_get_tasks_results(
        request=request,
        db=db,
        id=req.id
    )

    return result


@router.post('/cancel', summary='取消任务', description='取消任务')
def cancelTasks(
    request: Request,
    db: Session = Depends(get_db),
    req: TaskCancelTasksRequest = Body()
) -> dict:
    '''
    取消任务
    '''
    result = handler_task_cancel_tasks(
        request=request,
        db=db,
        ids=req.ids
    )

    return result


@router.post('/run', summary='执行任务', description='执行任务')
def runTasks(
    request: Request,
    req: TaskRunTasksRequest = Body()
) -> dict:
    '''
    执行任务
    '''
    result = handler_task_run_tasks(
        request=request,
        name=req.name,
        session_id=req.session_id,
        message=req.message,
        priority=req.priority,
        coordinator=req.coordinator
    )
    
    return result


@router.post('/messages', summary='获取指定任务，指定数字员工消息', description='获取指定任务，指定数字员工消息')
def getTasksMessages(
    request: Request,
    db: Session = Depends(get_db),
    req: TaskMessagesItemsRequest = Body()
) -> dict:
    '''
    获取指定任务，指定数字员工/协调器消息
    '''
    result = handler_task_get_tasks_robots_messages_items(
        request=request,
        db=db,
        id=req.id,
        name=req.name,
        page=req.page,
        size=req.size,
        roles=req.roles,
        content=req.content,
        coordinator=req.coordinator
    )
    
    return result



@router.post('/update/priority', summary='更新任务优先级', description='更新任务优先级')
def updateTasksPriority(
    request: Request,
    db: Session = Depends(get_db),
    req: TaskUpdateTasksPriorityRequest = Body()
) -> dict:
    '''
    更新任务优先级
    '''
    result = handler_task_update_tasks_priority(
        request=request,
        db=db,
        id=req.id,
        priority=req.priority
    )
    
    return result


@router.post('/items', summary='获取全部或指定会话任务列表', description='获取全部或指定会话任务列表')
def getTasksItems(
    request: Request,
    db: Session = Depends(get_db),
    req: TaskItemsRequest = Body(default_factory=TaskItemsRequest)
) -> dict:
    '''
    获取全部或指定会话任务列表
    '''
    result = handler_task_get_tasks_items(
        request=request,
        db=db,
        page=req.page,
        size=req.size,
        message=req.message,
        project_id=req.project_id,
        types=req.types,
        priorities=req.priorities,
        statuses=req.statuses,
        robots=req.robots,
        triggers=req.triggers,
        start_created_time=req.start_created_time,
        end_created_time=req.end_created_time,
        start_updated_time=req.start_updated_time,
        end_updated_time=req.end_updated_time,
        order_by=req.order_by,
        order_type=req.order_type
    )
    
    return result


@router.post('/paste/upload', summary='上传粘贴图片', description='上传粘贴图片')
def uploadPasteImage(
    request: Request,
    uf: UploadFile = File(..., description='待上传的文件'),
    session_id: str = Form(..., description='会话ID'),
) -> dict:
    '''
    上传粘贴图片
    '''
    result = handler_task_upload_paste_image(
        request=request, 
        uf=uf,
        session_id=session_id
    )

    if result['code'] != 20000:
        return JSONResponse(content=result, status_code=400)
    else:
        return result


@router.get('/paste', summary='获取粘贴图片', description='获取粘贴图片')
def getPasteImage(
    request: Request,
    req: TaskGetPasteImageRequest = Query()
) -> dict:
    '''
    获取粘贴图片
    '''
    result = handler_task_get_paste_image(
        request=request,
        session_id=req.session_id,
        file_name=req.file_name
    )
    
    return result