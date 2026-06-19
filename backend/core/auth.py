'''
身份认证
'''


import jwt
import secrets
from argon2 import PasswordHasher
from datetime import datetime, timedelta, timezone
from core.config import settings


ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def hash_password(
    password: str
) -> tuple[bool, str, str]:
    '''
    密码哈希
    '''
    return True, 'success', ph.hash(password)


def verify_hashed_password(
    plain_password: str,
    hashed_password: str
) -> tuple[bool, str, None]:
    '''
    校验哈希密码
    '''
    try:
        ph.verify(hashed_password, plain_password)
        return True, 'success', None
    except:
        return False, 'failed', None
    

def create_jwt_token(
    username: str
) -> tuple[bool, str, str]:
    '''
    创建 JWT 令牌
    '''
    payload = {
        'sub': username,
        'exp': datetime.now(timezone.utc) + timedelta(hours=settings.TOKEN_EXPIRE_HOUR),
        'iat': datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return True, 'success', token


def parse_jwt_token(
    token: str
) -> tuple[bool, str, dict | None]:
    '''
    解析 JWT 令牌
    '''
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return True, 'success', payload
    except:
        return False, 'token_invalid_or_expired', None


def login(
    username: str,
    password: str
) -> tuple[bool, str, dict | None]:
    '''
    登录
    '''
    if username != settings.USERNAME or not verify_hashed_password(password, settings.PASSWORD)[0]:
        return False, 'invalid_username_or_password', None
    else:
        token = create_jwt_token(username)[-1]
        result = {
            'username': username,
            'token': token
        }
        return True, 'success', result
    

def logout() -> tuple[bool, str, None]:
    '''
    注销
    '''
    settings.SECRET_KEY = secrets.token_hex(32)
    return True, 'success', None