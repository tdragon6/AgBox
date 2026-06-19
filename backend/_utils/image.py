'''
图片工具
'''


import shutil
import traceback
from pathlib import Path

import requests
from _utils.file import get_bytes_type
from core.config import settings
from core.logger import logger
from fastapi import UploadFile


ALLOWED_AVATAR_MIME_TYPES = ['image/png']
ALLOWED_AVATAR_EXTS = ['png']


def check_avatar_valid(
    uf: UploadFile
) -> tuple[bool, str, str | None]:
    '''
    校验头像MIME类型 + 文件后缀 + 魔数
    '''
    filename = uf.filename or ''
    ext = filename.split('.')[-1].lower()
    if ext not in ALLOWED_AVATAR_EXTS:
        return False, 'ext_not_valid', None

    uf.file.seek(0)
    header = uf.file.read(2048)
    uf.file.seek(0)

    data = get_bytes_type(header)[-1]
    if data['mime_type'] not in ALLOWED_AVATAR_MIME_TYPES:
        return False, 'mime_type_not_valid', None
    if data['ext'] != ext:
        return False, 'ext_not_valid', None

    return True, 'success', ext


def download_dicebear_image(
    path: Path
) -> tuple[bool, str, dict]:
    '''
    下载 DiceBear 图片
    '''
    url = f'https://api.dicebear.com/9.x/avataaars/png?radius=30&seed={path.parent.name}'

    try:
        with requests.get(url, stream=True) as response:
            with path.open('wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
    except:
        logger.error(traceback.format_exc())
        shutil.copy2(settings.STORE_DIR / 'tdragon6.png', path)
    
    return True, 'success', {'path': path}
