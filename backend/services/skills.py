'''
技能管理 业务逻辑
'''


import re
import yaml
import shutil
import traceback
from datetime import datetime
from pathlib import Path

import requests
import shortuuid
from _utils.file import find_file_dirs
from core.config import settings
from core.logger import logger
from core.security import args_security_check_config
from git import Repo


def get_skills_info(
    path: Path
) -> tuple[bool, str, dict | None]:
    '''
    获取 skills 的 name、description、category、is_script 和 path 信息
    '''
    skill_info = {'path': path}

    with (path / 'SKILL.md').open('r', encoding='utf-8') as f:
        lines = []
        for line_num in range(30):
            line = f.readline()
            if line is None:
                break
            if line.strip() == '---':
                if line_num == 0:
                    continue
                else:
                    break
            lines.append(line)
        
        skills_content = ''.join(lines)
    
    try:
        skills_content_dict = yaml.safe_load(skills_content)
    except:
        logger.error(traceback.format_exc())
        skills_content_dict = {}
    
    name = skills_content_dict.get('name', '').strip().strip('"\'')
    if re.match(args_security_check_config['name']['regex'], name):
        skill_info['name'] = name
    
    skill_info['description'] = skills_content_dict.get('description', '').strip().strip('"\'')
    
    if not skill_info.get('name') or not skill_info.get('description'):
        return False, 'skills_format_error', None
    
    if path.parent == settings.SKILLS_DIR or path.parent.parent.parent == settings.ROBOTS_DIR:
        skill_info['category'] = ''
    else:
        skill_info['category'] = path.parent.name
    
    if (path / 'scripts').is_dir() and any((path / 'scripts').iterdir()):
        skill_info['is_script'] = True
    else:
        skill_info['is_script'] = False

    return True, 'success', skill_info


def get_skills_root_dir(
    robot: str = None
):
    '''
    获取指定数字员工的技能根目录
    '''
    if not robot:
        skills_dir = settings.SKILLS_DIR
    else:
        skills_dir = settings.ROBOTS_DIR / robot / 'skills'
    
    return True, 'success', skills_dir


def get_skills_path_list(
    robot: str = None
) -> tuple[bool, str, list[Path]]:
    '''
    获取指定数字员工技能的 path 列表
    '''
    skills_root_dir = get_skills_root_dir(robot)[-1]

    exist_skills_path = [ skill_path for skill_path in find_file_dirs(skills_root_dir, 'SKILL.md')[-1] ]

    return True, 'success', exist_skills_path


def get_skills_path(
    name: str,
    robot: str = None,
) -> tuple[bool, str, Path | None]:
    '''
    获取指定数字员工，指定 name 技能的 path
    '''
    exist_skills_path = get_skills_path_list(robot)[-1]

    for skill_path in exist_skills_path:
        if name == skill_path.name:
            return True, 'success', skill_path
    
    return False, 'skill_not_found', None


def import_skills(
    tmp_skills_path: Path,
    category: str = None
) -> tuple[bool, str, list[str] | None]:
    '''
    导入技能
    '''
    try:
        tmp_skill_dirs = find_file_dirs(tmp_skills_path, 'SKILL.md')[-1]
        if not tmp_skill_dirs:
            return False, 'no_skill_found_in_archive', None
        
        # 获取 skills 信息，检查格式
        tmp_skills_info_list = []
        for skill_path in tmp_skill_dirs:
            status, msg, skill_info = get_skills_info(skill_path)
            if settings.SKILLS_FORMAT_CHECK and not status:
                return False, msg, None
        
            tmp_skills_info_list.append(skill_info)
        
        exist_skills = [ skill.name for skill in find_file_dirs(settings.SKILLS_DIR, 'SKILL.md')[-1] ]

        # 兼容异常情况，非预期取值时按 None 处理直接拦截导入
        if settings.SKILLS_OVERWRITE != True and \
            settings.SKILLS_OVERWRITE != False and \
            any(skill_info['name'] in exist_skills for skill_info in tmp_skills_info_list):
            # 检查是否存在同名技能
            return False, 'import_skill_exists', [skill_info['name']]

        has_imported = []

        for skill_info in tmp_skills_info_list:
            if skill_info['name'] in exist_skills:
                if settings.SKILLS_OVERWRITE == False:
                    continue

            if category is not None:
                save_skills_path = settings.SKILLS_DIR / category / skill_info['name']
            else:
                save_skills_path = settings.SKILLS_DIR / skill_info['name']

            shutil.copytree(skill_info['path'], save_skills_path, dirs_exist_ok=True)
            has_imported.append(skill_info['name'])

        return True, 'success', has_imported
    finally:
        shutil.rmtree(tmp_skills_path)


def get_skills_category_items(
    robot: str = None
) -> tuple[bool, str, list[str] | None]:
    '''
    获取技能分类
    '''
    result = []

    skills_root_dir = get_skills_root_dir(robot)[-1]

    for category in skills_root_dir.glob('*/'):
        if not (category / 'SKILL.md').exists():
            result.append(category.name)
    
    return True, 'success', result


def delete_skills_category(
    category: str,
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    删除技能分类
    '''
    skills_root_dir = get_skills_root_dir(robot)[-1]

    shutil.rmtree(skills_root_dir / category)
    
    result = {'category': category, 'robot': robot}
   
    return True, 'success', result


def create_skills_category(
    category: str,
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    创建技能分类
    '''
    skills_root_dir = get_skills_root_dir(robot)[-1]

    (skills_root_dir / category).mkdir(exist_ok=True)
    
    result = {'category': category, 'robot': robot}
   
    return True, 'success', result


def rename_skills_category(
    old_category: str,
    new_category: str,
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    重命名技能分类
    '''
    skills_root_dir = get_skills_root_dir(robot)[-1]

    old_category_path = skills_root_dir / old_category
    new_category_path = skills_root_dir / new_category

    old_category_path.replace(new_category_path)
    
    result = {'old_category': old_category, 'new_category': new_category, 'robot': robot}
   
    return True, 'success', result


def get_skills_items(
    page: int = 1,
    size: int = 10,
    name: str = None,
    description: str = None,
    category: str = None,
    is_script: bool = None,
    order_by: args_security_check_config['skills_order_by'] = 'name',     # type: ignore[reportUndefinedVariable]
    order_type: args_security_check_config['order_type'] = 'desc',     # type: ignore[reportUndefinedVariable]
    robot: str = None
) -> tuple[bool, str, list[dict]]:
    '''
    获取技能列表
    '''
    exist_skills_path = get_skills_path_list(robot)[-1]

    skills_list = []

    for skill_path in exist_skills_path:
        skill_info = get_skills_info(skill_path)[-1]
        
        if name and name.lower() not in skill_info['name'].lower():
            continue
        if description and description.lower() not in skill_info['description'].lower():
            continue
        if not category and skill_info['category'] != '':
            continue
        if category and category.lower() != skill_info['category'].lower():
            continue
        if is_script is not None and is_script != skill_info['is_script']:
            continue

        skills_list.append(skill_info)

    total = len(skills_list)

    skills_list = sorted(skills_list, key=lambda x: x[order_by], reverse=order_type == 'desc')
    
    if page > 0:
        skip = (page - 1) * size
    else:
        skip = None

    skills_list = skills_list[skip:skip + size] if skip is not None else skills_list
    
    result = {
        'items': skills_list,
        'total': total,
        'page': page,
        'size': size
    }

    return True, 'success', result
    

def delete_skills(
    names: list[str],
    robot: str = None
) -> tuple[bool, str, dict]:
    '''
    删除技能
    '''
    for name in names:
        skill_path = get_skills_path(name, robot)[-1]
        shutil.rmtree(skill_path)
    
    result = {'names': names, 'robot': robot}
   
    return True, 'success', result


def get_skillsmp_items(
    q: str,
    page: int = 1,
    limit: int = 20,
    sortBy: args_security_check_config['skillsmp_sort_by'] = 'recent',     # type: ignore[reportUndefinedVariable]
    category: str = None,
    occupation: str = None
) -> tuple[bool, str, list[dict] | None]:
    '''
    获取 skillsmp 技能列表
    '''
    resp = requests.get(
        settings.SKILLSMP_API_URL,
        params={
            'q': q,
            'page': page,
            'limit': limit,
            'sortBy': sortBy,
            'category': category,
            'occupation': occupation
        }
    )
    
    try:
        data = resp.json()
        if data['success']:
            items = data['data']['skills']
            for item in items:
                item['updatedAt'] = datetime.fromtimestamp(int(item['updatedAt']))
                del item['id']
            
            result = {
                'items': items,
                'total': data['data']['pagination']['total'],
                'page': page,
                'size': limit
            }
            return True, 'success', result
        else:
            return False, data['error']['message'], None
    except:
        logger.error(traceback.format_exc())
        return False, 'get_skillsmp_items_failed', None
    

def install_skills_from_skillsmp(
    url: str,
    category: str = None
) -> tuple[bool, str, dict | None]:
    '''
    从 skillsmp 安装技能
    '''
    url_parts = url.split('/tree/')
    repo_url = url_parts[0]
    sub_path = Path().joinpath(*url_parts[-1].split('/')[1:])
    
    tmp_path = settings.TEMP_DIR / shortuuid.uuid()
    tmp_sub_path = tmp_path / sub_path

    try:
        repo = Repo.clone_from(
            url=repo_url,
            to_path=tmp_path,
            filter='blob:none',
            sparse=True
        )

        repo.git.sparse_checkout('set', sub_path)

        status, msg, result = import_skills(
            tmp_skills_path=tmp_sub_path,
            category=category
        )
        if not status:
            return False, msg, None

        result = {'url': url, 'category': category}
        return True, 'success', result
    except:
        logger.error(traceback.format_exc())
        return False, 'install_skills_from_skillsmp_failed', None
    finally:
        if tmp_path.exists():
            shutil.rmtree(tmp_path)
