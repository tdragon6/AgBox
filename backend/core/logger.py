'''
日志
'''


import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent.parent / 'store' / 'logs'


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.handlers.clear()


log_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
max_size = 10 * 1024 * 1024
backup_cnt = 5


server_handler = RotatingFileHandler(
    filename=str(LOG_DIR / 'server.log'),
    maxBytes=max_size,
    backupCount=backup_cnt,
    encoding='utf-8'
)
server_handler.setLevel(logging.DEBUG)
class ServerFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.INFO
server_handler.addFilter(ServerFilter())
server_handler.setFormatter(log_format)


error_handler = RotatingFileHandler(
    filename=str(LOG_DIR / 'error.log'),
    maxBytes=max_size,
    backupCount=backup_cnt,
    encoding='utf-8'
)
error_handler.setLevel(logging.WARNING)
error_handler.setFormatter(log_format)

logger.addHandler(server_handler)
logger.addHandler(error_handler)


def log_format(obj: any) -> any:
    '''
    日志打印格式化处理
    '''
    if obj is None:
        return None

    if isinstance(obj, (list, tuple)) or (hasattr(obj, '__iter__') and not isinstance(obj, (str, dict, bytes))):
        return [log_format(item) for item in obj]

    try:
        return {c.key: log_format(getattr(obj, c.key)) for c in obj.__mapper__.columns}
    except:
        pass

    if isinstance(obj, dict):
        return {k: log_format(v) for k, v in obj.items()}

    return obj