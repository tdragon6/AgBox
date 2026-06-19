'''
全局配置
'''


import secrets
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, get_args

from core.security import args_security_check_config
from dotenv import set_key
from pydantic import Field
from pydantic_settings import BaseSettings

ENV_PATH = Path(__file__).parent.parent / 'env' / '.env'

ENV_FIELDS = [
    'HOST',
    'PORT',
    'DEBUG',
    'TOKEN_EXPIRE_HOUR',
    'USERNAME',
    'PASSWORD',
    'LANG',
    'ROBOTS_MARKET_URL',
    'SKILLSMP_API_URL',
    'MAX_IMAGE_SIZE',
    'MAX_FILE_SIZE'
] + list(get_args(args_security_check_config['web_env_fields']))

_STORE_DIR = Path(__file__).parent.parent.parent / 'store'


def write_env_var(
    env_path: Path,
    name: str,
    value: Any
):
    '''
    写入环境变量
    '''
    if isinstance(value, bool):
        value_str = 'true' if value else 'false'
    elif value is None:
        value_str = ''
    else:
        value_str = str(value)

    env_key = 'AGBOX_' + name

    set_key(env_path, env_key, value_str)


class Settings(BaseSettings):
    APP_NAME: str = Field('AgBox - 数字员工 OPC 托管平台', validation_alias='AGBOX_APP_NAME')
    APP_VERSION: str = Field('v0.1.0', validation_alias='AGBOX_APP_VERSION')

    HOST: str = Field('127.0.0.1', validation_alias='AGBOX_HOST')
    PORT: int = Field(8000, validation_alias='AGBOX_PORT')
    DEBUG: bool = Field(False, validation_alias='AGBOX_DEBUG')

    # python 解释器路径
    PYTHON_EXECUTABLE: str = Field(sys.executable, validation_alias='AGBOX_PYTHON_EXECUTABLE')

    # hermes 启动路径
    HERMES_EXECUTABLE: str = Field(str(Path(sys.executable).parent / 'hermes'), validation_alias='AGBOX_HERMES_EXECUTABLE')

    # 同步协调器脚本路径
    COORDINATOR_SYNC_SCRIPT_PATH: Path = Field(Path(__file__).parent.parent / 'services' / 'tasks' / 'loop.py', validation_alias='AGBOX_COORDINATOR_SYNC_SCRIPT_PATH')

    # 协调器标记（coordinator 的 md5）
    COORDINATOR_MARK: str = Field('c4312c2a07bf7ded608a4d7cee2228dd', validation_alias='AGBOX_COORDINATOR_MARK')

    # 数据库配置
    DATABASE_URL: str = Field(f'sqlite:///{Path(__file__).parent.parent.parent / "store" / "agbox.db"}', validation_alias='AGBOX_DATABASE_URL')

    # JWT 配置
    SECRET_KEY: str = Field(secrets.token_hex(32), validation_alias='AGBOX_SECRET_KEY')
    ALGORITHM: str = Field('HS256', validation_alias='AGBOX_ALGORITHM')
    TOKEN_EXPIRE_HOUR: int = Field(24 * 7, validation_alias='AGBOX_TOKEN_EXPIRE_HOUR')
    USERNAME: str = Field('tdragon6', validation_alias='AGBOX_USERNAME')
    PASSWORD: str = Field('', validation_alias='AGBOX_PASSWORD')
    
    # 多语言配置
    TRANSLATIONS: dict = Field({}, validation_alias='AGBOX_TRANSLATIONS')
    LANG: str = Field('zh-CN', validation_alias='AGBOX_LANG')

    # 路径配置
    STORE_DIR: Path = Field(_STORE_DIR, validation_alias='AGBOX_STORE_DIR')
    COORDINATOR_DIR: Path = Field(_STORE_DIR / 'coordinator', validation_alias='AGBOX_COORDINATOR_DIR')
    SKILLS_DIR: Path = Field(_STORE_DIR / 'skills', validation_alias='AGBOX_SKILLS_DIR')
    HERMES_SELF_SKILLS_RECORD_PATH: Path = Field(_STORE_DIR / 'hermes_self_skills.json', validation_alias='AGBOX_HERMES_SELF_SKILLS_RECORD_PATH')
    
    LOGS_DIR: Path = Field(_STORE_DIR / 'logs', validation_alias='AGBOX_LOGS_DIR')
    ROBOTS_DIR: Path = Field(_STORE_DIR / 'robots', validation_alias='AGBOX_ROBOTS_DIR')
    WORKSPACE_DIR: Path = Field(Path.home() / '.agbox_workspace', validation_alias='AGBOX_WORKSPACE_DIR')
    TEMP_DIR: Path = Field(_STORE_DIR / '.tmp', validation_alias='AGBOX_TEMP_DIR')

    # 技能导入配置
    SKILLS_OVERWRITE: bool | None = Field(None, validation_alias='AGBOX_SKILLS_OVERWRITE')
    SKILLS_FORMAT_CHECK: bool = Field(True, validation_alias='AGBOX_SKILLS_FORMAT_CHECK')

    # 数字员工导入配置
    ROBOTS_OVERWRITE: bool | None = Field(None, validation_alias='AGBOX_ROBOTS_OVERWRITE')
    ROBOTS_FORMAT_CHECK: bool = Field(True, validation_alias='AGBOX_ROBOTS_FORMAT_CHECK')
    ROBOTS_CREATE_IMPORT_HERMES_SELF_SKILLS: bool = Field(True, validation_alias='AGBOX_ROBOTS_CREATE_IMPORT_HERMES_SELF_SKILLS')

    # 数字员工市场配置
    ROBOTS_MARKET_URL: str = Field('https://raw.githubusercontent.com/tdragon6/AgBox-Market/refs/heads/main/robots.json', validation_alias='AGBOX_ROBOTS_MARKET_URL')

    # skillsmp api 地址
    SKILLSMP_API_URL: str = Field('https://skillsmp.com/api/v1/skills/search', validation_alias='AGBOX_SKILLSMP_API_URL')

    # 定时任务配置
    SCHEDULER_MAX_JOBS: int = Field(10, validation_alias='AGBOX_SCHEDULER_MAX_JOBS')
    SCHEDULER_COALESCE: bool = Field(False, validation_alias='AGBOX_SCHEDULER_COALESCE')
    SCHEDULER_MAX_INSTANCES: int = Field(1, validation_alias='AGBOX_SCHEDULER_MAX_INSTANCES')

    # 文件大小限制
    MAX_IMAGE_SIZE: int = Field(2 * 1024 * 1024, validation_alias='AGBOX_MAX_IMAGE_SIZE')
    # 安全限制，防止过大文件导入
    MAX_FILE_SIZE: int = Field(50 * 1024 * 1024, validation_alias='AGBOX_MAX_FILE_SIZE')

    # Hermes 模型消耗相关字段
    HERMES_MODEL_COST_KEYS: list[str] = Field(
        [
            'input_tokens',
            'output_tokens',
            'cache_read_tokens',
            'cache_write_tokens',
            'reasoning_tokens',
            'estimated_cost_usd',
            'actual_cost_usd',
        ], 
        validation_alias='AGBOX_HERMES_MODEL_COST_KEYS'
    )


    model_config = {
        'env_file': ENV_PATH,
        'case_sensitive': True,
        'env_file_encoding': 'utf-8',
        'env_ignore_empty': True
    }

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in ENV_FIELDS:
            write_env_var(
                env_path=ENV_PATH,
                name=name,
                value=value
            )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()