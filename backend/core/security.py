'''
参数安全校验
'''


from typing import Literal

args_security_check_config = {
    # 通用
    'short_uuid': {
        # uuid 格式校验
        'regex': r'^[2-9a-zA-Z]{22}$'
    },
    'session_id': {
        # 会话ID 格式校验
        'regex': r'^\d{8}_\d{6}_[0-9a-f]{6}$'
    },
    'name': {
        # 限制大小写字母、数字、下划线和短横线
        'regex': r'^[a-zA-Z0-9_-]+$'
    },
    'url': {
        # 限制合法 URL 格式
        'regex': r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)$'
    },
    'order_type': Literal['asc', 'desc'],

    # 文件管理
    'scope': Literal['skills', 'workspaces'],
    'file_type': Literal['file', 'dir'],

    # skills
    'skills_order_by': Literal['name', 'is_script'],

    # 数字员工
    'rank_scope': Literal['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9'],
    'quality_scope': Literal['legendary', 'epic', 'rare', 'uncommon', 'common'],
    'robots_order_by': Literal['name', 'department', 'rank', 'quality', 'created_time', 'updated_time'],
    'reasoning_effort': Literal['none', 'minimal', 'low', 'medium', 'high', 'xhigh'],

    # skillsmp
    'skillsmp_sort_by': Literal['stars', 'recent'],
    'skillsmp_max_limit': 100,

    # 任务
    'priority': Literal['P1', 'P2', 'P3', 'P4'],
    'tasks_order_by': Literal['project_id', 'type', 'trigger', 'priority', 'status', 'created_time', 'updated_time'],
    'task_type': Literal['session', 'agbox-coordinator-async', 'agbox-coordinator-sync'],
    'task_status': Literal['pending', 'running', 'finished', 'interrupted', 'failed'],
    'trigger': Literal['user', 'scheduler'],

    # 项目
    'projects_order_by': Literal['name', 'created_time', 'updated_time'],

    # hermes
    'hermes_messages_role': Literal['user', 'assistant', 'tool'],

    # 定时任务
    'scheduler_order_by': Literal['name', 'created_time', 'updated_time', 'robot', 'mount_name', 'priority', 'coordinator', 'next_run_time', 'is_paused'],

    # 收件箱
    'inbox_type': Literal['tasks', 'upgrade'],
    'inbox_status': Literal['finished', 'interrupted', 'failed', 'rank', 'quality'],
    'inbox_order_by': Literal['type', 'status', 'is_read', 'created_time', 'updated_time'],

    # web 可配置的系统设置
    'web_env_fields': Literal[
        'SKILLS_OVERWRITE',
        'SKILLS_FORMAT_CHECK',
        'ROBOTS_OVERWRITE',
        'ROBOTS_FORMAT_CHECK',
        'ROBOTS_CREATE_IMPORT_HERMES_SELF_SKILLS',
        'SCHEDULER_MAX_JOBS',
        'SCHEDULER_COALESCE',
        'SCHEDULER_MAX_INSTANCES'
    ]
}
