'''
数字员工 API
'''


from api.v1.robots.manage import router as robots_manage_router
from api.v1.robots.market import router as robots_market_router
from fastapi import APIRouter


router = APIRouter()


router.include_router(robots_manage_router, prefix='/manage', tags=['Robots - Manage'])
router.include_router(robots_market_router, prefix='/market', tags=['Robots - Market'])
