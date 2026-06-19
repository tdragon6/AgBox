'''
数字员工市场 handler
'''


from datetime import datetime

from core.decorator import _handler
from core.security import args_security_check_config
from fastapi import Request
from models.model import Model
from services.robots.market import get_robots_market_items, install_robots_from_market
from sqlalchemy.orm import Session


@_handler
def handler_market_get_robots_items(
    request: Request,
    page: int = 1,
    size: int = 10,
    name: str = None,
    description: str = None,
    author: str = None,
    department: str = None,
    ranks: list[args_security_check_config['rank_scope']] = None,     # type: ignore[reportUndefinedVariable]
    qualities: list[args_security_check_config['quality_scope']] = None,     # type: ignore[reportUndefinedVariable]
    start_created_time: datetime = None,
    end_created_time: datetime = None,
    start_updated_time: datetime = None,
    end_updated_time: datetime = None,
    order_by: args_security_check_config['robots_order_by'] = 'updated_time',   # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc'   # type: ignore[reportUndefinedVariable]
):
    '''
    获取数字员工市场清单 handler
    '''
    result = get_robots_market_items(
        page=page,
        size=size,
        name=name,
        description=description,
        author=author,
        department=department,
        ranks=ranks,
        qualities=qualities,
        start_created_time=start_created_time,
        end_created_time=end_created_time,
        start_updated_time=start_updated_time,
        end_updated_time=end_updated_time,
        order_by=order_by,
        order_type=order_type
    )

    return result


@_handler
def handler_market_install_robots_from_market(
    request: Request,
    db: Session,
    url: str,
    model_config_id: str
):
    '''
    从市场安装数字员工 handler
    '''
    model_record = db.get(Model, model_config_id)
    if model_config_id is not None and not model_record:
        return False, 'model_config_not_found', None
    
    result = install_robots_from_market(
        db=db,
        url=url,
        model_config_id=model_config_id
    )
    
    return result