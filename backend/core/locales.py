'''
多语言
'''

import traceback
from pathlib import Path

import json5
from core.logger import logger


def load_translations():
    '''
    加载多语言翻译文件
    '''
    locale_dir = Path(__file__).parent.parent / 'locales'

    translations = {}
    if locale_dir.exists():
        for lang_file in locale_dir.iterdir():
            if lang_file.suffix == '.jsonc':
                with lang_file.open(encoding='utf-8') as f:
                    try:
                        translations[lang_file.stem] = json5.loads(f.read())
                    except:
                        logger.error(traceback.format_exc())
                        pass
    
    return translations
        