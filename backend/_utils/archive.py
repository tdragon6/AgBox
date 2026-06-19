'''
压缩包工具
'''


import shutil
import traceback
import zipfile
from io import BytesIO
from pathlib import Path

import shortuuid
from core.config import settings
from core.logger import logger
from fastapi import UploadFile


ALLOWED_ARCHIVE_MIME_TYPES = ['application/zip']
ALLOWED_ARCHIVE_EXTS = ['zip']
MAGIC_ZIP = b'PK\x03\x04'


def check_archive_valid(
    uf: UploadFile
) -> tuple[bool, str, str | None]:
    '''
    校验压缩包文件MIME类型 + 校验压缩包文件后缀 + 魔数
    '''
    # magic 识别 zip 字节流有 bug，这里手动校验魔数
    # windows 前端不自动加请求头，为兼容，注释掉校验 MIME 类型代码
    # content_type = uf.content_type or ''
    # if content_type not in ALLOWED_ARCHIVE_MIME_TYPES:
    #     return False, 'mime_type_not_valid', None
        
    filename = uf.filename or ''
    ext = filename.split('.')[-1].lower()
    if ext not in ALLOWED_ARCHIVE_EXTS:
        return False, 'ext_not_valid', None

    uf.file.seek(0)
    header = uf.file.read(10)
    uf.file.seek(0)

    if ext == 'zip' and not header.startswith(MAGIC_ZIP):
        return False, 'zip_not_valid', None

    return True, 'success', ext


def extract_archive(
    uf: UploadFile,
) -> tuple[bool, str, Path | None]:
    '''
    压缩包解压
    '''
    dest = settings.TEMP_DIR / shortuuid.uuid()
    
    ext = uf.filename.split('.')[-1].lower()

    # python 3.11.15 以上版本 extractall 函数考虑了路径遍历等安全问题
    if ext == 'zip':
        try:
            with zipfile.ZipFile(uf.file, 'r') as zf:
                zf.extractall(dest)
            return True, 'success', dest
        except:
            logger.error(traceback.format_exc())
            if dest.exists():
                shutil.rmtree(dest)
            return False, 'zip_extract_error', None       
    

def zip_dir(
    dir: Path,
    white_parent_dir: list[Path] = None
) -> BytesIO:
    '''
    zip 压缩目录到内存字节流
    '''
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for file_path in dir.rglob('*'):
            if file_path.is_file() and \
            (
                white_parent_dir is None or \
                any([file_path.is_relative_to(white_path) for white_path in white_parent_dir])
            ):
                archive_path = file_path.relative_to(dir)
                zf.write(file_path, archive_path)

    zip_buffer.seek(0)
    return zip_buffer