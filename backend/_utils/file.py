'''
文件工具
'''

import magic
import mimetypes
import traceback
from pathlib import Path

from _utils.process import ProcessWorkerThread
from core.config import settings
from core.logger import logger
from fastapi import UploadFile


def find_file_dirs(
    path: Path,
    file_name: str
) -> tuple[bool, str, list[Path]]:
    '''
    查找目录下指定文件所在目录路径
    '''
    result = [ file.parent for file in list(path.rglob(file_name)) ]

    return True, 'success', result


def get_directory_tree(
    root_path: Path,
    sub_path: Path = None
) -> tuple[bool, str, dict]:
    '''
    获取目录树
    '''
    if sub_path is None:
        sub_path = root_path
    
    relative_path = sub_path.relative_to(root_path)

    # 适配 arco design 的 tree 组件
    node = {
        'key': relative_path,
        'title': sub_path.name,
        'isLeaf': sub_path.is_file(),
        'children': []
    }
    
    if node['isLeaf']:
        return True, 'success', node
    
    for child in sub_path.iterdir():
        _, _, child_node = get_directory_tree(root_path, child)
        node['children'].append(child_node)

    return True, 'success', node


def get_file_content(
    path: Path
) -> tuple[bool, str, str | dict | None]:
    '''
    获取文件内容
    '''
    try:
        with path.open('r', encoding='utf-8') as f:
            return True, 'success', {'file_type': 'file', 'content': f.read()}
    except:
        status, _, result = get_file_type(path)
        if not status:
            logger.error(traceback.format_exc())
            return False, 'cannot_read_file_content', None
        else:
            return True, 'success', {'file_type': result['file_type'], 'content': path}


def save_file_content(
    path: Path,
    content: str
) -> tuple[bool, str, Path]:
    '''
    保存文件内容
    '''
    try:
        with path.open('w', encoding='utf-8') as f:
            f.write(content)
            return True, 'success', path
    except:
        logger.error(traceback.format_exc())
        return False, 'cannot_save_file_content', None


def check_path_is_in_parent(
    child_path: Path,
    parent_path: Path
) -> tuple[bool, str, dict | None]:
    '''
    判断子路径是否在父路径内
    '''    
    parent = parent_path.resolve()
    child = child_path.resolve()

    if parent == child:
        return False, 'path_invalid', None
    
    if child.is_relative_to(parent):
        return True, 'success', {'child_path': child_path, 'parent_path': parent_path}
    else:
        return False, 'path_invalid', None
    

def init_git_repo(
    repo_dir: Path
) -> tuple[bool, str, dict]:
    '''
    初始化 git 仓库
    '''
    init_command = ['git', 'init']
    init_worker = ProcessWorkerThread(
        command=init_command,
        cwd=repo_dir
    )
    init_worker.start()
    init_worker.join()

    with (repo_dir / '.gitignore').open('w', encoding='utf-8') as f:
        f.write('.worktrees')

    add_command = ['git', 'add', '.']
    add_worker = ProcessWorkerThread(
        command=add_command,
        cwd=repo_dir
    )
    add_worker.start()
    add_worker.join()

    commit_command = ['git', 'commit', '-m', 'init']
    commit_worker = ProcessWorkerThread(
        command=commit_command,
        cwd=repo_dir
    )
    commit_worker.start()
    commit_worker.join()
    
    return True, 'success', {'repo_dir': repo_dir}


def judge_file_size_is_valid(
    uf: UploadFile,
    is_image: bool = False
) -> tuple[bool, str, dict | None]:
    '''
    判断文件大小是否有效
    '''
    total_size = 0

    limit_size = settings.MAX_IMAGE_SIZE if is_image else settings.MAX_FILE_SIZE
    
    while True:
        chunk = uf.file.read(1024)
        if not chunk:
            break
        
        total_size += len(chunk)
        
        if total_size > limit_size:
            return False, 'file_size_not_valid', None
    
    uf.file.seek(0)

    return True, 'success', None


def get_file_type(path: Path) -> tuple[bool, str, str | None]:
    '''
    获取文件类型
    '''
    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(path)
        file_type = mime_type.split('/')[0]
        ext = mimetypes.guess_extension(mime_type, strict=False)[1:]
        result = {'mime_type': mime_type, 'file_type': file_type, 'ext': ext}

        return True, 'success', result
    except:
        logger.error(traceback.format_exc())
        return False, 'failed', None
    

def get_bytes_type(buffer: bytes) -> tuple[bool, str, str | None]:
    '''
    获取字节流文件类型
    '''
    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(buffer)
        file_type = mime_type.split('/')[0]
        ext = mimetypes.guess_extension(mime_type, strict=False)[1:]
        result = {'mime_type': mime_type, 'file_type': file_type, 'ext': ext}

        return True, 'success', result
    except:
        logger.error(traceback.format_exc())
        return False, 'failed', None