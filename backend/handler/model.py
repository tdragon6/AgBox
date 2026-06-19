'''
模型管理 handler
'''


from _utils.func import desensitize
from core.decorator import _handler
from fastapi import Request
from models.model import Model
from services.model.hermes import (
    get_model_list,
    get_model_provider_base_url,
    get_model_providers_list,
    judge_provider_in_registry,
)
from services.model.model import (
    create_model_config,
    delete_models_config,
    get_model_config_detail,
    get_models_config_items,
    judge_model_config_online,
    update_model_config,
)
from sqlalchemy.orm import Session


@_handler
def handler_get_model_providers_list(
    request: Request
):
    '''
    获取模型提供商列表 handler
    '''
    result = get_model_providers_list()

    return result


@_handler
def handler_get_model_provider_base_url(
    request: Request,
    id: str
):
    '''
    获取模型提供商 base url handler
    '''
    if not judge_provider_in_registry(
        id=id
    ):
        return False, 'provider_not_found', None
    
    result = get_model_provider_base_url(
        id=id
    )

    return result


@_handler
def handler_get_model_provider_list(
    request: Request,
    api_key: str,
    base_url: str
):
    '''
    获取可用模型列表 handler
    '''
    result = get_model_list(
        base_url=base_url,
        api_key=api_key
    )

    return result


@_handler
def handler_create_model_config(
    request: Request,
    db: Session,
    name: str,
    provider_id: str,
    model: str,
    base_url: str,
    api_key: str = None
):
    '''
    创建模型配置 handler
    '''
    status, msg, _ = judge_model_config_online(
        provider_id=provider_id,
        model=model,
        base_url=base_url,
        api_key=api_key
    )
    if not status:
        return False, msg, None
    
    result = create_model_config(
        db=db,
        name=name,
        provider_id=provider_id,
        model=model,
        base_url=base_url,
        api_key=api_key
    )

    return result


@_handler
def handler_update_model_config(
    request: Request,
    db: Session,
    id: str,
    name: str,
    provider_id: str,
    model: str,
    base_url: str,
    api_key: str = None
):
    '''
    更新模型配置 handler
    '''
    model_record = db.get(Model, id)
    if not model_record:
        return False, 'model_config_not_found', None
    
    status, msg, _ = judge_model_config_online(
        provider_id=provider_id,
        model=model,
        base_url=base_url,
        api_key=api_key
    )
    if not status:
        return False, msg, None
    
    result = update_model_config(
        db=db,
        id=id,
        name=name,
        provider_id=provider_id,
        model=model,
        base_url=base_url,
        api_key=api_key
    )

    return result


@_handler
def handler_get_models_config_items(
    request: Request,
    db: Session,
    keyword: str = None,
    is_online: bool = None
):
    '''
    获取模型配置列表 handler
    '''
    status, msg, data = get_models_config_items(
        db=db,
        keyword=keyword,
        is_online=is_online
    )

    for item in data:
        item['api_key'] = desensitize(item['api_key'])

    return status, msg, data


@_handler
def handler_get_model_config_detail(
    request: Request,
    db: Session,
    id: str
):
    '''
    获取模型配置详情 handler
    '''
    model_record = db.get(Model, id)
    if not model_record:
        return False, 'model_config_not_found', None
    
    status, msg, data = get_model_config_detail(
        db=db,
        id=id
    )
    
    data['api_key'] = desensitize(data['api_key'])

    return status, msg, data


@_handler
def handler_delete_models_config(
    request: Request,
    db: Session,
    ids: list[str]
):
    '''
    删除模型配置 handler
    '''
    for id in ids:
        model_record = db.get(Model, id)
        if not model_record:
            return False, 'model_config_not_found', None
    
    result = delete_models_config(
        db=db,
        ids=ids
    )

    return result
