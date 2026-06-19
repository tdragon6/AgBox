'''
系统设置 handler
'''


from core.decorator import _handler
from fastapi import Request
from services.settings import (
    get_system_settings,
    judge_system_settings_value_valid,
    set_system_settings,
)
from _utils.sysinfo import get_system_info
from core.config import settings


@_handler
def handler_get_system_settings(
    request: Request,
    name: str
):
    '''
    获取系统设置 handler
    '''    
    result = get_system_settings(
        name=name
    )

    return result


@_handler
def handler_set_system_settings(
    request: Request,
    name: str,
    value: str | bool | int | None
):
    '''
    设置系统设置 handler
    '''
    status, msg, _ = judge_system_settings_value_valid(
        name=name,
        value=value
    )
    if not status:
        return False, msg, None

    result = set_system_settings(
        name=name,
        value=value
    )

    return result


@_handler
def handler_get_system_info(
    request: Request
):
    '''
    获取系统信息 handler
    '''
    status, msg, data = get_system_info()
    data['host'] = settings.HOST
    data['port'] = settings.PORT
    data['version'] = settings.APP_VERSION
    return status, msg, data
