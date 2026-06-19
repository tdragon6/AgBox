'''
通用工具
'''


def desensitize(
    string: str
) -> str:
    '''
    字符串脱敏
    '''
    if not string:
        return ''
    length = len(string)

    if length <= 4:
        return string[:-1] + '*'
    elif length <= 8:
        pre, suf = 1, 1
    elif length <= 16:
        pre, suf = 2, 2
    elif length <= 32:
        pre, suf = 3, 3
    elif length <= 64:
        pre, suf = 4, 4
    else:
        pre, suf = 5, 5

    secret_lenghth = length - pre - suf
    if secret_lenghth > 16:
        secret_lenghth = 16

    return string[:pre] + '*' * secret_lenghth + string[-suf:]