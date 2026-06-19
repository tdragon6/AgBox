'''
收件箱 API
'''


from fastapi import APIRouter, Body, Request
from handler.auth import handler_login, handler_logout
from schemas.auth import LoginRequest

router = APIRouter()


@router.post('/login', summary='登录', description='登录')
def login(
    request: Request,
    req: LoginRequest = Body()
) -> dict:
    '''
    登录
    '''
    result = handler_login(
        request=request,
        username=req.username,
        password=req.password
    )

    return result


@router.post('/logout', summary='注销', description='注销')
def logout(
    request: Request
) -> dict:
    '''
    注销
    '''
    result = handler_logout(
        request=request
    )

    return result