'''
初始化
'''


import traceback
from pathlib import Path

import yaml
from core.config import settings
from core.database import Base, db_engine, db_session
from core.scheduler import scheduler
from dotenv import dotenv_values
from services.model.hermes import get_model_provider_api_key_env_vars
from services.model.model import create_model_config, judge_model_config_online, get_models_config_items
from core.database import db_session


def init_i18n():
    '''
    初始化多语言配置
    '''
    from core.locales import load_translations

    settings.TRANSLATIONS = load_translations()


def init_coordinator_config():
    '''
    初始化协调器配置
    '''
    from _utils.process import ProcessWorkerThread
    from services.robots.manage import init_robots_config, set_robots_config

    for coordinator in ['agbox-coordinator-async', 'agbox-coordinator-sync']:
        coordinator_path = settings.COORDINATOR_DIR / coordinator

        if not (coordinator_path / 'config.yaml').exists():
            init_robots_config(coordinator_path)
            set_robots_config(coordinator_path, 'agent.max_turns', '900')

            command = [settings.HERMES_EXECUTABLE, 'tools', 'disable', 'delegation']
            worker = ProcessWorkerThread(
                command=command,
                env={'HERMES_HOME': str(coordinator_path)}
            )
            worker.start()
            worker.join()

            command = [settings.HERMES_EXECUTABLE, 'tools', 'disable', 'clarify']
            worker = ProcessWorkerThread(
                command=command,
                env={'HERMES_HOME': str(coordinator_path)}
            )
            worker.start()
            worker.join()


def init_scheduler():
    '''
    初始化定时任务调度器
    '''
    scheduler.start()


def init_db():
    '''
    初始化数据库
    '''
    Base.metadata.create_all(bind=db_engine)


def init_existed_hermes_model_config():
    '''
    初始化已存在的 hermes 模型配置
    '''
    with db_session() as db:
        online_model_config_items = get_models_config_items(
            db=db,
            is_online=True,
        )[-1]
        
        if not online_model_config_items:
            pass
        else:
            return
    
    from core.logger import logger

    hermes_home = Path.home() / '.hermes'
    config_path = hermes_home / 'config.yaml'
    env_path = hermes_home / '.env'

    if not config_path.exists() or not env_path.exists():
        return
    
    with config_path.open('r', encoding='utf-8') as f:
        try:
            config_data = yaml.safe_load(f)
        except:
            logger.error(traceback.format_exc())
            return

    model_config = config_data.get('model')
    if not isinstance(model_config, dict):
        return
    
    result = {
        'provider': model_config.get('provider'),
        'model': model_config.get('default'),
        'base_url': model_config.get('base_url'),
        'api_key': ''
    }
    
    try:
        env_config = dotenv_values(env_path)
    except:
        logger.error(traceback.format_exc())
        return

    api_key_vars_name_tuple = get_model_provider_api_key_env_vars(model_config['provider'])[-1]
    for api_key_vars_name in api_key_vars_name_tuple:
        api_key_value = env_config.get(api_key_vars_name)
        if not api_key_value:
            continue
        else:
            result['api_key'] = api_key_value
            break
    
    result['is_online'] = judge_model_config_online(
        provider_id=result['provider'],
        model=result['model'],
        base_url=result['base_url'],
        api_key=result['api_key']
    )[0]

    if not result['is_online']:
        return
    else:
        with db_session() as db:
            create_model_config(
                db=db,
                name='default_local_load',
                provider_id=result['provider'],
                model=result['model'],
                base_url=result['base_url'],
                api_key=result['api_key'],
            )