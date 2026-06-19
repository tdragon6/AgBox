'''
数字员工管理 API
'''


from core.database import get_db
from fastapi import APIRouter, Body, Depends, File, Form, Query, Request, UploadFile
from fastapi.responses import JSONResponse
from handler.robots.manage import (
    handler_manage_clone_from_robots,
    handler_manage_create_robots,
    handler_manage_delete_robots,
    handler_manage_download_robots,
    handler_manage_get_robots_avatar,
    handler_manage_get_robots_config,
    handler_manage_get_robots_env_config,
    handler_manage_get_robots_items,
    handler_manage_get_robots_memory,
    handler_manage_get_robots_model_config,
    handler_manage_get_robots_rule,
    handler_manage_import_robots,
    handler_manage_robots_skills_import,
    handler_manage_save_robots_config,
    handler_manage_save_robots_env_config,
    handler_manage_save_robots_memory,
    handler_manage_save_robots_model_config,
    handler_manage_save_robots_rule,
    handler_manage_update_robots,
    handler_manage_upload_robots_avatar,
)
from schemas.robots.manage import (
    ManageRobotsAvatarRequest,
    ManageRobotsCloneRequest,
    ManageRobotsConfigReadRequest,
    ManageRobotsConfigSaveRequest,
    ManageRobotsCreateRequest,
    ManageRobotsDeleteRequest,
    ManageRobotsDownloadRequest,
    ManageRobotsEnvReadRequest,
    ManageRobotsEnvSaveRequest,
    ManageRobotsItemsRequest,
    ManageRobotsMemoryReadRequest,
    ManageRobotsMemorySaveRequest,
    ManageRobotsModelConfigRequest,
    ManageRobotsModelConfigSaveRequest,
    ManageRobotsRuleReadRequest,
    ManageRobotsRuleSaveRequest,
    ManageRobotsSkillsImportRequest,
    ManageRobotsUpdateRequest,
)
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/rule/read', summary='获取数字员工规则', description='获取数字员工规则')
def getRobotsRule(
    request: Request,
    req: ManageRobotsRuleReadRequest = Body()
):
    '''
    获取数字员工规则
    '''
    result = handler_manage_get_robots_rule(
        request=request,
        name=req.name
    )

    return result


@router.post('/rule/save', summary='保存数字员工规则', description='保存数字员工规则')
def saveRobotsRule(
    request: Request,
    req: ManageRobotsRuleSaveRequest = Body()
):
    '''
    保存数字员工规则
    '''
    result = handler_manage_save_robots_rule(
        request=request,
        name=req.name,
        content=req.content
    )

    return result


@router.post('/memory/read', summary='获取数字员工记忆', description='获取数字员工记忆')
def getRobotsMemory(
    request: Request,
    req: ManageRobotsMemoryReadRequest = Body()
):
    '''
    获取数字员工记忆
    '''
    result = handler_manage_get_robots_memory(
        request=request,
        name=req.name
    )

    return result


@router.post('/memory/save', summary='保存数字员工记忆', description='保存数字员工记忆')
def saveRobotsMemory(
    request: Request,
    req: ManageRobotsMemorySaveRequest = Body()
):
    '''
    保存数字员工记忆
    '''
    result = handler_manage_save_robots_memory(
        request=request,
        name=req.name,
        content=req.content
    )

    return result


@router.post('/config/read', summary='获取数字员工配置', description='获取数字员工配置')
def getRobotsConfig(
    request: Request,
    req: ManageRobotsConfigReadRequest = Body()
):
    '''
    获取数字员工配置
    '''
    result = handler_manage_get_robots_config(
        request=request,
        name=req.name
    )

    return result


@router.post('/config/save', summary='保存数字员工配置', description='保存数字员工配置')
def saveRobotsConfig(
    request: Request,
    req: ManageRobotsConfigSaveRequest = Body()
):
    '''
    保存数字员工配置
    '''
    result = handler_manage_save_robots_config(
        request=request,
        name=req.name,
        content=req.content
    )

    return result


@router.post('/env/read', summary='获取数字员工环境配置', description='获取数字员工环境配置')
def getRobotsEnv(
    request: Request,
    req: ManageRobotsEnvReadRequest = Body()
):
    '''
    获取数字员工环境配置
    '''
    result = handler_manage_get_robots_env_config(
        request=request,
        name=req.name
    )

    return result


@router.post('/env/save', summary='保存数字员工环境配置', description='保存数字员工环境配置')
def saveRobotsEnv(
    request: Request,
    req: ManageRobotsEnvSaveRequest = Body()
):
    '''
    保存数字员工环境配置
    '''
    result = handler_manage_save_robots_env_config(
        request=request,
        name=req.name,
        content=req.content
    )

    return result


@router.post('/skills/import', summary='导入数字员工技能', description='导入数字员工技能')
def importRobotsSkills(
    request: Request,
    req: ManageRobotsSkillsImportRequest = Body()
):
    '''
    导入数字员工技能
    '''
    result = handler_manage_robots_skills_import(
        request=request,
        name=req.name,
        skills_list=req.skills_list,
        category=req.category
    )

    return result


@router.post('/items', summary='获取数字员工列表', description='获取数字员工列表')
def getRobotsItems(
    request: Request,
    req: ManageRobotsItemsRequest = Body(default_factory=ManageRobotsItemsRequest)
):
    '''
    获取数字员工列表
    '''
    result = handler_manage_get_robots_items(
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


@router.post('/create', summary='创建数字员工', description='创建数字员工')
def createRobots(
    request: Request,
    db: Session = Depends(get_db),
    req: ManageRobotsCreateRequest = Body()
):
    '''
    创建数字员工
    '''
    result = handler_manage_create_robots(
        request=request,
        db=db,
        name=req.name,
        description=req.description,
        department=req.department,
        reasoning_effort=req.reasoning_effort,
        max_turns=req.max_turns,
        model_config_id=req.model_config_id
    )

    return result


@router.post('/update', summary='更新数字员工', description='更新数字员工')
def updateRobots(
    request: Request,
    db: Session = Depends(get_db),
    req: ManageRobotsUpdateRequest = Body()
):
    '''
    更新数字员工
    '''
    result = handler_manage_update_robots(
        request=request,
        db=db,
        name=req.name,
        rename=req.rename,
        description=req.description,
        department=req.department,
        reasoning_effort=req.reasoning_effort,
        max_turns=req.max_turns,
        model_config_id=req.model_config_id
    )

    return result


@router.post('/delete', summary='删除数字员工', description='删除数字员工')
def deleteRobots(
    request: Request,
    db: Session = Depends(get_db),
    req: ManageRobotsDeleteRequest = Body()
):
    '''
    删除数字员工
    '''
    result = handler_manage_delete_robots(
        request=request,
        db=db,
        names=req.names
    )

    return result


@router.post('/import', summary='导入数字员工', description='导入数字员工')
def importRobots(
    request: Request,
    db: Session = Depends(get_db),
    uf: UploadFile = File(..., description='待上传的数字员工压缩包文件'),
    model_config_id: str = Form(..., description='模型配置ID')
):
    '''
    导入数字员工
    '''
    result = handler_manage_import_robots(
        request=request,
        db=db,
        uf=uf,
        model_config_id=model_config_id
    )

    if result['code'] != 20000:
        return JSONResponse(content=result, status_code=400)
    else:
        return result


@router.post('/clone', summary='克隆数字员工', description='克隆数字员工')
def cloneRobots(
    request: Request,
    req: ManageRobotsCloneRequest = Body()
):
    '''
    克隆数字员工
    '''
    result = handler_manage_clone_from_robots(
        request=request,
        name=req.name,
        clone_name=req.clone_name
    )

    return result


@router.get('/download', summary='下载数字员工', description='下载数字员工')
def downloadRobots(
    request: Request,
    req: ManageRobotsDownloadRequest = Query()
):
    '''
    下载数字员工
    '''
    result = handler_manage_download_robots(
        request=request,
        name=req.name
    )
    
    return result


@router.post('/model/config', summary='获取数字员工/协调器模型配置', description='获取数字员工/协调器模型配置')
def importRobotsModelConfig(
    request: Request,
    req: ManageRobotsModelConfigRequest = Body()
):
    '''
    获取数字员工/协调器模型配置
    '''
    result = handler_manage_get_robots_model_config(
        request=request,
        name=req.name,
        coordinator=req.coordinator
    )
    
    return result


@router.post('/model/config/save', summary='保存数字员工/协调器模型配置', description='保存数字员工/协调器模型配置')
def saveRobotsModelConfig(
    request: Request,
    db: Session = Depends(get_db),
    req: ManageRobotsModelConfigSaveRequest = Body()
):
    '''
    保存数字员工/协调器模型配置
    '''
    result = handler_manage_save_robots_model_config(
        request=request,
        db=db,
        name=req.name,
        model_config_id=req.model_config_id,
        coordinator=req.coordinator
    )
    
    return result


@router.post('/avatar/upload', summary='上传数字员工头像', description='上传数字员工头像')
def uploadRobotsAvatar(
    request: Request,
    uf: UploadFile = File(..., description='待上传的数字员工头像文件'),
    name: str = Form(..., description='数字员工名称')
):
    '''
    上传数字员工头像
    '''
    result = handler_manage_upload_robots_avatar(
        request=request,
        uf=uf,
        name=name
    )

    if result['code'] != 20000:
        return JSONResponse(content=result, status_code=400)
    else:
        return result


@router.get('/avatar', summary='获取数字员工头像', description='获取数字员工头像')
def getRobotsAvatar(
    request: Request,
    req: ManageRobotsAvatarRequest = Query()
):
    '''
    获取数字员工头像
    '''
    result = handler_manage_get_robots_avatar(
        request=request,
        name=req.name
    )
    
    return result