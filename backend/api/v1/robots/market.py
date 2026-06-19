'''
数字员工市场 API
'''


from core.database import get_db
from fastapi import APIRouter, Body, Depends, Request
from handler.robots.market import handler_market_get_robots_items, handler_market_install_robots_from_market
from schemas.robots.market import MarketRobotsItemsRequest, MarketRobotsInstallRequest
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/items', summary='获取数字员工市场清单', description='获取数字员工市场清单')
def getRobotsMarketItems(
    request: Request,
    req: MarketRobotsItemsRequest = Body(default_factory=MarketRobotsItemsRequest)
):
    '''
    获取数字员工市场清单
    '''
    result = handler_market_get_robots_items(
        request=request,
        page=req.page,
        size=req.size,
        name=req.name,
        description=req.description,
        author=req.author,
        department=req.department,
        ranks=req.ranks,
        qualities=req.qualities,
        start_created_time=req.start_created_time,
        end_created_time=req.end_created_time,
        start_updated_time=req.start_updated_time,
        end_updated_time=req.end_updated_time,
        order_by=req.order_by,
        order_type=req.order_type
    )

    return result


@router.post('/install', summary='从市场安装数字员工', description='从市场安装数字员工')
def installSkillsFromSkillsmp(
    request: Request,
    db: Session = Depends(get_db),
    req: MarketRobotsInstallRequest = Body()
):
    '''
    从市场安装数字员工
    '''
    result = handler_market_install_robots_from_market(
        request=request,
        db=db,
        url=req.url,
        model_config_id=req.model_config_id
    )
    
    return result