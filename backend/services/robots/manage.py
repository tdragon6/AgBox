'''
数字员工管理 业务逻辑
'''


import json
import shutil
import traceback
from datetime import datetime
from pathlib import Path

import yaml
from _utils.archive import zip_dir
from _utils.file import find_file_dirs, get_file_content, save_file_content
from _utils.image import download_dicebear_image
from _utils.process import ProcessWorkerThread
from core.config import settings
from core.logger import logger
from core.security import args_security_check_config
from dotenv import dotenv_values
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from services.model.hermes import get_model_provider_api_key_env_vars
from services.model.model import get_model_config_detail, judge_model_config_online
from services.skills import get_skills_path
from services.inbox import get_inbox_items, delete_inbox_record
from models.task import Task
from sqlalchemy.orm import Session


def get_robots_info(
    path: Path
) -> tuple[bool, str, dict | None]:
    '''
    获取数字员工信息
    '''
    robot_info = {'path': path}

    with (path / 'robot.json').open('r', encoding='utf-8') as f:
        try:
            robot_info.update(json.loads(f.read()))
            robot_info['created_time'] = datetime.strptime(robot_info['created_time'], '%Y-%m-%d %H:%M:%S')
            robot_info['updated_time'] = datetime.strptime(robot_info['updated_time'], '%Y-%m-%d %H:%M:%S')
        except:
            logger.error(traceback.format_exc())
            return False, 'robots_format_error', None
    
    if not all(
        [
            robot_info.get('name'),
            robot_info.get('description'),
            robot_info.get('department'),
            robot_info.get('rank'),
            robot_info.get('quality'),
            robot_info.get('exp') is not None,
            robot_info.get('created_time'),
            robot_info.get('updated_time')
        ]
    ):
        return False, 'robots_format_error', None

    if 'author' not in robot_info.keys():
        robot_info['author'] = 'Anonymous'

    return True, 'success', robot_info


def get_robots_path_list() -> tuple[bool, str, list[Path]]:
    '''
    获取所有数字员工 path 列表
    '''
    robots_root_dir = settings.ROBOTS_DIR

    exist_robots_path = list(robots_root_dir.glob('*/'))

    return True, 'success', exist_robots_path


def get_robots_path(
    name: str
) -> tuple[bool, str, Path | None]:
    '''
    获取指定数字员工的path
    '''
    exist_robots_path = get_robots_path_list()[-1]

    for robot_path in exist_robots_path:
        if name == robot_path.name:
            return True, 'robot_exists', robot_path
    
    return False, 'robot_not_found', None


def get_robots_rule(
    name: str
) -> tuple[bool, str, str]:
    '''
    获取数字员工规则
    '''
    path = settings.ROBOTS_DIR / name / 'SOUL.md'
    result = get_file_content(path)
    
    return result


def save_robots_rule(
    name: str,
    content: str
) -> tuple[bool, str, dict]:
    '''
    保存数字员工规则
    '''
    path = settings.ROBOTS_DIR / name / 'SOUL.md'
    result = save_file_content(path, content)
    
    return result


def get_robots_memory(
    name: str
) -> tuple[bool, str, str]:
    '''
    获取数字员工记忆（业务模块不同，不与规则文件复用）
    '''
    path = settings.ROBOTS_DIR / name / 'memories' / 'MEMORY.md'
    result = get_file_content(path)
    
    return result


def save_robots_memory(
    name: str,
    content: str
) -> tuple[bool, str, dict]:
    '''
    保存数字员工记忆（业务模块不同，不与规则文件复用）
    '''
    path = settings.ROBOTS_DIR / name / 'memories' / 'MEMORY.md'
    result = save_file_content(path, content)
    
    return result


def save_robots_info(
    name: str,
    description: str,
    author: str,
    department: str,
    rank: str,
    quality: str,
    exp: int,
    created_time: datetime = None
) -> tuple[bool, str, dict]:
    '''
    保存数字员工信息
    '''
    now_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    robot_info = {
        'name': name,
        'description': description,
        'author': author,
        'department': department,
        'rank': rank,
        'quality': quality,
        'exp': exp,
        'created_time': datetime.strftime(created_time, '%Y-%m-%d %H:%M:%S') if created_time is not None else now_time,
        'updated_time': now_time
    }
    
    save_file_content(settings.ROBOTS_DIR / name / 'robot.json', json.dumps(robot_info, ensure_ascii=False, indent=4))
    
    result = {'name': name, 'description': description, 'department': department, 'rank': rank, 'quality': quality, 'exp': exp, 'created_time': created_time}
        
    return True, 'success', result


def get_robots_model_config(
    name: str,
    coordinator: bool = False
) -> tuple[bool, str, dict | None]:
    '''
    获取数字员工/协调器模型配置
    '''
    result = {}

    if coordinator:
        config_dir = settings.COORDINATOR_DIR / name
    else:
        config_dir = settings.ROBOTS_DIR / name
    
    yaml_path = config_dir / 'config.yaml'
    env_path = config_dir / '.env'

    if not yaml_path.exists() or not env_path.exists():
        return False, 'model_config_error', None
    
    with yaml_path.open('r', encoding='utf-8') as f:
        try:
            config_data = yaml.safe_load(f)
        except:
            logger.error(traceback.format_exc())
            return False, 'model_config_error', None

    model_config = config_data.get('model')
    if not isinstance(model_config, dict):
        return False, 'model_config_error', None
    
    result = {
        'provider_id': model_config.get('provider'),
        'model': model_config.get('default'),
        'base_url': model_config.get('base_url'),
        'api_key': ''
    }
    
    try:
        env_config = dotenv_values(env_path)
    except:
        logger.error(traceback.format_exc())
        return False, 'model_config_error', None

    api_key_vars_name_tuple = get_model_provider_api_key_env_vars(result['provider_id'])[-1]
    for api_key_vars_name in api_key_vars_name_tuple:
        api_key_value = env_config.get(api_key_vars_name)
        if not api_key_value:
            continue
        else:
            result['api_key'] = api_key_value
            break
    
    result['is_online'] = judge_model_config_online(
        provider_id=result['provider_id'],
        model=result['model'],
        base_url=result['base_url'],
        api_key=result.get('api_key')
    )[0]
    
    return True, 'success', result


def save_robots_model_config(
    db: Session,
    name: str,
    model_config_id: str,
    coordinator: bool = False
) -> tuple[bool, str, dict]:
    '''
    保存数字员工/协调器模型配置
    '''
    model_config = get_model_config_detail(db, model_config_id)[-1]
    set_dict = {
        'model.provider': model_config['provider_id'],
        'model.default': model_config['model'],
        'model.base_url': model_config['base_url']
    }
    api_key_vars_name_tuple = get_model_provider_api_key_env_vars(model_config['provider_id'])[-1]
    for api_key_vars_name in api_key_vars_name_tuple:
        set_dict[api_key_vars_name] = model_config['api_key']
    
    if coordinator:
        hermes_home = settings.COORDINATOR_DIR / name
    else:
        hermes_home = settings.ROBOTS_DIR / name
    
    for key, value in set_dict.items():
        command = [settings.HERMES_EXECUTABLE, 'config', 'set', key, value]
        worker = ProcessWorkerThread(
            command=command,
            env={'HERMES_HOME': str(hermes_home)}
        )
        worker.start()
        worker.join()

    result = {'name': name, 'model_config_id': model_config_id} 
    
    return True, 'success', result


def get_robots_config(
    name: str
) -> tuple[bool, str, str]:
    '''
    获取数字员工配置
    '''
    path = settings.ROBOTS_DIR / name / 'config.yaml'
    result = get_file_content(path)
    
    return result


def save_robots_config(
    name: str,
    content: str
) -> tuple[bool, str, dict]:
    '''
    保存数字员工配置
    '''
    path = settings.ROBOTS_DIR / name / 'config.yaml'
    result = save_file_content(path, content)
        
    return result


def get_robots_env_config(
    name: str
) -> tuple[bool, str, str]:
    '''
    获取数字员工环境变量配置
    '''
    path = settings.ROBOTS_DIR / name / '.env'
    result = get_file_content(path)
    
    return result


def save_robots_env_config(
    name: str,
    content: str
) -> tuple[bool, str, dict]:
    '''
    保存数字员工环境变量配置
    '''
    path = settings.ROBOTS_DIR / name / '.env'
    result = save_file_content(path, content)
        
    return result


def init_robots_config(
    robots_path: Path,
):
    '''
    初始化数字员工配置
    '''
    command = [settings.HERMES_EXECUTABLE, 'setup', '--reset', '--non-interactive']
    worker = ProcessWorkerThread(
        command=command,
        env={'HERMES_HOME': str(robots_path)}
    )
    worker.start()
    worker.join()

    return True, 'success', None


def set_robots_config(
    robots_path: Path,
    key: str,
    value: str
):
    '''
    设置数字员工配置
    '''
    command = [settings.HERMES_EXECUTABLE, 'config', 'set', key, value]
    worker = ProcessWorkerThread(
        command=command,
        env={'HERMES_HOME': str(robots_path)}
    )
    worker.start()
    worker.join()

    return True, 'success', None


def robots_skills_import(
    name: str,
    skills_list: list[str],
    category: str = None
) -> tuple[bool, str, dict]:
    '''
    导入数字员工技能
    '''
    for skill in skills_list:
        skill_path = get_skills_path(skill, None)[-1]

        if category is not None:
            robots_skills_path = settings.ROBOTS_DIR / name / 'skills' / category / skill_path.name
        else:
            robots_skills_path = settings.ROBOTS_DIR / name / 'skills' / skill_path.name
        
        shutil.copytree(skill_path, robots_skills_path, dirs_exist_ok=True)
    
    result = {'name': name, 'skills_list': skills_list, 'category': category}
        
    return True, 'success', result
        

def get_robots_items(
    page: int = 1,
    size: int = 10,
    name: str = None,
    description: str = None,
    author: str = None,
    department: str = None,
    ranks: list[args_security_check_config['rank_scope']] = None,     # type: ignore[reportUndefinedVariable]
    qualities: list[args_security_check_config['quality_scope']] = None,     # type: ignore[reportUndefinedVariable]
    start_created_time: datetime = None,
    end_created_time: datetime = None,
    start_updated_time: datetime = None,
    end_updated_time: datetime = None,
    order_by: args_security_check_config['robots_order_by'] = 'updated_time',     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc'     # type: ignore[reportUndefinedVariable]
) -> tuple[bool, str, dict]:
    '''
    根据查询条件获取数字员工列表
    '''
    robots_info_list = []

    exist_robots_path = get_robots_path_list()[-1]

    for robot_path in exist_robots_path:
        robot_info = get_robots_info(robot_path)[-1]
        
        if name is not None and name.lower() not in robot_info['name'].lower():
            continue
        if description is not None and description.lower() not in robot_info['description'].lower():
            continue
        if author is not None and author.lower() not in robot_info['author'].lower():
            continue
        if department is not None and department.lower() not in robot_info['department'].lower():
            continue
        if ranks is not None and robot_info['rank'] not in ranks:
            continue
        if qualities is not None and robot_info['quality'] not in qualities:
            continue
        if start_created_time is not None and robot_info['created_time'] < start_created_time:
            continue
        if end_created_time is not None and robot_info['created_time'] > end_created_time:
            continue
        if start_updated_time is not None and robot_info['updated_time'] < start_updated_time:
            continue
        if end_updated_time is not None and robot_info['updated_time'] > end_updated_time:
            continue
        
        robots_info_list.append(robot_info)

    total = len(robots_info_list)

    robots_info_list = sorted(robots_info_list, key=lambda x: x[order_by], reverse=order_type == 'desc')
    
    if page > 0:
        skip = (page - 1) * size
    else:
        skip = None

    robots_info_list = robots_info_list[skip:skip + size] if skip is not None else robots_info_list
    
    for robot_info in robots_info_list:
        with (robot_info['path'] / 'config.yaml').open('r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)

        robot_info['reasoning_effort'] = config_data.get('agent', {}).get('reasoning_effort')
        robot_info['max_turns'] = config_data.get('agent', {}).get('max_turns')

    result = {
        'items': robots_info_list,
        'total': total,
        'page': page,
        'size': size
    }

    return True, 'success', result


def create_robots(
    db: Session,
    name: str,
    description: str,
    department: str,
    reasoning_effort: args_security_check_config['reasoning_effort'],     # type: ignore[reportUndefinedVariable]
    max_turns: int,
    model_config_id: str
) -> tuple[bool, str, dict]:
    '''
    创建数字员工
    '''
    # 创建目录/文件
    robots_path = settings.ROBOTS_DIR / name
    robots_path.mkdir(exist_ok=True)
    (robots_path / 'SOUL.md').touch(exist_ok=True)
    (robots_path / 'skills').mkdir(exist_ok=True)
    (robots_path / 'memories').mkdir(exist_ok=True)
    (robots_path / 'memories' / 'MEMORY.md').touch(exist_ok=True)

    # 是否导入 hermes 原生技能
    if settings.ROBOTS_CREATE_IMPORT_HERMES_SELF_SKILLS:
        hermes_self_skills_record = json.loads(get_file_content(settings.HERMES_SELF_SKILLS_RECORD_PATH)[-1]['content'])
        
        for skill_record in hermes_self_skills_record:
            status, _, skill_path = get_skills_path(skill_record['name'], None)
            if status:
                (robots_path / 'skills' / skill_record['category']).mkdir(exist_ok=True)
                shutil.copytree(skill_path, robots_path / 'skills' / skill_record['category'] / skill_record['name'], dirs_exist_ok=True)
    
    # 初始化配置文件
    init_robots_config(robots_path)

    # 写入配置
    set_robots_config(robots_path, 'agent.reasoning_effort', reasoning_effort)
    set_robots_config(robots_path, 'agent.max_turns', str(max_turns))

    # 写入模型配置
    save_robots_model_config(db, name, model_config_id)

    # 关闭 clarify 工具
    command = [settings.HERMES_EXECUTABLE, 'tools', 'disable', 'clarify']
    worker = ProcessWorkerThread(
        command=command,
        env={'HERMES_HOME': str(robots_path)}
    )
    worker.start()
    worker.join()
    
    # 写入数字员工信息
    save_robots_info(
        name=name,
        description=description,
        author=settings.USERNAME,
        department=department,
        rank='L1',
        quality='common',
        exp=0
    )

    # 下载头像
    download_dicebear_image(robots_path / 'avatar.png')
    
    result = {'name': name, 'description': description, 'department': department, 'reasoning_effort': reasoning_effort, 'max_turns': max_turns, 'model_config_id': model_config_id}
        
    return True, 'success', result


def update_robots(
    db: Session,
    name: str,
    rename: str = None,
    description: str = None,
    department: str = None,
    reasoning_effort: args_security_check_config['reasoning_effort'] = None,     # type: ignore[reportUndefinedVariable]
    max_turns: int = None,
    exp: int = None,
    model_config_id: str = None
) -> tuple[bool, str, dict]:
    '''
    更新数字员工信息
    '''
    # 更新模型配置
    if model_config_id:
        save_robots_model_config(db, name, model_config_id)
    
    # 更新数字员工信息
    robot_path = settings.ROBOTS_DIR / name
    robot_info = get_robots_info(robot_path)[-1]
    if rename:
        robot_info['name'] = rename
        new_robot_path = settings.ROBOTS_DIR / rename
        robot_path.replace(new_robot_path)

        from services.tasks.project import get_projects_items, update_projects_record
        from services.tasks.task import get_tasks_items, update_tasks_record

        # 更新任务记录中的数字员工名称
        for item in get_tasks_items(
            db=db,
            page=0,
            robots=[name]
        )[-1]['items']:
            update_tasks_record(
                db=db,
                id=item['id'],
                robots=[ robot for robot in item['robots'] if robot != name ] + [rename],
                updated_time=db.get(Task, item['id']).updated_time
            )
        
        # 更新项目记录中的数字员工名称
        for item in get_projects_items(
            db=db,
            page=0,
            robots=[name]
        )[-1]['items']:
            rebots = [ robot for robot in item['robots'] if robot != name ] + [rename]
            history_rebots = [ robot for robot in item['history_robots'] if robot != name ] + [rename]

            update_projects_record(
                db=db,
                id=item['id'],
                robots=rebots,
                history_robots=history_rebots
            )
    if description:
        robot_info['description'] = description
    if department:
        robot_info['department'] = department
    if reasoning_effort:
        set_robots_config(new_robot_path, 'agent.reasoning_effort', reasoning_effort)
    if max_turns is not None:
        set_robots_config(new_robot_path, 'agent.max_turns', str(max_turns))
    if exp is not None:
        rank_quality_quality = calculate_robots_rank_and_quality(exp)[-1]
        robot_info['rank'] = rank_quality_quality['rank']
        robot_info['quality'] = rank_quality_quality['quality']
        robot_info['exp'] = exp
    
    save_robots_info(
        name=robot_info['name'],
        description=robot_info['description'],
        author=robot_info['author'],
        department=robot_info['department'],
        rank=robot_info['rank'],
        quality=robot_info['quality'],
        exp=robot_info['exp'],
        created_time=robot_info['created_time']
    )
        
    result = {'name': name, 'rename': rename, 'description': description, 'department': department, 'reasoning_effort': reasoning_effort, 'max_turns': max_turns, 'exp': exp, 'model_config_id': model_config_id}
        
    return True, 'success', result


def delete_robots(
    db: Session,
    names: list[str]
) -> tuple[bool, str, dict]:
    '''
    删除数字员工
    '''
    from services.tasks.project import get_projects_items, update_projects_record
    from services.tasks.task import (
        delete_tasks_record,
        get_tasks_items,
        update_tasks_record,
    )

    for name in names:
        delete_task_ids = []
        update_task_ids = []
        delete_session_ids = []

        for item in get_tasks_items(
            db=db,
            page=0,
            robots=[name]
        )[-1]['items']:
            if item['type'] == 'session':
                delete_task_ids.append(item['id'])
                if item['project_id'] not in delete_session_ids:
                    delete_session_ids.append(item['project_id'])
            else:
                update_task_ids.append(item['id'])

        # 删除会话类任务记录
        delete_tasks_record(
            db=db,
            ids=delete_task_ids
        )

        # 删除项目类任务中的数字员工记录
        for task_id in update_task_ids:
            update_tasks_record(
                db=db,
                id=task_id,
                robots=[ robot for robot in item['robots'] if robot != name ],
                updated_time=db.get(Task, task_id).updated_time
            )

        # 删除项目中的数字员工记录
        for item in get_projects_items(
            db=db,
            page=0,
            robots=[name]
        )[-1]['items']:
            rebots = [ robot for robot in item['robots'] if robot != name ]
            history_rebots = [ robot for robot in item['history_robots'] if robot != name ]

            update_projects_record(
                db=db,
                id=item['id'],
                robots=rebots,
                history_robots=history_rebots
            )
        
        # 删除会话类任务工作目录
        for session_id in delete_session_ids:
            shutil.rmtree(settings.WORKSPACE_DIR / session_id)
        
        # 删除数字员工目录
        robots_path = settings.ROBOTS_DIR / name
        shutil.rmtree(robots_path)

        # 删除收件箱相关通知
        items = get_inbox_items(
            db=db,
            page=0,
            robot=name,
            coordinator=False
        )[-1]['items']
        
        delete_inbox_record(
            db=db,
            ids=[item['id'] for item in items]
        )
    
    result = {'names': names}
        
    return True, 'success', result


def import_robots(
    db: Session,
    tmp_robots_path: Path,
    model_config_id: str
) -> tuple[bool, str, list[str] | None]:
    '''
    导入数字员工
    '''
    try:
        tmp_robot_dirs = find_file_dirs(tmp_robots_path, 'robot.json')[-1]
        if not tmp_robot_dirs:
            return False, 'no_robots_found_in_archive', None
        
        # 获取数字员工信息，检查格式
        tmp_robot_info_list = []
        for robot_path in tmp_robot_dirs:
            status, msg, robot_info = get_robots_info(robot_path)
            if settings.ROBOTS_FORMAT_CHECK and not status:
                return False, msg, None
            
            if any(
                [
                    not (robot_path / 'SOUL.md').exists(),
                    not (robot_path / 'memories').exists(),
                    not (robot_path / 'skills').exists()
                ]
            ):
                return False, 'robots_format_error', None
        
            tmp_robot_info_list.append(robot_info)
        
        exist_robots = [ robot.name for robot in find_file_dirs(settings.ROBOTS_DIR, 'robot.json')[-1] ]

        # 兼容异常情况，非预期取值时按 None 处理直接拦截导入
        if settings.ROBOTS_OVERWRITE != True and \
            settings.ROBOTS_OVERWRITE != False and \
            (
                # 检查是否存在同名数字员工
                any(robot_info['name'] in exist_robots for robot_info in tmp_robot_info_list)
            ):
            return False, 'import_robot_exists', [robot_info['name']]

        has_imported = []

        for robot_info in tmp_robot_info_list:
            if robot_info['name'] in exist_robots:
                if settings.ROBOTS_OVERWRITE == False:
                    continue

            save_robots_path = settings.ROBOTS_DIR / robot_info['name']

            shutil.copytree(robot_info['path'], save_robots_path, dirs_exist_ok=True)

            # 初始化配置文件
            init_robots_config(save_robots_path)

            # 写入配置
            set_robots_config(save_robots_path, 'agent.reasoning_effort', 'medium')
            set_robots_config(save_robots_path, 'agent.max_turns', '900')

            # 写入模型配置
            save_robots_model_config(db, robot_info['name'], model_config_id)

            # 关闭 clarify 工具
            command = [settings.HERMES_EXECUTABLE, 'tools', 'disable', 'clarify']
            worker = ProcessWorkerThread(
                command=command,
                env={'HERMES_HOME': str(save_robots_path)}
            )
            worker.start()
            worker.join()

            # 设置头像
            if not (save_robots_path / 'avatar.png').exists():
                download_dicebear_image(save_robots_path / 'avatar.png')
            
            has_imported.append(robot_info['name'])

        return True, 'success', has_imported
    finally:
        shutil.rmtree(tmp_robots_path)


def clone_from_robots(
    name: str,
    clone_name: str
) -> tuple[bool, str, dict]:
    '''
    克隆数字员工
    '''
    clone_from_robot_path = settings.ROBOTS_DIR / clone_name
    robot_path = settings.ROBOTS_DIR / name
    
    clone_from_robot_path.mkdir(exist_ok=True)

    for obj_file in ['robot.json', 'SOUL.md', 'config.yaml', '.env']:
        shutil.copy(robot_path / obj_file, clone_from_robot_path / obj_file)

    clone_from_robot_info = get_robots_info(clone_from_robot_path)[-1]
    save_robots_info(
        name=clone_name,
        description=clone_from_robot_info['description'],
        author=clone_from_robot_info['author'],
        department=clone_from_robot_info['department'],
        rank=clone_from_robot_info['rank'],
        quality=clone_from_robot_info['quality'],
        exp=clone_from_robot_info['exp'],
        created_time=clone_from_robot_info['created_time']
    )

    for obj_dir in ['memories', 'skills']:
        shutil.copytree(robot_path / obj_dir, clone_from_robot_path / obj_dir, dirs_exist_ok=True)
    
    download_dicebear_image(clone_from_robot_path / 'avatar.png')

    result = {'name': name, 'clone_name': clone_name}
        
    return True, 'success', result
    

def download_robots(
    name: str
) -> tuple[bool, str, StreamingResponse]:
    '''
    下载数字员工
    '''
    robot_path = get_robots_path(name)[-1]

    white_parent_dir = [
        Path(robot_path / obj) for obj in [
            'robot.json',
            'SOUL.md',
            'skills',
            'memories',
            'avatar.png'
        ]
    ]
    
    zip_buffer = zip_dir(robot_path, white_parent_dir)
    
    result = StreamingResponse(
        zip_buffer,
        media_type='application/zip',
        headers={
            'Content-Disposition': f'attachment; filename={robot_path.name}.zip'
        }
    )
    
    return True, 'success', result


def calculate_robots_rank_and_quality(
    exp: int
) -> tuple[bool, str, dict]:
    '''
    计算数字员工等级和品质
    '''
    quality_dict = {
        0: 'common',
        1: 'uncommon',
        2: 'rare',
        3: 'epic',
        4: 'legendary',
    }
    
    if exp < 0:
        rank = 'L1'
        quality = 'common'
    elif 0 <= exp < 900:
        rank = f'L{(exp // 100) + 1}'
        quality = quality_dict[exp // 200]
    else:
        rank = 'L9'
        quality = 'legendary'
    
    return True, 'success', {'rank': rank, 'quality': quality}


def upload_robots_avatar(
    uf: UploadFile,
    name: str
) -> tuple[bool, str, dict]:
    '''
    上传数字员工头像
    '''
    robot_path = get_robots_path(name)[-1]
    avatar_path = robot_path / 'avatar.png'
    
    with avatar_path.open('wb') as f:
        f.write(uf.file.read())
    
    return True, 'success', {'name': name}
    

def get_robots_avatar(
    name: str
) -> tuple[bool, str, StreamingResponse]:
    '''
    获取数字员工头像
    '''
    robot_path = get_robots_path(name)[-1]
    robot_avatar_path = robot_path / 'avatar.png'

    if not robot_avatar_path.exists():
        download_dicebear_image(robot_avatar_path)

    result = StreamingResponse(
        robot_avatar_path.open('rb'),
        media_type='image/png',
        headers={
            'Content-Disposition': f'attachment; filename={robot_avatar_path.name}'
        }
    )
    
    return True, 'success', result
