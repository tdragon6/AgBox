'''
任务管理 API
'''


from api.v1.tasks.project import router as project_router
from api.v1.tasks.scheduler import router as scheduler_router
from api.v1.tasks.session import router as session_router
from api.v1.tasks.task import router as task_router
from fastapi import APIRouter

router = APIRouter()


router.include_router(session_router, prefix='/session', tags=['Tasks - Session'])
router.include_router(task_router, prefix='', tags=['Tasks - Task'])
router.include_router(project_router, prefix='/project', tags=['Tasks - Project'])
router.include_router(scheduler_router, prefix='/scheduler', tags=['Tasks - Scheduler'])
