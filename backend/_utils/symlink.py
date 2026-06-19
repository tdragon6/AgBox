'''
软链接工具（考虑兼容进化，后续设计skills、plugin等为单独副本模式，此模块未使用）
'''


from pathlib import Path


def create_symlink(
    src: Path,
    link: Path
) -> tuple[bool, str, Path | None]:
    '''
    创建软链接
    '''
    if not src.exists():
        return False, 'path_not_found', None
    
    src = src.resolve()

    if link.exists() and link.is_symlink():
        link.unlink()
    
    link = link.resolve()
    
    link.symlink_to(src, target_is_directory=src.is_dir())
    return True, 'success', link


def list_symlinks(
    dir: Path
) -> list[Path]:
    '''
    列出指定目录下所有软链接
    '''
    if not dir.exists():
        return False, 'path_not_found', None
    
    symlinks = [ path for path in dir.iterdir() if path.is_symlink() ]
    
    return True, 'success', symlinks


def delete_symlink(
    link: Path
) -> tuple[bool, str, Path | None]:
    '''
    删除软链接
    '''
    if not link.exists():
        return False, 'path_not_found', None

    if not link.is_symlink():
        return False, 'is_not_symlink', None
    
    link.unlink()
    
    return True, 'success', link
    