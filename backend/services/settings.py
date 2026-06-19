'''
系统设置
'''


from core.config import settings


def get_system_settings(
    name: str
) -> tuple[bool, str, str]:
    '''
    获取系统设置
    '''
    result = getattr(settings, name)
    
    return True, 'success', result


def set_system_settings(
    name: str,
    value: str | bool | int | None
) -> tuple[bool, str, dict]:
    '''
    设置系统设置
    '''    
    setattr(settings, name, value)

    return True, 'success', {'name': name, 'value': value}


def judge_system_settings_value_valid(
    name: str,
    value: str | bool | int | None
) -> tuple[bool, str, dict | None]:
    '''
    判断系统设置值是否有效
    '''
    if name == 'LANG' and value not in ['zh-CN', 'en-US']:
        return False, 'setting_not_valid', None
    
    elif name in ['SKILLS_OVERWRITE', 'ROBOTS_OVERWRITE'] and value not in [True, False, None]:
        return False, 'setting_not_valid', None
    
    elif name in [
        'SKILLS_FORMAT_CHECK',
        'ROBOTS_FORMAT_CHECK',
        'ROBOTS_CREATE_IMPORT_HERMES_SELF_SKILLS',
        'SCHEDULER_COALESCE'
    ] and value not in [True, False]:
        return False, 'setting_not_valid', None
    
    elif name in ['SCHEDULER_MAX_JOBS', 'SCHEDULER_MAX_INSTANCES']:
        if any(
            [
                not isinstance(value, int),
                isinstance(value, bool),
                value <= 0
            ]
        ):
            return False, 'setting_not_valid', None

    return True, 'success', {'name': name, 'value': value}