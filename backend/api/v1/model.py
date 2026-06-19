'''
模型管理 API
'''


from core.database import get_db
from fastapi import APIRouter, Body, Depends, Request
from handler.model import (
    handler_create_model_config,
    handler_delete_models_config,
    handler_get_model_config_detail,
    handler_get_model_provider_base_url,
    handler_get_model_provider_list,
    handler_get_model_providers_list,
    handler_get_models_config_items,
    handler_update_model_config,
)
from schemas.model import (
    ModelCreateRequest,
    ModelDeleteRequest,
    ModelDetailRequest,
    ModelItemsRequest,
    ModelListRequest,
    ModelProviderBaseUrlRequest,
    ModelUpdateRequest,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/provider', summary='获取模型提供商列表', description='获取模型提供商列表')
def getModelProviderList(
    request: Request
):
    '''
    获取模型提供商列表
    '''
    result = handler_get_model_providers_list(
        request=request
    )

    return result


@router.post('/base_url', summary='获取模型提供商 base url', description='获取模型提供商 base url')
def getModelProviderBaseUrl(
    request: Request,
    req: ModelProviderBaseUrlRequest = Body()
):
    '''
    获取模型提供商 base url
    '''
    result = handler_get_model_provider_base_url(
        request=request,
        id=req.id
    )

    return result


@router.post('/list', summary='获取可用模型列表', description='获取可用模型列表')
def getModelProviderList(
    request: Request,
    req: ModelListRequest = Body()
):
    '''
    获取可用模型列表
    '''
    result = handler_get_model_provider_list(
        request=request,
        api_key=req.api_key,
        base_url=req.base_url
    )

    return result


@router.post('/create', summary='创建模型配置', description='创建模型配置')
def createModelConfig(
    request: Request,
    db: Session = Depends(get_db),
    req: ModelCreateRequest = Body()
):
    '''
    创建模型配置
    '''
    result = handler_create_model_config(
        request=request,
        db=db,
        name=req.name,
        provider_id=req.provider_id,
        model=req.model,
        base_url=req.base_url,
        api_key=req.api_key
    )

    return result


@router.post('/update', summary='更新模型配置', description='更新模型配置')
def updateModelConfig(
    request: Request,
    db: Session = Depends(get_db),
    req: ModelUpdateRequest = Body()
):
    '''
    更新模型配置
    '''
    result = handler_update_model_config(
        request=request,
        db=db,
        id=req.id,
        name=req.name,
        provider_id=req.provider_id,
        model=req.model,
        base_url=req.base_url,
        api_key=req.api_key
    )

    return result


@router.post('/items', summary='获取模型配置列表', description='获取模型配置列表')
def getModelConfigItems(
    request: Request,
    db: Session = Depends(get_db),
    req: ModelItemsRequest = Body(default_factory=ModelItemsRequest)
):
    '''
    获取模型配置列表
    '''
    result = handler_get_models_config_items(
        request=request,
        db=db,
        keyword=req.keyword,
        is_online=req.is_online
    )

    return result


@router.post('/detail', summary='获取模型配置详情', description='获取模型配置详情')
def getModelConfigDetail(
    request: Request,
    db: Session = Depends(get_db),
    req: ModelDetailRequest = Body()
):
    '''
    获取模型配置详情
    '''
    result = handler_get_model_config_detail(
        request=request,
        db=db,
        id=req.id
    )

    return result


@router.post('/delete', summary='删除模型配置', description='删除模型配置')
def deleteModelConfig(
    request: Request,
    db: Session = Depends(get_db),
    req: ModelDeleteRequest = Body()
):
    '''
    删除模型配置
    '''
    result = handler_delete_models_config(
        request=request,
        db=db,
        ids=req.ids
    )

    return result