'''
v1 版本 API
'''


from api.v1.auth import router as auth_router
from api.v1.inbox import router as inbox_router
from api.v1.model import router as model_router
from api.v1.robots.router import router as robots_router
from api.v1.settings import router as settings_router
from api.v1.skills import router as skills_router
from api.v1.tasks.router import router as tasks_router
from api.v1.files import router as files_router


from fastapi import APIRouter

router = APIRouter()


router.include_router(auth_router, prefix='/auth', tags=['Auth'])
router.include_router(inbox_router, prefix='/inbox', tags=['Inbox'])
router.include_router(robots_router, prefix='/robots')
router.include_router(tasks_router, prefix='/tasks')
router.include_router(model_router, prefix='/model', tags=['Model'])
router.include_router(skills_router, prefix='/skills', tags=['Skills'])
router.include_router(files_router, prefix='/files', tags=['Files'])
router.include_router(settings_router, prefix='/settings', tags=['Settings'])
