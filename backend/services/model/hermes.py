'''
hermes 模型管理 业务逻辑
'''


from hermes_cli.auth import PROVIDER_REGISTRY, ProviderConfig
from hermes_cli.models import fetch_api_models
from providers import list_providers


def add_extra_providers_to_registry() -> tuple[bool, str, None]:
    '''
    添加额外提供商信息到提供商注册表中
    '''
    for extra_provider in list_providers():
        if extra_provider.name not in [ *PROVIDER_REGISTRY.keys(), 'custom' ]:
            PROVIDER_REGISTRY[extra_provider.name] = ProviderConfig(
                id=extra_provider.name,
                name=extra_provider.display_name,
                auth_type=extra_provider.auth_type,
                portal_base_url=extra_provider.signup_url,
                inference_base_url=extra_provider.base_url,
                client_id='',
                scope='',
                extra={},
                api_key_env_vars=extra_provider.env_vars,
                base_url_env_var=''
            )
    
    return True, 'success', None


add_extra_providers_to_registry()


def judge_provider_in_registry(
    id: str
) -> bool:
    '''
    判断提供商是否在注册表中
    '''
    return id in PROVIDER_REGISTRY and getattr(PROVIDER_REGISTRY[id], 'auth_type', '') == 'api_key'


def get_model_provider_name(
    id: str
) -> tuple[bool, str, str]:
    '''
    获取指定提供商的名称
    '''  
    provider_name = getattr(PROVIDER_REGISTRY[id], 'name', id)
    
    return True, 'success', provider_name


def get_model_provider_api_key_env_vars(
    id: str
) -> tuple[bool, str, str]:
    '''
    获取指定提供商的 api_key 环境变量名
    '''
    api_key_vars_name = getattr(PROVIDER_REGISTRY[id], 'api_key_env_vars', ())
    return True, 'success', api_key_vars_name


def get_model_providers_list() -> tuple[bool, str, list[dict]]:
    '''
    获取所有模型提供商列表
    '''
    result = []

    for provider_id, provider_config in PROVIDER_REGISTRY.items():
        if getattr(provider_config, 'auth_type', '') == 'api_key':
            result.append(
                {
                    'id': provider_id,
                    'name': get_model_provider_name(provider_id)[-1]
                }
            )

    return True, 'success', result


def get_model_provider_base_url(
    id: str
) -> tuple[bool, str, str]:
    '''
    获取指定提供商的 base_url
    '''
    base_url = getattr(PROVIDER_REGISTRY[id], 'inference_base_url', '')
    return True, 'success', base_url
    

def get_model_list(
    base_url: str,
    api_key: str = None,
) -> tuple[bool, str, list | None]:
    '''
    获取可用模型列表
    '''
    result = fetch_api_models(api_key=api_key, base_url=base_url)

    if not result:
        return False, 'no_models_found', None
    
    return True, 'success', result