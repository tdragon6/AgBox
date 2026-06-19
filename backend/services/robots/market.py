'''
数字员工市场 业务逻辑
'''


import shortuuid
import shutil
import traceback
import requests
from datetime import datetime
from pathlib import Path

from services.robots.manage import import_robots
from core.config import settings
from core.security import args_security_check_config
from core.logger import logger
from sqlalchemy.orm import Session
from git import Repo


def get_robots_market_list(
) -> tuple[bool, str, list | None]:
    '''
    获取数字员工市场清单
    '''
    try:
        data = requests.get(settings.ROBOTS_MARKET_URL, timeout=10).json()
    except:
        logger.error(traceback.format_exc())
        return False, 'robots_market_list_error', None
    
    for item in data:
        item['created_time'] = datetime.strptime(item['created_time'], '%Y-%m-%d %H:%M:%S')
        item['updated_time'] = datetime.strptime(item['updated_time'], '%Y-%m-%d %H:%M:%S')
        
        if 'author' not in item.keys():
            item['author'] = 'Anonymous'

    return True, 'success', data


def get_robots_market_items(
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
    根据查询条件获取数字员工市场清单
    '''
    status, msg, data = get_robots_market_list()
    if not status:
        return status, msg, None

    robots_info_list = []
    
    for robot_info in data:
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

    result = {
        'items': robots_info_list,
        'total': total,
        'page': page,
        'size': size
    }

    return True, 'success', result


def install_robots_from_market(
    db: Session,
    url: str,
    model_config_id: str
) -> tuple[bool, str, dict | None]:
    '''
    从市场安装数字员工
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

        status, msg, result = import_robots(
            db=db,
            tmp_robots_path=tmp_sub_path,
            model_config_id=model_config_id
        )
        if not status:
            return False, msg, None

        result = {'url': url}
        return True, 'success', result
    except:
        logger.error(traceback.format_exc())
        return False, 'install_robots_from_market_failed', None
    finally:
        if tmp_path.exists():
            shutil.rmtree(tmp_path)