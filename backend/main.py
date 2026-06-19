'''
FastAPI 应用入口
'''


from core.config import ENV_FIELDS, settings


# 优先初始化目录
for path in [
    settings.LOGS_DIR,
    settings.ROBOTS_DIR,
    settings.WORKSPACE_DIR,
    settings.TEMP_DIR
]:
    path.mkdir(exist_ok=True)


from contextlib import asynccontextmanager

import uvicorn
from api.v1.router import router as v1_router
from core.init import (
    init_coordinator_config,
    init_db,
    init_existed_hermes_model_config,
    init_i18n,
    init_scheduler,
)
from core.auth import parse_jwt_token
from core.database import db_session
from core.scheduler import scheduler
from _utils.cert import generate_cert
from services.tasks.task import get_tasks_items, cancel_tasks
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from pathlib import Path


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    应用生命周期管理
    '''
    # 启动时初始化所有组件  
    init_i18n()
    init_coordinator_config()
    init_scheduler()
    init_db()
    init_existed_hermes_model_config()

    # 打印信息
    rprint(f'\n[green]Server Started[/green]: {settings.APP_NAME} {settings.APP_VERSION}  [light_pink1]By tdragon6[/light_pink1]\n')

    console = Console()
    table = Table(
        title='[light_salmon1]⚙️  AgBox Settings[/light_salmon1]',
        header_style='light_salmon1',
        border_style='light_salmon1',
        show_lines=True
    )
    
    table.add_column('name', style='light_salmon1', justify='left')
    table.add_column('value', style='light_salmon1', justify='left')

    for field in ENV_FIELDS:
        value = getattr(settings, field)
        table.add_row(field, str(value))
    
    console.print(table)
    
    print('')
    
    yield

    # 停止定时器
    scheduler.shutdown(wait=False)

    # 取消所有运行中或等待中的任务
    with db_session() as db:
        running_pending_tasks = get_tasks_items(
            db=db,
            page=0,
            statuses=['running', 'pending']
        )[-1]['items']

        if not running_pending_tasks:
            pass
        else:
            cancel_tasks(
                db=db,
                ids=[item['id'] for item in running_pending_tasks]
            )
    
    # 清空 PID 文件
    with (Path(__file__).parent / 'pid').open('w') as f:
        f.write('')
    
    console.print(f'[green][✓][/green] {"服务已停止" if settings.LANG == "zh-CN" else "Service stopped"}')


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)


# 注册 v1 版本 API
app.include_router(v1_router, prefix='/api/v1')

@app.get('/health')
def health():
    '''
    服务健康检查，返回基础信息
    '''
    result = {
        'status': 'UP',
        'app': settings.APP_NAME,
        'version': settings.APP_VERSION,
        'author': 'tdragon6',
        'docs': '/docs',
    }

    return result

# 前端文件目录
FRONTEND_DIST_DIR = Path(__file__).parent / 'dist'

# 挂载前端静态资源
app.mount('/', StaticFiles(directory=FRONTEND_DIST_DIR))


class SPAFallbackMiddleware(BaseHTTPMiddleware):
    '''
    前端托管中间件
    '''
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        if response.status_code == 404:
            return FileResponse(FRONTEND_DIST_DIR / 'index.html')
        
        return response

app.add_middleware(SPAFallbackMiddleware)


class AuthMiddleware(BaseHTTPMiddleware):
    '''
    认证中间件
    '''
    async def dispatch(self, request, call_next):
        if not request.url.path.startswith('/api/v1') or request.url.path == '/api/v1/auth/login':
            return await call_next(request)
    
        accept_language = request.headers.get('Accept-Language', settings.LANG)
        lang = accept_language.split(',')[0].split(';')[0]
        authorization = request.headers.get('authorization', '')
        
        if not authorization.startswith('Bearer '):
            unauthorized_msg = 'token_invalid_or_expired'
            return JSONResponse(
                status_code=200,
                content={
                    'code': 40001,
                    'status': 'fail',
                    'msg': settings.TRANSLATIONS.get(lang, {}).get(unauthorized_msg, unauthorized_msg),
                    'data': None
                }
            )
        
        token = authorization.split(' ')[1]
        status, msg, data = parse_jwt_token(token)
        if not status:
            return JSONResponse(
                status_code=200,
                content={
                    'code': 40001,
                    'status': 'fail',
                    'msg': settings.TRANSLATIONS.get(lang, {}).get(msg, msg),
                    'data': data
                }
            )

        return await call_next(request)


# 认证中间件
app.add_middleware(AuthMiddleware)


# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['Content-Disposition']
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    accept_language = request.headers.get('Accept-Language', settings.LANG)
    lang = accept_language.split(',')[0].split(';')[0]
    return JSONResponse(
        status_code=422,
        content={
            'code': 50000,
            'status': 'fail',
            'msg': settings.TRANSLATIONS.get(lang, {}).get(exc.errors()[0].get('msg'), exc.errors()[0].get('msg')),
            'data': None
        }
    )


if __name__ == '__main__':
    # 生成 https 证书
    generate_cert()

    uvicorn.run(
        app='main:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        ssl_keyfile=Path(__file__).parent / 'key.pem',
        ssl_certfile=Path(__file__).parent / 'cert.pem',
        timeout_graceful_shutdown=0
    )