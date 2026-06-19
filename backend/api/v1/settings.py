'''
系统设置 API
'''


from fastapi import APIRouter, Body, Request
from handler.settings import handler_get_system_settings, handler_set_system_settings, handler_get_system_info
from schemas.settings import SettingsGetRequest, SettingsSetRequest

router = APIRouter()


@router.post('/get', summary='获取系统设置', description='获取系统设置')
def getSystemSettings(
    request: Request,
    req: SettingsGetRequest = Body()
):
    '''
    获取系统设置
    '''
    result = handler_get_system_settings(
        request=request,
        name=req.name
    )

    return result


@router.post('/set', summary='设置系统设置', description='设置系统设置')
def setSystemSettings(
    request: Request,
    req: SettingsSetRequest = Body()
):
    '''
    设置系统设置
    '''
    result = handler_set_system_settings(
        request=request,
        name=req.name,
        value=req.value
    )

    return result


@router.get('/system/info', summary='获取系统信息', description='获取系统信息')
def getSystemInfo(
    request: Request
):
    '''
    获取系统信息
    '''
    result = handler_get_system_info(
        request=request
    )

    return result