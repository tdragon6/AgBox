'''
模型管理 业务逻辑
'''


import traceback

import shortuuid
from core.logger import logger
from fastapi.encoders import jsonable_encoder
from models.model import Model
from services.model.hermes import (
    get_model_list,
    get_model_provider_name,
    judge_provider_in_registry,
)
from sqlalchemy import delete, or_, select
from sqlalchemy.orm import Session


def auto_set_coordinator_model_config(
    db: Session,
    model_config_id: str
) -> tuple[bool, str, dict | None]:
    '''
    自动设置协调器模型配置
    '''
    from services.robots.manage import get_robots_model_config, save_robots_model_config
    
    for coordinator in ['agbox-coordinator-async', 'agbox-coordinator-sync']:
        status, _, data = get_robots_model_config(
            name=coordinator,
            coordinator=True
        )
        if status and data['is_online']:
            continue
        else:
            save_robots_model_config(
                db=db,
                name=coordinator,
                model_config_id=model_config_id,
                coordinator=True
            )

    return True, 'success', None


def create_model_config(
    db: Session,
    name: str,
    provider_id: str,
    model: str,
    base_url: str,
    api_key: str = None,
) -> tuple[bool, str, dict | None]:
    '''
    创建模型配置
    '''
    id = shortuuid.uuid()
    
    provider_name = get_model_provider_name(provider_id)[-1]
    
    model_record = Model(
        id=id,
        name=name,
        provider_id=provider_id,
        provider_name=provider_name,
        model=model,
        base_url=base_url,
        api_key=api_key
    )

    db.add(model_record)

    try:
        db.commit()
        db.refresh(model_record)

        # 每次创建模型配置后，自动设置协调器模型配置
        auto_set_coordinator_model_config(
            db=db,
            model_config_id=model_record.id
        )
        return True, 'success', {'id': model_record.id}
    except:
        logger.error(traceback.format_exc())
        db.rollback()
        return False, 'create_model_config_failed', None


def update_model_config(
    db: Session,
    id: str,
    name: str = None,
    provider_id: str = None,
    model: str = None,
    base_url: str = None,
    api_key: str = None
) -> tuple[bool, str, dict | None]:
    '''
    更新模型配置
    '''
    model_record = db.get(Model, id)
    
    if any([model, base_url, api_key]):
        _model = model or model_record.model
        _base_url = base_url or model_record.base_url
        _api_key = api_key or model_record.api_key
        
        status, msg, model_list = get_model_list(_base_url, _api_key)

        if not status:
            return False, msg, None
        if _model not in model_list:
            return False, 'model_not_in_list', None
        
    if name:
        model_record.name = name
    if provider_id:
        provider_name = get_model_provider_name(provider_id)[-1]
        model_record.provider_id = provider_id
        model_record.provider_name = provider_name
    if model:
        model_record.model = model
    if base_url:
        model_record.base_url = base_url
    if api_key:
        model_record.api_key = api_key

    try:
        db.commit()
        db.refresh(model_record)
        return True, 'success', {'id': model_record.id}
    except:
        logger.error(traceback.format_exc())
        db.rollback()
        return False, 'update_model_config_failed', None


def get_models_config_items(
    db: Session,
    keyword: str = None,
    is_online: bool = None
) -> tuple[bool, str, list[dict]]:
    '''
    根据搜索内容获取模型配置列表
    '''
    stmt = select(Model)

    if keyword:
        stmt = stmt.where(
            or_(
                Model.id.contains(keyword),
                Model.name.contains(keyword),
                Model.provider_id.contains(keyword),
                Model.provider_name.contains(keyword),
                Model.model.contains(keyword),
                Model.base_url.contains(keyword)
            )
        )

    stmt = stmt.order_by(Model.updated_time.desc())

    items = db.execute(stmt).scalars().all()

    result = jsonable_encoder(items)

    for item in result:
        item['is_online'] = judge_model_config_online(
            provider_id=item['provider_id'],
            model=item['model'],
            base_url=item['base_url'],
            api_key=item['api_key']
        )[0]
    
    if is_online is not None:
        result = [ item for item in result if item['is_online'] == is_online ]

    return True, 'success', result


def get_model_config_detail(
    db: Session,
    id: str
) -> tuple[bool, str, dict]:
    '''
    根据id获取模型配置详情
    '''
    model_record = db.get(Model, id)

    result = jsonable_encoder(model_record)
    
    result['is_online'] = judge_model_config_online(
        provider_id=result['provider_id'],
        model=result['model'],
        base_url=result['base_url'],
        api_key=result['api_key']
    )[0]

    return True, 'success', result


def delete_models_config(
    db: Session,
    ids: list[str]
) -> tuple[bool, str, dict | None]:
    '''
    删除模型配置
    '''
    if not ids:
        return True, 'success', ids
    
    or_conditions = []

    for id in ids:
        or_conditions.append(Model.id == id)
    
    stmt = delete(Model).where(
        or_(*or_conditions)
    )
    
    try:
        db.execute(stmt)
        db.commit()
        return True, 'success', {'ids': ids}
    except:
        logger.error(traceback.format_exc())
        db.rollback()
        return False, 'delete_model_config_failed', None
    

def judge_model_config_online(
    provider_id: str,
    model: str,
    base_url: str,
    api_key: str = None
) -> tuple[bool, str, None]:
    '''
    判断模型配置是否在线
    '''
    if not judge_provider_in_registry(
        id=provider_id
    ):
        return False, 'provider_not_found', None
    
    status, msg, data = get_model_list(
        base_url=base_url,
        api_key=api_key
    )
    if not status:
        return False, msg, None
    
    if model not in data:
        return False, 'model_not_in_list', None
    
    return True, 'success', None