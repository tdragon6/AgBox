'''
装饰器和包装器
'''


import inspect
import traceback
from pathlib import Path
from typing import Any, Callable

from core.config import settings
from core.logger import log_format, logger


def _handler(
    func: Callable
) -> tuple[bool, str, Any]:
    '''
    统一 handler 入口装饰器
    '''
    def wrapper(*args, **kwargs):
        # 获取语言
        request = kwargs.get('request')
        accept_language = request.headers.get('Accept-Language', settings.LANG)
        lang = accept_language.split(',')[0].split(';')[0]

        # 处理日志中的文件路径
        file_ads_path = Path(inspect.getsourcefile(func))
        file_path = file_ads_path.relative_to(settings.STORE_DIR.parent)
        _, start_line = inspect.getsourcelines(func)

        try:
            # 执行业务函数
            status, msg, data = func(*args, **kwargs)

            if request.url.path not in [
                '/api/v1/auth/login',
                '/api/v1/inbox/robots/count/unread'
            ]:
                logger.info(f'{file_path.parent}:{file_path.name}:{start_line} - {func.__name__} - {log_format(data)}')

            if status:
                return {
                    'code': 20000,
                    'status': 'ok',
                    'msg': settings.TRANSLATIONS.get(lang, {}).get(msg, msg),
                    'data': data
                }
            else:
                return {
                    'code': 50000,
                    'status': 'fail',
                    'msg': settings.TRANSLATIONS.get(lang, {}).get(msg, msg),
                    'data': data
                }
        except:
            logger.error(f'{file_path.parent}:{file_path.name}:{start_line} - {func.__name__} - {traceback.format_exc()}')

            msg = 'failed'
            data = None

            return {
                'code': 50000,
                'status': 'fail',
                'msg': settings.TRANSLATIONS.get(lang, {}).get(msg, msg),
                'data': data
            }
        
    return wrapper