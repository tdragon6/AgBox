'''
认证 handler
'''

from core.decorator import _handler
from core.auth import login, logout
from fastapi import Request


@_handler
def handler_login(
    request: Request,
    username: str,
    password: str
):
    '''
    登录 handler
    '''
    result = login(
        username=username,
        password=password
    )

    return result


@_handler
def handler_logout(
    request: Request
):
    '''
    注销 handler
    '''
    result = logout()

    return result