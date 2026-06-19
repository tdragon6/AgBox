'''
技能管理 API
'''


from fastapi import APIRouter, Body, File, Form, Query, Request, UploadFile
from fastapi.responses import JSONResponse
from handler.skills import (
    handler_create_skills_category,
    handler_delete_skills,
    handler_delete_skills_category,
    handler_get_skills_category_items,
    handler_get_skills_items,
    handler_get_skillsmp_items,
    handler_import_skills,
    handler_install_skills_from_skillsmp,
    handler_rename_skills_category,
)
from schemas.skills import (
    SkillsCategoryCreateRequest,
    SkillsCategoryDeleteRequest,
    SkillsCategoryItemsRequest,
    SkillsCategoryRenameRequest,
    SkillsDeleteRequest,
    SkillsItemsRequest,
    SkillsmpInstallRequest,
    SkillsmpItemsRequest,
)

router = APIRouter()


@router.post('/import', summary='导入技能', description='导入技能')
def importSkills(
    request: Request,
    uf: UploadFile = File(..., description='待上传的技能压缩包文件'),
    category: str = Form(None, description='技能分类')
):
    '''
    导入技能
    '''
    result = handler_import_skills(
        request=request,
        uf=uf,
        category=category
    )

    if result['code'] != 20000:
        return JSONResponse(content=result, status_code=400)
    else:
        return result


@router.post('/category/items', summary='获取技能分类', description='获取技能分类')
def getSkillsCategoryItems(
    request: Request,
    req: SkillsCategoryItemsRequest = Body(default_factory=SkillsCategoryItemsRequest)
):
    '''
    获取技能分类
    '''
    result = handler_get_skills_category_items(
        request=request,
        robot=req.robot
    )

    return result


@router.post('/category/delete', summary='删除技能分类', description='删除技能分类')
def deleteSkillsCategory(
    request: Request,
    req: SkillsCategoryDeleteRequest = Body()
):
    '''
    删除技能分类
    '''
    result = handler_delete_skills_category(
        request=request,
        category=req.category,
        robot=req.robot
    )

    return result


@router.post('/category/create', summary='创建技能分类', description='创建技能分类')
def createSkillsCategory(
    request: Request,
    req: SkillsCategoryCreateRequest = Body()
):
    '''
    创建技能分类
    '''
    result = handler_create_skills_category(
        request=request,
        category=req.category,
        robot=req.robot
    )

    return result


@router.post('/category/rename', summary='重命名技能分类', description='重命名技能分类')
def renameSkillsCategory(
    request: Request,
    req: SkillsCategoryRenameRequest = Body()
):
    '''
    重命名技能分类
    '''
    result = handler_rename_skills_category(
        request=request,
        old_category=req.old_category,
        new_category=req.new_category,
        robot=req.robot
    )

    return result


@router.post('/items', summary='获取技能列表', description='获取技能列表')
def getSkillsItems(
    request: Request,
    req: SkillsItemsRequest = Body(default_factory=SkillsItemsRequest)
):
    '''
    获取技能列表
    '''
    result = handler_get_skills_items(
        request=request,
        page=req.page,
        size=req.size,
        name=req.name,
        description=req.description,
        category=req.category,
        is_script=req.is_script,
        order_by=req.order_by,
        order_type=req.order_type,
        robot=req.robot
    )
    
    return result


@router.post('/delete', summary='删除技能', description='删除技能')
def deleteSkills(
    request: Request,
    req: SkillsDeleteRequest = Body()
):
    '''
    删除技能
    '''
    result = handler_delete_skills(
        request=request,
        names=req.names,
        robot=req.robot
    )
    
    return result


@router.post('/skillsmp/items', summary='获取 skillsmp 技能列表', description='获取 skillsmp 技能列表')
def getSkillsmpItems(
    request: Request,
    req: SkillsmpItemsRequest = Body(default_factory=SkillsmpItemsRequest)
):
    '''
    获取 skillsmp 技能列表
    '''
    result = handler_get_skillsmp_items(
        request=request,
        q=req.q,
        page=req.page,
        limit=req.limit,
        sortBy=req.sortBy,
        category=req.category,
        occupation=req.occupation
    )
    
    return result


@router.post('/skillsmp/install', summary='从 skillsmp 安装技能', description='从 skillsmp 安装技能')
def installSkillsFromSkillsmp(
    request: Request,
    req: SkillsmpInstallRequest = Body()
):
    '''
    从 skillsmp 安装技能
    '''
    result = handler_install_skills_from_skillsmp(
        request=request,
        url=req.url,
        category=req.category
    )
    
    return result