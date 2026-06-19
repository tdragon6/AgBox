'''
文件管理 API
'''


from fastapi import APIRouter, File, Body, Form, Query, Request, UploadFile
from fastapi.responses import JSONResponse
from core.security import args_security_check_config
from handler.files import (
    handler_files_get_dir_tree,
    handler_files_read_file,
    handler_files_save_file,
    handler_files_create_file,
    handler_files_delete_file,
    handler_files_rename_file,
    handler_files_download_dir,
    handler_files_download_file,
    handler_files_upload_file,
)
from schemas.files import (
    FilesDirTreeRequest,
    FilesFileReadRequest,
    FilesFileSaveRequest,
    FilesFileCreateRequest,
    FilesFileDeleteRequest,
    FilesFileRenameRequest,
    FilesDirDownloadRequest,
    FilesFileDownloadRequest,
)

router = APIRouter()


@router.post('/tree', summary='获取目录树', description='获取目录树')
def getDirTree(
    request: Request,
    req: FilesDirTreeRequest = Body()
):
    '''
    获取目录树
    '''
    result = handler_files_get_dir_tree(
        request=request,
        name=req.name,
        scope=req.scope,
        robot=req.robot
    )
    
    return result


@router.post('/read', summary='获取文件内容', description='获取文件内容')
def fileRead(
    request: Request,
    req: FilesFileReadRequest = Body()
):
    '''
    读取文件内容
    '''
    result = handler_files_read_file(
        request=request,
        name=req.name,
        scope=req.scope,
        file_path=req.file_path,
        robot=req.robot
    )
    
    return result


@router.post('/save', summary='保存文件内容', description='保存文件内容')
def fileSave(
    request: Request,
    req: FilesFileSaveRequest = Body()
):
    '''
    保存文件内容
    '''
    result = handler_files_save_file(
        request=request,
        name=req.name,
        scope=req.scope,
        file_path=req.file_path,
        content=req.content,
        robot=req.robot
    )
    
    return result


@router.post('/delete', summary='删除文件/目录', description='删除文件/目录')
def fileDelete(
    request: Request,
    req: FilesFileDeleteRequest = Body()
):
    '''
    删除文件/目录
    '''
    result = handler_files_delete_file(
        request=request,
        name=req.name,
        scope=req.scope,
        file_path=req.file_path,
        robot=req.robot
    )
    
    return result


@router.post('/create', summary='创建文件/目录', description='创建文件/目录')
def fileCreate(
    request: Request,
    req: FilesFileCreateRequest = Body()
):
    '''
    创建文件/目录
    '''
    result = handler_files_create_file(
        request=request,
        name=req.name,
        scope=req.scope,
        file_path=req.file_path,
        type=req.type,
        robot=req.robot
    )
    
    return result


@router.post('/rename', summary='重命名文件/目录', description='重命名文件/目录')
def fileRename(
    request: Request,
    req: FilesFileRenameRequest = Body()
):
    '''
    重命名文件/目录
    '''
    result = handler_files_rename_file(
        request=request,
        name=req.name,
        scope=req.scope,
        file_path=req.file_path,
        rename_file_path=req.rename_file_path,
        robot=req.robot
    )
    
    return result


@router.get('/dir/download', summary='下载目录', description='下载目录')
def downloadFiles(
    request: Request,
    req: FilesDirDownloadRequest = Query()
):
    '''
    下载目录
    '''
    result = handler_files_download_dir(
        request=request,
        name=req.name,
        scope=req.scope,
        robot=req.robot
    )
    
    return result


@router.get('/file/download', summary='下载文件', description='下载文件')
def downloadFile(
    request: Request,
    req: FilesFileDownloadRequest = Query()
):
    '''
    下载文件
    '''
    result = handler_files_download_file(
        request=request,
        name=req.name,
        scope=req.scope,
        file_path=req.file_path,
        robot=req.robot
    )
    
    return result


@router.post('/file/upload', summary='上传文件', description='上传文件')
def uploadFile(
    request: Request,
    uf: UploadFile = File(..., description='待上传的文件'),
    name: str = Form(..., description='目录名称'),
    scope: args_security_check_config['scope'] = Form(..., description='目录作用域'),     # type: ignore[reportUndefinedVariable]
    file_path: str = Form(..., description='文件路径'),
    robot: str = Form(None, description='数字员工')
):
    '''
    上传文件
    '''
    result = handler_files_upload_file(
        request=request,
        uf=uf,
        name=name,
        scope=scope,
        file_path=file_path,
        robot=robot
    )
    
    if result['code'] != 20000:
        return JSONResponse(content=result, status_code=400)
    else:
        return result